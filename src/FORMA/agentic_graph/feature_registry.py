"""Scoped observed-feature entries and immutable FA ballots for the new graph.

The registry imports the new SH/VI artifacts, not the legacy Evidence Graph.
Line identities remain hypothesis judgments; FA only grades observed signal.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from FORMA.core.line_status import STATUSES, is_kept_evidence

from .skyline_risk import skyline_risk


REGISTRY_SCHEMA = "forma-agentic-feature-registry-v1"
ALLOWED_ANSWERS = {"yes", "no"}
ALLOWED_ORIGINS = {"model", "offline_fixture"}


def _digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _artifact(path: Path, kind: str) -> dict:
    resolved = path.resolve(strict=True)
    return {"path": str(resolved), "sha256": _digest(resolved), "kind": kind}


def _check_artifact(node: dict, path_field: str, digest_field: str) -> Path:
    path = Path(node[path_field]).resolve(strict=True)
    if _digest(path) != node[digest_field]:
        raise ValueError(f"{path_field} changed after SH node commit")
    return path


def build_feature_registry(manifest_path: str | Path,
                           sh_node_paths: Iterable[str | Path], *,
                           required_votes: int = 3) -> dict:
    """Import every SH pre-analysis and select only its adopted measurements.

    The complete set of Redrock hypotheses must be present. CWT IDs merge
    within this run; Gaussian fit IDs remain scoped to their hypothesis.
    """
    if type(required_votes) is not int or required_votes < 1 or required_votes % 2 != 1:
        raise ValueError("required_votes must be a positive odd integer")
    manifest_file = Path(manifest_path).resolve(strict=True)
    manifest = _load(manifest_file)
    run_id = manifest["run_id"]
    spectrum_digest = manifest["spectrum_npz_sha256"]
    entries: dict[str, dict] = {}
    hypotheses: dict[str, dict] = {}
    artifacts = {"vi_manifest": _artifact(manifest_file, "vi_manifest")}
    spectrum_file = Path(manifest["spectrum_npz_path"]).resolve(strict=True)
    if _digest(spectrum_file) != spectrum_digest:
        raise ValueError("VI spectrum changed since measurement freeze")
    artifacts["spectrum_npz"] = _artifact(spectrum_file, "spectrum_input")
    cwt_file = manifest_file.with_name("cwt_features.json")
    if _load(cwt_file) != manifest["cwt_features"]:
        raise ValueError("run-shared CWT feature artifact differs from VI manifest")
    artifacts["vi_cwt_features"] = _artifact(cwt_file, "vi_cwt_features")

    for node_file_raw in sh_node_paths:
        node_file = Path(node_file_raw).resolve(strict=True)
        node = _load(node_file)
        hyp = node["hypothesis_ref"]
        if hyp not in manifest["hypotheses"] or hyp in hypotheses:
            raise ValueError("unknown or repeated SH hypothesis")
        manifest_catalog = Path(manifest["hypotheses"][hyp]["catalog_path"]).resolve(strict=True)
        catalog_file = _check_artifact(node, "measurement_catalog_path",
                                       "measurement_catalog_sha256")
        if catalog_file != manifest_catalog:
            raise ValueError("SH node refers to another VI catalog")
        catalog = _load(catalog_file)
        if (catalog["run_id"] != run_id or catalog["hypothesis_ref"] != hyp
                or catalog["redshift"] != node["hypothesis_redshift"]
                or catalog["spectrum_npz_sha256"] != spectrum_digest):
            raise ValueError("SH and VI catalog identity differs")
        judgment_file = _check_artifact(node, "judgment_path", "judgment_sha256")
        line_review = node.get("schema_version") == "forma-sh-line-review-v1"
        for path_field, digest_field in (
            ("csv_path", "csv_sha256"), ("session_stage1_path", "session_stage1_sha256"),
            *((() if line_review else (("report_path", "report_sha256"),
                                       ("session_stage2_path", "session_stage2_sha256")))),
        ):
            _check_artifact(node, path_field, digest_field)
        prefix = f"sh/{hyp}/"
        attempts_file = Path(manifest["hypotheses"][hyp]["fit_attempts_path"])
        if _load(attempts_file) != catalog["fit_attempts"]:
            raise ValueError("VI fit attempts differ from frozen SH catalog")
        artifacts[prefix + "fit_attempts"] = _artifact(attempts_file, "vi_fit_attempts")
        artifact_rows = [
            ("node", node_file, "sh_node"), ("catalog", catalog_file, "vi_catalog"),
            ("judgments", judgment_file, "sh_judgments"),
            ("csv", Path(node["csv_path"]), "sh_csv"),
            ("stage1_session", Path(node["session_stage1_path"]), "sh_session"),
        ]
        if not line_review:
            artifact_rows.extend([
                ("report", Path(node["report_path"]), "sh_report"),
                ("stage2_session", Path(node["session_stage2_path"]), "sh_session"),
            ])
        for name, path, kind in artifact_rows:
            artifacts[prefix + name] = _artifact(path, kind)
        measurements = {item["id"]: item for item in catalog["measurements"]}
        known_lines = {item["id"] for item in catalog["lines"]}
        if (len(measurements) != len(catalog["measurements"])
                or len(known_lines) != len(catalog["lines"])):
            raise ValueError("duplicate measurement or line ID in VI catalog")
        references = _load(judgment_file)
        if not isinstance(references, list):
            raise ValueError("SH judgments must be a list")
        judged_lines = [item.get("line_id") for item in references]
        if len(judged_lines) != len(known_lines) or set(judged_lines) != known_lines:
            raise ValueError("SH judgments must cover each catalog line exactly once")
        for judgment in references:
            ref = judgment.get("measurement_id")
            status = judgment.get("status")
            if status not in STATUSES:
                raise ValueError("SH judgment has an unknown line status")
            if ref is None:
                if is_kept_evidence(status):
                    raise ValueError("adopted SH line lacks a measurement")
                continue
            if (judgment.get("line_id") not in known_lines
                    or not is_kept_evidence(status)
                    or ref not in measurements or not measurements[ref]["adoptable"]):
                raise ValueError("SH judgment has an invalid adopted reference")
            measured = measurements[ref]
            is_cwt = measured["source"] == "CWT"
            if is_cwt:
                key = "emission" if measured["kind"] == "emission" else "absorption"
                run_cwt = {item["feature_id"]: item
                           for item in manifest["cwt_features"][key]}
                if ref not in run_cwt or run_cwt[ref] != measured["record"]:
                    raise ValueError("CWT measurement differs from run-shared VI feature")
            elif not ref.startswith(f"fit:{hyp}:"):
                raise ValueError("Gaussian fit ID is not scoped to its hypothesis")
            record = measured["record"]
            center = record.get("wavelength") if is_cwt else record.get("center")
            if center is None:
                raise ValueError("adopted feature has no centre")
            if ref not in entries:
                entries[ref] = {
                    "feature_id": ref, "scope": "run" if is_cwt else "hypothesis",
                    "hypothesis_ref": None if is_cwt else hyp,
                    "source": measured["source"], "kind": measured["kind"],
                    "center_angstrom": center, "references": [],
                    "skyline_risk": skyline_risk(center),
                    "votes": [], "required_votes": required_votes,
                    "observed_signal_state": "pending", "vote_summary": None,
                    "review_blocker": None,
                }
            entry = entries[ref]
            if (entry["center_angstrom"] != center or entry["kind"] != measured["kind"]
                    or entry["source"] != measured["source"]
                    or (entry["scope"] == "hypothesis" and entry["hypothesis_ref"] != hyp)):
                raise ValueError("feature ID points to conflicting measurements")
            entry["references"].append({
                "hypothesis_ref": hyp, "line_id": judgment["line_id"],
                "sh_status": judgment["status"],
            })
        hypotheses[hyp] = {
            "classification": None if line_review else node["classification"],
            "pre_analysis_status": node["status"],
            "redshift": node["hypothesis_redshift"],
            "node_artifact": prefix + "node",
        }

    if set(hypotheses) != set(manifest["hypotheses"]):
        raise ValueError("SH pre-analysis is incomplete for this VI manifest")
    for entry in entries.values():
        entry["references"].sort(key=lambda item: (item["hypothesis_ref"], item["line_id"]))
    return {"schema_version": REGISTRY_SCHEMA, "run_id": run_id,
            "spectrum_npz_sha256": spectrum_digest,
            "hypotheses": hypotheses, "features": dict(sorted(entries.items())),
            "artifacts": dict(sorted(artifacts.items()))}


def cast_vote(registry: dict, feature_id: str, *, vote_id: str, reviewer_id: str,
              answer: str, origin: str, artifact_ref: str | None = None,
              artifact_index: dict | None = None) -> dict:
    """Add one independent ballot, projecting a state only at odd quorum."""
    if answer not in ALLOWED_ANSWERS or origin not in ALLOWED_ORIGINS:
        raise ValueError("invalid FA answer or origin")
    if not vote_id or not reviewer_id:
        raise ValueError("vote and reviewer IDs are required")
    entry = registry["features"][feature_id]
    if entry.get("review_blocker") is not None:
        raise ValueError("feature review is blocked by unusable data")
    votes = entry["votes"]
    if len(votes) >= entry["required_votes"]:
        raise ValueError("feature already has its required votes")
    if any(v["vote_id"] == vote_id or v["reviewer_id"] == reviewer_id for v in votes):
        raise ValueError("duplicate FA vote or reviewer")
    if artifact_ref is not None and artifact_ref not in (
            registry["artifacts"] if artifact_index is None else artifact_index):
        raise ValueError("vote artifact is not registered")
    ballot = {"vote_id": vote_id, "reviewer_id": reviewer_id, "answer": answer,
              "origin": origin, "artifact_ref": artifact_ref}
    votes.append(ballot)
    if len(votes) == entry["required_votes"]:
        yes_count = sum(v["answer"] == "yes" for v in votes)
        yes_fraction = yes_count / len(votes)
        entry["observed_signal_state"] = (
            "signal_present" if yes_count > len(votes) / 2 else "signal_absent")
        entry["vote_summary"] = {
            "yes": yes_count, "no": len(votes) - yes_count,
            "yes_fraction": yes_fraction,
            "assurance": ("assured" if max(yes_fraction, 1 - yes_fraction) > 0.75
                          else "contested"),
            "contains_offline_fixture": any(v["origin"] == "offline_fixture" for v in votes),
        }
    return {"feature_id": feature_id, "vote_count": len(votes),
            "observed_signal_state": entry["observed_signal_state"],
            "vote_summary": entry["vote_summary"]}
