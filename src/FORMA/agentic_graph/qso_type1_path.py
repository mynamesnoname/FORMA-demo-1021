"""Q4–Q10: branch-scoped Type 1 investigation from frozen SH/FA and NPZ inputs."""

from __future__ import annotations

import hashlib
import json
import math
import random
from pathlib import Path
from typing import Any, Callable

import numpy as np
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from FORMA.core.config.analysis_method import load_analysis_method
from FORMA.core.constants import SIGMA_TO_FWHM, SPEED_OF_LIGHT_KMS

from .execution_artifacts import allocate_execution
from .feature_registry import _digest
from .qso_entry import _key, _save_node
from .qso_report import _active_node, _read_artifact
from .qso_type1_gate import TYPE1_LINES, infer_type1_gate, select_type1_gate_lines
from .session_markdown import MarkdownSessionRecorder


INSPECT_SYSTEM = """Inspect one predicted QSO broad emission line in a frozen local spectrum.
Return only a JSON object with keys finding, broad_envelope, absorption_fragmentation, reason.
finding must be one of plausible_uncatalogued_signal, no_coherent_signal_seen,
data_limited, ambiguous. broad_envelope and absorption_fragmentation are booleans.
Narrow absorption, especially in Ly-alpha, can split a broad emission envelope into
lobes. A CWT miss or a narrow fitted lobe is not evidence that the whole broad line
is absent. Check both sides, the troughs, blending and usable samples. If a common
envelope cannot be judged, answer ambiguous or data_limited. Do not infer a type.
"""
PICK_SYSTEM = """Select one peak and two outer baseline reference samples, one on
each side of the same emission envelope, from this single unlabelled window.
Return only JSON {"left_sample_id": integer, "peak_sample_id": integer,
"right_sample_id": integer, "reason": string}, or
{"no_valid_pair": true, "reason": string}. Choose usable samples only. Do not
choose an internal absorption trough as an outer baseline reference. For a
fragmented line, inspect both sides of the common envelope; if you cannot
locate both outer references, return no_valid_pair. You do not know whether
this is a target or reference window; do not infer a line identity. The supplied
edge-sigma value is a later code conversion convention, not a measured wing
level that you must locate in the pixels.
"""
COMPARE_SYSTEM = """Given two independently measured peak-above-local-baseline
amplitude proxies, decide whether their ratio is acceptable for the named QSO
line pair under the stated local caveats. Return only JSON with vote (accept or
reject) and reason. A rejection means this ratio is not accepted; it does not
prove that a line is physically absent. The points define local baseline
amplitudes; this session does not judge line width. Do not change the supplied
numbers.
"""


def _json_object(content: str) -> dict:
    if not isinstance(content, str):
        raise ValueError("model did not return text")
    raw = content.strip()
    if raw.startswith("```json") and raw.endswith("```"):
        raw = raw[7:-3].strip()
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("model response is not a JSON object")
    return value


def _write_json(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def _spectrum(trace: dict, catalog: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ref = trace["artifacts"]["spectrum_npz"]
    path = Path(ref["path"]).resolve(strict=True)
    if (_digest(path) != ref["sha256"] or path != Path(catalog["spectrum_npz_path"]).resolve()
            or ref["sha256"] != catalog["spectrum_npz_sha256"]):
        raise ValueError("QSO spectrum differs from frozen catalog")
    with np.load(path) as data:
        wl, flux = np.asarray(data["wavelength"]), np.asarray(data["flux"])
        ivar = np.asarray(data["ivar"]) if "ivar" in data else np.full_like(flux, np.nan)
    if (wl.ndim != 1 or not len(wl) or flux.shape != wl.shape or ivar.shape != wl.shape
            or not np.isfinite(wl).all() or not np.all(np.diff(wl) > 0)):
        raise ValueError("invalid frozen QSO spectrum arrays")
    return wl, flux, ivar


def _explicit_mask_covers(start: float, end: float, regions: list) -> bool:
    """Prove continuous interval coverage; masked sample count alone is insufficient."""
    cursor = start
    for low, high in sorted((float(a), float(b)) for a, b in regions):
        if low > cursor:
            break
        cursor = max(cursor, high)
        if cursor >= end:
            return True
    return False


def local_window(wl: np.ndarray, flux: np.ndarray, ivar: np.ndarray, *,
                 center: float, half_width: float, masked_regions: list) -> dict:
    if not math.isfinite(center) or not math.isfinite(half_width) or half_width <= 0:
        raise ValueError("invalid QSO line window")
    lo, hi = center - half_width, center + half_width
    in_range = wl[0] <= center <= wl[-1]
    subset = np.flatnonzero((wl >= lo) & (wl <= hi))
    rows = []
    explicit_count = 0
    for index in subset:
        x, y, iv = float(wl[index]), float(flux[index]), float(ivar[index])
        explicit = any(float(a) <= x <= float(b) for a, b in masked_regions)
        explicit_count += int(explicit)
        valid = math.isfinite(y) and math.isfinite(iv) and iv > 0 and not explicit
        rows.append({"sample_id": int(index), "wavelength_angstrom": x,
                     "flux": y if math.isfinite(y) else None,
                     "ivar": iv if math.isfinite(iv) else None,
                     "explicit_mask": explicit, "valid": valid})
    usable = sum(row["valid"] for row in rows)
    full_mask = (in_range and rows and usable == 0
                 and _explicit_mask_covers(lo, hi, masked_regions))
    if not in_range:
        coverage = "outside_range"
    elif full_mask:
        coverage = "fully_masked"
    elif not usable:
        coverage = "no_usable_data"
    elif usable < len(rows) or wl[0] > lo or wl[-1] < hi:
        coverage = "partial"
    else:
        coverage = "usable"
    return {"center_angstrom": center, "requested_window_angstrom": [lo, hi],
            "actual_window_angstrom": [rows[0]["wavelength_angstrom"],
                                          rows[-1]["wavelength_angstrom"]] if rows else None,
            "coverage": coverage, "total_samples": len(rows),
            "usable_samples": usable, "explicit_masked_samples": explicit_count,
            "full_window_explicit_mask_proof": bool(full_mask), "samples": rows}


async def _model_json(llm: Any, *, trace: dict, hypothesis_ref: str,
                      stage: str, system: str, user: str, path: Path,
                      validator: Callable[[dict], Any] | None = None) -> tuple[dict, list[dict]]:
    messages = [SystemMessage(content=system), HumanMessage(content=user)]
    recorder = MarkdownSessionRecorder(
        path, run_id=trace["run_id"], hypothesis_ref=hypothesis_ref,
        stage=stage, system_prompt=system, input_messages=messages[1:],
        tools=[], session_kind="QSO", subject_label="Hypothesis")
    try:
        response = await llm.ainvoke(messages)
        if not isinstance(response, AIMessage):
            raise ValueError("QSO model returned no AI message")
        recorder.record_event({"model": {"messages": [response]}})
        obj = _json_object(response.content)
        if validator is not None:
            validator(obj)
        recorder.finish(status="complete")
        return obj, recorder.model_calls
    except Exception as exc:
        recorder.finish(status="failed", error_type=type(exc).__name__)
        exc.model_usage = recorder.model_calls
        raise


def _validate_inspection(obj: dict) -> dict:
    findings = {"plausible_uncatalogued_signal", "no_coherent_signal_seen",
                "data_limited", "ambiguous"}
    if (set(obj) != {"finding", "broad_envelope", "absorption_fragmentation", "reason"}
            or obj["finding"] not in findings
            or type(obj["broad_envelope"]) is not bool
            or type(obj["absorption_fragmentation"]) is not bool
            or not isinstance(obj["reason"], str) or not obj["reason"].strip()):
        raise ValueError("Q6 finding does not satisfy its contract")
    if obj["finding"] == "plausible_uncatalogued_signal" and not obj["broad_envelope"]:
        raise ValueError("Q6 candidate lacks a broad-envelope claim")
    return obj


def _point_measurement(obj: dict, window: dict,
                       center_bound: float | None = None,
                       edge_sigma: float | None = None) -> dict | None:
    if not isinstance(obj.get("reason"), str) or not obj["reason"].strip():
        raise ValueError("Q8 point answer requires a reason")
    if obj.get("no_valid_pair") is True and set(obj) == {"no_valid_pair", "reason"}:
        return None
    if set(obj) != {"left_sample_id", "peak_sample_id", "right_sample_id", "reason"}:
        raise ValueError("Q8 point submission has invalid keys")
    if any(type(obj[key]) is not int for key in
           ("left_sample_id", "peak_sample_id", "right_sample_id")):
        raise ValueError("Q8 point IDs must be integers")
    samples = {row["sample_id"]: row for row in window["samples"]}
    left, peak, right = (samples.get(obj[key]) for key in
                         ("left_sample_id", "peak_sample_id", "right_sample_id"))
    if (any(row is None or not row["valid"] for row in (left, peak, right))
            or not left["wavelength_angstrom"] < peak["wavelength_angstrom"]
                   < right["wavelength_angstrom"]
            or peak["flux"] <= max(left["flux"], right["flux"])):
        raise ValueError("Q8 points are not a valid ordered peak/baseline triple")
    center = window["center_angstrom"]
    if center_bound is None:
        center_bound = load_analysis_method().gaussian_fit.center_bound_half_angstrom
    if edge_sigma is None:
        edge_sigma = load_analysis_method().qso_type1.envelope_edge_sigma
    if not math.isfinite(edge_sigma) or edge_sigma <= 0:
        raise ValueError("Q8 envelope sigma convention must be positive")
    if abs(peak["wavelength_angstrom"] - center) > center_bound:
        raise ValueError("Q8 peak is too far from the investigated line center")
    span = right["wavelength_angstrom"] - left["wavelength_angstrom"]
    baseline = left["flux"] + (right["flux"] - left["flux"]) * (
        peak["wavelength_angstrom"] - left["wavelength_angstrom"]) / span
    amplitude = peak["flux"] - baseline
    if not math.isfinite(amplitude) or amplitude <= 0:
        raise ValueError("Q8 peak must exceed the interpolated local baseline")
    sigma_proxy = span / (2 * edge_sigma)
    fwhm_proxy = sigma_proxy * SIGMA_TO_FWHM
    return {"left_sample_id": left["sample_id"],
            "peak_sample_id": peak["sample_id"],
            "right_sample_id": right["sample_id"],
            "left_wavelength_angstrom": left["wavelength_angstrom"],
            "peak_wavelength_angstrom": peak["wavelength_angstrom"],
            "right_wavelength_angstrom": right["wavelength_angstrom"],
            "left_flux": left["flux"], "peak_flux": peak["flux"],
            "right_flux": right["flux"], "baseline_at_peak": baseline,
            "amplitude_proxy": amplitude,
            "envelope_span_angstrom": span,
            "edge_sigma_assumption": edge_sigma,
            "fwhm_proxy_angstrom": fwhm_proxy,
            "fwhm_proxy_km_s": fwhm_proxy / peak["wavelength_angstrom"] * SPEED_OF_LIGHT_KMS,
            "envelope_asymmetry_fraction": abs(
                (peak["wavelength_angstrom"] - left["wavelength_angstrom"])
                - (right["wavelength_angstrom"] - peak["wavelength_angstrom"])) / span,
            "measurement_source": "llm_selected_envelope_proxy",
            "reason": obj["reason"]}


def _validate_comparison(obj: dict) -> dict:
    if (set(obj) != {"vote", "reason"} or obj["vote"] not in {"accept", "reject"}
            or not isinstance(obj["reason"], str) or not obj["reason"].strip()):
        raise ValueError("invalid Q8 comparison vote")
    return obj


def _pick_user(window: dict, edge_sigma: float) -> str:
    return json.dumps({"window": window["requested_window_angstrom"],
                       "edge_sigma_assumption": edge_sigma,
                       "samples": [{"sample_id": r["sample_id"],
                                    "wavelength_angstrom": r["wavelength_angstrom"],
                                    "flux": r["flux"], "valid": r["valid"]}
                       for r in window["samples"]]},
                      ensure_ascii=False, allow_nan=False)


async def _strength_vote(llm: Any, trace: dict, hypothesis_ref: str,
                         allocation, target: dict, reference: dict,
                         target_id: str, reference_id: str, caveat: str,
                         *, n: int = 3, max_attempts_per_seat: int = 2,
                         center_bound: float | None = None,
                         edge_sigma: float | None = None) -> tuple[dict, dict]:
    """Isolated 2n point sessions, seeded pairing, then n isolated accept votes."""
    if n < 1 or n % 2 == 0 or max_attempts_per_seat < 1:
        raise ValueError("Q8 requires an odd positive quorum and a bounded retry count")
    if edge_sigma is None:
        edge_sigma = load_analysis_method().qso_type1.envelope_edge_sigma
    if not math.isfinite(edge_sigma) or edge_sigma <= 0:
        raise ValueError("Q8 envelope sigma convention must be positive")
    files: dict[str, tuple[str, str]] = {}
    all_attempts = []
    picks: dict[str, list[dict]] = {"a": [], "b": []}
    for label, window in (("a", target), ("b", reference)):
        for seat in range(n):
            for attempt in range(max_attempts_per_seat):
                name = f"pick_{label}_{seat}_{attempt}.md"
                files[name[:-3]] = (name, "qso_session")
                try:
                    obj, usage = await _model_json(
                        llm, trace=trace, hypothesis_ref=hypothesis_ref,
                        stage="Q8 isolated point selection", system=PICK_SYSTEM,
                        user=_pick_user(window, edge_sigma), path=allocation.path(name),
                        validator=lambda answer: _point_measurement(answer, window,
                                                                      center_bound,
                                                                      edge_sigma))
                    measured = _point_measurement(obj, window, center_bound,
                                                  edge_sigma)
                    all_attempts.append({"stage": "pick", "window": label,
                                         "seat": seat, "attempt": attempt,
                                         "answer": obj, "measurement": measured,
                                         "model_usage": usage, "session": name})
                    if measured is not None:
                        picks[label].append(measured)
                    break  # no_valid_pair is a valid non-vote, not a reason to retry
                except Exception as exc:
                    all_attempts.append({"stage": "pick", "window": label,
                                         "seat": seat, "attempt": attempt,
                                         "error_type": type(exc).__name__,
                                         "model_usage": getattr(exc, "model_usage", []),
                                         "session": name})
    seed = int.from_bytes(hashlib.sha256(
        f"{trace['run_id']}|{hypothesis_ref}|{allocation.branch_id}|{allocation.node_execution_id}".encode()
    ).digest()[:8], "big")
    order = list(range(n))
    random.Random(seed).shuffle(order)
    pairings = []
    votes = []
    if len(picks["a"]) == n and len(picks["b"]) == n:
        for seat, other in enumerate(order):
            a, b = picks["a"][seat], picks["b"][other]
            ratio = a["amplitude_proxy"] / b["amplitude_proxy"]
            pair = {"target_seat": seat, "reference_seat": other,
                    "target_amplitude_proxy": a["amplitude_proxy"],
                    "reference_amplitude_proxy": b["amplitude_proxy"], "ratio": ratio}
            pairings.append(pair)
            comparison_fields = ("left_wavelength_angstrom", "peak_wavelength_angstrom",
                                 "right_wavelength_angstrom", "left_flux", "peak_flux",
                                 "right_flux", "baseline_at_peak", "amplitude_proxy")
            measured_a = {key: a[key] for key in comparison_fields}
            measured_b = {key: b[key] for key in comparison_fields}
            user = json.dumps({"target_line_id": target_id, "reference_line_id": reference_id,
                               "target_points": measured_a, "reference_points": measured_b,
                               "ratio": ratio, "target_caveat": caveat,
                               "target_coverage": target["coverage"],
                               "reference_coverage": reference["coverage"]},
                              ensure_ascii=False, allow_nan=False)
            for attempt in range(max_attempts_per_seat):
                name = f"compare_{seat}_{attempt}.md"
                files[name[:-3]] = (name, "qso_session")
                try:
                    obj, usage = await _model_json(
                        llm, trace=trace, hypothesis_ref=hypothesis_ref,
                        stage="Q8 isolated strength comparison", system=COMPARE_SYSTEM,
                        user=user, path=allocation.path(name),
                        validator=_validate_comparison)
                    votes.append({"seat": seat, **obj})
                    all_attempts.append({"stage": "compare", "seat": seat,
                                         "attempt": attempt, "answer": obj,
                                         "model_usage": usage, "session": name})
                    break
                except Exception as exc:
                    all_attempts.append({"stage": "compare", "seat": seat,
                                         "attempt": attempt,
                                         "error_type": type(exc).__name__,
                                         "model_usage": getattr(exc, "model_usage", []),
                                         "session": name})
    p = sum(v["vote"] == "accept" for v in votes) / n if len(votes) == n else None
    status = ("measurement_unavailable" if len(picks["a"]) != n or len(picks["b"]) != n
              else "vote_incomplete" if len(votes) != n
              else "accepted" if p > 0.5 else "rejected" if p < 0.5 else "tied")
    vote_band = (None if p is None else
                 "accept_consistent" if p > 0.75 else
                 "accept_split" if p > 0.5 else
                 "tie" if p == 0.5 else
                 "reject_split" if p >= 0.25 else "reject_consistent")
    representative = None
    if status == "accepted":
        # The middle-width target pick is one complete, reproducible submission.
        seat = sorted(range(n), key=lambda i: (picks["a"][i]["fwhm_proxy_km_s"], i))[n // 2]
        representative = {"target_seat": seat, "selection_rule": "median_target_width",
                          **picks["a"][seat]}
    output = {"target_line_id": target_id, "reference_line_id": reference_id,
              "quorum": n, "status": status, "p_accept": p,
              "vote_band": vote_band, "seed": seed,
              "edge_sigma_assumption": edge_sigma,
              "measurement_method_version": "qso-two-sided-envelope-proxy-v1",
              "pairing_order": order if pairings else [], "target_picks": picks["a"],
              "reference_picks": picks["b"], "pairings": pairings, "votes": votes,
              "representative_target_measurement": representative,
              "contested": bool(pairings and
                                (min(x["ratio"] for x in pairings) < 1 <
                                 max(x["ratio"] for x in pairings)
                                 or len({v["vote"] for v in votes}) > 1)),
              "attempts": all_attempts}
    _write_json(allocation.path("vote_record.json"), output)
    files["vote_record"] = ("vote_record.json", "qso_vote_record")
    return output, files


async def run_qso_type1_path(trace: dict, *, branch_id: str, hypothesis_ref: str,
                             output_root: str | Path, llm: Any,
                             vote_quorum: int | None = None) -> dict:
    """Continue an active Q3 into Q4–Q10; Q11 is dispatched by the caller."""
    q3 = _active_node(trace, branch_id, hypothesis_ref, "qso.broad_line_inventory")
    if q3 is None:
        raise ValueError("QSO Type 1 path requires Q3")
    if _active_node(trace, branch_id, hypothesis_ref, "qso.type1_formal_gate"):
        raise ValueError("Type 1 path already closed; fork before revisiting")
    catalog_ref = f"sh/{hypothesis_ref}/catalog"
    catalog = _read_artifact(trace, catalog_ref)
    wl, flux, ivar = _spectrum(trace, catalog)
    analysis_method = load_analysis_method()
    method = analysis_method.qso_type1
    half_width = method.local_read_half_angstrom
    vote_quorum = method.strength_vote_quorum if vote_quorum is None else vote_quorum
    method_snapshot = {"qso_type1": method.model_dump(mode="json"),
                       "peak_center_bound_half_angstrom":
                           analysis_method.gaussian_fit.center_bound_half_angstrom,
                       "effective_vote_quorum": vote_quorum}
    method_digest = hashlib.sha256(json.dumps(
        method_snapshot, sort_keys=True, separators=(",", ":"),
        allow_nan=False).encode()).hexdigest()
    inventory = {row["line_id"]: row for row in q3[1]["output"]["lines"]}
    windows = {line_id: local_window(
        wl, flux, ivar, center=inventory[line_id]["predicted_obs_angstrom"],
        half_width=half_width, masked_regions=catalog.get("masked_regions", []))
        for line_id in TYPE1_LINES}
    coverage = {line_id: window["coverage"] for line_id, window in windows.items()}
    selected = select_type1_gate_lines(coverage)
    queue = []
    for line_id in selected:
        row = inventory[line_id]
        if row["cleaned_pairing"] == "adopted" and row["broadness"] == "supported":
            continue
        queue.append({"line_id": line_id,
                      "predicted_obs_angstrom": row["predicted_obs_angstrom"],
                      "reason": row["cleaned_pairing"] if row["cleaned_pairing"] != "adopted"
                                else "width_not_supported",
                      "coverage_preview": coverage[line_id]})
    q4 = _save_node(trace, branch_id, hypothesis_ref, "qso.missing_broad_line_queue",
                    {"selected_line_ids": selected, "queue": queue,
                     "coverage_preview": coverage,
                     "window_half_width_angstrom": half_width,
                     "window_parameter": "analysis_method.qso_type1.local_read_half_angstrom",
                     "method_snapshot": method_snapshot,
                     "method_snapshot_sha256": method_digest},
                    [q3[0], catalog_ref, "spectrum_npz"], output_root)
    nodes = [q4]
    states: dict[str, str] = {}
    state_refs: dict[str, list[str]] = {}
    coverage_refs: dict[str, str] = {}
    for line_id in selected:
        window = windows[line_id]
        q5 = _save_node(trace, branch_id, hypothesis_ref, f"qso.coverage/{line_id}",
                        {key: value for key, value in window.items() if key != "samples"},
                        [q4["artifact_ref"], "spectrum_npz", catalog_ref], output_root)
        nodes.append(q5)
        coverage_refs[line_id] = q5["artifact_ref"]
        state_refs[line_id] = [q5["artifact_ref"]]
        row = inventory[line_id]
        if coverage[line_id] in {"outside_range", "fully_masked", "no_usable_data"}:
            states[line_id] = "unresolved"
            continue
        if row["cleaned_pairing"] == "adopted" and row["broadness"] == "supported":
            states[line_id] = "paired"
            state_refs[line_id].append(q3[0])
            continue
        # An adopted narrow/unknown-width measurement is not a new candidate.
        # A targeted Q6 read can still find a broader envelope around it.
        node_type = f"qso.inspect_line/{line_id}"
        allocation = allocate_execution(output_root, run_id=trace["run_id"],
                                        branch_id=branch_id,
                                        node_key=_key(hypothesis_ref, node_type))
        _write_json(allocation.path("window.json"), window)
        user = json.dumps({"line_id": line_id,
                           "predicted_obs_angstrom": row["predicted_obs_angstrom"],
                           "coverage": coverage[line_id],
                           "samples": window["samples"]},
                          ensure_ascii=False, allow_nan=False)
        finding, usage = await _model_json(
            llm, trace=trace, hypothesis_ref=hypothesis_ref, stage="Q6 local inspection",
            system=INSPECT_SYSTEM, user=user, path=allocation.path("session.md"),
            validator=_validate_inspection)
        q6 = _save_node(trace, branch_id, hypothesis_ref, node_type,
                        {"line_id": line_id, **finding,
                         "model_usage": usage,
                         "window_ref": f"sh2/{allocation.node_execution_id}/window",
                         "session_ref": f"sh2/{allocation.node_execution_id}/session"},
                        [q5["artifact_ref"], "spectrum_npz"], output_root,
                        allocation=allocation, created_by="mixed",
                        extra_artifacts={"window": ("window.json", "qso_local_window"),
                                         "session": ("session.md", "qso_session")})
        nodes.append(q6)
        state_refs[line_id].append(q6["artifact_ref"])
        if finding["finding"] == "no_coherent_signal_seen":
            states[line_id] = "failed"
            continue
        states[line_id] = "unresolved"
        if finding["finding"] != "plausible_uncatalogued_signal":
            continue
        candidate_id = f"targeted:{hypothesis_ref}:{line_id}:{q6['node']['node_execution_id']}"
        q7 = _save_node(trace, branch_id, hypothesis_ref,
                        f"qso.proposed_observation/{line_id}",
                        {"line_id": line_id, "candidate_id": candidate_id,
                         "provenance": "targeted_read", "q6_ref": q6["artifact_ref"],
                         "measurement_status": "awaiting_q8_point_selection",
                         "broad_envelope_claim": finding["broad_envelope"],
                         "absorption_fragmentation": finding["absorption_fragmentation"],
                         "fa_status": "not_re_reviewed",
                         "original_sh_fa_pairing_unchanged": True},
                        [q6["artifact_ref"], q6["extra_artifact_refs"]["window"]],
                        output_root)
        nodes.append(q7)
        state_refs[line_id].append(q7["artifact_ref"])
        references = [other for other in TYPE1_LINES if other != line_id
                      and inventory[other]["cleaned_pairing"] == "adopted"
                      and inventory[other]["broadness"] == "supported"
                      and coverage[other] in {"usable", "partial"}]
        if not references:
            # Q8 exists as a node with an explicit unavailable result, not a fake vote.
            q8 = _save_node(trace, branch_id, hypothesis_ref,
                            f"qso.relative_strength/{line_id}",
                            {"line_id": line_id, "status": "reference_unavailable",
                             "reference_line_id": None, "votes": []},
                            [q7["artifact_ref"]], output_root)
        else:
            reference_id = references[0]
            q8_type = f"qso.relative_strength/{line_id}"
            vote_allocation = allocate_execution(output_root, run_id=trace["run_id"],
                                                 branch_id=branch_id,
                                                 node_key=_key(hypothesis_ref, q8_type))
            result, files = await _strength_vote(
                llm, trace, hypothesis_ref, vote_allocation, window,
                windows[reference_id], line_id, reference_id, finding["reason"],
                n=vote_quorum, max_attempts_per_seat=method.max_attempts_per_vote_seat,
                center_bound=analysis_method.gaussian_fit.center_bound_half_angstrom,
                edge_sigma=method.envelope_edge_sigma)
            result["candidate_id"] = candidate_id
            result["q7_ref"] = q7["artifact_ref"]
            result["strict_broad_fwhm_km_s"] = q3[1]["output"]["strict_broad_fwhm_km_s"]
            representative = result["representative_target_measurement"]
            result["representative_broadness"] = (
                "supported_proxy" if representative is not None and
                representative["fwhm_proxy_km_s"] >= result["strict_broad_fwhm_km_s"]
                else "not_supported_proxy" if representative is not None else "unresolved")
            result["session_refs"] = [f"sh2/{vote_allocation.node_execution_id}/{name}"
                                      for name in files if name != "vote_record"]
            result["vote_record_ref"] = f"sh2/{vote_allocation.node_execution_id}/vote_record"
            q8 = _save_node(trace, branch_id, hypothesis_ref, q8_type, result,
                            [q7["artifact_ref"], "spectrum_npz", catalog_ref],
                            output_root, allocation=vote_allocation,
                            extra_artifacts=files, created_by="mixed")
            if result["status"] == "accepted" and result["representative_broadness"] == "supported_proxy":
                states[line_id] = "vote_explained"
            elif result["status"] == "rejected":
                states[line_id] = "failed"
        nodes.append(q8)
        state_refs[line_id].append(q8["artifact_ref"])
    gate = infer_type1_gate(coverage, states)
    q9 = _save_node(trace, branch_id, hypothesis_ref, "qso.type1_formal_gate",
                    {"selected_line_ids": list(gate.selected_line_ids),
                     "gate_status": gate.status,
                     "effective_line_states": [list(item) for item in gate.effective_line_states],
                     "raw_line_states": states,
                     "coverage": coverage, "state_source_refs": state_refs,
                     "reason_codes": [f"{line_id}:{state}" for line_id, state in
                                      gate.effective_line_states if state not in
                                      {"paired", "vote_explained"}]},
                    sorted({q4["artifact_ref"], *coverage_refs.values(),
                            *(ref for refs in state_refs.values() for ref in refs)}),
                    output_root)
    nodes.append(q9)
    status = {"type1_supported": "survive", "type1_failed": "dead",
              "type1_unresolved": "unresolved"}[gate.status]
    q10 = _save_node(trace, branch_id, hypothesis_ref, "qso.route_result",
                     {"path_status": status,
                      "candidate_type": "Type 1 QSO" if status == "survive" else None,
                      "rule_id": "project:qso-type1-formal-gate",
                      "reason_codes": q9["node"]["output"]["reason_codes"]},
                     [q9["artifact_ref"]], output_root)
    nodes.append(q10)
    return {"path_status": status, "candidate_type": q10["node"]["output"]["candidate_type"],
            "nodes": nodes}
