"""Hypothesis-local, report-bound review of shared SH feature assignments.

The original SH and FA evidence is immutable. A vote describes pixels in a
local window; only this module assigns the selected slots to line IDs.
"""

from __future__ import annotations

import asyncio
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import quote

import numpy as np
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from FORMA.core.config.analysis_method import load_analysis_method
from FORMA.core.constants import SIGMA_TO_FWHM, SPEED_OF_LIGHT_KMS
from FORMA.core.line_status import is_kept_evidence

from .cleaned_line_view import cleaned_line_view
from .execution_artifacts import allocate_execution
from .feature_registry import _digest
from .reasoning_trace import record_analysis, register_artifact, register_execution
from .session_markdown import MarkdownSessionRecorder
from .vote_runtime import summarize_usage


SCHEMA = "forma-sh-line-alignment-v1"
QSO_DIAGNOSTICS = frozenset({
    "line:lya-1216", "line:civ-1549", "line:ciii-1909",
    "line:mgii-2800", "line:nev-3426",
})
ELG_DIAGNOSTICS = frozenset({"line:oii-3727", "line:oiii-4960", "line:oiii-5008"})
CA_LINES = frozenset({"line:cak-3934-abs", "line:cah-3969-abs"})
OIII_TRIAD = frozenset({"line:hbet-4862", "line:oiii-4960", "line:oiii-5008"})

SYSTEM = """Inspect only the supplied spectrum samples. Each sample array uses
the declared sample_columns order: sample ID, wavelength, flux, valid. The anonymous slots A/B/C
are predicted positions, not verified line identities. For each slot choose one
emission peak or absorption valley and one usable outer shoulder on each side,
or return null when you cannot defend a distinct signal. Do not reuse an
extremum for two slots, invent sample IDs, or classify the source. Return only
JSON: {"slots":{"A":null or {"left_sample_id":int,"extremum_sample_id":int,
"right_sample_id":int}, ...},"reason":"short explanation"}. Include every
supplied slot exactly once. This is a fresh independent session.
"""


def alignment_key(hypothesis_ref: str, graph: str) -> str:
    if graph not in {"QSO", "ELG", "LRG/BGS"}:
        raise ValueError("unsupported alignment graph")
    return f"sh2.alignment/{quote(hypothesis_ref, safe='')}/{quote(graph, safe='')}"


def _source(trace: dict, ref: str) -> Path:
    item = trace["artifacts"].get(ref)
    if item is None:
        raise ValueError(f"missing alignment source: {ref}")
    path = Path(item["path"]).resolve(strict=True)
    if _digest(path) != item["sha256"]:
        raise ValueError(f"changed alignment source: {ref}")
    return path


def alignment_jobs(view: dict, graph: str) -> list[dict]:
    """Find many-lines-to-one-measurement collisions; never infer one-to-many."""
    if graph not in {"QSO", "ELG", "LRG/BGS"}:
        raise ValueError("unsupported alignment graph")
    by_measurement: dict[str, list[dict]] = defaultdict(list)
    for row in view["lines"]:
        if (row["measurement_id"] is not None and is_kept_evidence(row["sh_status"])
                and row["fa_state"] != "signal_absent"):
            by_measurement[row["measurement_id"]].append(row)
    jobs = []
    eligible_rows = [row for row in view["lines"]
                     if row["measurement_id"] is not None
                     and is_kept_evidence(row["sh_status"])
                     and row["fa_state"] != "signal_absent"]
    processed_groups = set()
    for measurement_id, rows in sorted(by_measurement.items()):
        if len(rows) < 2:
            continue
        ids = {row["line_id"] for row in rows}
        if graph == "LRG/BGS" and ids.intersection(CA_LINES):
            target = CA_LINES
            group = "ca_k_h_region"
            group_key = group
        elif graph == "ELG" and ids.intersection(ELG_DIAGNOSTICS):
            triad = bool(ids.intersection(OIII_TRIAD) and "line:oii-3727" not in ids)
            target = OIII_TRIAD if triad else ids
            group = "hbeta_oiii" if triad else "elg_diagnostic"
            group_key = group if group == "hbeta_oiii" else measurement_id
        elif graph == "QSO" and ids.intersection(QSO_DIAGNOSTICS):
            target = ids - {"line:oiii-4960", "line:oiii-5008"}
            group = "qso_diagnostic"
            group_key = measurement_id
        else:
            target = frozenset()
            group = "unresolved_non_diagnostic"
            group_key = measurement_id
        if group_key in processed_groups:
            continue
        processed_groups.add(group_key)
        related = (eligible_rows if group_key in {"ca_k_h_region", "hbeta_oiii"}
                   else rows)
        shared_ids = ([mid for mid, claim_rows in by_measurement.items()
                       if len(claim_rows) >= 2 and any(row["line_id"] in target for row in claim_rows)]
                      if group_key in {"ca_k_h_region", "hbeta_oiii"} else [measurement_id])
        colliding_ids = {row["line_id"] for mid in shared_ids for row in by_measurement[mid]}
        slots = sorted((row for row in related if row["line_id"] in target),
                       key=lambda row: (row["predicted_obs_angstrom"], row["line_id"]))
        jobs.append({"measurement_id": measurement_id,
                     "shared_measurement_ids": sorted(shared_ids),
                     "tbd_line_ids": sorted(colliding_ids), "group": group,
                     "slots": [{"slot": chr(65 + index), "line_id": row["line_id"],
                                "predicted_obs_angstrom": row["predicted_obs_angstrom"],
                                "kind": row["line_kind"]}
                               for index, row in enumerate(slots)],
                     "eligible": bool(slots) and len(slots) >= 2
                     and len(slots) <= 3 and len({row["line_kind"] for row in slots}) == 1
                     and all(row["fa_state"] == "signal_present" for row in slots),
                     "ca_h_region_includes_unresolved_h_epsilon": group == "ca_k_h_region"})
    return jobs


def _window(wl: np.ndarray, flux: np.ndarray, ivar: np.ndarray, *,
            slots: list[dict], half: float, masked_regions: list) -> dict:
    positions = [item["predicted_obs_angstrom"] for item in slots]
    lo, hi = min(positions) - half, max(positions) + half
    indexes = np.flatnonzero((wl >= lo) & (wl <= hi))
    samples = []
    for index in indexes:
        x, y, weight = float(wl[index]), float(flux[index]), float(ivar[index])
        masked = any(float(a) <= x <= float(b) for a, b in masked_regions)
        valid = math.isfinite(y) and math.isfinite(weight) and weight > 0 and not masked
        samples.append({"sample_id": int(index), "wavelength_angstrom": x,
                        "flux": y if math.isfinite(y) else None, "valid": valid})
    return {"requested_window_angstrom": [lo, hi], "samples": samples,
            "usable_samples": sum(item["valid"] for item in samples),
            "coverage": "usable" if all(item["valid"] for item in samples) and samples
                        else "partial" if any(item["valid"] for item in samples)
                        else "unreviewable"}


def validate_selection(answer: dict, slots: list[dict], window: dict,
                       edge_sigma: float) -> dict:
    """Resolve selected pixel IDs and reject shared or misplaced extrema."""
    if (not isinstance(answer, dict) or set(answer) != {"slots", "reason"}
            or not isinstance(answer["reason"], str) or not answer["reason"].strip()
            or not isinstance(answer["slots"], dict)
            or set(answer["slots"]) != {slot["slot"] for slot in slots}):
        raise ValueError("alignment answer must cover every anonymous slot")
    samples = {row["sample_id"]: row for row in window["samples"]}
    used_extrema = set()
    output = {}
    for index, slot in enumerate(slots):
        label = slot["slot"]
        choice = answer["slots"][label]
        if choice is None:
            output[label] = None
            continue
        if (not isinstance(choice, dict)
                or set(choice) != {"left_sample_id", "extremum_sample_id", "right_sample_id"}
                or any(type(value) is not int for value in choice.values())):
            raise ValueError("alignment selection needs three integer pixel IDs")
        left, center, right = (samples.get(choice[key]) for key in
                               ("left_sample_id", "extremum_sample_id", "right_sample_id"))
        if any(row is None or not row["valid"] for row in (left, center, right)):
            raise ValueError("alignment selection uses an invalid or masked pixel")
        x0, x, x1 = (row["wavelength_angstrom"] for row in (left, center, right))
        low = (slots[index - 1]["predicted_obs_angstrom"]
               + slot["predicted_obs_angstrom"]) / 2 if index else window["requested_window_angstrom"][0]
        high = (slot["predicted_obs_angstrom"]
                + slots[index + 1]["predicted_obs_angstrom"]) / 2 if index + 1 < len(slots) else window["requested_window_angstrom"][1]
        if not (low <= x0 < x < x1 <= high and
                choice["extremum_sample_id"] not in used_extrema):
            raise ValueError("alignment extremum is duplicated or belongs to another slot")
        baseline = left["flux"] + (right["flux"] - left["flux"]) * (x - x0) / (x1 - x0)
        amplitude = ((center["flux"] - baseline) if slot["kind"] == "emission"
                     else (baseline - center["flux"]))
        extremum_supported = (center["flux"] > max(left["flux"], right["flux"])
                              if slot["kind"] == "emission" else
                              center["flux"] < min(left["flux"], right["flux"]))
        if not math.isfinite(amplitude) or amplitude <= 0 or not extremum_supported:
            raise ValueError("alignment extremum has no positive contrast")
        width = (x1 - x0) / (2 * edge_sigma) * SIGMA_TO_FWHM
        output[label] = {**choice, "center_angstrom": x,
                         "amplitude_proxy": amplitude,
                         "fwhm_proxy_angstrom": width,
                         "fwhm_proxy_km_s": width / x * SPEED_OF_LIGHT_KMS,
                         "outer_reference_sigma_assumption": edge_sigma,
                         "measurement_source": "llm_selected_envelope_proxy"}
        used_extrema.add(choice["extremum_sample_id"])
    return output


def summarize_selections(slots: list[dict], ballots: list[dict], quorum: int) -> dict:
    """A slot passes only with a complete odd quorum and a strict majority."""
    result = {}
    for slot in slots:
        label = slot["slot"]
        positives = [(item["seat"], item["selections"][label]) for item in ballots
                     if item["selections"][label] is not None]
        count = len(positives)
        status = ("incomplete" if len(ballots) != quorum else
                  "resolved" if count > quorum // 2 else "not_separately_supported")
        representative = None
        if status == "resolved":
            median_width = statistics.median(item[1]["fwhm_proxy_angstrom"]
                                             for item in positives)
            seat, selected = min(positives,
                                 key=lambda item: (abs(item[1]["fwhm_proxy_angstrom"]
                                                       - median_width), item[0]))
            chosen_ballot = next(item for item in ballots if item["seat"] == seat)
            if not isinstance(chosen_ballot.get("vote_ref"), str):
                raise ValueError("resolved alignment candidate has no immutable vote reference")
            representative = {**selected, "seat": seat,
                              "candidate_id": f"alignment:{chosen_ballot['vote_ref']}:{label}",
                              "vote_ref": chosen_ballot["vote_ref"]}
        result[slot["line_id"]] = {"slot": label, "status": status,
                                   "positive_votes": count, "total_votes": len(ballots),
                                   "representative": representative}
    return result


def render_alignment_markdown(output: dict | None, *, node_ref: str | None = None) -> str:
    """Human-readable advisory section; never rewrites the original line rows."""
    if not output or not output["collisions"]:
        return ""
    lines = ["## Shared-feature alignment", "",
             "Original SH/FA pairings remain archived. A null slot means no separately "
             "defensible feature, not proof that the line is absent.", ""]
    if node_ref is not None:
        lines.extend([f"- Alignment source: `{node_ref}`", ""])
    for conflict in output["collisions"]:
        lines.append(f"- Shared feature(s) `{conflict['shared_measurement_ids']}`: "
                     f"`{conflict['status']}`; affected claims "
                     f"`{conflict['tbd_line_ids']}`.")
        if conflict["ca_h_region_includes_unresolved_h_epsilon"]:
            lines.append("  - The red Ca H region may contain Hε; its components were not separated.")
        for line_id, result in conflict["line_results"].items():
            rep = result["representative"]
            detail = (f"; centre {rep['center_angstrom']} Å, amplitude proxy "
                      f"{rep['amplitude_proxy']}, FWHM proxy "
                      f"{rep['fwhm_proxy_angstrom']} Å / {rep['fwhm_proxy_km_s']} km/s, "
                      f"candidate `{rep['candidate_id']}`" if rep else "")
            lines.append(f"  - `{line_id}`: `{result['status']}` "
                         f"({result['positive_votes']}/{result['total_votes']} positive){detail}.")
    return "\n".join(lines) + "\n"


def project_aligned_claims(view: dict, collisions: list[dict]) -> list[dict]:
    """Expose report/HS-facing claims without mutating frozen SH/FA rows."""
    claims = {row["line_id"]: {
        "line_id": row["line_id"], "original_measurement_id": row["measurement_id"],
        "status": ("original_claim" if row["measurement_id"] is not None
                   and row["fa_state"] == "signal_present" else "unassigned"),
        "effective_feature_id": (row["measurement_id"] if row["measurement_id"] is not None
                                 and row["fa_state"] == "signal_present" else None),
    } for row in view["lines"]}
    for collision in collisions:
        for line_id in collision["tbd_line_ids"]:
            claims[line_id]["status"] = "tbd"
            claims[line_id]["effective_feature_id"] = None
        for line_id, result in collision["line_results"].items():
            if result["status"] == "resolved":
                claims[line_id]["status"] = "resolved"
                claims[line_id]["effective_feature_id"] = result["representative"]["candidate_id"]
    return [claims[key] for key in sorted(claims)]


async def run_line_alignment(trace: dict, *, branch_id: str, hypothesis_ref: str,
                             graph: str, output_root: str | Path, llm: Any | None,
                             concurrency: int = 3) -> dict:
    """Record all collisions, vote on diagnostic ones, then commit one branch node."""
    key = alignment_key(hypothesis_ref, graph)
    if key in trace["branches"][branch_id]["state"]["analysis_results"]:
        raise ValueError("line alignment already active; fork before revisiting")
    if concurrency < 1:
        raise ValueError("alignment concurrency must be positive")
    view = cleaned_line_view(trace, branch_id, hypothesis_ref)
    jobs = alignment_jobs(view, graph)
    catalog_ref = f"sh/{hypothesis_ref}/catalog"
    catalog = json.loads(_source(trace, catalog_ref).read_text(encoding="utf-8"))
    spectrum_ref = "spectrum_npz"
    spectrum = _source(trace, spectrum_ref)
    if (spectrum != Path(catalog["spectrum_npz_path"]).resolve(strict=True)
            or trace["artifacts"][spectrum_ref]["sha256"] != catalog["spectrum_npz_sha256"]):
        raise ValueError("alignment spectrum differs from frozen SH catalog")
    with np.load(spectrum) as data:
        wl, flux = np.asarray(data["wavelength"]), np.asarray(data["flux"])
        ivar = np.asarray(data["ivar"]) if "ivar" in data else np.full_like(flux, np.nan)
    if (wl.ndim != 1 or not len(wl) or flux.shape != wl.shape or ivar.shape != wl.shape
            or not np.isfinite(wl).all() or not np.all(np.diff(wl) > 0)):
        raise ValueError("invalid alignment spectrum arrays")
    method = load_analysis_method().audit
    quorum = method.line_alignment.vote_quorum
    semaphore = asyncio.Semaphore(concurrency)
    attempt_refs = []
    calls = []
    outputs = []
    for job in jobs:
        record = {**job, "status": "tbd", "ballots": [], "line_results": {},
                  "window": None}
        if not job["eligible"] or llm is None:
            record["reason"] = "no_diagnostic_vote" if not job["eligible"] else "model_unavailable"
            outputs.append(record)
            continue
        window = _window(wl, flux, ivar, slots=job["slots"],
                         half=method.feature_read_half_angstrom,
                         masked_regions=catalog.get("masked_regions", []))
        record["window"] = {key: value for key, value in window.items() if key != "samples"}
        positions = [item["predicted_obs_angstrom"] for item in job["slots"]]
        cores = []
        for index, position in enumerate(positions):
            low = (positions[index - 1] + position) / 2 if index else position - method.feature_read_half_angstrom
            high = (position + positions[index + 1]) / 2 if index + 1 < len(positions) else position + method.feature_read_half_angstrom
            cores.append(sum(row["valid"] and low <= row["wavelength_angstrom"] < high
                             for row in window["samples"]))
        record["usable_samples_by_slot"] = dict(zip((slot["slot"] for slot in job["slots"]), cores))
        if min(cores) < 3:
            record["reason"] = "insufficient_usable_pixels_in_slot"
            outputs.append(record)
            continue
        user = json.dumps({"slots": [{"slot": slot["slot"],
                                      "predicted_center_angstrom": slot["predicted_obs_angstrom"],
                                      "kind": slot["kind"]} for slot in job["slots"]],
                           "window_angstrom": window["requested_window_angstrom"],
                           "sample_columns": ["sample_id", "wavelength_angstrom", "flux", "valid"],
                           "samples": [[row["sample_id"], row["wavelength_angstrom"],
                                        row["flux"], row["valid"]] for row in window["samples"]]},
                          ensure_ascii=False, separators=(",", ":"), allow_nan=False)

        async def one(seat: int) -> tuple[dict | None, list[dict], list[dict]]:
            attempts = []
            for attempt_number in range(1, method.line_alignment.max_attempts_per_vote_seat + 1):
                allocation = allocate_execution(output_root, run_id=trace["run_id"],
                                                branch_id=branch_id,
                                                node_key=f"{key}/{job['measurement_id']}/seat-{seat}")
                recorder = MarkdownSessionRecorder(
                    allocation.path("session.md"), run_id=trace["run_id"],
                    hypothesis_ref=hypothesis_ref, stage="SH line alignment vote",
                    system_prompt=SYSTEM, input_messages=[HumanMessage(content=user)],
                    tools=[], session_kind="SH", subject_label="Anonymous line slots")
                selection = None
                failure = None
                try:
                    async with semaphore:
                        response = await llm.ainvoke([SystemMessage(content=SYSTEM),
                                                      HumanMessage(content=user)])
                    if not isinstance(response, AIMessage) or not isinstance(response.content, str):
                        raise ValueError("alignment model returned no JSON text")
                    recorder.record_event({"model": {"messages": [response]}})
                    raw = response.content.strip()
                    if raw.startswith("```json") and raw.endswith("```"):
                        raw = raw[7:-3].strip()
                    selection = validate_selection(json.loads(raw), job["slots"], window,
                                                   method.line_alignment.outer_reference_sigma)
                    recorder.finish(status="complete")
                except Exception as exc:
                    failure = type(exc).__name__
                    recorder.finish(status="failed", error_type=failure)
                payload = {"seat": seat, "attempt": attempt_number,
                           "selection": selection, "error_type": failure,
                           "model_calls": recorder.model_calls}
                filename = "vote.json" if failure is None else "failure.json"
                allocation.path(filename).write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                    encoding="utf-8")
                attempts.append({"allocation": allocation, "filename": filename,
                                 "payload": payload})
                if failure is None:
                    break
            success = next((item for item in attempts if item["payload"]["error_type"] is None), None)
            return ({"seat": seat, "selections": success["payload"]["selection"],
                     "vote_ref": f"alignment/{success['allocation'].node_execution_id}/vote.json"}
                    if success else None), attempts, [call for item in attempts
                                                       for call in item["payload"]["model_calls"]]

        results = await asyncio.gather(*(one(seat) for seat in range(quorum)))
        for ballot, attempts, seat_calls in results:
            calls.extend(seat_calls)
            if ballot is not None:
                record["ballots"].append(ballot)
            for attempt in attempts:
                allocation = attempt["allocation"]
                register_execution(trace, allocation)
                for filename in ("session.md", attempt["filename"]):
                    ref = f"alignment/{allocation.node_execution_id}/{filename}"
                    register_artifact(trace, ref, allocation.path(filename), "line_alignment_vote",
                                      node_execution_id=allocation.node_execution_id)
                    attempt_refs.append(ref)
        record["line_results"] = summarize_selections(job["slots"], record["ballots"], quorum)
        record["status"] = ("resolved" if all(item["status"] == "resolved"
                                             for item in record["line_results"].values())
                            else "tbd")
        record["reason"] = None if record["status"] == "resolved" else "vote_not_conclusive"
        outputs.append(record)

    source_refs = [*view["source_refs"], spectrum_ref, *sorted({ref for row in view["lines"]
                               for ref in row["fa_vote_artifact_refs"]})]
    for ref in source_refs:
        _source(trace, ref)
    allocation = allocate_execution(output_root, run_id=trace["run_id"],
                                    branch_id=branch_id, node_key=key)
    node = {"schema_version": SCHEMA, "run_id": trace["run_id"],
            "branch_id": branch_id, "hypothesis_ref": hypothesis_ref,
            "graph": graph, "node_key": key, "node_execution_id": allocation.node_execution_id,
            "input_refs": source_refs, "vote_refs": attempt_refs,
            "output": {"collisions": outputs,
                       "aligned_claims": project_aligned_claims(view, outputs),
                       "model_usage": summarize_usage(calls),
                       "window_half_angstrom": method.feature_read_half_angstrom,
                       "vote_quorum": quorum,
                       "max_attempts_per_vote_seat": method.line_alignment.max_attempts_per_vote_seat,
                       "outer_reference_sigma": method.line_alignment.outer_reference_sigma,
                       "concurrency": concurrency}}
    allocation.path("node.json").write_text(
        json.dumps(node, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8")
    register_execution(trace, allocation)
    ref = f"alignment/{allocation.node_execution_id}/node"
    register_artifact(trace, ref, allocation.path("node.json"), "line_alignment_node",
                      node_execution_id=allocation.node_execution_id)
    record_analysis(trace, branch_id, kind="analysis_result", analysis_ref=key,
                    artifact_refs=[ref, *source_refs, *attempt_refs],
                    node_execution_id=allocation.node_execution_id)
    return {"artifact_ref": ref, "node": node}


def active_alignment(trace: dict, branch_id: str, hypothesis_ref: str,
                     graph: str) -> tuple[str, dict] | None:
    """Read the branch's committed alignment, including an ancestor at fork time."""
    from .reasoning_trace import reachable_events
    key = alignment_key(hypothesis_ref, graph)
    for event in reversed(reachable_events(trace, branch_id)):
        if event["kind"] == "analysis_result" and event["payload"]["analysis_ref"] == key:
            refs = [ref for ref in event["artifact_refs"]
                    if trace["artifacts"][ref]["kind"] == "line_alignment_node"
                    and trace["artifacts"][ref].get("node_execution_id")
                    == event["execution"]["node_execution_id"]]
            if len(refs) != 1:
                raise ValueError("alignment event has no unique node artifact")
            ref = refs[0]
            node = json.loads(_source(trace, ref).read_text(encoding="utf-8"))
            if (node["node_key"] != key or node["hypothesis_ref"] != hypothesis_ref
                    or node["run_id"] != trace["run_id"]):
                raise ValueError("alignment node identity differs")
            for source_ref in [*node["input_refs"], *node["vote_refs"]]:
                _source(trace, source_ref)
            return ref, node
    return None
