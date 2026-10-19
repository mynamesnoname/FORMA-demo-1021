"""Branch-local LRG/BGS graph: frozen Dn4000 and Ca H/K evidence."""

from __future__ import annotations

import asyncio
import json
import math
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from FORMA.core.config.analysis_method import load_analysis_method
from FORMA.core.constants import SIGMA_TO_FWHM, SPEED_OF_LIGHT_KMS
from FORMA.core.line_status import MASKED

from .cleaned_line_view import cleaned_line_view
from .elg_path import _dn4000, _line
from .execution_artifacts import allocate_execution
from .fa_doublet import _component_payload, build_doublet_window
from .feature_registry import _digest
from .line_alignment import render_alignment_markdown, run_line_alignment
from .qso_transfer_guard import type1_transfer_evidence
from .reasoning_trace import (record_analysis, record_type_handoff,
                              register_artifact, register_execution)
from .sh_pre_analysis import PROMPT_DIR, _render
from .session_markdown import MarkdownSessionRecorder
from .vote_runtime import collect_advisory_votes, summarize_usage, vote_tally


GRAPH_VERSION = "forma-lrg-bgs-type-graph-v2"
NEV = "line:nev-3426"
CA_LINES = ("line:cak-3934-abs", "line:cah-3969-abs")
ROUTE_RULE = "project:lrg-bgs-dn4000-or-cahk-v2"

SAMPLE_SYSTEM = """Select a local Ca absorption trough and one usable outer
reference sample on each side, using only the supplied frozen pixel IDs. Return
one JSON object with left_sample_id, trough_sample_id, right_sample_id and a
nonempty reason. If no defensible trough and two shoulders exist, return
{"no_valid_trough": true, "reason": "..."}. Do not classify the source, infer
another line, or invent measurements. The outer-reference sigma value is a
later code conversion convention, not a measured wing level. This session has
no prior context.
"""


def _absorption_sample(answer: dict, window: dict, center: float,
                       half_width: float, edge_sigma: float | None = None) -> dict | None:
    if not isinstance(answer.get("reason"), str) or not answer["reason"].strip():
        raise ValueError("Ca sample needs a reason")
    if answer.get("no_valid_trough") is True and set(answer) == {"no_valid_trough", "reason"}:
        return None
    keys = {"left_sample_id", "trough_sample_id", "right_sample_id", "reason"}
    if set(answer) != keys or any(type(answer[key]) is not int for key in keys - {"reason"}):
        raise ValueError("Ca sample needs three frozen sample IDs")
    samples = {item["sample_id"]: item for item in window["samples"]}
    left, trough, right = (samples.get(answer[key]) for key in
                           ("left_sample_id", "trough_sample_id", "right_sample_id"))
    if any(item is None or not item["valid"] for item in (left, trough, right)):
        raise ValueError("Ca sample selects an invalid or masked pixel")
    if not (left["wavelength_angstrom"] < trough["wavelength_angstrom"]
            < right["wavelength_angstrom"]
            and abs(trough["wavelength_angstrom"] - center) <= half_width
            and left["wavelength_angstrom"] >= center - half_width
            and right["wavelength_angstrom"] <= center + half_width):
        raise ValueError("Ca trough or shoulders are outside the component core")
    baseline = left["flux"] + (right["flux"] - left["flux"]) * (
        (trough["wavelength_angstrom"] - left["wavelength_angstrom"])
        / (right["wavelength_angstrom"] - left["wavelength_angstrom"]))
    depth = baseline - trough["flux"]
    if not math.isfinite(depth) or depth <= 0 or trough["flux"] >= min(left["flux"], right["flux"]):
        raise ValueError("Ca selection does not show a local absorption trough")
    if edge_sigma is None:
        edge_sigma = load_analysis_method().audit.doublet_review.cahk_outer_reference_sigma
    if not math.isfinite(edge_sigma) or edge_sigma <= 0:
        raise ValueError("Ca outer-reference sigma convention must be positive")
    span = right["wavelength_angstrom"] - left["wavelength_angstrom"]
    fwhm = span / (2 * edge_sigma) * SIGMA_TO_FWHM
    return {"left_sample_id": left["sample_id"],
            "trough_sample_id": trough["sample_id"],
            "right_sample_id": right["sample_id"],
            "trough_wavelength_angstrom": trough["wavelength_angstrom"],
            "baseline_at_trough": baseline, "absorption_depth_proxy": depth,
            "outer_reference_span_angstrom": span,
            "outer_reference_sigma_assumption": edge_sigma,
            "fwhm_proxy_angstrom": fwhm,
            "fwhm_proxy_km_s": fwhm / trough["wavelength_angstrom"] * SPEED_OF_LIGHT_KMS,
            "measurement_source": "llm_selected_absorption_envelope_proxy",
            "reason": answer["reason"]}


async def _sample_missing_cahk(trace: dict, *, branch_id: str, hypothesis_ref: str,
                               output_root: str | Path, llm: Any, window: dict,
                               components: list[dict], quorum: int, max_attempts: int,
                               concurrency: int) -> tuple[dict, list[str]]:
    """Independent pixel-ID selections; preserve all attempts and one complete pick."""
    if llm is None:
        return {"status": "pending", "candidates": [], "reason": "model_unavailable"}, []
    missing = [item for item in components if item["cleaned_pairing"] != "adopted"]
    semaphore = asyncio.Semaphore(concurrency)
    prompt_samples = [{key: sample[key] for key in
                       ("sample_id", "wavelength_angstrom", "flux", "valid")}
                      for sample in window["samples"]]

    async def one(component: dict, seat: int) -> list[dict]:
        attempts = []
        center = component["expected_obs_angstrom"]
        method = load_analysis_method().audit.doublet_review
        half = method.component_check_half_angstrom
        edge_sigma = method.cahk_outer_reference_sigma
        user = json.dumps({"predicted_center_angstrom": center,
                           "component_core_angstrom": [center - half, center + half],
                           "outer_reference_sigma_assumption": edge_sigma,
                           "samples": [sample for sample in prompt_samples
                                       if center - half <= sample["wavelength_angstrom"]
                                       <= center + half]}, ensure_ascii=False, allow_nan=False)
        for attempt in range(max_attempts):
            allocation = allocate_execution(output_root, run_id=trace["run_id"],
                                            branch_id=branch_id,
                                            node_key=_key(hypothesis_ref,
                                                          f"lrg_bgs.cahk_sample/{component['line_id']}/{seat}"))
            recorder = MarkdownSessionRecorder(
                allocation.path("session.md"), run_id=trace["run_id"],
                hypothesis_ref=hypothesis_ref, stage="LRG/BGS Ca H/K isolated selection",
                system_prompt=SAMPLE_SYSTEM, input_messages=[HumanMessage(content=user)],
                tools=[], session_kind="LRG/BGS", subject_label="Ca absorption core")
            selection = None
            error = None
            try:
                async with semaphore:
                    response = await llm.ainvoke([SystemMessage(content=SAMPLE_SYSTEM),
                                                  HumanMessage(content=user)])
                if not isinstance(response, AIMessage) or not isinstance(response.content, str):
                    raise ValueError("Ca sample model returned no JSON text")
                recorder.record_event({"model": {"messages": [response]}})
                raw = response.content.strip()
                if raw.startswith("```json") and raw.endswith("```"):
                    raw = raw[7:-3].strip()
                answer = json.loads(raw)
                if not isinstance(answer, dict):
                    raise ValueError("Ca sample response is not an object")
                selection = _absorption_sample(answer, window, center, half, edge_sigma)
                recorder.finish(status="complete")
            except Exception as exc:
                error = type(exc).__name__
                recorder.finish(status="failed", error_type=error)
            outcome = {"line_id": component["line_id"], "seat": seat,
                       "attempt": attempt, "selection": selection,
                       "status": "complete" if error is None else "failed",
                       "error_type": error, "model_usage": recorder.model_calls,
                       "node_execution_id": allocation.node_execution_id}
            (allocation.path("selection.json") if error is None else
             allocation.path("failure.json")).write_text(
                 json.dumps(outcome, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                 encoding="utf-8")
            attempts.append({"allocation": allocation, "outcome": outcome})
            if error is None:
                break  # no_valid_trough is a valid, nonpositive selection
        return attempts

    groups = await asyncio.gather(*(one(component, seat) for component in missing
                                    for seat in range(quorum)))
    refs, calls, picks = [], [], {component["line_id"]: [] for component in missing}
    for group in groups:
        for entry in group:
            allocation, outcome = entry["allocation"], entry["outcome"]
            register_execution(trace, allocation)
            calls.extend(outcome["model_usage"])
            prefix = f"lrg_bgs_cahk_sample/{allocation.node_execution_id}"
            filenames = ("session.md", "selection.json") if outcome["status"] == "complete" else (
                "session.md", "failure.json")
            for filename in filenames:
                ref = f"{prefix}/{filename}"
                register_artifact(trace, ref, allocation.path(filename),
                                  "lrg_bgs_cahk_sample", node_execution_id=allocation.node_execution_id)
                refs.append(ref)
            if outcome["status"] == "complete" and outcome["selection"] is not None:
                picks[outcome["line_id"]].append({**outcome["selection"],
                    "seat": outcome["seat"], "artifact_ref": f"{prefix}/selection.json"})
    candidates = []
    for component in missing:
        selected = picks[component["line_id"]]
        if len(selected) != quorum:
            return {"status": "pending", "candidates": candidates,
                    "reason": "incomplete_or_nonpositive_component_samples",
                    "selections": picks, "model_usage": summarize_usage(calls)}, refs
        representative = sorted(selected, key=lambda item: (item["fwhm_proxy_angstrom"],
                                                           item["seat"]))[quorum // 2]
        candidates.append({"candidate_id": f"candidate:cahk/{representative['artifact_ref'].split('/')[1]}",
                           "line_id": component["line_id"],
                           "representative": representative,
                           "selections": selected,
                           "source": "branch_local_llm_selected_absorption"})
    return {"status": "complete", "candidates": candidates,
            "reason": None, "selections": picks,
            "model_usage": summarize_usage(calls)}, refs


def _key(hypothesis_ref: str, node_type: str) -> str:
    return f"sh2.lrg_bgs/{quote(hypothesis_ref, safe='')}/{node_type}"


def _checked(trace: dict, ref: str) -> Path:
    item = trace["artifacts"].get(ref)
    if item is None:
        raise ValueError(f"unregistered LRG/BGS source: {ref}")
    path = Path(item["path"]).resolve(strict=True)
    if _digest(path) != item["sha256"]:
        raise ValueError(f"changed LRG/BGS source: {ref}")
    return path


def _save(trace: dict, branch_id: str, hypothesis_ref: str, node_type: str,
          output: dict, source_refs: list[str], output_root: str | Path,
          *, extra: dict[str, tuple[str, str]] | None = None) -> dict:
    key = _key(hypothesis_ref, node_type)
    if key in trace["branches"][branch_id]["state"]["analysis_results"]:
        raise ValueError("LRG/BGS node already active; fork before revisiting")
    for ref in source_refs:
        _checked(trace, ref)
    allocation = allocate_execution(output_root, run_id=trace["run_id"],
                                    branch_id=branch_id, node_key=key)
    node = {
        "schema_version": "forma-lrg-bgs-node-v1", "graph_version": GRAPH_VERSION,
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
    node_ref = f"sh2/{allocation.node_execution_id}/node"
    register_artifact(trace, node_ref, allocation.path("node.json"), "lrg_bgs_node",
                      node_execution_id=allocation.node_execution_id)
    extras = {}
    for name, (content, extension) in (extra or {}).items():
        if extension not in {"json", "md"}:
            raise ValueError("unsupported LRG/BGS artifact extension")
        path = allocation.path(f"{name}.{extension}")
        path.write_text(content, encoding="utf-8")
        ref = f"sh2/{allocation.node_execution_id}/{name}"
        register_artifact(trace, ref, path, f"lrg_bgs_{name}",
                          node_execution_id=allocation.node_execution_id)
        extras[name] = ref
    record_analysis(trace, branch_id, kind="analysis_result", analysis_ref=key,
                    artifact_refs=[node_ref, *extras.values(), *source_refs],
                    node_execution_id=allocation.node_execution_id)
    return {"node": node, "artifact_ref": node_ref, "extra_refs": extras}


def _cahk_inventory(rows: dict[str, dict], catalog: dict, z: float,
                    advisory: dict | None) -> dict:
    components = []
    measurements = {item["id"]: item for item in catalog["measurements"]}
    for line_id in CA_LINES:
        payload = _component_payload(line_id, rows.get(line_id), measurements, z)
        if rows.get(line_id) is not None:
            payload["predicted_obs_angstrom"] = rows[line_id]["predicted_obs_angstrom"]
        components.append(payload)
    adopted = [item for item in components if item["cleaned_pairing"] == "adopted"]
    for item in adopted:
        center = item["measured_center_angstrom"]
        if center is None or any(float(low) <= center <= float(high)
                                 for low, high in catalog.get("masked_regions", [])):
            raise ValueError("adopted Ca component has no usable center or falls in a frozen mask")
    distinct = {item["measurement_id"] for item in adopted}
    if len(distinct) != len(adopted):
        raise ValueError("one measurement cannot establish both Ca H/K components")
    uncertain = any(item["sh_status"] == MASKED or item["cleaned_pairing"] in {
        "pending_review", "unreviewable_data", "outside_sh_catalog"}
        for item in components)
    return {
        "components": components, "adopted_count": len(adopted),
        "adopted_line_ids": [item["line_id"] for item in adopted],
        "inventory_status": "unknown" if uncertain else "assessed",
        "unknown_is_negative": False, "doublet_advisory": advisory,
    }


def _report(hypothesis_ref: str, z: float, route: dict, nev: dict,
            dn: dict | None, inventory: dict | None, review: dict | None,
            alignment: dict | None = None, alignment_ref: str | None = None) -> str:
    lines = ["# LRG/BGS hypothesis graph report", "",
             f"- Hypothesis: `{hypothesis_ref}`", f"- Tested redshift: `{z!r}`",
             f"- Graph path: `{route['path_status']}`",
             f"- Candidate type: `{route['candidate_type'] or 'unresolved'}`",
             f"- Route rule: `{route['rule_id']}`", "",
             "## Recorded evidence", "",
             f"- [Ne V] pairing: `{nev['cleaned_pairing']}`; measurement: "
             f"`{nev['measurement_id'] or 'none'}`",
             f"- Type 1 transfer pairs: `{route.get('qso_trigger_pairs', [])}`",
             f"- Retained diagnostic pairs: `{route.get('retained_diagnostic_pairs', [])}`",
             f"- Galaxy retained by Mg II emission/absorption pair: "
             f"`{route.get('galaxy_retention_by_mgii_pair', False)}`",
             f"- Dn4000: `{dn['value'] if dn else None}`; reference strength: "
             f"`{dn['reference_strength'] if dn else 'not_evaluated'}`",
             f"- Adopted Ca H/K components: "
             f"`{inventory['adopted_line_ids'] if inventory else []}`",
             f"- Ca H/K inventory status: "
             f"`{inventory['inventory_status'] if inventory else 'not_evaluated'}`",
             f"- Targeted Ca H/K advice: "
             f"`{review['status'] if review else 'not_evaluated'}`", "",
             f"- Targeted Ca H/K sampled candidates: "
             f"`{[item['candidate_id'] for item in review.get('sampled_observation', {}).get('candidates', [])] if review else []}`",
             *(f"- `{item['line_id']}` sampled trough: "
               f"`{item['representative']['trough_wavelength_angstrom']}` Å; "
               f"depth proxy `{item['representative']['absorption_depth_proxy']}`; "
               f"FWHM proxy `{item['representative']['fwhm_proxy_angstrom']}` Å / "
               f"`{item['representative']['fwhm_proxy_km_s']}` km/s "
               f"(outer references assumed ±`{item['representative']['outer_reference_sigma_assumption']}`σ); "
               f"candidate `{item['candidate_id']}`"
               for item in (review.get("sampled_observation", {}).get("candidates", [])
                            if review else [])),
             "",
             "## Route", "",
             f"- Reason: `{route['reason_code']}`",
             f"- Transfer target: `{route['to_graph'] or 'none'}`", "",
             "## Open items", ""]
    lines.extend(f"- `{reason}`" for reason in route["unresolved_reasons"])
    if not route["unresolved_reasons"]:
        lines.append("- None recorded.")
    if alignment and alignment["collisions"]:
        lines.extend(["", render_alignment_markdown(alignment,
                                                     node_ref=alignment_ref).rstrip()])
    return "\n".join(lines) + "\n"


async def run_lrg_bgs_path(trace: dict, *, branch_id: str, hypothesis_ref: str,
                           output_root: str | Path, llm: Any | None = None,
                           agent_factory: Callable[..., Any] = create_agent,
                           concurrency: int = 3, recursion_limit: int = 30,
                           align_before_report: bool = False) -> dict:
    """Execute G0–G7 with Dn4000-or-Ca entry and source-bound Ca recovery."""
    if concurrency < 1 or recursion_limit < 1:
        raise ValueError("concurrency and recursion limit must be positive")
    state = trace["branches"][branch_id]["state"]
    if hypothesis_ref not in state["active_pre_analysis"]:
        raise ValueError("LRG/BGS requires active SH pre-analysis")
    hypothesis = state["registry"]["hypotheses"][hypothesis_ref]
    if hypothesis["classification"] != "LRG/BGS":
        raise ValueError("LRG/BGS requires its preliminary classification")
    if any(vote["origin"] == "offline_fixture"
           for feature in state["registry"]["features"].values()
           for vote in feature["votes"]):
        raise ValueError("fixture FA ballots cannot enter the LRG/BGS graph")
    source = f"sh/{hypothesis_ref}/node"
    if source != hypothesis["node_artifact"]:
        raise ValueError("LRG/BGS pre-analysis identity differs")
    view = cleaned_line_view(trace, branch_id, hypothesis_ref)
    rows = {row["line_id"]: row for row in view["lines"]}
    vote_refs = sorted({ref for row in view["lines"]
                        for ref in row["fa_vote_artifact_refs"]})
    catalog_ref = f"sh/{hypothesis_ref}/catalog"
    catalog = json.loads(_checked(trace, catalog_ref).read_text(encoding="utf-8"))
    spectrum_ref = "spectrum_npz"
    if (_checked(trace, spectrum_ref) != Path(catalog["spectrum_npz_path"]).resolve(strict=True)
            or trace["artifacts"][spectrum_ref]["sha256"] != catalog["spectrum_npz_sha256"]):
        raise ValueError("LRG/BGS spectrum differs from frozen SH catalog")
    for ref in [source, *view["source_refs"], *vote_refs]:
        _checked(trace, ref)
    z = hypothesis["redshift"]
    preliminary_inventory = _cahk_inventory(rows, catalog, z, None)
    nodes = []
    entry = _save(trace, branch_id, hypothesis_ref, "lrg_bgs.entry", {
        "preliminary_classification": "LRG/BGS", "fixed_redshift": z,
        "pre_analysis_ref": source, "entry_mode": "initial", "current_graph": "LRG/BGS",
    }, [source], output_root)
    nodes.append(entry)
    evidence = _save(trace, branch_id, hypothesis_ref, "lrg_bgs.evidence_view", {
        "cleaned_line_view": view,
    }, [entry["artifact_ref"], *view["source_refs"], *vote_refs], output_root)
    nodes.append(evidence)
    nev = _line(rows.get(NEV), NEV)
    nev_node = _save(trace, branch_id, hypothesis_ref, "lrg_bgs.nev_guard", {
        "line": nev, "adopted": nev["cleaned_pairing"] == "adopted",
        "next_node": ("qso.nev_pairing_gate" if nev["cleaned_pairing"] == "adopted"
                      else "lrg_bgs.qso_type1_guard"),
    }, [evidence["artifact_ref"], *nev["fa_vote_artifact_refs"]], output_root)
    nodes.append(nev_node)
    last_ref = nev_node["artifact_ref"]
    type1 = type1_transfer_evidence(view["lines"])
    if nev["cleaned_pairing"] != "adopted":
        guard = _save(trace, branch_id, hypothesis_ref, "lrg_bgs.qso_type1_guard", type1,
                      [last_ref, *sorted({ref for row in type1["observed_lines"]
                                          for ref in row["fa_vote_artifact_refs"]})],
                      output_root)
        nodes.append(guard)
        last_ref = guard["artifact_ref"]
    dn = inventory = review = None
    if nev["cleaned_pairing"] != "adopted" and not type1["trigger_pairs"]:
        dn = _dn4000(trace, hypothesis_ref, z, catalog)
        dn_node = _save(trace, branch_id, hypothesis_ref,
                        "lrg_bgs.dn4000_assessment", dn,
                        [last_ref, catalog_ref, spectrum_ref], output_root)
        nodes.append(dn_node)
        last_ref = dn_node["artifact_ref"]
        if dn["reference_strength"] == "strong" or preliminary_inventory["adopted_count"] >= 1:
            # FA doublet advice is disclosed to HS comparison only. This type
            # graph keeps its own targeted Ca H/K evidence and gate.
            inventory = _cahk_inventory(rows, catalog, z, None)
            inventory_node = _save(trace, branch_id, hypothesis_ref,
                                   "lrg_bgs.cahk_inventory", inventory,
                                   [last_ref], output_root)
            nodes.append(inventory_node)
            last_ref = inventory_node["artifact_ref"]
            if inventory["adopted_count"] < 2:
                method = load_analysis_method().audit.doublet_review
                window = build_doublet_window(
                    _checked(trace, spectrum_ref), components=inventory["components"],
                    masked_regions=catalog.get("masked_regions", []), method=method)
                bounds = window["coverage"]["spectrum_bounds_angstrom"]
                full_cores = all(
                    bounds[0] <= item["predicted_obs_angstrom"] - method.component_check_half_angstrom
                    and item["predicted_obs_angstrom"] + method.component_check_half_angstrom <= bounds[1]
                    for item in inventory["components"])
                if not full_cores:
                    window["coverage"]["assessable"] = False
                    window["coverage"]["unreviewable_reason"] = "component_core_outside_spectrum"
                assessable = window["coverage"]["assessable"]
                batch = {"ballots": [], "attempt_refs": [],
                         "model_usage": summarize_usage([]), "prompt_identity": None}
                if assessable and llm is not None:
                    system = (PROMPT_DIR / "lrg_bgs_cahk_targeted_system.md").read_text(
                        encoding="utf-8")
                    user = _render("lrg_bgs_cahk_targeted_user.md", {
                        "REDSHIFT": repr(z),
                        "REVIEW_ROLE": ("Additional evidence; Dn4000 already supports this path."
                                        if dn["reference_strength"] == "strong" else
                                        "A completed doublet vote and separately verified pixel-ID "
                                        "samples are both required for a Ca-supported route."),
                        "COMPONENTS": json.dumps(inventory["components"], ensure_ascii=False, allow_nan=False),
                        "COVERAGE": json.dumps(window["coverage"], ensure_ascii=False, allow_nan=False),
                        "SAMPLES": window["samples_markdown"]}, PROMPT_DIR)
                    batch = await collect_advisory_votes(
                        trace=trace, branch_id=branch_id,
                        node_key=_key(hypothesis_ref, "lrg_bgs.cahk_targeted_review"),
                        output_root=output_root, llm=llm, system=system, user=user,
                        tool_name="submit_cahk_vote", stage="LRG/BGS Ca H/K review",
                        vote_quorum=method.vote_quorum,
                        max_attempts=method.max_attempts_per_vote_seat,
                        concurrency=concurrency, recursion_limit=recursion_limit,
                        agent_factory=agent_factory, artifact_namespace="lrg_bgs_cahk_vote")
                tally = vote_tally(batch["ballots"], method.vote_quorum, assessable)
                review = {"status": tally["status"], "source": "targeted_window",
                          "pair_supported": tally["positive"],
                          "vote_summary": tally["vote_summary"],
                          "consultative_only": dn["reference_strength"] == "strong",
                          "coverage": window["coverage"],
                          "model_usage": batch["model_usage"],
                          "ballots": batch["ballots"],
                          "prompt_identity": batch["prompt_identity"],
                          "unresolved_reasons": ([] if tally["status"] == "complete"
                                                 else ["cahk_review_" + tally["status"]])}
                attempt_refs = batch["attempt_refs"]
                review["sampled_observation"] = {"status": "not_required",
                                                  "candidates": []}
                if review["pair_supported"] is True and window["coverage"]["assessable"]:
                    sampled, sample_refs = await _sample_missing_cahk(
                        trace, branch_id=branch_id, hypothesis_ref=hypothesis_ref,
                        output_root=output_root, llm=llm, window=window,
                        components=inventory["components"], quorum=method.vote_quorum,
                        max_attempts=method.max_attempts_per_vote_seat,
                        concurrency=concurrency)
                    review["sampled_observation"] = sampled
                    attempt_refs.extend(sample_refs)
                review_node = _save(
                    trace, branch_id, hypothesis_ref, "lrg_bgs.cahk_targeted_review",
                    review, [last_ref, catalog_ref, spectrum_ref, *attempt_refs],
                    output_root,
                    extra={"window": (json.dumps(window["coverage"], ensure_ascii=False, indent=2), "json"),
                           "samples": (window["samples_markdown"], "md")})
                nodes.append(review_node)
                last_ref = review_node["artifact_ref"]
    if nev["cleaned_pairing"] == "adopted":
        status, candidate, reason, target = "transfer", None, "adopted_nev", "QSO"
        unresolved = []
    elif type1["trigger_pairs"]:
        status, candidate, reason, target = "transfer", None, "adopted_qso_diagnostic", "QSO"
        unresolved = []
    elif dn["reference_strength"] == "strong":
        status, candidate, reason, target = "survive", "LRG/BGS", "dn4000_strong", None
        unresolved = []
        if inventory["inventory_status"] == "unknown":
            unresolved.append("cahk_inventory_unknown")
        if review and review["status"] in {"pending", "unreviewable"}:
            unresolved.append("cahk_review_" + review["status"])
        if review and review.get("pair_supported") is True and review["sampled_observation"]["status"] != "complete":
            unresolved.append("cahk_sampling_" + review["sampled_observation"]["status"])
    elif inventory is not None and inventory["adopted_count"] == 2:
        status, candidate, reason, target = "survive", "LRG/BGS", "cahk_pair_adopted", None
        unresolved = [dn["unresolved_reason"]] if dn["reference_strength"] == "unknown" else []
    elif inventory is not None and inventory["adopted_count"] == 1:
        missing = next(item for item in inventory["components"]
                       if item["cleaned_pairing"] != "adopted")
        sample_status = review["sampled_observation"]["status"] if review else "pending"
        if (review and review["status"] == "complete"
                and review["pair_supported"] is True and sample_status == "complete"
                and missing["cleaned_pairing"] in {"no_pairing", "outside_sh_catalog"}
                and missing["sh_status"] != MASKED):
            status, candidate, reason, target = "survive", "LRG/BGS", "cahk_sampled_pair", None
            unresolved = [dn["unresolved_reason"]] if dn["reference_strength"] == "unknown" else []
        elif (review and review["status"] == "complete"
              and review["pair_supported"] is False
              and dn["reference_strength"] != "unknown"
              and inventory["inventory_status"] == "assessed"):
            status, candidate, reason, target = "dead", None, "cahk_review_rejected", None
            unresolved = []
        else:
            status, candidate, reason, target = "unresolved", None, "cahk_pair_unresolved", None
            unresolved = ["cahk_review_" + (review["status"] if review else "not_run")]
            if review and review["pair_supported"] is True:
                unresolved.append("cahk_sampling_" + sample_status)
            if missing["cleaned_pairing"] in {"rejected_measurement", "pending_review",
                                               "unreviewable_data"}:
                unresolved.append("cahk_requires_fa_recheck")
            if missing["sh_status"] == MASKED:
                unresolved.append("cahk_masked_sh_requires_reconciliation")
            if dn["reference_strength"] == "unknown":
                unresolved.append(dn["unresolved_reason"])
    elif dn["reference_strength"] == "unknown" or preliminary_inventory["inventory_status"] == "unknown":
        status, candidate, reason, target = "unresolved", None, "dn4000_or_cahk_unknown", None
        unresolved = ([dn["unresolved_reason"]] if dn["reference_strength"] == "unknown" else [])
        if preliminary_inventory["inventory_status"] == "unknown":
            unresolved.append("cahk_inventory_unknown")
    else:
        status, candidate, reason, target = "dead", None, "dn4000_and_cahk_not_supported", None
        unresolved = []
    route = {"path_status": status, "candidate_type": candidate,
             "reason_code": reason, "from_graph": "LRG/BGS", "to_graph": target,
             "fixed_redshift": z, "preliminary_classification": "LRG/BGS",
             "rule_id": ROUTE_RULE, "rule_version": GRAPH_VERSION,
             "gate_inputs": {"dn4000_strength": dn["reference_strength"] if dn else None,
                             "adopted_cahk_count": (inventory or preliminary_inventory)["adopted_count"]
                             if dn else None,
                             "cahk_inventory_status": (inventory or preliminary_inventory)["inventory_status"]
                             if dn else None},
             "sampled_candidate_ids": [item["candidate_id"] for item in
                                       review.get("sampled_observation", {}).get("candidates", [])]
                                      if review else [],
             "qso_transfer_mode": ("type2" if reason == "adopted_nev" else "type1"
                                   if target else None),
             "qso_trigger_pairs": type1["trigger_pairs"] if reason == "adopted_qso_diagnostic" else [],
             "retained_diagnostic_pairs": type1["retained_diagnostic_pairs"],
             "galaxy_retention_by_mgii_pair": type1["galaxy_retention_by_mgii_pair"],
             "nev_measurement_id": nev["measurement_id"] if reason == "adopted_nev" else None,
             "unresolved_reasons": unresolved, "evidence_refs": [last_ref]}
    route_node = _save(trace, branch_id, hypothesis_ref,
                       "lrg_bgs.route_result", route, [last_ref], output_root)
    nodes.append(route_node)
    alignment = (await run_line_alignment(trace, branch_id=branch_id,
                                          hypothesis_ref=hypothesis_ref,
                                          graph="LRG/BGS", output_root=output_root,
                                          llm=llm, concurrency=concurrency)
                 if align_before_report else None)
    report = _report(hypothesis_ref, z, route, nev, dn, inventory, review,
                     alignment["node"]["output"] if alignment else None,
                     alignment["artifact_ref"] if alignment else None)
    report_node = _save(trace, branch_id, hypothesis_ref,
                        "lrg_bgs.analysis_report",
                        {"path_status": status, "candidate_type": candidate,
                         "route_ref": route_node["artifact_ref"],
                         "alignment_ref": alignment["artifact_ref"] if alignment else None},
                        [route_node["artifact_ref"],
                         *([alignment["artifact_ref"]] if alignment else [])], output_root,
                        extra={"report": (report, "md")})
    nodes.append(report_node)
    handoff = qso = None
    if status == "transfer":
        handoff = record_type_handoff(
            trace, branch_id, hypothesis_ref=hypothesis_ref,
            from_graph="LRG/BGS", to_graph="QSO",
            route_ref=route_node["artifact_ref"],
            evidence_refs=[last_ref])
        from .qso_entry import run_qso_entry
        qso = run_qso_entry(trace, branch_id=branch_id,
                            hypothesis_ref=hypothesis_ref, output_root=output_root,
                            handoff_ref=route_node["artifact_ref"])
    return {"path_status": status, "candidate_type": candidate,
            "nodes": nodes, "handoff_event": handoff, "qso_entry": qso,
            "report_ref": report_node["extra_refs"]["report"]}


async def run_lrg_bgs_path_through_report(trace: dict, *, branch_id: str,
                                          hypothesis_ref: str,
                                          output_root: str | Path, llm: Any,
                                          agent_factory: Callable[..., Any] = create_agent) -> dict:
    """Run G0–G7 and any transferred QSO path through Q11."""
    result = await run_lrg_bgs_path(
        trace, branch_id=branch_id, hypothesis_ref=hypothesis_ref,
        output_root=output_root, llm=llm, agent_factory=agent_factory,
        align_before_report=True)
    if result["qso_entry"] is not None:
        if result["qso_entry"]["path_status"] == "in_progress":
            from .qso_type1_path import run_qso_type1_path
            result["qso_type1"] = await run_qso_type1_path(
                trace, branch_id=branch_id, hypothesis_ref=hypothesis_ref,
                output_root=output_root, llm=llm)
        elif result["qso_entry"]["path_status"] != "survive":
            raise ValueError("LRG/BGS QSO handoff did not reach a supported exit")
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
