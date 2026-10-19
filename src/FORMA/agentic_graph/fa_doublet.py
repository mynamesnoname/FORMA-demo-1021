"""Branch-scoped advisory FA review of an SH doublet or orphan component."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Callable

import numpy as np
from langchain.agents import create_agent

from FORMA.core.config.analysis_method import DoubletReviewMethod, load_analysis_method
from FORMA.core.reasoning.ontology.query import oiii_ratio_window_a_over_b
from FORMA.core.reasoning.ontology.registry import ONTOLOGY

from .cleaned_line_view import _read_artifact, cleaned_line_view
from .execution_artifacts import allocate_execution
from .feature_registry import _digest
from .node_keys import fa_doublet_key
from .reasoning_trace import record_analysis, register_artifact, register_execution
from .sh_pre_analysis import PROMPT_DIR, _render
from .vote_runtime import collect_advisory_votes, summarize_usage, vote_tally


SCHEMA = "forma-fa-doublet-review-v1"
_ELIGIBLE = frozenset({"doublet:oiii", "doublet:sii", "doublet:nii",
                       "doublet:cahk", "doublet:na-d"})


def claimed_doublet_ids(trace: dict, branch_id: str, hypothesis_ref: str) -> list[str]:
    """Find old-FA doublets with at least one SH-adopted component."""
    view = cleaned_line_view(trace, branch_id, hypothesis_ref)
    kept = {row["line_id"] for row in view["lines"] if row["measurement_id"] is not None}
    return [record.id for record in ONTOLOGY.doublets
            if record.id in _ELIGIBLE and kept.intersection(record.component_ids)]


def _record(doublet_id: str):
    if doublet_id not in _ELIGIBLE:
        raise ValueError(f"doublet is not in the FA review set: {doublet_id}")
    return next(record for record in ONTOLOGY.doublets if record.id == doublet_id)


def _finite_number(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        number = float(value)
        if math.isfinite(number):
            return number
    return None


def _component_payload(line_id: str, row: dict | None,
                       measurements: dict, z: float) -> dict:
    declared = ONTOLOGY.line_index()[line_id]
    expected = declared.rest_wavelength * (1 + z)
    if row is not None and not math.isclose(float(row["predicted_obs_angstrom"]),
                                             expected, rel_tol=1e-7, abs_tol=0.01):
        raise ValueError(f"frozen SH prediction differs from ontology for {line_id}")
    measurement_id = row["measurement_id"] if row else None
    measurement = measurements.get(measurement_id) if measurement_id else None
    if measurement_id and measurement is None:
        raise ValueError(f"missing frozen measurement: {measurement_id}")
    if measurement is not None:
        raw = measurement["record"]
        key = "wavelength" if measurement["source"] == "CWT" else "center"
        center = _finite_number(raw.get(key))
        amp = _finite_number(raw.get("amplitude"))
    else:
        center = amp = None
    return {"line_id": line_id, "line_name": declared.name,
            "rest_angstrom": declared.rest_wavelength,
            "expected_obs_angstrom": expected,
            "sh_status": row["sh_status"] if row else "outside_sh_catalog",
            "measurement_id": measurement_id,
            "measurement_source": row["measurement_source"] if row else None,
            "measured_center_angstrom": center, "amplitude": amp,
            "measured_offset_from_expected_angstrom": (center - expected
                                                       if center is not None else None),
            "fa_state": row["fa_state"] if row else None,
            "cleaned_pairing": row["cleaned_pairing"] if row else "outside_sh_catalog",
            "fa_vote_artifact_refs": row["fa_vote_artifact_refs"] if row else []}


def _numeric_metrics(record, components: list[dict]) -> dict:
    a, b = components
    ca, cb = a["measured_center_angstrom"], b["measured_center_angstrom"]
    aa, ab = a["amplitude"], b["amplitude"]
    expected_sep = abs(b["expected_obs_angstrom"] - a["expected_obs_angstrom"])
    measured_sep = abs(cb - ca) if ca is not None and cb is not None else None
    ratio = abs(aa) / abs(ab) if aa is not None and ab not in (None, 0) else None
    window = (oiii_ratio_window_a_over_b() if record.id == "doublet:oiii"
              else list(record.ratio_window) if record.ratio_window else None)
    if ratio is None:
        ratio_ok = None
    elif record.id == "doublet:cahk":
        ratio_ok = abs(aa) > abs(ab)
    else:
        ratio_ok = window[0] <= ratio <= window[1] if window else None
    return {"expected_separation_angstrom": expected_sep,
            "registry_rest_separation_angstrom": record.rest_separation,
            "measured_separation_angstrom": measured_sep,
            "separation_difference_angstrom": (measured_sep - expected_sep
                                                if measured_sep is not None else None),
            "amplitude_ratio_a_over_b": ratio,
            "reference_ratio_window_a_over_b": window,
            "reference_ratio_note": record.amplitude_ratio_note,
            "reference_ratio_within_window": ratio_ok,
            "reference_ratio_is_advisory": True}


def build_doublet_window(npz_path: str | Path, *, components: list[dict],
                         masked_regions: list, method: DoubletReviewMethod) -> dict:
    """Return complete local pixels and a deterministic two-core coverage check."""
    if len(components) != 2:
        raise ValueError("doublet needs two components")
    with np.load(npz_path) as spectrum:
        wl = spectrum["wavelength"]
        flux = spectrum["flux"]
        ivar = spectrum["ivar"] if "ivar" in spectrum else np.full_like(flux, np.nan)
    if (wl.ndim != 1 or len(wl) == 0 or flux.shape != wl.shape or ivar.shape != wl.shape
            or not np.all(np.isfinite(wl)) or not np.all(np.diff(wl) > 0)):
        raise ValueError("doublet spectrum needs ordered finite wavelength and aligned arrays")
    centers = [item["expected_obs_angstrom"] for item in components]
    if any(not math.isfinite(center) or center <= 0 for center in centers):
        raise ValueError("doublet predicted positions must be finite and positive")
    left = min(centers) - method.context_margin_angstrom
    right = max(centers) + method.context_margin_angstrom
    selected = (wl >= left) & (wl <= right)
    local_wl, local_flux, local_ivar = wl[selected], flux[selected], ivar[selected]
    masked = np.zeros(len(local_wl), dtype=bool)
    for region in masked_regions or []:
        if (not isinstance(region, (list, tuple)) or len(region) != 2
                or not all(isinstance(x, (int, float)) and math.isfinite(x) for x in region)
                or region[0] > region[1]):
            raise ValueError("invalid doublet mask interval")
        masked |= (local_wl >= region[0]) & (local_wl <= region[1])
    valid = np.isfinite(local_flux) & np.isfinite(local_ivar) & (local_ivar > 0) & ~masked
    cores = []
    for item in components:
        center = item["expected_obs_angstrom"]
        core = abs(local_wl - center) <= method.component_check_half_angstrom
        in_bounds = bool(wl[0] <= center <= wl[-1])
        count = int(np.count_nonzero(valid & core))
        cores.append({"line_id": item["line_id"], "predicted_obs_angstrom": center,
                      "center_within_spectrum_bounds": in_bounds,
                      "samples": int(np.count_nonzero(core)), "valid_samples": count,
                      "masked_samples": int(np.count_nonzero(masked & core)),
                      "assessable": in_bounds and count >= method.min_valid_component_samples})
    assessable = all(core["assessable"] for core in cores)
    reason = None if assessable else (
        "component_outside_spectrum" if any(not core["center_within_spectrum_bounds"]
                                            for core in cores)
        else "insufficient_valid_component_samples")
    coverage = {"requested_window_angstrom": [left, right],
                "actual_window_angstrom": ([float(local_wl[0]), float(local_wl[-1])]
                                            if len(local_wl) else None),
                "spectrum_bounds_angstrom": [float(wl[0]), float(wl[-1])],
                "component_cores": cores, "assessable": assessable,
                "unreviewable_reason": reason}
    sample_ids = np.flatnonzero(selected)
    samples = [{"sample_id": int(index), "wavelength_angstrom": float(w),
                "flux": float(f) if math.isfinite(f) else None,
                "ivar": float(v) if math.isfinite(v) else None,
                "valid": bool(ok)}
               for index, w, f, v, ok in zip(sample_ids, local_wl, local_flux,
                                                local_ivar, valid, strict=True)]
    rows = ["| sample ID | wavelength (Å) | flux | ivar | usable |",
            "|---:|---:|---:|---:|---|"]
    rows.extend(f"| {row['sample_id']} | {row['wavelength_angstrom']:.8g} | "
                f"{row['flux']} | {row['ivar']} | {'yes' if row['valid'] else 'no'} |"
                for row in samples)
    return {"coverage": coverage,
            "samples": samples,
            "samples_markdown": "\n".join(rows) if len(local_wl) else "No samples."}


def _user_prompt(record, z: float, mode: str, components: list[dict],
                 metrics: dict, window: dict) -> str:
    summaries = []
    for label, item in zip(("a", "b"), components):
        summaries.append(
            f"- {label}: {item['line_name']} (`{item['line_id']}`), expected "
            f"{item['expected_obs_angstrom']:.6f} Å, SH={item['sh_status']}, "
            f"measurement={item['measurement_id'] or 'none'}, "
            f"measured center={item['measured_center_angstrom']}, "
            f"offset from prediction={item['measured_offset_from_expected_angstrom']} Å, "
            f"amplitude={item['amplitude']}, single-feature FA={item['fa_state'] or 'none'}, "
            f"cleaned pairing={item['cleaned_pairing']}")
    return _render("fa_doublet_user.md", {
        "DOUBLET_NAME": record.name, "DOUBLET_ID": record.id,
        "REDSHIFT": f"{z:.8g}", "CLAIM_MODE": mode,
        "COMPONENTS": "\n".join(summaries),
        "METRICS": json.dumps(metrics, ensure_ascii=False, allow_nan=False),
        "COVERAGE": json.dumps(window["coverage"], ensure_ascii=False, allow_nan=False),
        "SAMPLES": window["samples_markdown"]}, PROMPT_DIR)


async def review_doublet(*, trace: dict, branch_id: str, hypothesis_ref: str,
                         doublet_id: str, output_root: str | Path, llm: Any,
                         agent_factory: Callable[..., Any] = create_agent,
                         concurrency: int = 3, recursion_limit: int = 30) -> dict:
    """Vote on an SH doublet claim without changing either component's FA state."""
    if concurrency < 1 or recursion_limit < 1:
        raise ValueError("concurrency and recursion limit must be positive")
    record = _record(doublet_id)
    branch = trace["branches"][branch_id]
    key = fa_doublet_key(trace["run_id"], hypothesis_ref, doublet_id)
    if (hypothesis_ref not in branch["state"]["active_pre_analysis"]
            or key in branch["state"]["analysis_results"]):
        raise ValueError("doublet needs an active, not-yet-reviewed SH hypothesis")
    root = Path(output_root).resolve()
    if trace.get("artifact_root", str(root)) != str(root):
        raise ValueError("doublet output root differs from branch artifact root")
    source_refs = [f"sh/{hypothesis_ref}/node", f"sh/{hypothesis_ref}/catalog",
                   f"sh/{hypothesis_ref}/judgments", "spectrum_npz"]
    for ref in source_refs:
        item = trace["artifacts"].get(ref)
        if item is None or _digest(Path(item["path"]).resolve(strict=True)) != item["sha256"]:
            raise ValueError(f"doublet source is missing or changed: {ref}")
    view = cleaned_line_view(trace, branch_id, hypothesis_ref)
    rows = {row["line_id"]: row for row in view["lines"]}
    if not any(rows.get(line_id, {}).get("measurement_id") for line_id in record.component_ids):
        raise ValueError("doublet review requires at least one kept SH component")
    catalog = _read_artifact(trace, f"sh/{hypothesis_ref}/catalog")
    if (catalog["run_id"] != trace["run_id"]
            or catalog["spectrum_npz_sha256"] != trace["artifacts"]["spectrum_npz"]["sha256"]):
        raise ValueError("doublet catalog differs from active spectrum")
    measurements = {item["id"]: item for item in catalog["measurements"]}
    components = [_component_payload(line_id, rows.get(line_id), measurements,
                                     view["fixed_redshift"])
                  for line_id in record.component_ids]
    mode = "complete_pair" if all(item["measurement_id"] for item in components) else "orphan"
    metrics = _numeric_metrics(record, components)
    method = load_analysis_method().audit.doublet_review
    window = build_doublet_window(trace["artifacts"]["spectrum_npz"]["path"],
                                  components=components,
                                  masked_regions=catalog.get("masked_regions", []),
                                  method=method)
    source_refs.extend(dict.fromkeys(ref for item in components
                                      for ref in item["fa_vote_artifact_refs"]))
    for ref in source_refs:
        if ref not in trace["artifacts"]:
            raise ValueError(f"doublet FA vote source is not registered: {ref}")
        if _digest(Path(trace["artifacts"][ref]["path"]).resolve(strict=True)) != trace["artifacts"][ref]["sha256"]:
            raise ValueError(f"doublet source changed: {ref}")
    user = _user_prompt(record, view["fixed_redshift"], mode, components, metrics, window)
    if window["coverage"]["assessable"]:
        batch = await collect_advisory_votes(
            trace=trace, branch_id=branch_id, node_key=key,
            output_root=root, llm=llm,
            system=(PROMPT_DIR / "fa_doublet_system.md").read_text(encoding="utf-8"),
            user=user, tool_name="submit_doublet_vote",
            stage="FA doublet review", vote_quorum=method.vote_quorum,
            max_attempts=method.max_attempts_per_vote_seat,
            concurrency=concurrency, recursion_limit=recursion_limit,
            agent_factory=agent_factory, artifact_namespace="fa_doublet")
    else:
        batch = {"ballots": [], "attempt_refs": [], "model_usage": summarize_usage([]),
                 "prompt_identity": None}
    ballots = batch["ballots"]
    tally = vote_tally(ballots, method.vote_quorum, window["coverage"]["assessable"])
    node = {"schema_version": SCHEMA, "node_type": "fa.doublet_review",
            "node_key": key, "run_id": trace["run_id"], "branch_id": branch_id,
            "hypothesis_ref": hypothesis_ref, "doublet_id": doublet_id,
            "claim_mode": mode, "components": components, "metrics": metrics,
            "coverage": window["coverage"], "status": tally["status"],
            "pair_supported": tally["positive"],
            "consultative_only": True, "method_snapshot": method.model_dump(mode="json"),
            "vote_summary": tally["vote_summary"], "ballots": ballots,
            "successful_votes": tally["successful_votes"],
            "required_votes": tally["required_votes"],
            "failed_seats": tally["failed_seats"],
            "model_usage": batch["model_usage"],
            "prompt_identity": batch["prompt_identity"],
            "source_refs": source_refs, "attempt_refs": batch["attempt_refs"]}
    allocation = allocate_execution(root, run_id=trace["run_id"],
                                    branch_id=branch_id, node_key=key)
    node["node_execution_id"] = allocation.node_execution_id
    allocation.path("node.json").write_text(
        json.dumps(node, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8")
    register_execution(trace, allocation)
    node_ref = f"fa_doublet/{allocation.node_execution_id}/node"
    register_artifact(trace, node_ref, allocation.path("node.json"), "fa_doublet_node",
                      node_execution_id=allocation.node_execution_id)
    record_analysis(trace, branch_id, kind="analysis_result", analysis_ref=key,
                    artifact_refs=[node_ref, *source_refs, *batch["attempt_refs"]],
                    node_execution_id=allocation.node_execution_id)
    return {"node": node, "node_ref": node_ref, "model_usage": node["model_usage"]}


def read_doublet_information(trace: dict, *, branch_id: str, hypothesis_ref: str,
                             doublet_id: str) -> dict | None:
    """Read a reachable branch result for later HS/RA; no implicit gate."""
    key = fa_doublet_key(trace["run_id"], hypothesis_ref, doublet_id)
    if key not in trace["branches"][branch_id]["state"]["analysis_results"]:
        return None
    current, cutoff = branch_id, None
    while True:
        branch = trace["branches"][current]
        events = branch["events"]
        if cutoff is not None:
            indices = [i for i, event in enumerate(events) if event["event_id"] == cutoff]
            if len(indices) != 1:
                raise ValueError("doublet fork point is absent from parent")
            events = events[:indices[0] + 1]
        event = next((event for event in reversed(events)
                      if event["kind"] == "analysis_result"
                      and event["payload"]["analysis_ref"] == key), None)
        if event is not None:
            break
        current, cutoff = branch["parent_branch_id"], branch["fork_event_id"]
        if current is None:
            raise ValueError("active doublet result has no reachable event")
    matches = [(ref, trace["artifacts"][ref]) for ref in event["artifact_refs"]
               if trace["artifacts"][ref]["kind"] == "fa_doublet_node"]
    if len(matches) != 1:
        raise ValueError("doublet event must cite one result node")
    ref, item = matches[0]
    path = Path(item["path"]).resolve(strict=True)
    if _digest(path) != item["sha256"]:
        raise ValueError("doublet result changed since registration")
    node = json.loads(path.read_text(encoding="utf-8"))
    if (node.get("schema_version") != SCHEMA or node.get("node_key") != key
            or node.get("hypothesis_ref") != hypothesis_ref
            or node.get("doublet_id") != doublet_id
            or node.get("consultative_only") is not True):
        raise ValueError("doublet result contract differs from active claim")
    for source_ref in node["source_refs"]:
        source = trace["artifacts"].get(source_ref)
        if source is None or _digest(Path(source["path"]).resolve(strict=True)) != source["sha256"]:
            raise ValueError(f"doublet result source changed: {source_ref}")
    return {"node_ref": ref, "status": node["status"],
            "pair_supported": node["pair_supported"],
            "claim_mode": node["claim_mode"], "components": node["components"],
            "metrics": node["metrics"], "coverage": node["coverage"],
            "vote_summary": node["vote_summary"], "ballots": node["ballots"],
            "consultative_only": True}
