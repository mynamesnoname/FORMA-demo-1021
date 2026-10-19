"""Bounded independent FA reality sessions with branch-aware vote persistence."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Callable, Iterable

from .execution_artifacts import ExecutionAllocation
from .fa_feature_reality import (build_feature_window, measured_feature_width,
                                 run_feature_reality)
from .feature_registry import _digest
from .node_keys import fa_node_key
from .reasoning_trace import (
    record_fa_attempt_failed, record_fa_review_blocked, record_fa_vote,
    register_artifact, register_execution, write_trace,
)
from .sh_pre_analysis import PROMPT_DIR
from .vote_runtime import (VoteSeat, VoteSessionFailure, iter_vote_seats,
                           prompt_identity, summarize_usage)


def _write_new(path: Path, data: dict) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def _catalog_for_feature(manifest: dict, entry: dict, active: set[str]) -> Path:
    refs = sorted({ref["hypothesis_ref"] for ref in entry["references"]} & active)
    if not refs:
        raise ValueError("FA feature has no active SH hypothesis")
    if entry["scope"] == "hypothesis":
        if entry["hypothesis_ref"] not in refs:
            raise ValueError("hypothesis-scoped fit is inactive")
        hypothesis = entry["hypothesis_ref"]
    else:
        hypothesis = refs[0]
    return Path(manifest["hypotheses"][hypothesis]["catalog_path"]).resolve(strict=True)


async def review_feature_reality(
    *, trace: dict, branch_id: str, vi_manifest_path: str | Path,
    output_root: str | Path, llm: Any, feature_ids: Iterable[str] | None = None,
    concurrency: int = 4, max_attempts_per_vote: int = 2,
    agent_factory: Callable[..., Any] | None = None,
) -> dict:
    """Review selected entries until quorum or bounded failure, preserving all attempts.

    Each seat creates a fresh agent/session and never sees other seats' answers.
    Only successful, validated submissions count; all results are serialized
    into the branch trace as workers finish. A failed seat leaves the feature
    pending and is reported explicitly. The caller owns the trace and output
    root, which should be a new directory for a new run.
    """
    if type(concurrency) is not int or concurrency < 1:
        raise ValueError("concurrency must be positive")
    if type(max_attempts_per_vote) is not int or max_attempts_per_vote < 1:
        raise ValueError("max_attempts_per_vote must be positive")
    branch = trace["branches"][branch_id]
    registry = branch["state"]["registry"]
    manifest_file = Path(vi_manifest_path).resolve(strict=True)
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if (trace["run_id"] != manifest["run_id"]
            or registry["spectrum_npz_sha256"] != manifest["spectrum_npz_sha256"]
            or _digest(Path(manifest["spectrum_npz_path"])) != manifest["spectrum_npz_sha256"]):
        raise ValueError("FA manifest or spectrum differs from the branch registry")
    if any(vote["origin"] != "model"
           for entry in registry["features"].values() for vote in entry["votes"]):
        raise ValueError("cannot continue a branch containing fixture votes")
    selected = sorted(registry["features"] if feature_ids is None else set(feature_ids))
    if any(feature_id not in registry["features"] for feature_id in selected):
        raise ValueError("requested FA feature is absent from the registry")
    root = Path(output_root).resolve()
    if trace.get("artifact_root") not in (None, str(root)):
        raise ValueError("FA output root differs from the branch trace artifact root")
    root.mkdir(parents=True, exist_ok=True)
    if (root / "reasoning_branches.json").exists() or (root / "fa_review_summary.json").exists():
        raise FileExistsError("FA output already contains a completed review")
    snapshots = root / "trace_snapshots"
    snapshots.mkdir(exist_ok=True)
    active = set(branch["state"]["active_pre_analysis"])
    jobs: list[VoteSeat] = []
    catalogs: dict[str, Path] = {}
    frozen_prompts: dict[str, dict] = {}
    system = (PROMPT_DIR / "fa_real_feature_system.md").read_text(encoding="utf-8")
    blocked: list[str] = []
    for feature_id in selected:
        entry = registry["features"][feature_id]
        if entry.get("review_blocker") is not None or len(entry["votes"]) >= entry["required_votes"]:
            continue
        catalog = _catalog_for_feature(manifest, entry, active)
        catalog_data = json.loads(catalog.read_text(encoding="utf-8"))
        if (Path(catalog_data["spectrum_npz_path"]).resolve() !=
                Path(manifest["spectrum_npz_path"]).resolve()
                or ("masked_regions" in manifest and
                    catalog_data.get("masked_regions", []) != manifest["masked_regions"])):
            raise ValueError("VI catalog and manifest disagree on the spectrum or masks")
        if entry["scope"] == "run":
            for ref in entry["references"]:
                other = json.loads(Path(manifest["hypotheses"][ref["hypothesis_ref"]]
                                        ["catalog_path"]).read_text(encoding="utf-8"))
                if other.get("masked_regions", []) != catalog_data.get("masked_regions", []):
                    raise ValueError("shared CWT feature has inconsistent VI masks")
        try:
            matches = [item for item in catalog_data["measurements"]
                       if item["id"] == feature_id]
            if len(matches) != 1 or not matches[0].get("adoptable"):
                raise ValueError("FA feature has no unique adoptable measurement")
            width_a, width_kms = measured_feature_width(matches[0])
            user = build_feature_window(manifest["spectrum_npz_path"],
                                        center=entry["center_angstrom"], kind=entry["kind"],
                                        masked_regions=catalog_data.get("masked_regions"),
                                        measured_fwhm_angstrom=width_a,
                                        measured_fwhm_km_s=width_kms)
        except ValueError as exc:
            if str(exc) not in {"no samples in target window", "target window has no usable samples"}:
                raise
            if entry["votes"]:
                raise ValueError("previous votes exist but FA window is now unusable") from exc
            record_fa_review_blocked(trace, branch_id, feature_id,
                                     reason="no_usable_samples",
                                     artifact_refs=[f"sh/{catalog_data['hypothesis_ref']}/catalog"])
            blocked.append(feature_id)
            continue
        catalogs[feature_id] = catalog
        frozen_prompts[feature_id] = prompt_identity(system, user, "submit_feature_reality")
        for seat in range(entry["required_votes"] - len(entry["votes"])):
            jobs.append(VoteSeat(feature_id, seat, fa_node_key(trace["run_id"], feature_id)))

    async def invoke(seat: VoteSeat, allocation: ExecutionAllocation) -> dict:
        kwargs = {"agent_factory": agent_factory} if agent_factory is not None else {}
        result = await run_feature_reality(
            llm=llm, run_id=trace["run_id"], measurement_id=seat.target_id,
            vi_catalog_path=catalogs[seat.target_id], execution=allocation,
            frozen_prompt_identity=frozen_prompts[seat.target_id], **kwargs)
        try:
            node_file = allocation.path("node.json")
            if json.loads(node_file.read_text(encoding="utf-8")) != result["node"]:
                raise ValueError("FA node file differs from submitted result")
            if (result["node"]["measurement_id"] != seat.target_id
                    or result["node"]["answer"] not in {"yes", "no"}
                    or result["node"].get("prompt_identity") != frozen_prompts[seat.target_id]
                    or _digest(allocation.path("session.md")) != result["node"]["session_sha256"]):
                raise ValueError("FA node identity, prompt or session digest differs")
        except Exception as exc:
            raise VoteSessionFailure(exc, result["model_usage"]) from exc
        return {"answer": result["node"]["answer"],
                "model_calls": result["model_usage"]}

    def checkpoint() -> None:
        write_trace(trace, snapshots / f"trace-{uuid.uuid4().hex}.json")

    if blocked:
        checkpoint()
    failed_seats: list[dict] = []
    successful_votes = 0
    model_calls: list[dict] = []
    async for outcome in iter_vote_seats(
            root=root, run_id=trace["run_id"], branch_id=branch_id,
            seats=jobs, concurrency=concurrency,
            max_attempts=max_attempts_per_vote, invoke=invoke):
        feature_id = outcome.seat.target_id
        for attempt in outcome.attempts:
            allocation = attempt.allocation
            execution_id = allocation.node_execution_id
            register_execution(trace, allocation)
            model_calls.extend(attempt.model_calls)
            if attempt.status == "failed":
                ref = f"fa/{execution_id}/failure"
                register_artifact(trace, ref, allocation.path("failure.json"), "fa_attempt_failure",
                                  node_execution_id=execution_id)
                register_artifact(trace, f"fa/{execution_id}/model_usage.json",
                                  allocation.path("model_usage.json"), "fa_model_usage",
                                  node_execution_id=execution_id)
                for name in ("session.md", "node.json"):
                    if allocation.path(name).is_file():
                        register_artifact(trace, f"fa/{execution_id}/{name}",
                                          allocation.path(name), "fa_partial",
                                          node_execution_id=execution_id)
                record_fa_attempt_failed(trace, branch_id, feature_id,
                                         node_execution_id=execution_id,
                                         artifact_ref=ref,
                                         error_type=attempt.error_type)
            else:
                ref = f"fa/{execution_id}/node"
                for name, kind in (("node.json", "fa_node"),
                                   ("session.md", "fa_session"),
                                   ("model_usage.json", "fa_model_usage")):
                    register_artifact(trace, ref if name == "node.json" else f"fa/{execution_id}/{name}",
                                      allocation.path(name), kind,
                                      node_execution_id=execution_id)
                record_fa_vote(trace, branch_id, feature_id,
                               vote_id=f"model:{execution_id}",
                               reviewer_id=f"session:{execution_id}",
                               answer=attempt.result["answer"], origin="model",
                               artifact_ref=ref, node_execution_id=execution_id)
                successful_votes += 1
            checkpoint()
        if outcome.attempts[-1].status == "failed":
            failed_seats.append({"feature_id": feature_id, "seat": outcome.seat.seat,
                                 "attempts": len(outcome.attempts)})

    usage = summarize_usage(model_calls)
    summary = {
        "run_id": trace["run_id"], "branch_id": branch_id,
        "requested_features": len(selected), "scheduled_vote_seats": len(jobs),
        "successful_votes": successful_votes, "failed_seats": failed_seats,
        "blocked_features": blocked,
        "signal_present": sorted(fid for fid in selected if registry["features"][fid]["observed_signal_state"] == "signal_present"),
        "signal_absent": sorted(fid for fid in selected if registry["features"][fid]["observed_signal_state"] == "signal_absent"),
        "pending_features": sorted(fid for fid in selected if registry["features"][fid]["observed_signal_state"] == "pending"),
        "model_call_count": usage["calls"],
        "input_tokens": usage["input_tokens"],
        "output_tokens": usage["output_tokens"],
        "cache_hit_tokens": usage["cache_hit_tokens"],
        "cache_hit_reported_calls": usage["cache_hit_reported_calls"],
        "cache_hit_unreported_calls": usage["cache_hit_unreported_calls"],
    }
    _write_new(root / "fa_review_summary.json", summary)
    write_trace(trace, root / "reasoning_branches.json")
    return summary
