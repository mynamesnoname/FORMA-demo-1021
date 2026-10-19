"""Code-owned, non-exclusive evidence checks for the first type graph."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

from .cleaned_line_view import cleaned_line_view
from .elg_path import _dn4000
from .execution_artifacts import allocate_execution
from .feature_registry import _digest
from .qso_transfer_guard import type1_transfer_evidence
from .reasoning_trace import (record_entry_route, register_artifact,
                              register_execution)


NEV = "line:nev-3426"
CA = ("line:cak-3934-abs", "line:cah-3969-abs")
OII = "line:oii-3727"
OIII = ("line:oiii-4960", "line:oiii-5008")


def route_type_entry(trace: dict, *, branch_id: str, hypothesis_ref: str,
                     output_root: str | Path) -> dict:
    """Record every check; choose a first investigation graph, not a final class."""
    hypothesis = trace["branches"][branch_id]["state"]["registry"]["hypotheses"][hypothesis_ref]
    if hypothesis.get("classification") is not None or hypothesis.get("entry_route_ref"):
        raise ValueError("code route requires a line-only SH node without an earlier route")
    view = cleaned_line_view(trace, branch_id, hypothesis_ref)
    rows = {row["line_id"]: row for row in view["lines"]}
    def adopted(line_id: str) -> dict | None:
        row = rows.get(line_id)
        return ({"line_id": line_id, "measurement_id": row["measurement_id"]}
                if row and row["cleaned_pairing"] == "adopted" else None)
    nev = adopted(NEV)
    type1 = type1_transfer_evidence(view["lines"])
    ca = [pair for line_id in CA if (pair := adopted(line_id))]
    oii = adopted(OII)
    oiii = [pair for line_id in OIII if (pair := adopted(line_id))]
    oiii_pair = (len(oiii) == 2 and
                 oiii[0]["measurement_id"] != oiii[1]["measurement_id"])
    catalog_ref = f"sh/{hypothesis_ref}/catalog"
    catalog_item = trace["artifacts"][catalog_ref]
    catalog_file = Path(catalog_item["path"]).resolve(strict=True)
    if _digest(catalog_file) != catalog_item["sha256"]:
        raise ValueError("VI catalog changed before code route")
    catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
    dn = _dn4000(trace, hypothesis_ref, hypothesis["redshift"], catalog)
    checks = [
        {"name": "nev", "positive": bool(nev), "pairs": [nev] if nev else []},
        {"name": "qso_type1", "positive": bool(type1["trigger_pairs"]),
         "pairs": type1["trigger_pairs"],
         "mgii_pair_retains_galaxy": type1["galaxy_retention_by_mgii_pair"]},
        {"name": "old_population", "positive": dn["reference_strength"] == "strong" or bool(ca),
         "pairs": ca, "dn4000": dn},
        {"name": "emission_galaxy", "positive": bool(oii or oiii_pair),
         "oii_pair": oii, "oiii_pairs": oiii,
         "oiii_distinct_pair": oiii_pair},
    ]
    if nev:
        graph, reason = "QSO", "adopted_nev"
    elif type1["trigger_pairs"]:
        graph, reason = "QSO", "adopted_qso_diagnostic"
    elif dn["reference_strength"] == "strong" or ca:
        graph, reason = "LRG/BGS", "old_population_candidate"
    elif oii or oiii_pair:
        graph, reason = "ELG", "emission_candidate"
    else:
        graph, reason = None, "no_adopted_entry_evidence"
    eligible = []
    for item in checks:
        if not item["positive"]:
            continue
        candidate = ("QSO" if item["name"] in {"nev", "qso_type1"} else
                     "LRG/BGS" if item["name"] == "old_population" else "ELG")
        if candidate not in eligible:
            eligible.append(candidate)
    key = f"sh2.entry_router/{quote(hypothesis_ref, safe='')}"
    allocation = allocate_execution(output_root, run_id=trace["run_id"],
                                    branch_id=branch_id, node_key=key)
    vote_refs = sorted({ref for row in view["lines"]
                        for ref in row["fa_vote_artifact_refs"]})
    refs = [*view["source_refs"], catalog_ref, "spectrum_npz", *vote_refs]
    for ref in refs:
        item = trace["artifacts"][ref]
        if _digest(Path(item["path"])) != item["sha256"]:
            raise ValueError(f"entry evidence changed: {ref}")
    node = {"schema_version": "forma-type-entry-route-v1",
            "run_id": trace["run_id"], "branch_id": branch_id,
            "hypothesis_ref": hypothesis_ref, "node_key": key,
            "input_refs": sorted(set(refs)),
            "output": {"checks": checks, "selected_initial_graph": graph,
                       "selected_reason": reason,
                       "eligible_graphs": eligible}}
    path = allocation.path("node.json")
    with path.open("x", encoding="utf-8") as stream:
        json.dump(node, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    register_execution(trace, allocation)
    ref = f"entry_route/{allocation.node_execution_id}/node"
    register_artifact(trace, ref, path, "entry_route_node",
                      node_execution_id=allocation.node_execution_id)
    record_entry_route(trace, branch_id, hypothesis_ref=hypothesis_ref,
                       initial_graph=graph, route_ref=ref,
                       node_execution_id=allocation.node_execution_id)
    return {"node": node, "artifact_ref": ref}
