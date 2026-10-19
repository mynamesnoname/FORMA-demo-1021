"""Source-bound, deterministic HS consolidation of surviving type-graph hypotheses.

The input SH/FA/type nodes remain immutable. A merged anchor redshift is a new
result, never a replacement for any Redrock or SH redshift.
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

from FORMA.core.reasoning.ontology.registry import ONTOLOGY

from .cleaned_line_view import cleaned_line_view
from .execution_artifacts import allocate_execution
from .feature_registry import _digest
from .line_alignment import active_alignment
from .qso_report import _active_node
from .reasoning_trace import (reachable_events, record_analysis,
                              register_artifact, register_execution)


SCHEMA = "forma-hs-hypothesis-merge-v1"
KEY_LINES = {
    "Type 1 QSO": frozenset({"line:lya-1216", "line:civ-1549",
                              "line:ciii-1909", "line:mgii-2800"}),
    "Type 2 QSO": frozenset({"line:nev-3426"}),
    "ELG": frozenset({"line:oii-3727", "line:oiii-4960", "line:oiii-5008"}),
    "LRG/BGS": frozenset({"line:cak-3934-abs", "line:cah-3969-abs"}),
}
ABSORPTION_ORDER = ("line:cak-3934-abs", "line:cah-3969-abs")
_LINES = {item.id: item for item in ONTOLOGY.lines}


def _checked(trace: dict, ref: str) -> Path:
    item = trace["artifacts"].get(ref)
    if item is None:
        raise ValueError(f"missing HS source: {ref}")
    path = Path(item["path"]).resolve(strict=True)
    if _digest(path) != item["sha256"]:
        raise ValueError(f"changed HS source: {ref}")
    return path


def _terminal_route_ref(trace: dict, branch_id: str, hypothesis_ref: str,
                        candidate_type: str) -> str:
    """Bind the HS type to the active terminal node rather than a caller label."""
    if "QSO" in candidate_type:
        active = (_active_node(trace, branch_id, hypothesis_ref, "qso.route_result")
                  or _active_node(trace, branch_id, hypothesis_ref, "qso.nev_pairing_gate"))
        if active is None:
            raise ValueError("HS QSO candidate lacks an active terminal route")
        ref, node = active
    else:
        prefix = "elg" if candidate_type == "ELG" else "lrg_bgs"
        key = f"sh2.{prefix}/{quote(hypothesis_ref, safe='')}/{prefix}.route_result"
        events = [event for event in reachable_events(trace, branch_id)
                  if event["kind"] == "analysis_result"
                  and event["payload"]["analysis_ref"] == key]
        if len(events) != 1:
            raise ValueError("HS galaxy candidate lacks one active terminal route")
        event = events[0]
        refs = [ref for ref in event["artifact_refs"]
                if trace["artifacts"][ref]["kind"] == f"{prefix}_node"
                and trace["artifacts"][ref].get("node_execution_id")
                == event["execution"]["node_execution_id"]]
        if len(refs) != 1:
            raise ValueError("HS galaxy route has no unique node artifact")
        ref = refs[0]
        node = json.loads(_checked(trace, ref).read_text(encoding="utf-8"))
        if node.get("node_key") != key or node.get("hypothesis_ref") != hypothesis_ref:
            raise ValueError("HS galaxy route identity differs")
    outcome = node["output"]
    if outcome.get("path_status") != "survive" or outcome.get("candidate_type") != candidate_type:
        raise ValueError("HS candidate differs from its active type route")
    _checked(trace, ref)
    return ref


def _claim(ref: str, row: dict, feature: dict, *, status: str,
           source_ref: str, source: str | None = None) -> dict:
    line = _LINES.get(row["line_id"])
    if line is None:
        raise ValueError(f"unknown HS line: {row['line_id']}")
    center = feature["center_angstrom"]
    if (not isinstance(center, (int, float)) or not math.isfinite(center)
            or center <= 0):
        raise ValueError("HS feature lacks a finite positive centre")
    targeted = (source or feature["source"]) == "LLM_SELECTED"
    return {"hypothesis_ref": ref, "line_id": row["line_id"],
            "feature_id": feature["feature_id"], "wavelength_angstrom": float(center),
            "rest_wavelength_angstrom": line.rest_wavelength,
            "line_kind": line.line_type, "ionization_ev": line.ionization_ev,
            "measurement_source": source or feature["source"],
            "fa_state": None if targeted else row.get("fa_state"),
            "fa_review_status": "not_reviewed" if targeted else "original_measurement",
            "prior_measurement_id": row.get("measurement_id") if targeted else None,
            "prior_measurement_fa_state": row.get("fa_state") if targeted else None,
            "assignment_status": status,
            "source_refs": [source_ref]}


def collect_hypothesis(trace: dict, branch_id: str, ref: str,
                       candidate_type: str, report_refs: list[str]) -> dict:
    """Import original, TBD, aligned and accepted Q8 claims by exact identity."""
    if candidate_type not in KEY_LINES:
        raise ValueError("HS needs a terminal surviving type")
    state = trace["branches"][branch_id]["state"]
    hypothesis = state["registry"]["hypotheses"][ref]
    terminal_ref = _terminal_route_ref(trace, branch_id, ref, candidate_type)
    view = cleaned_line_view(trace, branch_id, ref)
    source_refs = set(view["source_refs"] + report_refs + [terminal_ref])
    for ref_id in source_refs:
        _checked(trace, ref_id)
    graph = "QSO" if "QSO" in candidate_type else candidate_type
    alignment = active_alignment(trace, branch_id, ref, graph)
    aligned = {}
    if alignment is not None:
        source_refs.add(alignment[0])
        aligned = {item["line_id"]: item
                   for item in alignment[1]["output"]["aligned_claims"]}
    claims = []
    unregistered = []
    registry_features = state["registry"]["features"]
    by_line = {row["line_id"]: row for row in view["lines"]}
    for row in view["lines"]:
        measurement_id = row["measurement_id"]
        if measurement_id is None or row["fa_state"] == "signal_absent":
            continue
        if row["line_id"] not in _LINES:
            unregistered.append({"line_id": row["line_id"],
                                 "measurement_id": measurement_id,
                                 "reason": "missing_ontology_line_record"})
            continue
        feature = registry_features[measurement_id]
        assignment = aligned.get(row["line_id"], {})
        status = ("non_tbd" if row["cleaned_pairing"] == "adopted"
                  and assignment.get("status", "original_claim") == "original_claim"
                  else "tbd")
        claims.append(_claim(ref, row, feature, status=status,
                             source_ref=f"sh/{ref}/judgments"))
        source_refs.update(row["fa_vote_artifact_refs"])
        if assignment.get("status") == "resolved":
            feature_id = assignment["effective_feature_id"]
            representative = next((result["representative"]
                                   for collision in alignment[1]["output"]["collisions"]
                                   for line_id, result in collision["line_results"].items()
                                   if line_id == row["line_id"]
                                   and result["status"] == "resolved"
                                   and result["representative"]["candidate_id"] == feature_id), None)
            if representative is None:
                raise ValueError("aligned HS feature lacks its selected pixel evidence")
            claims.append(_claim(ref, row, {"feature_id": feature_id,
                                            "center_angstrom": representative["center_angstrom"],
                                            "source": "LLM_SELECTED"},
                                 status="llm_selected", source_ref=alignment[0]))
    if "QSO" in candidate_type:
        for line_id, row in by_line.items():
            if line_id not in _LINES:
                continue
            node = _active_node(trace, branch_id, ref, f"qso.relative_strength/{line_id}")
            if node is None:
                continue
            source_refs.add(node[0])
            result = node[1]["output"]
            selected = result.get("representative_target_measurement")
            if result.get("status") != "accepted" or selected is None:
                continue
            if result.get("representative_broadness") != "supported_proxy":
                continue
            claims.append(_claim(ref, row, {"feature_id": result["candidate_id"],
                                            "center_angstrom": selected["peak_wavelength_angstrom"],
                                            "source": "LLM_SELECTED"},
                                 status="llm_selected", source_ref=node[0]))
    for item in claims:
        for source_ref in item["source_refs"]:
            _checked(trace, source_ref)
    return {"hypothesis_ref": ref, "candidate_type": candidate_type,
            "original_redshift": hypothesis["redshift"], "claims": claims,
            "unregistered_claims": unregistered,
            "source_refs": sorted(source_refs)}


def _key_pairs(record: dict) -> set[tuple[str, str]]:
    """Shared FA-confirmed CWT pairs link hypotheses even if still TBD."""
    return {(item["line_id"], item["feature_id"]) for item in record["claims"]
            if item["line_id"] in KEY_LINES[record["candidate_type"]]
            and item["measurement_source"] == "CWT"
            and item["fa_state"] == "signal_present"}


def _edges(records: list[dict]) -> list[dict]:
    edges = []
    for i, left in enumerate(records):
        for right in records[i + 1:]:
            if left["candidate_type"] != right["candidate_type"]:
                continue
            shared = sorted(_key_pairs(left) & _key_pairs(right))
            if shared:
                edges.append({"left": left["hypothesis_ref"],
                              "right": right["hypothesis_ref"],
                              "key_pairs": [{"line_id": line, "feature_id": feature}
                                            for line, feature in shared]})
    return edges


def _components(records: list[dict], edges: list[dict]) -> list[list[str]]:
    parent = {row["hypothesis_ref"]: row["hypothesis_ref"] for row in records}

    def find(ref: str) -> str:
        while parent[ref] != ref:
            parent[ref] = parent[parent[ref]]
            ref = parent[ref]
        return ref

    for edge in edges:
        parent[find(edge["right"])] = find(edge["left"])
    groups: dict[str, list[str]] = {}
    for ref in sorted(parent):
        groups.setdefault(find(ref), []).append(ref)
    return sorted(groups.values(), key=lambda group: group[0])


def _pool(records: list[dict]) -> list[dict]:
    def provenance(claim: dict) -> dict:
        return {key: claim.get(key) for key in (
            "hypothesis_ref", "assignment_status", "fa_state", "fa_review_status",
            "measurement_source", "prior_measurement_id", "prior_measurement_fa_state",
            "source_refs")}

    pooled: dict[tuple[str, str], dict] = {}
    for record in records:
        for claim in record["claims"]:
            key = claim["line_id"], claim["feature_id"]
            previous = pooled.get(key)
            if previous is None:
                pooled[key] = {**claim, "provenance": [provenance(claim)]}
            else:
                if (previous["wavelength_angstrom"] != claim["wavelength_angstrom"]
                        or previous["rest_wavelength_angstrom"]
                        != claim["rest_wavelength_angstrom"]):
                    raise ValueError("same HS pair has conflicting measurements")
                previous["provenance"].append(provenance(claim))
    feature_centres: dict[str, float] = {}
    for item in pooled.values():
        feature_id = item["feature_id"]
        centre = item["wavelength_angstrom"]
        if feature_id in feature_centres and feature_centres[feature_id] != centre:
            raise ValueError("one HS feature ID has conflicting observed centres")
        feature_centres[feature_id] = centre
    for item in pooled.values():
        item["provenance"].sort(key=lambda row: row["hypothesis_ref"])
        states = {row["assignment_status"] for row in item["provenance"]}
        item["best_assignment_status"] = ("non_tbd" if "non_tbd" in states else
                                          "tbd" if "tbd" in states else "llm_selected")
        item.pop("hypothesis_ref")
        item.pop("assignment_status")
        item.pop("fa_state")
        item.pop("fa_review_status", None)
        item.pop("prior_measurement_id", None)
        item.pop("prior_measurement_fa_state", None)
        item.pop("source_refs")
    return sorted(pooled.values(), key=lambda item: (
        item["rest_wavelength_angstrom"], item["line_id"], item["feature_id"]))


def _anchor(selected: list[dict], candidate_type: str,
            records: list[dict]) -> tuple[float, dict]:
    eligible = [item for item in selected
                if item["best_assignment_status"] == "non_tbd"
                and item["measurement_source"] != "LLM_SELECTED"]
    emission = [item for item in eligible if item["line_kind"] == "emission"
                and item["ionization_ev"] is not None]
    absorption = [item for item in eligible if item["line_kind"] == "absorption"]
    if candidate_type == "LRG/BGS" and absorption:
        chosen = min(absorption, key=lambda item: (
            ABSORPTION_ORDER.index(item["line_id"])
            if item["line_id"] in ABSORPTION_ORDER else len(ABSORPTION_ORDER),
            item["rest_wavelength_angstrom"], item["feature_id"]))
    elif emission:
        chosen = min(emission, key=lambda item: (
            item["ionization_ev"], item["rest_wavelength_angstrom"],
            item["line_id"], item["feature_id"]))
    elif absorption:
        chosen = min(absorption, key=lambda item: (
            ABSORPTION_ORDER.index(item["line_id"])
            if item["line_id"] in ABSORPTION_ORDER else len(ABSORPTION_ORDER),
            item["rest_wavelength_angstrom"], item["feature_id"]))
    else:
        chosen = None
    if chosen is not None:
        z = chosen["wavelength_angstrom"] / chosen["rest_wavelength_angstrom"] - 1
        return z, {"kind": "line", "line_id": chosen["line_id"],
                   "feature_id": chosen["feature_id"]}
    # The user's fallback chooses an original redshift from the hypothesis
    # with the smallest diagnostic relative observed/predicted error.
    ranked = []
    for record in records:
        z = record["original_redshift"]
        diagnostic = [item for item in record["claims"]
                      if item["line_id"] in KEY_LINES[candidate_type]]
        candidates = diagnostic or record["claims"]
        error = min((abs(item["wavelength_angstrom"]
                         / (item["rest_wavelength_angstrom"] * (1 + z)) - 1)
                     for item in candidates), default=math.inf)
        ranked.append((error, record["hypothesis_ref"], z))
    error, ref, z = min(ranked)
    return z, {"kind": "original_redshift_fallback",
               "hypothesis_ref": ref, "minimum_relative_error": error if math.isfinite(error) else None}


def _score_better(left: tuple, right: tuple) -> bool:
    """Cardinality, L1, squared residual, then stable pair IDs."""
    if left[0] != right[0]:
        return left[0] > right[0]
    for index in (1, 2):
        if not math.isclose(left[index], right[index], rel_tol=1e-12, abs_tol=1e-14):
            return left[index] < right[index]
    return left[3] < right[3]


def _assignment(pool: list[dict], z: float) -> dict:
    if not math.isfinite(z) or z <= -1:
        raise ValueError("HS anchor redshift must be finite and above -1")
    by_line: dict[str, list[dict]] = {}
    for item in pool:
        by_line.setdefault(item["line_id"], []).append(item)
    lines = sorted(by_line, key=lambda line_id: (
        by_line[line_id][0]["rest_wavelength_angstrom"], line_id))
    choices = [sorted(by_line[line_id], key=lambda item: item["feature_id"])
               for line_id in lines]
    feature_lines: dict[str, set[str]] = {}
    for item in pool:
        feature_lines.setdefault(item["feature_id"], set()).add(item["line_id"])
    shared_feature_ids = {feature_id for feature_id, assigned_lines in feature_lines.items()
                          if len(assigned_lines) > 1}

    @lru_cache(maxsize=None)
    def solve(index: int, used: frozenset[str], max_wavelength: float) -> tuple:
        if index == len(lines):
            return (0, 0.0, 0.0, ())
        best = solve(index + 1, used, max_wavelength)
        rest = choices[index][0]["rest_wavelength_angstrom"]
        previous_rest = (choices[index - 1][0]["rest_wavelength_angstrom"]
                         if index else None)
        for item in choices[index]:
            wl = item["wavelength_angstrom"]
            if (item["feature_id"] in used
                    or previous_rest is not None and rest > previous_rest
                    and wl <= max_wavelength):
                continue
            tail = solve(index + 1, (used | {item["feature_id"]}
                                     if item["feature_id"] in shared_feature_ids else used),
                         max(max_wavelength, wl))
            residual = abs(wl / (rest * (1 + z)) - 1)
            candidate = (tail[0] + 1, tail[1] + residual,
                         tail[2] + residual * residual,
                         ((item["line_id"], item["feature_id"]), *tail[3]))
            if _score_better(candidate, best):
                best = candidate
        return best

    count, absolute_error, square_error, keys = solve(0, frozenset(), 0.0)
    selected = [next(item for item in pool if (item["line_id"], item["feature_id"]) == key)
                for key in keys]
    selected.sort(key=lambda item: (item["rest_wavelength_angstrom"], item["line_id"]))
    selected_by_line = {item["line_id"]: item for item in selected}
    selected_by_feature = {item["feature_id"]: item for item in selected}
    excluded = []
    for item in pool:
        if (item["line_id"], item["feature_id"]) in keys:
            continue
        if item["line_id"] in selected_by_line:
            reason = "another_feature_selected_for_line"
        elif item["feature_id"] in selected_by_feature:
            reason = "feature_selected_for_another_line"
        else:
            reason = "wavelength_order_or_global_score"
        excluded.append({"line_id": item["line_id"], "feature_id": item["feature_id"],
                         "had_fa_confirmation": any(
                             p["fa_state"] == "signal_present" for p in item["provenance"]),
                         "reason": reason})
    return {"selected_pairs": selected, "retained_line_count": count,
            "relative_error_l1": absolute_error,
            "relative_error_l2_squared": square_error,
            "excluded_pairs": excluded}


def _resolve(records: list[dict], edges: list[dict]) -> dict:
    candidate_type = records[0]["candidate_type"]
    all_candidates = _pool(records)
    confirmed_lines = {item["line_id"] for item in all_candidates
                       if any(p["fa_state"] == "signal_present"
                              for p in item["provenance"])}
    fa_excluded = [item for item in all_candidates
                   if item["line_id"] in confirmed_lines
                   and not any(p["fa_state"] == "signal_present"
                               for p in item["provenance"])]
    pool = [item for item in all_candidates if item not in fa_excluded]
    line_features: dict[str, set[str]] = {}
    for item in pool:
        line_features.setdefault(item["line_id"], set()).add(item["feature_id"])
    conflicts = [line_id for line_id, ids in line_features.items() if len(ids) > 1]
    z, anchor = _anchor(pool, candidate_type, records)
    seen = set()
    iterations = []
    stable = False
    result = None
    for _ in range(len(pool) + 2):
        result = _assignment(pool, z)
        next_z, next_anchor = _anchor(result["selected_pairs"], candidate_type, records)
        signature = (z, tuple((item["line_id"], item["feature_id"])
                              for item in result["selected_pairs"]))
        iterations.append({"scoring_redshift": z, "anchor_source": anchor,
                           "retained_line_count": result["retained_line_count"],
                           "relative_error_l1": result["relative_error_l1"],
                           "relative_error_l2_squared": result["relative_error_l2_squared"]})
        if next_z == z:
            stable = True
            anchor = next_anchor
            break
        if signature in seen:
            break
        seen.add(signature)
        z, anchor = next_z, next_anchor
    assert result is not None
    selected_keys = {(item["line_id"], item["feature_id"])
                     for item in result["selected_pairs"]}
    key_evidence = {(pair["line_id"], pair["feature_id"])
                    for edge in edges for pair in edge["key_pairs"]}
    lost_keys = sorted(key_evidence - selected_keys)
    support_lines = {claim["line_id"] for record in records for claim in record["claims"]
                     if claim["line_id"] in KEY_LINES[candidate_type]
                     and (claim["fa_state"] == "signal_present"
                          or claim["measurement_source"] == "LLM_SELECTED")}
    lost_support_lines = sorted(support_lines - {line for line, _ in selected_keys})
    selected = []
    for item in result["selected_pairs"]:
        selected.append({**item,
                         "merge_conflict": item["line_id"] in conflicts,
                         "final_assignment_status": item["best_assignment_status"]})
    type_recheck = bool(lost_keys or lost_support_lines
                        or not any(item["line_id"] in KEY_LINES[candidate_type]
                                   for item in selected))
    return {"merge_status": ("anchor_assignment_unstable" if not stable else
                             "type_recheck_required" if type_recheck else "merged"),
            "merged_anchor_redshift": z if stable else None,
            "anchor_source": anchor if stable else None,
            "all_candidate_pairs": all_candidates,
            "selected_pairs": selected,
            "excluded_pairs": [*result["excluded_pairs"], *({
                "line_id": item["line_id"], "feature_id": item["feature_id"],
                "had_fa_confirmation": False,
                "reason": "fa_confirmed_alternative_for_line"} for item in fa_excluded)],
            "fa_resolved_line_ids": sorted({item["line_id"] for item in fa_excluded}),
            "merge_tbd_line_ids": sorted(conflicts),
            "lost_shared_key_pairs": [{"line_id": line, "feature_id": feature}
                                      for line, feature in lost_keys],
            "lost_type_support_line_ids": lost_support_lines,
            "type_recheck_required": type_recheck,
            "retained_line_count": result["retained_line_count"],
            "relative_error_l1": result["relative_error_l1"],
            "relative_error_l2_squared": result["relative_error_l2_squared"],
            "iterations": iterations}


def merge_hypotheses(records: list[dict]) -> dict:
    """Freeze original connectivity, merge closest eligible groups, solve globally."""
    refs = [row["hypothesis_ref"] for row in records]
    if len(refs) != len(set(refs)):
        raise ValueError("duplicate HS hypothesis")
    if any(row["candidate_type"] not in KEY_LINES for row in records):
        raise ValueError("unsupported HS type")
    by_ref = {row["hypothesis_ref"]: row for row in records}
    edges = _edges(records)
    groups = []
    for members in _components(records, edges):
        candidate_type = by_ref[members[0]]["candidate_type"]
        component_edges = [edge for edge in edges
                           if edge["left"] in members and edge["right"] in members]
        active = [{"members": [ref], "redshift": by_ref[ref]["original_redshift"]}
                  for ref in members]
        steps = []
        while len(active) > 1:
            eligible = []
            for i, left in enumerate(active):
                for j in range(i + 1, len(active)):
                    right = active[j]
                    bridges = [edge for edge in component_edges if (
                        edge["left"] in left["members"] and edge["right"] in right["members"]
                        or edge["right"] in left["members"] and edge["left"] in right["members"])]
                    if bridges:
                        eligible.append((abs(left["redshift"] - right["redshift"]),
                                         left["members"], right["members"], i, j, bridges))
            if not eligible:
                raise ValueError("connected HS group has no eligible pair")
            distance, left_ids, right_ids, i, j, bridges = min(eligible)
            joined = sorted(left_ids + right_ids)
            interim = _resolve([by_ref[ref] for ref in joined],
                               [edge for edge in component_edges
                                if edge["left"] in joined and edge["right"] in joined])
            steps.append({"left_members": left_ids, "right_members": right_ids,
                          "redshift_distance": distance,
                          "bridging_edges": bridges,
                          "interim_status": interim["merge_status"],
                          "interim_anchor_redshift": interim["merged_anchor_redshift"]})
            next_z = (interim["merged_anchor_redshift"] if interim["merged_anchor_redshift"] is not None
                      else min((by_ref[ref]["original_redshift"], ref) for ref in joined)[0])
            active = [item for k, item in enumerate(active) if k not in {i, j}]
            active.append({"members": joined, "redshift": next_z})
            active.sort(key=lambda item: item["members"])
        resolution = (_resolve([by_ref[ref] for ref in members], component_edges)
                      if len(members) > 1 else None)
        groups.append({"group_id": "hs.merge/" + "+".join(quote(ref, safe="") for ref in members),
                       "candidate_type": candidate_type, "member_hypotheses": members,
                       "original_redshifts": {ref: by_ref[ref]["original_redshift"]
                                              for ref in members},
                       "unregistered_claims": {ref: by_ref[ref].get("unregistered_claims", [])
                                               for ref in members},
                       "shared_key_edges": component_edges,
                       "merge_steps": steps,
                       "merge_status": resolution["merge_status"] if resolution else "singleton",
                       "merged_anchor_redshift": (resolution["merged_anchor_redshift"]
                                                  if resolution else by_ref[members[0]]["original_redshift"]),
                       "resolution": resolution})
    return {"schema_version": SCHEMA, "groups": groups, "shared_key_edges": edges}


def run_hs_merge(trace: dict, *, branch_id: str, routes: dict,
                 output_root: str | Path) -> dict:
    """Persist a replayable HS consolidation node after every type path closes."""
    key = "hs.merge_groups"
    if key in trace["branches"][branch_id]["state"]["analysis_results"]:
        raise ValueError("HS merge already active; fork before rerunning")
    records = []
    for ref, route in sorted(routes.items()):
        if route["path_status"] != "survive":
            continue
        reports = [route[field] for field in ("report_ref", "qso_report_ref")
                   if route.get(field)]
        records.append(collect_hypothesis(trace, branch_id, ref,
                                          route["candidate_type"], reports))
    merged = merge_hypotheses(records)
    source_refs = sorted({source for record in records for source in record["source_refs"]})
    for source in source_refs:
        _checked(trace, source)
    allocation = allocate_execution(output_root, run_id=trace["run_id"],
                                    branch_id=branch_id, node_key=key)
    node = {"schema_version": SCHEMA, "run_id": trace["run_id"],
            "branch_id": branch_id, "node_key": key,
            "node_execution_id": allocation.node_execution_id,
            "attempt_id": allocation.attempt_id, "input_refs": source_refs,
            "output": merged}
    allocation.path("node.json").write_text(
        json.dumps(node, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8")
    register_execution(trace, allocation)
    ref = f"hs/{allocation.node_execution_id}/node"
    register_artifact(trace, ref, allocation.path("node.json"), "hs_merge_node",
                      node_execution_id=allocation.node_execution_id)
    record_analysis(trace, branch_id, kind="analysis_result", analysis_ref=key,
                    artifact_refs=[ref, *source_refs],
                    node_execution_id=allocation.node_execution_id)
    return {"artifact_ref": ref, "node": node}
