"""Run optional FA observations after feature reality, before type routing."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from FORMA.core.line_status import is_kept_evidence

from .cleaned_line_view import _read_artifact
from .fa_doublet import claimed_doublet_ids, review_doublet
from .fa_lya_forest import LYA_ID, review_lya_forest


async def review_fa_advisories(*, trace: dict, branch_id: str,
                               output_root: str | Path, llm: Any,
                               concurrency: int = 3) -> dict:
    """Review eligible SH claims without changing feature votes or type gates."""
    if concurrency < 1:
        raise ValueError("FA advisory concurrency must be positive")
    root = Path(output_root).resolve()
    if trace.get("artifact_root") != str(root):
        raise ValueError("FA advisory root differs from the reasoning tree")
    entries = []
    active = trace["branches"][branch_id]["state"]["active_pre_analysis"]
    for ref in active:
        judgments = _read_artifact(trace, f"sh/{ref}/judgments")
        forest_eligible = any(row["line_id"] == LYA_ID
                              and is_kept_evidence(row["status"])
                              for row in judgments)
        doublets = claimed_doublet_ids(trace, branch_id, ref)
        entry = {"hypothesis_ref": ref, "lya_forest": None, "doublets": []}
        if forest_eligible:
            result = await review_lya_forest(
                trace=trace, branch_id=branch_id, hypothesis_ref=ref,
                output_root=root, llm=llm, concurrency=concurrency)
            entry["lya_forest"] = {"node_ref": result["node_ref"],
                                   "status": result["node"]["status"]}
        for doublet_id in doublets:
            result = await review_doublet(
                trace=trace, branch_id=branch_id, hypothesis_ref=ref,
                doublet_id=doublet_id, output_root=root, llm=llm,
                concurrency=concurrency)
            entry["doublets"].append({"doublet_id": doublet_id,
                                      "node_ref": result["node_ref"],
                                      "status": result["node"]["status"]})
        entries.append(entry)
    summary = {"schema_version": "forma-fa-advisory-summary-v1",
               "run_id": trace["run_id"], "branch_id": branch_id,
               "consultative_only": True, "hypotheses": entries}
    (root / "fa_advisory_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8")
    return summary
