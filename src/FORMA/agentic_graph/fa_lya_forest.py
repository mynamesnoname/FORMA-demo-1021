"""Advisory, hypothesis-scoped FA review of observed Lyα-forest structure.

This node records a visual observation. It never updates feature reality,
cleaned line pairings, or a type-graph gate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Callable

import numpy as np
from langchain.agents import create_agent

from FORMA.core.config.analysis_method import LyalphaForestMethod, load_analysis_method
from FORMA.core.line_status import is_kept_evidence

from .execution_artifacts import allocate_execution
from .feature_registry import _digest
from .node_keys import fa_lya_forest_key
from .reasoning_trace import record_analysis, register_artifact, register_execution
from .sh_pre_analysis import PROMPT_DIR, _render
from .vote_runtime import collect_advisory_votes, summarize_usage, vote_tally


LYA_ID = "line:lya-1216"
SCHEMA = "forma-fa-lya-forest-v1"


def _read_bound_artifact(trace: dict, ref: str) -> tuple[Path, Any]:
    item = trace["artifacts"].get(ref)
    if item is None:
        raise ValueError(f"forest source is not registered: {ref}")
    path = Path(item["path"]).resolve(strict=True)
    if _digest(path) != item["sha256"]:
        raise ValueError(f"forest source changed: {ref}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if ref.endswith("/catalog") and not isinstance(value, dict):
        raise ValueError("VI catalog must be an object")
    return path, value


def _format_samples(wl: np.ndarray, flux: np.ndarray, ivar: np.ndarray,
                    valid: np.ndarray) -> str:
    rows = ["| wavelength (Å) | flux | ivar | usable |",
            "|---:|---:|---:|---|"]
    rows.extend(f"| {w:.8g} | {f:.8g} | {v:.8g} | {'yes' if ok else 'no'} |"
                for w, f, v, ok in zip(wl, flux, ivar, valid))
    return "\n".join(rows) if len(wl) else "No samples in this region."


def build_lya_forest_window(npz_path: str | Path, *, lya_wavelength: float,
                            masked_regions: list, method: LyalphaForestMethod) -> dict:
    """Return code-owned coverage plus the complete model-facing local pixels."""
    if not math.isfinite(lya_wavelength) or lya_wavelength <= 0:
        raise ValueError("Lyα position must be finite and positive")
    with np.load(npz_path) as spectrum:
        wl = spectrum["wavelength"]
        flux = spectrum["flux"]
        ivar = spectrum["ivar"] if "ivar" in spectrum else np.full_like(flux, np.nan)
    if (wl.ndim != 1 or not len(wl) or flux.shape != wl.shape or ivar.shape != wl.shape
            or not np.all(np.isfinite(wl)) or not np.all(np.diff(wl) > 0)):
        raise ValueError("forest spectrum needs ordered finite wavelength and aligned arrays")
    blue_start = lya_wavelength - method.blueward_span_angstrom
    red_end = lya_wavelength + method.redward_reference_span_angstrom
    if blue_start <= 0:
        raise ValueError("forest blueward window must have positive wavelengths")
    selected = (wl >= blue_start) & (wl <= red_end)
    local_wl, local_flux, local_ivar = wl[selected], flux[selected], ivar[selected]
    masked = np.zeros(len(local_wl), dtype=bool)
    for region in masked_regions or []:
        if (not isinstance(region, (list, tuple)) or len(region) != 2
                or not all(isinstance(x, (int, float)) and math.isfinite(x) for x in region)
                or region[0] > region[1]):
            raise ValueError("invalid forest mask interval")
        masked |= (local_wl >= region[0]) & (local_wl <= region[1])
    valid = (np.isfinite(local_flux) & np.isfinite(local_ivar)
             & (local_ivar > 0) & ~masked)
    blue = local_wl < lya_wavelength
    red = ~blue
    blue_valid = int(np.count_nonzero(valid & blue))
    blue_samples = int(np.count_nonzero(blue))
    red_valid = int(np.count_nonzero(valid & red))
    covered = bool(wl[0] <= blue_start and wl[-1] >= lya_wavelength)
    assessable = blue_valid >= method.min_valid_blue_samples
    noise = (float(np.median(1 / np.sqrt(local_ivar[valid & blue])))
             if blue_valid else None)
    coverage = {
        "blue_requested_angstrom": [blue_start, lya_wavelength],
        "red_requested_angstrom": [lya_wavelength, red_end],
        "actual_window_angstrom": ([float(local_wl[0]), float(local_wl[-1])]
                                    if len(local_wl) else None),
        "blue_samples": blue_samples, "blue_valid_samples": blue_valid,
        "red_valid_samples": red_valid,
        "blue_masked_samples": int(np.count_nonzero(masked & blue)),
        "blue_invalid_ivar_or_flux_samples": int(np.count_nonzero(~valid & ~masked & blue)),
        "requested_blue_interval_within_spectrum_bounds": covered,
        "assessable": assessable,
        "unreviewable_reason": None if assessable else "insufficient_valid_blue_samples",
        "median_blue_pixel_noise": noise,
    }
    user = _render("fa_lya_forest_user.md", {
        "LYA_WAVELENGTH": f"{lya_wavelength:.8g}",
        "BLUE_REQUESTED": f"[{blue_start:.8g}, {lya_wavelength:.8g})",
        "RED_REQUESTED": f"[{lya_wavelength:.8g}, {red_end:.8g}]",
        "ACTUAL_RANGE": (f"[{local_wl[0]:.8g}, {local_wl[-1]:.8g}]"
                         if len(local_wl) else "no samples"),
        "COVERAGE_SUMMARY": (f"blue: {blue_valid}/{blue_samples} usable, "
                             f"{coverage['blue_masked_samples']} explicitly masked; "
                             f"redward reference: {red_valid} usable; "
                             f"requested blue interval within spectrum bounds: {covered}"),
        "NOISE_SUMMARY": (f"{noise:.6g} flux units; this is not a forest-detection significance"
                          if noise is not None else "unavailable"),
        "BLUE_SAMPLES": _format_samples(local_wl[blue], local_flux[blue],
                                         local_ivar[blue], valid[blue]),
        "RED_SAMPLES": _format_samples(local_wl[red], local_flux[red],
                                        local_ivar[red], valid[red]),
    }, PROMPT_DIR)
    return {"coverage": coverage, "user_prompt": user}


async def review_lya_forest(*, trace: dict, branch_id: str, hypothesis_ref: str,
                            output_root: str | Path, llm: Any,
                            agent_factory: Callable[..., Any] = create_agent,
                            concurrency: int = 3, recursion_limit: int = 30) -> dict:
    """Record independent forest votes as advisory branch information only."""
    if concurrency < 1 or recursion_limit < 1:
        raise ValueError("concurrency and recursion limit must be positive")
    branch = trace["branches"][branch_id]
    key = fa_lya_forest_key(trace["run_id"], hypothesis_ref)
    if (hypothesis_ref not in branch["state"]["active_pre_analysis"]
            or key in branch["state"]["analysis_results"]):
        raise ValueError("forest needs an active, not-yet-reviewed SH hypothesis")
    catalog_ref = f"sh/{hypothesis_ref}/catalog"
    judgments_ref = f"sh/{hypothesis_ref}/judgments"
    source_refs = [f"sh/{hypothesis_ref}/node", catalog_ref,
                   judgments_ref, "spectrum_npz"]
    for ref in source_refs:
        item = trace["artifacts"].get(ref)
        if item is None or _digest(Path(item["path"])) != item["sha256"]:
            raise ValueError(f"forest source is missing or changed: {ref}")
    _, catalog = _read_bound_artifact(trace, catalog_ref)
    _, judgments = _read_bound_artifact(trace, judgments_ref)
    if not isinstance(judgments, list):
        raise ValueError("SH judgments must be a list")
    if (catalog["run_id"] != trace["run_id"]
            or catalog["hypothesis_ref"] != hypothesis_ref
            or catalog["spectrum_npz_sha256"] != trace["artifacts"]["spectrum_npz"]["sha256"]):
        raise ValueError("forest catalog identity differs from active hypothesis")
    lines = [line for line in catalog["lines"] if line["id"] == LYA_ID]
    claims = [row for row in judgments if row["line_id"] == LYA_ID]
    if len(lines) != 1 or len(claims) != 1 or not is_kept_evidence(claims[0]["status"]):
        raise ValueError("forest review requires exactly one kept Lyα claim")
    predicted = float(lines[0]["predicted_obs"])
    method = load_analysis_method().audit.lyalpha_forest
    window = build_lya_forest_window(trace["artifacts"]["spectrum_npz"]["path"],
                                     lya_wavelength=predicted,
                                     masked_regions=catalog.get("masked_regions", []),
                                     method=method)
    root = Path(output_root).resolve()
    if trace.get("artifact_root", str(root)) != str(root):
        raise ValueError("forest output root differs from branch artifact root")
    if window["coverage"]["assessable"]:
        batch = await collect_advisory_votes(
            trace=trace, branch_id=branch_id, node_key=key,
            output_root=root, llm=llm,
            system=(PROMPT_DIR / "fa_lya_forest_system.md").read_text(encoding="utf-8"),
            user=window["user_prompt"], tool_name="submit_lya_forest_vote",
            stage="Lyα forest visibility", vote_quorum=method.vote_quorum,
            max_attempts=method.max_attempts_per_vote_seat,
            concurrency=concurrency, recursion_limit=recursion_limit,
            agent_factory=agent_factory, artifact_namespace="fa_forest")
    else:
        batch = {"ballots": [], "attempt_refs": [], "model_usage": summarize_usage([]),
                 "prompt_identity": None}
    ballots = batch["ballots"]
    tally = vote_tally(ballots, method.vote_quorum, window["coverage"]["assessable"])
    outcome = (None if tally["positive"] is None else
               "visible" if tally["positive"] else "not_seen")
    node = {
        "schema_version": SCHEMA, "node_type": "fa.lyalpha_forest_visibility",
        "node_key": key, "run_id": trace["run_id"], "branch_id": branch_id,
        "hypothesis_ref": hypothesis_ref, "line_id": LYA_ID,
        "predicted_obs_angstrom": predicted,
        "status": tally["status"], "forest_visible": tally["positive"],
        "visibility": outcome, "consultative_only": True,
        "coverage": window["coverage"], "method_snapshot": method.model_dump(mode="json"),
        "vote_summary": tally["vote_summary"], "ballots": ballots,
        "successful_votes": tally["successful_votes"],
        "required_votes": tally["required_votes"],
        "failed_seats": tally["failed_seats"],
        "model_usage": batch["model_usage"], "prompt_identity": batch["prompt_identity"],
        "source_refs": source_refs, "attempt_refs": batch["attempt_refs"],
    }
    allocation = allocate_execution(root, run_id=trace["run_id"],
                                    branch_id=branch_id, node_key=key)
    node["node_execution_id"] = allocation.node_execution_id
    allocation.path("node.json").write_text(
        json.dumps(node, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8")
    register_execution(trace, allocation)
    node_ref = f"fa_forest/{allocation.node_execution_id}/node"
    register_artifact(trace, node_ref, allocation.path("node.json"), "fa_forest_node",
                      node_execution_id=allocation.node_execution_id)
    record_analysis(trace, branch_id, kind="analysis_result", analysis_ref=key,
                    artifact_refs=[node_ref, *source_refs, *batch["attempt_refs"]],
                    node_execution_id=allocation.node_execution_id)
    return {"node": node, "node_ref": node_ref, "model_usage": node["model_usage"]}


def read_lya_forest_information(trace: dict, *, branch_id: str,
                                hypothesis_ref: str) -> dict | None:
    """Return the active advisory result for a future HS/RA consumer.

    An inherited branch sees only events through its fork point. A missing
    result is `None`; neither `not_seen` nor `unreviewable` is a negative gate.
    """
    key = fa_lya_forest_key(trace["run_id"], hypothesis_ref)
    if key not in trace["branches"][branch_id]["state"]["analysis_results"]:
        return None

    def find_event(current_branch: str, cutoff: str | None = None) -> dict | None:
        branch = trace["branches"][current_branch]
        events = branch["events"]
        if cutoff is not None:
            positions = [i for i, event in enumerate(events) if event["event_id"] == cutoff]
            if len(positions) != 1:
                raise ValueError("forest fork point is absent from parent")
            events = events[:positions[0] + 1]
        for event in reversed(events):
            if (event["kind"] == "analysis_result"
                    and event["payload"]["analysis_ref"] == key):
                return event
        parent = branch["parent_branch_id"]
        return (find_event(parent, branch["fork_event_id"])
                if parent is not None else None)

    event = find_event(branch_id)
    if event is None:
        raise ValueError("active forest result has no reachable event")
    matches = [(ref, trace["artifacts"][ref]) for ref in event["artifact_refs"]
               if trace["artifacts"][ref]["kind"] == "fa_forest_node"]
    if len(matches) != 1:
        raise ValueError("forest event must cite one result node")
    ref, item = matches[0]
    path = Path(item["path"]).resolve(strict=True)
    if _digest(path) != item["sha256"]:
        raise ValueError("forest result changed since registration")
    node = json.loads(path.read_text(encoding="utf-8"))
    if (node.get("schema_version") != SCHEMA or node.get("node_key") != key
            or node.get("hypothesis_ref") != hypothesis_ref
            or node.get("consultative_only") is not True):
        raise ValueError("forest result contract differs from active claim")
    return {"node_ref": ref, "status": node["status"],
            "visibility": node["visibility"],
            "forest_visible": node["forest_visible"],
            "vote_summary": node["vote_summary"],
            "coverage": node["coverage"],
            "ballots": node["ballots"],
            "consultative_only": True}
