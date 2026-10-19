"""Branch-local ELG type graph from frozen SH/FA evidence.

The Canvas' [Ne V] handoff is executable. Its Ca/Dn4000 exclusion and
emission-absence failure remain unresolved until their scientific contracts
are approved; neither is silently promoted to a hard gate here.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from urllib.parse import quote

import numpy as np

from FORMA.core.config.analysis_method import load_analysis_method
from FORMA.core.reasoning.ontology.query import (
    dn4000_interpretation_bands, get_index_band,
)

from .cleaned_line_view import cleaned_line_view
from .execution_artifacts import allocate_execution
from .feature_registry import _digest
from .line_alignment import active_alignment, render_alignment_markdown, run_line_alignment
from .qso_transfer_guard import type1_transfer_evidence
from .reasoning_trace import (
    reachable_events, record_analysis, record_type_handoff, register_artifact,
    register_execution,
)


GRAPH_VERSION = "forma-elg-type-graph-v1"
NEV = "line:nev-3426"
CA_K = "line:cak-3934-abs"
CA_H = "line:cah-3969-abs"
OIII = ("line:oiii-4960", "line:oiii-5008")
OII = "line:oii-3727"


def _key(hypothesis_ref: str, node_type: str) -> str:
    return f"sh2.elg/{quote(hypothesis_ref, safe='')}/{node_type}"


def _checked_artifact(trace: dict, ref: str) -> Path:
    item = trace["artifacts"].get(ref)
    if item is None:
        raise ValueError(f"unregistered ELG source: {ref}")
    path = Path(item["path"]).resolve(strict=True)
    if _digest(path) != item["sha256"]:
        raise ValueError(f"changed ELG source: {ref}")
    return path


def _save(trace: dict, branch_id: str, hypothesis_ref: str, node_type: str,
          output: dict, source_refs: list[str], output_root: str | Path,
          *, report: str | None = None) -> dict:
    key = _key(hypothesis_ref, node_type)
    if key in trace["branches"][branch_id]["state"]["analysis_results"]:
        raise ValueError("ELG node already active on branch; fork before revisiting")
    for ref in source_refs:
        _checked_artifact(trace, ref)
    allocation = allocate_execution(output_root, run_id=trace["run_id"],
                                    branch_id=branch_id, node_key=key)
    node = {
        "schema_version": "forma-elg-node-v1", "graph_version": GRAPH_VERSION,
        "run_id": trace["run_id"], "branch_id": branch_id,
        "hypothesis_ref": hypothesis_ref, "node_key": key,
        "node_type": node_type, "status": "completed",
        "input_refs": source_refs, "evidence_refs": source_refs,
        "output": output, "unresolved_reasons": output.get("unresolved_reasons", []),
        "created_by": "code", "node_execution_id": allocation.node_execution_id,
        "attempt_id": allocation.attempt_id,
    }
    with allocation.path("node.json").open("x", encoding="utf-8") as stream:
        json.dump(node, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    register_execution(trace, allocation)
    ref = f"sh2/{allocation.node_execution_id}/node"
    register_artifact(trace, ref, allocation.path("node.json"), "elg_node",
                      node_execution_id=allocation.node_execution_id)
    refs = [ref]
    if report is not None:
        allocation.path("report.md").write_text(report, encoding="utf-8")
        report_ref = f"sh2/{allocation.node_execution_id}/report"
        register_artifact(trace, report_ref, allocation.path("report.md"), "elg_report",
                          node_execution_id=allocation.node_execution_id)
        refs.append(report_ref)
    record_analysis(trace, branch_id, kind="analysis_result", analysis_ref=key,
                    artifact_refs=[*refs, *source_refs],
                    node_execution_id=allocation.node_execution_id)
    return {"node": node, "artifact_ref": ref,
            "report_ref": refs[1] if report is not None else None}


def _line(row: dict | None, line_id: str) -> dict:
    return {
        "line_id": line_id,
        "measurement_id": row["measurement_id"] if row else None,
        "sh_status": row["sh_status"] if row else "outside_sh_catalog",
        "fa_state": row["fa_state"] if row else None,
        "cleaned_pairing": row["cleaned_pairing"] if row else "outside_sh_catalog",
        "fa_vote_artifact_refs": row["fa_vote_artifact_refs"] if row else [],
    }


def _dn4000(trace: dict, hypothesis_ref: str, redshift: float,
            catalog: dict) -> dict:
    """Mask-aware reference index, never a type veto."""
    spectrum = _checked_artifact(trace, "spectrum_npz")
    if (spectrum != Path(catalog["spectrum_npz_path"]).resolve(strict=True)
            or trace["artifacts"]["spectrum_npz"]["sha256"]
            != catalog["spectrum_npz_sha256"]):
        raise ValueError("ELG spectrum differs from frozen catalog")
    band = get_index_band("index:dn4000")
    if band is None:
        raise ValueError("Dn4000 ontology band is absent")
    with np.load(spectrum) as data:
        wl = np.asarray(data["wavelength"])
        flux = np.asarray(data["flux"])
        ivar = np.asarray(data["ivar"]) if "ivar" in data else np.full_like(flux, np.nan)
    if (wl.ndim != 1 or not len(wl) or flux.shape != wl.shape or ivar.shape != wl.shape
            or not np.isfinite(wl).all() or not np.all(np.diff(wl) > 0)):
        raise ValueError("invalid frozen spectrum for ELG Dn4000")
    masked = np.zeros(len(wl), dtype=bool)
    for region in catalog.get("masked_regions", []):
        if (not isinstance(region, (list, tuple)) or len(region) != 2
                or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in region)
                or region[0] > region[1]):
            raise ValueError("invalid frozen ELG mask interval")
        masked |= (wl >= region[0]) & (wl <= region[1])
    valid = np.isfinite(flux) & np.isfinite(ivar) & (ivar > 0) & ~masked
    windows = {
        "blue": (band.blue_low * (1 + redshift), band.blue_high * (1 + redshift)),
        "red": (band.red_low * (1 + redshift), band.red_high * (1 + redshift)),
    }
    minimum = load_analysis_method().evaluation.dn4000_min_samples_per_band
    samples = {}
    for name, (low, high) in windows.items():
        within = (wl >= low) & (wl < high)
        usable = within & valid
        samples[name] = {
            "window_angstrom": [low, high],
            "fully_covered": bool(wl[0] <= low and high <= wl[-1]),
            "sample_count": int(np.count_nonzero(within)),
            "usable_sample_count": int(np.count_nonzero(usable)),
            "mean_flux": float(np.mean(flux[usable])) if np.any(usable) else None,
        }
    usable_index = all(item["fully_covered"] and
                       item["usable_sample_count"] >= minimum
                       for item in samples.values())
    blue = samples["blue"]["mean_flux"]
    red = samples["red"]["mean_flux"]
    if usable_index and blue is not None and red is not None and blue > 0:
        value = red / blue
        if not math.isfinite(value):
            value = None
    else:
        value = None
    bands = dn4000_interpretation_bands()
    return {
        "index_id": "index:dn4000", "rule_id": "rule:formal-dn4000-interpretation",
        "reference_bands": bands, "minimum_valid_samples_per_band": minimum,
        "windows": samples, "value": value,
        "reference_strength": ("strong" if value is not None and value > bands["strong"]
                               else "moderate" if value is not None and
                               value > bands["moderate_low"]
                               else "not_strong" if value is not None else "unknown"),
        "consultative_only": True,
        "unresolved_reason": None if value is not None else "insufficient_usable_band_data",
    }


def _report(hypothesis_ref: str, redshift: float, route: dict,
            nev: dict, old: dict, emission: dict, alignment: dict | None = None,
            alignment_ref: str | None = None) -> str:
    def item(value: dict) -> str:
        return f"{value['cleaned_pairing']} ({value['measurement_id'] or 'none'})"

    lines = [
        "# ELG hypothesis graph report", "",
        f"- Hypothesis: `{hypothesis_ref}`", f"- Tested redshift: `{redshift!r}`",
        f"- Graph path: `{route['path_status']}`",
        f"- Candidate type: `{route['candidate_type'] or 'unresolved'}`", "",
        "## Recorded evidence", "",
        f"- [Ne V]: {item(nev)}",
        f"- Type 1 transfer pairs: {route.get('qso_trigger_pairs', [])}",
        f"- Retained diagnostic pairs: {route.get('retained_diagnostic_pairs', [])}",
        f"- Galaxy retained by Mg II emission/absorption pair: "
        f"{route.get('galaxy_retention_by_mgii_pair', False)}",
        f"- Ca K/H adopted components: {', '.join(old['adopted_ca_line_ids']) or 'none'}",
        f"- Dn4000: {old['dn4000']['value']!r} "
        f"({old['dn4000']['reference_strength']}; advisory)",
        f"- [O III] doublet A: {emission['A']}",
        f"- [O II] B: {emission['B']}", "",
        "## Route", "",
        f"- Reason: `{route['reason_code']}`",
        f"- Transfer target: `{route.get('to_graph') or 'none'}`", "",
        "## Open items", "",
    ]
    lines.extend(f"- `{reason}`" for reason in route["unresolved_reasons"])
    if not route["unresolved_reasons"]:
        lines.append("- None recorded.")
    if alignment and alignment["collisions"]:
        lines.extend(["", render_alignment_markdown(alignment,
                                                     node_ref=alignment_ref).rstrip()])
    return "\n".join(lines) + "\n"


def run_elg_path(trace: dict, *, branch_id: str, hypothesis_ref: str,
                 output_root: str | Path, defer_report: bool = False) -> dict:
    """Run E0–E5; adopted Ne V or diagnostic lines transfer to QSO."""
    branch = trace["branches"][branch_id]
    state = branch["state"]
    if hypothesis_ref not in state["active_pre_analysis"]:
        raise ValueError("ELG requires active SH pre-analysis")
    hypothesis = state["registry"]["hypotheses"][hypothesis_ref]
    fallback = None
    if hypothesis["classification"] != "ELG":
        events = [event for event in reachable_events(trace, branch_id)
                  if event["kind"] == "type_graph_fallback"
                  and event["payload"]["hypothesis_ref"] == hypothesis_ref
                  and event["payload"]["to_graph"] == "ELG"]
        if len(events) != 1 or hypothesis["classification"] != "LRG/BGS":
            raise ValueError("ELG path requires an ELG entry or verified fallback")
        fallback = events[0]["payload"]
        for ref in (fallback["route_ref"], fallback["entry_route_ref"]):
            _checked_artifact(trace, ref)
    if any(vote["origin"] == "offline_fixture"
           for feature in state["registry"]["features"].values()
           for vote in feature["votes"]):
        raise ValueError("fixture FA ballots cannot enter the ELG graph")
    view = cleaned_line_view(trace, branch_id, hypothesis_ref)
    by_id = {row["line_id"]: row for row in view["lines"]}
    vote_refs = sorted({ref for row in view["lines"]
                        for ref in row["fa_vote_artifact_refs"]})
    catalog_ref = f"sh/{hypothesis_ref}/catalog"
    catalog = json.loads(_checked_artifact(trace, catalog_ref).read_text(encoding="utf-8"))
    source = f"sh/{hypothesis_ref}/node"
    if source != hypothesis["node_artifact"]:
        raise ValueError("ELG pre-analysis identity differs")
    for ref in [source, *view["source_refs"], *vote_refs]:
        _checked_artifact(trace, ref)
    z = hypothesis["redshift"]
    dn = None
    nev = _line(by_id.get(NEV), NEV)
    ca = [_line(by_id.get(line_id), line_id) for line_id in (CA_K, CA_H)]
    oiii = [_line(by_id.get(line_id), line_id) for line_id in OIII]
    oii = _line(by_id.get(OII), OII)
    nodes = []
    entry = _save(trace, branch_id, hypothesis_ref, "elg.entry", {
        "preliminary_classification": hypothesis["classification"], "fixed_redshift": z,
        "pre_analysis_ref": source,
        "entry_mode": "fallback" if fallback else "initial", "current_graph": "ELG",
        "fallback_route_ref": fallback["route_ref"] if fallback else None,
    }, [source, *([fallback["route_ref"], fallback["entry_route_ref"]]
                 if fallback else [])], output_root)
    nodes.append(entry)
    evidence = _save(trace, branch_id, hypothesis_ref, "elg.evidence_view", {
        "cleaned_line_view": view,
    }, [entry["artifact_ref"], *view["source_refs"], *vote_refs], output_root)
    nodes.append(evidence)
    nev_node = _save(trace, branch_id, hypothesis_ref, "elg.nev_guard", {
        "line": nev, "adopted": nev["cleaned_pairing"] == "adopted",
        "next_node": "qso.nev_pairing_gate" if nev["cleaned_pairing"] == "adopted"
                     else "elg.qso_type1_guard",
    }, [evidence["artifact_ref"], *nev["fa_vote_artifact_refs"]], output_root)
    nodes.append(nev_node)
    type1 = type1_transfer_evidence(view["lines"])
    old_output = None
    emission_output = None
    last_ref = nev_node["artifact_ref"]
    if nev["cleaned_pairing"] != "adopted":
        guard = _save(trace, branch_id, hypothesis_ref, "elg.qso_type1_guard", type1,
                      [last_ref, *sorted({ref for row in type1["observed_lines"]
                                          for ref in row["fa_vote_artifact_refs"]})],
                      output_root)
        nodes.append(guard)
        last_ref = guard["artifact_ref"]
    if nev["cleaned_pairing"] != "adopted" and not type1["trigger_pairs"]:
        dn = _dn4000(trace, hypothesis_ref, z, catalog)
        adopted_ca = [row["line_id"] for row in ca
                      if row["cleaned_pairing"] == "adopted"]
        old_output = {
            "ca_lines": ca, "adopted_ca_line_ids": adopted_ca,
            "dn4000": dn,
            "old_population_hint": bool(adopted_ca or dn["reference_strength"] == "strong"),
            "classification_gate": False,
        }
        old_node = _save(trace, branch_id, hypothesis_ref,
                         "elg.old_population_guard", old_output,
                         [last_ref, catalog_ref, "spectrum_npz"], output_root)
        nodes.append(old_node)
        last_ref = old_node["artifact_ref"]
        both_adopted = all(row["cleaned_pairing"] == "adopted" for row in oiii)
        same_measurement = (both_adopted and
                            oiii[0]["measurement_id"] == oiii[1]["measurement_id"])
        a = "yes" if both_adopted and not same_measurement else "unknown"
        b = "yes" if oii["cleaned_pairing"] == "adopted" else "unknown"
        emission_output = {
            "A": a, "B": b, "oiii_components": oiii, "oii": oii,
            "oiii_component_id_conflict": same_measurement,
            "unknown_is_negative": False,
        }
        emission_node = _save(trace, branch_id, hypothesis_ref,
                              "elg.emission_evidence", emission_output,
                              [last_ref], output_root)
        nodes.append(emission_node)
        last_ref = emission_node["artifact_ref"]
    if nev["cleaned_pairing"] == "adopted":
        status, candidate, reason, target = "transfer", None, "adopted_nev", "QSO"
        unresolved = []
    elif type1["trigger_pairs"]:
        status, candidate, reason, target = "transfer", None, "adopted_qso_diagnostic", "QSO"
        unresolved = []
    elif emission_output["A"] == "yes" or emission_output["B"] == "yes":
        status, candidate, reason, target = "survive", "ELG", "emission_support", None
        unresolved = (["old_population_hint_not_a_hard_gate"]
                      if old_output["old_population_hint"] else [])
    else:
        status, candidate, reason, target = "unresolved", None, "emission_evidence_unknown", None
        unresolved = ["emission_absence_not_established"]
        if old_output["old_population_hint"]:
            unresolved.append("old_population_hint_not_a_hard_gate")
    route = {"path_status": status, "candidate_type": candidate,
             "reason_code": reason, "to_graph": target,
             "from_graph": "ELG", "fixed_redshift": z,
             "preliminary_classification": hypothesis["classification"],
             "unresolved_reasons": unresolved,
             "rule_id": "project:elg-canvas-v1", "rule_version": GRAPH_VERSION,
             "evidence_refs": [last_ref],
             "qso_transfer_mode": ("type2" if reason == "adopted_nev" else "type1"
                                   if target else None),
             "qso_trigger_pairs": type1["trigger_pairs"] if reason == "adopted_qso_diagnostic" else [],
             "retained_diagnostic_pairs": type1["retained_diagnostic_pairs"],
             "galaxy_retention_by_mgii_pair": type1["galaxy_retention_by_mgii_pair"],
             "nev_measurement_id": nev["measurement_id"] if reason == "adopted_nev" else None}
    route_node = _save(trace, branch_id, hypothesis_ref, "elg.route_result",
                       route, [last_ref], output_root)
    nodes.append(route_node)
    report_inputs = {"redshift": z, "route": route, "nev": nev,
                     "old": old_output or {"adopted_ca_line_ids": [],
                                           "dn4000": {"value": None,
                                                      "reference_strength": "not_evaluated"}},
                     "emission": emission_output or {"A": "not_evaluated", "B": "not_evaluated"},
                     "route_ref": route_node["artifact_ref"]}
    report_node = None if defer_report else _finish_elg_report(
        trace, branch_id, hypothesis_ref, output_root, report_inputs)
    if report_node:
        nodes.append(report_node)
    handoff = None
    qso = None
    if status == "transfer":
        handoff = record_type_handoff(trace, branch_id,
                                      hypothesis_ref=hypothesis_ref,
                                      from_graph="ELG", to_graph="QSO",
                                      route_ref=route_node["artifact_ref"],
                                      evidence_refs=[last_ref])
        from .qso_entry import run_qso_entry
        qso = run_qso_entry(trace, branch_id=branch_id,
                            hypothesis_ref=hypothesis_ref, output_root=output_root,
                            handoff_ref=route_node["artifact_ref"])
    return {"path_status": status, "candidate_type": candidate,
            "nodes": nodes, "handoff_event": handoff, "qso_entry": qso,
            "report_ref": report_node["report_ref"] if report_node else None,
            **({"deferred_report_inputs": report_inputs} if defer_report else {})}


def _finish_elg_report(trace: dict, branch_id: str, hypothesis_ref: str,
                       output_root: str | Path, inputs: dict) -> dict:
    alignment = active_alignment(trace, branch_id, hypothesis_ref, "ELG")
    report = _report(hypothesis_ref, inputs["redshift"], inputs["route"],
                     inputs["nev"], inputs["old"], inputs["emission"],
                     alignment[1]["output"] if alignment else None,
                     alignment[0] if alignment else None)
    return _save(trace, branch_id, hypothesis_ref, "elg.analysis_report", {
        "path_status": inputs["route"]["path_status"],
        "candidate_type": inputs["route"]["candidate_type"],
        "route_ref": inputs["route_ref"],
        "alignment_ref": alignment[0] if alignment else None,
    }, [inputs["route_ref"],
        *([alignment[0]] if alignment else [])], output_root, report=report)


async def run_elg_path_through_report(trace: dict, *, branch_id: str,
                                      hypothesis_ref: str,
                                      output_root: str | Path, llm) -> dict:
    """Complete ELG and any transferred QSO path through Q11."""
    result = run_elg_path(trace, branch_id=branch_id,
                          hypothesis_ref=hypothesis_ref, output_root=output_root,
                          defer_report=True)
    await run_line_alignment(trace, branch_id=branch_id,
                             hypothesis_ref=hypothesis_ref, graph="ELG",
                             output_root=output_root, llm=llm)
    report_node = _finish_elg_report(trace, branch_id, hypothesis_ref,
                                     output_root, result.pop("deferred_report_inputs"))
    result["nodes"].append(report_node)
    result["report_ref"] = report_node["report_ref"]
    if result["qso_entry"] is not None:
        if result["qso_entry"]["path_status"] == "in_progress":
            from .qso_type1_path import run_qso_type1_path
            result["qso_type1"] = await run_qso_type1_path(
                trace, branch_id=branch_id, hypothesis_ref=hypothesis_ref,
                output_root=output_root, llm=llm)
        elif result["qso_entry"]["path_status"] != "survive":
            raise ValueError("ELG QSO handoff did not reach a supported exit")
        from .qso_report import run_qso_report
        await run_line_alignment(trace, branch_id=branch_id,
                                 hypothesis_ref=hypothesis_ref, graph="QSO",
                                 output_root=output_root, llm=llm)
        result["qso_report"] = await run_qso_report(
            trace, branch_id=branch_id, hypothesis_ref=hypothesis_ref,
            output_root=output_root, llm=llm)
    else:
        result["qso_type1"] = None
        result["qso_report"] = None
    return result
