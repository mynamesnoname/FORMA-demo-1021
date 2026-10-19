"""Deterministic, hypothesis-local fits for predicted lines without nearby CWT data."""

from __future__ import annotations

import math

import numpy as np

from FORMA.core.reasoning.fuzzy import initial_predicates
from FORMA.core.reasoning.ontology.query import build_width3sigma_map
from .sh_provenance import blended_labels_for_pair
from .tools import (
    ABSORPTION_LINES, EMISSION_LINES, EMISSION_LINE_WIDTHS,
    _do_fit_doublet, _do_fit_peak,
)


def _local_cwt_candidate(features: list, rest: float, predicted: float,
                         z_min: float, z_max: float, offset_limit: float) -> bool:
    for feature in features:
        center = feature.get("wavelength")
        if not isinstance(center, (int, float)) or not math.isfinite(center):
            continue
        if abs(center - predicted) <= offset_limit and z_min <= center / rest - 1 <= z_max:
            return True
    return False


def _fit_status(result: dict, *, pair: bool = False) -> str:
    if pair:
        has_center = any(isinstance(result.get(key), dict) and
                         isinstance(result[key].get("center"), (int, float)) and
                         math.isfinite(result[key]["center"])
                         for key in ("component_1", "component_2"))
    else:
        has_center = (isinstance(result.get("center"), (int, float))
                      and math.isfinite(result["center"]))
    if not has_center:
        return "failed"
    separation = result.get("separation_check")
    if result.get("flags") or (isinstance(separation, dict) and separation.get("match") is False):
        return "warning"
    return "ok"


def run_sh_prefit(wavelength, flux, redshift: float, peaks: list, troughs: list,
                  z_min: float, z_max: float, masked_regions: list | None,
                  observable_doublets: list) -> tuple[list[dict], list[dict]]:
    """Fit each uncovered local target once; return attempts and candidate measurements.

    A successful optimizer result is exposed as a measurement candidate, not a
    line identification. Only results with finite fitted centres can be adopted
    later through ``prepare_sh_lines``.
    """
    wl = np.asarray(wavelength)
    fl = np.asarray(flux)
    if wl.size == 0 or wl.shape != fl.shape:
        return [], []
    bounds = next(p.membership.parameters for p in initial_predicates()
                  if p.membership.id == "membership:offset-quality")
    offset_limit = float(bounds["right"])
    widths = build_width3sigma_map()
    from FORMA.core.config.analysis_method import load_analysis_method
    center_bound = load_analysis_method().gaussian_fit.center_bound_half_angstrom
    ranges = [(float(a), float(b)) for a, b in (masked_regions or [])]
    lines = {name: (rest, "emission", peaks)
             for name, rest in EMISSION_LINES.items()}
    lines.update({name: (rest, "absorption", troughs)
                  for name, rest in ABSORPTION_LINES.items()})

    def eligible(name: str) -> bool:
        rest, _, features = lines[name]
        predicted = rest * (1 + redshift)
        return (float(wl[0]) <= predicted <= float(wl[-1])
                and not any(a <= predicted <= b for a, b in ranges)
                and not _local_cwt_candidate(features, rest, predicted,
                                             z_min, z_max, offset_limit))

    attempts: list[dict] = []
    measurements: list[dict] = []
    handled: set[str] = set()
    for pair, first, second, positions in observable_doublets:
        names = (first.name, second.name)
        if any(name not in lines or name in handled for name in names):
            continue
        if not all(float(wl[0]) <= pos <= float(wl[-1]) and
                   not any(a <= pos <= b for a, b in ranges)
                   for pos in positions):
            continue
        if not any(eligible(name) for name in names):
            continue
        kind = "absorption" if first.line_type == "absorption" else "emission"
        try:
            result = _do_fit_doublet(
                wl, fl, *positions, kind, widths[pair.fit_width_class],
                separation_expected_obs=abs(positions[1] - positions[0]),
                amp_ratio_expected=pair.amplitude_ratio,
            )
        except Exception as exc:
            result = {"component_1": None, "component_2": None,
                      "flags": ["fit_failed"],
                      "message": f"{type(exc).__name__}: {exc}"}
        attempts.append({"target": "/".join(names), "method": "fit_doublet",
                         "predicted_obs": list(positions), "result": result,
                         "status": _fit_status(result, pair=True)})
        for target_name, component in zip(names, (result.get("component_1"),
                                                   result.get("component_2"))):
            if (isinstance(component, dict)
                    and isinstance(component.get("center"), (int, float))
                    and math.isfinite(component["center"])):
                measurements.append({"source": "fit_doublet", "kind": kind,
                                     "target_line": target_name, **component})
        handled.update(names)
        # A resolved pair and its blended label describe the same feature.
        handled.update(blended_labels_for_pair(first, second) & lines.keys())

    for name, (rest, kind, _) in lines.items():
        if name in handled or not eligible(name):
            continue
        predicted = rest * (1 + redshift)
        width_class = (EMISSION_LINE_WIDTHS.get(name, "narrow")
                       if kind == "emission" else "absorption")
        try:
            result = _do_fit_peak(wl, fl, predicted, widths[width_class], kind)
        except Exception as exc:
            result = {"center": None, "flags": ["fit_failed"],
                      "message": f"{type(exc).__name__}: {exc}"}
        center = result.get("center")
        if (isinstance(center, (int, float)) and math.isfinite(center)
                and abs(center - predicted) >= center_bound - 0.1):
            result.setdefault("flags", []).append("center_at_bound")
        attempts.append({"target": name, "method": "fit_peak",
                         "predicted_obs": [predicted], "result": result,
                         "status": _fit_status(result)})
        if isinstance(result.get("center"), (int, float)) and math.isfinite(result["center"]):
            measurements.append({"source": "fit_peak", "kind": kind,
                                 "target_line": name, **result})
    return attempts, measurements


def render_fit_attempts(attempts: list[dict]) -> str:
    """Compact model-facing record of every executed prefit attempt."""
    rows = ["## Targeted Gaussian Fit Attempts", "",
            "Only executed fits appear here. A fit is a measurement candidate, not line confirmation.",
            "Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.", "",
            "| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |",
            "|---|---:|---|---|---:|---:|---:|---:|---|"]
    if not attempts:
        rows.append("| — | — | — | — | — | — | — | — | no fits attempted |")
    for attempt in attempts:
        result = attempt["result"]
        predicted = "/".join(f"{value:.1f}" for value in attempt["predicted_obs"])
        if attempt["method"] == "fit_doublet":
            components = [result.get("component_1"), result.get("component_2")]
        else:
            components = [result]
        def values(key: str) -> str:
            return "/".join(
                "—" if not isinstance(part, dict) or part.get(key) is None
                else str(part[key]) for part in components)
        center = "/".join(
            "—" if not isinstance(part, dict) or part.get("center") is None
            else f"{part['center']}±{part['center_err']}"
            if part.get("center_err") is not None else f"{part['center']}±—"
            for part in components)
        local_snr = result.get("local_snr")
        improvement = result.get("delta_chi2_per_n")
        flags = ", ".join(result.get("flags") or [])
        status = attempt["status"] + (f": {flags}" if flags else "")
        if attempt["status"] == "failed" and result.get("message"):
            status += f" ({result['message']})"
        if result.get("separation_check"):
            status += ("; separation " +
                       ("pass" if result["separation_check"].get("match") else "fail"))
        if result.get("amp_ratio_check"):
            ratio = result["amp_ratio_check"].get("observed_ratio")
            status += f"; component ratio {ratio if ratio is not None else '—'}"
        rows.append(
            f"| {attempt['target']} | {predicted} | {attempt['method']} | {center} | "
            f"{values('amplitude')} | {values('fwhm_km_s')} | "
            f"{local_snr if local_snr is not None else '—'} | "
            f"{improvement if improvement is not None else '—'} | {status} |"
        )
    return "\n".join(rows) + "\n"
