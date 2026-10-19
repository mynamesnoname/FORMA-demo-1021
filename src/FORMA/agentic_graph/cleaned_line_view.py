"""Recomputable, hypothesis-scoped join of SH line judgments and FA ballots."""

from __future__ import annotations

import json
import math
from pathlib import Path

from FORMA.core.line_status import STATUSES, is_kept_evidence

from .feature_registry import _digest


_FA_TO_PAIRING = {
    "signal_present": "adopted",
    "signal_absent": "rejected_measurement",
    "pending": "pending_review",
    "unreviewable": "unreviewable_data",
}


def _read_artifact(trace: dict, ref: str) -> dict | list:
    item = trace["artifacts"].get(ref)
    if item is None:
        raise ValueError(f"missing source artifact {ref}")
    path = Path(item["path"]).resolve(strict=True)
    if _digest(path) != item["sha256"]:
        raise ValueError(f"changed source artifact {ref}")
    return json.loads(path.read_text(encoding="utf-8"))


def cleaned_line_view(trace: dict, branch_id: str, hypothesis_ref: str) -> dict:
    """Join exact measurement IDs; absent and unknown signals remain distinct.

    Only the active branch's FA state is read. `skyline_risk` is intentionally
    excluded: the QSO type graph does not consume that feature attribute.
    """
    branch = trace["branches"][branch_id]
    state = branch["state"]
    registry = state["registry"]
    if hypothesis_ref not in state["active_pre_analysis"]:
        raise ValueError("SH pre-analysis is not active on this branch")
    hypothesis = registry["hypotheses"].get(hypothesis_ref)
    if hypothesis is None:
        raise ValueError("unknown hypothesis")
    prefix = f"sh/{hypothesis_ref}/"
    node = _read_artifact(trace, prefix + "node")
    catalog = _read_artifact(trace, prefix + "catalog")
    judgments = _read_artifact(trace, prefix + "judgments")
    if (node["hypothesis_ref"] != hypothesis_ref
            or catalog["hypothesis_ref"] != hypothesis_ref
            or node["hypothesis_redshift"] != hypothesis["redshift"]
            or catalog["redshift"] != hypothesis["redshift"]
            or node["judgment_sha256"] != trace["artifacts"][prefix + "judgments"]["sha256"]
            or node["measurement_catalog_sha256"] != trace["artifacts"][prefix + "catalog"]["sha256"]):
        raise ValueError("SH node, catalog or judgments disagree")
    lines = {item["id"]: item for item in catalog["lines"]}
    measurements = {item["id"]: item for item in catalog["measurements"]}
    if len(lines) != len(catalog["lines"]) or len(measurements) != len(catalog["measurements"]):
        raise ValueError("duplicate line or measurement IDs in catalog")
    if not isinstance(judgments, list) or {row["line_id"] for row in judgments} != set(lines):
        raise ValueError("SH judgments do not cover the frozen line catalog")
    if len(judgments) != len(lines):
        raise ValueError("duplicate SH line judgment")
    rows = []
    for judgment in judgments:
        line_id = judgment["line_id"]
        line = lines[line_id]
        sh_status = judgment["status"]
        if sh_status not in STATUSES:
            raise ValueError("SH judgment has an unknown line status")
        measurement_id = judgment.get("measurement_id")
        if measurement_id is None:
            if is_kept_evidence(sh_status):
                raise ValueError("unpaired SH judgment has an adopted status")
            feature = None
            pairing = "no_pairing"
            fa_state = None
            measurement = None
        else:
            if not is_kept_evidence(sh_status) or measurement_id not in measurements:
                raise ValueError("SH judgment has an invalid adopted measurement")
            measurement = measurements[measurement_id]
            feature = registry["features"].get(measurement_id)
            if (feature is None or not measurement["adoptable"]
                    or feature["kind"] != line["kind"]
                    or not any(ref["hypothesis_ref"] == hypothesis_ref
                               and ref["line_id"] == line_id
                               and ref["sh_status"] == sh_status
                               for ref in feature["references"])):
                raise ValueError("SH pairing has no matching scoped FA feature")
            fa_state = feature["observed_signal_state"]
            pairing = _FA_TO_PAIRING.get(fa_state)
            if pairing is None:
                raise ValueError("unknown FA signal state")
        record = measurement["record"] if measurement is not None else None
        width = (record.get("FWHM_km_s") if measurement and measurement["source"] == "CWT"
                 else record.get("fwhm_km_s") if record else None)
        if width is not None and (not isinstance(width, (int, float))
                                  or not math.isfinite(width) or width <= 0):
            width = None
        rows.append({
            "line_id": line_id, "line_name": line.get("name"),
            "line_kind": line["kind"], "predicted_obs_angstrom": line["predicted_obs"],
            "sh_status": sh_status, "measurement_id": measurement_id,
            "measurement_source": measurement["source"] if measurement else None,
            "measurement_flags": measurement.get("flags", []) if measurement else [],
            "fwhm_km_s": width,
            "fa_state": fa_state, "vote_summary": feature["vote_summary"] if feature else None,
            "cleaned_pairing": pairing,
            "fa_vote_artifact_refs": [vote["artifact_ref"] for vote in feature["votes"]
                                      if vote.get("artifact_ref")] if feature else [],
        })
    return {
        "schema_version": "forma-cleaned-line-view-v1",
        "run_id": trace["run_id"], "branch_id": branch_id,
        "hypothesis_ref": hypothesis_ref, "fixed_redshift": hypothesis["redshift"],
        "source_refs": [prefix + "node", prefix + "catalog", prefix + "judgments"],
        "lines": rows,
    }
