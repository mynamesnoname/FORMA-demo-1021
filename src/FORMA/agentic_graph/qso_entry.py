"""First executable QSO graph segment: hard route, cleaned view, Ne V and inventory."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

from FORMA.core.reasoning.ontology.registry import ONTOLOGY
from FORMA.core.reasoning.ontology.rule_parameters import effective_operand_threshold

from .cleaned_line_view import cleaned_line_view
from .execution_artifacts import ExecutionAllocation, allocate_execution, validate_execution
from .feature_registry import _digest
from .qso_type1_gate import TYPE1_LINES
from .qso_transfer_guard import type1_transfer_evidence
from .reasoning_trace import (reachable_events, record_analysis, register_artifact,
                              register_execution)


GRAPH_VERSION = "forma-qso-entry-v1"
NEV = "line:nev-3426"
_QSO_CLASSES = {"Type 1 QSO", "Type 2 QSO"}


def _key(hypothesis_ref: str, node_type: str) -> str:
    if node_type == "sh2.initial_route":
        return f"sh2.initial_route/{quote(hypothesis_ref, safe='')}"
    return f"sh2.qso/{quote(hypothesis_ref, safe='')}/{node_type}"


def _save_node(trace: dict, branch_id: str, hypothesis_ref: str, node_type: str,
               output: dict, source_refs: list[str], output_root: str | Path,
               *, allocation: ExecutionAllocation | None = None,
               extra_artifacts: dict[str, tuple[str, str]] | None = None,
               created_by: str = "code") -> dict:
    key = _key(hypothesis_ref, node_type)
    if key in trace["branches"][branch_id]["state"]["analysis_results"]:
        raise ValueError("QSO node already completed on this branch; fork before revisiting")
    if any(ref not in trace["artifacts"] for ref in source_refs):
        raise ValueError("QSO node cites an unknown source artifact")
    for ref in source_refs:
        item = trace["artifacts"][ref]
        if _digest(Path(item["path"])) != item["sha256"]:
            raise ValueError(f"QSO source artifact changed: {ref}")
    if created_by not in {"code", "mixed"}:
        raise ValueError("invalid QSO node creator")
    if allocation is None:
        allocation = allocate_execution(output_root, run_id=trace["run_id"],
                                        branch_id=branch_id, node_key=key)
    else:
        validate_execution(allocation)
        if (allocation.run_id != trace["run_id"] or allocation.branch_id != branch_id
                or allocation.node_key != key or allocation.root != Path(output_root).resolve()):
            raise ValueError("QSO allocation belongs to another node or root")
    node = {
        "schema_version": "forma-qso-node-v1", "graph_version": GRAPH_VERSION,
        "run_id": trace["run_id"], "branch_id": branch_id,
        "hypothesis_ref": hypothesis_ref, "node_key": key, "node_type": node_type,
        "status": "completed", "input_refs": source_refs, "output": output,
        "evidence_refs": source_refs, "unresolved_reasons": [],
        "created_by": created_by, "node_execution_id": allocation.node_execution_id,
        "attempt_id": allocation.attempt_id,
    }
    with allocation.path("node.json").open("x", encoding="utf-8") as stream:
        json.dump(node, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    register_execution(trace, allocation)
    result_ref = f"sh2/{allocation.node_execution_id}/node"
    register_artifact(trace, result_ref, allocation.path("node.json"), "qso_node",
                      node_execution_id=allocation.node_execution_id)
    extras = {}
    for name, (filename, kind) in (extra_artifacts or {}).items():
        ref = f"sh2/{allocation.node_execution_id}/{name}"
        register_artifact(trace, ref, allocation.path(filename), kind,
                          node_execution_id=allocation.node_execution_id)
        extras[name] = ref
    record_analysis(trace, branch_id, kind="analysis_result", analysis_ref=key,
                    artifact_refs=[result_ref, *extras.values(), *source_refs],
                    node_execution_id=allocation.node_execution_id)
    return {"node": node, "artifact_ref": result_ref,
            "extra_artifact_refs": extras,
            "node_path": str(allocation.path("node.json")),
            "node_sha256": _digest(allocation.path("node.json"))}


def _broad_inventory(view: dict, trace: dict) -> dict:
    by_id = {row["line_id"]: row for row in view["lines"]}
    registry_lines = {line.id: line for line in ONTOLOGY.lines}
    boundary = effective_operand_threshold("rule:formal-qso-broad-width", "fwhm_kms")
    catalog_item = trace["artifacts"][f"sh/{view['hypothesis_ref']}/catalog"]
    catalog = json.loads(Path(catalog_item["path"]).read_text(encoding="utf-8"))
    if _digest(Path(catalog_item["path"])) != catalog_item["sha256"]:
        raise ValueError("SH catalog changed during QSO inventory")
    inventory = []
    for line_id in TYPE1_LINES:
        line = registry_lines[line_id]
        predicted = line.rest_wavelength * (1 + view["fixed_redshift"])
        row = by_id.get(line_id)
        if row is None:
            if catalog["wavelength_min"] <= predicted <= catalog["wavelength_max"]:
                raise ValueError("in-range Type 1 line is missing from SH catalog")
            coverage = "outside_range"
            broadness = "unresolved"
        else:
            coverage = "needs_q5"
            width = row["fwhm_km_s"]
            if row["cleaned_pairing"] == "adopted" and width is not None:
                broadness = "supported" if width >= boundary["value"] else "not_supported"
            else:
                broadness = "unresolved"
        inventory.append({
            "line_id": line_id, "predicted_obs_angstrom": predicted,
            "coverage": coverage,
            "cleaned_pairing": row["cleaned_pairing"] if row else "out_of_scope",
            "measurement_id": row["measurement_id"] if row else None,
            "fwhm_km_s": row["fwhm_km_s"] if row else None,
            "broadness": broadness,
        })
    supported = [item for item in inventory if item["broadness"] == "supported"]
    return {
        "lines": inventory,
        "any_supported_broad_line": True if supported else None,
        "strict_broad_fwhm_km_s": boundary["value"],
        "strict_broad_threshold_source": boundary["source"],
        "strict_broad_threshold_payload_sha256": boundary["payload_digest"],
        "next_node": "qso.missing_broad_line_queue",
    }


def run_qso_entry(trace: dict, *, branch_id: str, hypothesis_ref: str,
                  output_root: str | Path, handoff_ref: str | None = None) -> dict:
    """Persist Q0–Q3 as needed; never inspect skyline risk or invent FA votes.

    Other preliminary object classes belong to their own type graphs. `null`
    is a hard prune; an adopted Ne V pair takes the project Type 2 exit.
    This segment deliberately stops before Q4 and any Type 1 survival claim.
    """
    branch = trace["branches"][branch_id]
    state = branch["state"]
    if hypothesis_ref not in state["active_pre_analysis"]:
        raise ValueError("SH pre-analysis must be active before QSO routing")
    registry = state["registry"]
    hypothesis = registry["hypotheses"][hypothesis_ref]
    classification = hypothesis["classification"]
    handoff = None
    handoff_event = None
    if handoff_ref is not None:
        handoff_sources = {
            "ELG": ("ELG", "elg", "elg_node"),
            "LRG/BGS": ("LRG/BGS", "lrg_bgs", "lrg_bgs_node"),
        }
        if classification not in handoff_sources:
            raise ValueError("QSO handoff requires a supported initial classification")
        from_graph, source_prefix, artifact_kind = handoff_sources[classification]
        from .qso_report import _event_at_or_before_fork
        route_key = f"sh2.{source_prefix}/{quote(hypothesis_ref, safe='')}/{source_prefix}.route_result"
        event = _event_at_or_before_fork(trace, branch_id, route_key)
        item = trace["artifacts"].get(handoff_ref)
        if (route_key not in state["analysis_results"] or event is None or item is None
                or item["kind"] != artifact_kind or handoff_ref not in event["artifact_refs"]):
            raise ValueError("QSO handoff has no active source route")
        path = Path(item["path"]).resolve(strict=True)
        if _digest(path) != item["sha256"]:
            raise ValueError("QSO handoff source route changed")
        handoff = json.loads(path.read_text(encoding="utf-8"))
        output = handoff.get("output", {})
        if (handoff.get("node_key") != route_key
                or handoff.get("hypothesis_ref") != hypothesis_ref
                or output.get("path_status") != "transfer"
                or output.get("from_graph") != from_graph
                or output.get("to_graph") != "QSO"
                or output.get("fixed_redshift") != registry["hypotheses"][hypothesis_ref]["redshift"]):
            raise ValueError("QSO handoff route identity or outcome differs")
        handoff_event = next((event for event in reversed(reachable_events(trace, branch_id))
                              if event["kind"] == "type_graph_handoff"
                              and event["payload"].get("route_ref") == handoff_ref
                              and event["payload"].get("hypothesis_ref") == hypothesis_ref
                              and event["payload"].get("from_graph") == from_graph
                              and event["payload"].get("to_graph") == "QSO"), None)
        if handoff_event is None:
            raise ValueError("QSO handoff event is missing")
    if classification is not None and classification not in _QSO_CLASSES and handoff is None:
        raise ValueError("this hypothesis belongs to a different initial type graph")
    if any(vote["origin"] == "offline_fixture"
           for entry in registry["features"].values() for vote in entry["votes"]):
        raise ValueError("fixture FA ballots cannot enter the scientific QSO graph")
    source = f"sh/{hypothesis_ref}/node"
    if source != hypothesis["node_artifact"]:
        raise ValueError("pre-analysis node artifact identity differs")
    # Validate the complete QSO input before recording the first route node.
    # A broken SH/FA source must not leave a partially completed graph path.
    view = None
    vote_refs: list[str] = []
    inventory = None
    if classification is not None:
        view = cleaned_line_view(trace, branch_id, hypothesis_ref)
        vote_refs = sorted({ref for row in view["lines"]
                            for ref in row["fa_vote_artifact_refs"]})
        for ref in vote_refs:
            item = trace["artifacts"].get(ref)
            if item is None or _digest(Path(item["path"])) != item["sha256"]:
                raise ValueError(f"QSO FA vote artifact missing or changed: {ref}")
        nev_rows = [row for row in view["lines"] if row["line_id"] == NEV]
        nev = nev_rows[0] if nev_rows and nev_rows[0]["measurement_id"] is not None else None
        if handoff is not None:
            output = handoff["output"]
            mode = output.get("qso_transfer_mode", "type2")
            if mode == "type2":
                if (output.get("reason_code") != "adopted_nev"
                        or nev is None or nev["cleaned_pairing"] != "adopted"
                        or nev["measurement_id"] != output.get("nev_measurement_id")):
                    raise ValueError("QSO handoff lacks the adopted Ne V measurement")
            elif mode == "type1":
                evidence = type1_transfer_evidence(view["lines"])
                if (output.get("reason_code") != "adopted_qso_diagnostic"
                        or nev is not None and nev["cleaned_pairing"] == "adopted"
                        or not evidence["trigger_pairs"]
                        or output.get("qso_trigger_pairs") != evidence["trigger_pairs"]
                        or output.get("galaxy_retention_by_mgii_pair")
                        != evidence["galaxy_retention_by_mgii_pair"]):
                    raise ValueError("QSO Type 1 handoff lacks valid adopted diagnostic lines")
            else:
                raise ValueError("unknown QSO handoff mode")
        if nev is None or nev["cleaned_pairing"] != "adopted":
            inventory = _broad_inventory(view, trace)
    if handoff is None:
        route = _save_node(trace, branch_id, hypothesis_ref, "sh2.initial_route", {
            "preliminary_classification": classification,
            "fixed_redshift": hypothesis["redshift"],
            "pre_analysis_ref": source,
            "route_status": "pruned" if classification is None else "entered",
            "reason": "preliminary_classification_null" if classification is None else None,
            "initial_graph": None if classification is None else "QSO",
        }, [source], output_root)
    else:
        route = None
    nodes = [route] if route is not None else []
    if classification is None:
        return {"route_status": "pruned", "path_status": "pruned", "nodes": nodes}

    entry = _save_node(trace, branch_id, hypothesis_ref, "qso.entry", {
        "preliminary_classification": classification,
        "fixed_redshift": hypothesis["redshift"],
        "pre_analysis_ref": source,
        "initial_route_ref": route["artifact_ref"] if route is not None else None,
        "handoff_ref": handoff_ref,
        "route_history": (handoff_event["payload"]["route_history"]
                          if handoff_event is not None else ["QSO"]),
        "current_graph": "QSO", "entry_mode": "handoff" if handoff else "initial",
    }, [route["artifact_ref"] if route is not None else handoff_ref, source], output_root)
    nodes.append(entry)
    q1 = _save_node(trace, branch_id, hypothesis_ref, "qso.evidence_view",
                    {"cleaned_line_view": view},
                    [entry["artifact_ref"], *view["source_refs"], *vote_refs],
                    output_root)
    nodes.append(q1)
    if nev is not None:
        pairing = nev["cleaned_pairing"]
        q2 = _save_node(trace, branch_id, hypothesis_ref, "qso.nev_pairing_gate", {
            "line_id": NEV, "measurement_id": nev["measurement_id"],
            "sh_status": nev["sh_status"], "fa_state": nev["fa_state"],
            "pairing_state": pairing,
            "candidate_type": "Type 2 QSO" if pairing == "adopted" else None,
            "path_status": "survive" if pairing == "adopted" else "continue",
            "next_node": "qso.analysis_report" if pairing == "adopted"
                         else "qso.broad_line_inventory",
        }, [q1["artifact_ref"], *nev["fa_vote_artifact_refs"]], output_root)
        nodes.append(q2)
        if pairing == "adopted":
            return {"route_status": "entered", "path_status": "survive",
                    "candidate_type": "Type 2 QSO", "nodes": nodes}

    q3 = _save_node(trace, branch_id, hypothesis_ref, "qso.broad_line_inventory",
                    inventory, [q1["artifact_ref"]], output_root)
    nodes.append(q3)
    return {"route_status": "entered", "path_status": "in_progress",
            "next_node": "qso.missing_broad_line_queue", "nodes": nodes}
