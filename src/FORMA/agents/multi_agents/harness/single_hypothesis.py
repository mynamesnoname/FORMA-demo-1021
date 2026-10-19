"""
single_hypothesis.py — Redrock line verification harness.

Builds CWT and predicted-line context, fits locally CWT-absent predictions
before the model call, then lets the LLM judge the observations and use tools
for unresolved questions.

Usage as module:
    from harness import run
    result = run(fits_path="/data/spectrum.fits", redshift=2.3,
                 npz_path="/data/spectrum.npz")
    print(result["report"])
    print(result["feature_catalog"])

Usage as CLI:
    python single_hypothesis.py /data/spectrum.fits 2.3 --npz /data/spectrum.npz
"""

import json
import math
import os
import re
import time
import asyncio
import logging
from FORMA.core.config.model_calls import temperature_for
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from langchain.agents import create_agent
from langchain_core.tools import tool

from FORMA.core.llm import _detect_vendor, _build_thinking_extra_body, _create_chat_openai
from .tools import (
    write_report, write_lines_csv as _write_lines_csv_core,
    _do_fit_peak, _do_fit_doublet,
    EMISSION_LINES, ABSORPTION_LINES, EMISSION_LINE_WIDTHS,
)
from .sh_provenance import prepare_sh_lines, validate_sh_catalog
from .sh_prefit import run_sh_prefit, render_fit_attempts

# ---------------------------------------------------------------------------
# Retry configuration
# ---------------------------------------------------------------------------

_HTTP_RETRIES = int(os.environ.get("MAX_TRIES", 3))
_HTTP_DELAYS = [2, 5, 10, 15, 20][:_HTTP_RETRIES]

_RETRYABLE_KW = (
    "429", "rate limit", "too many requests",
    "503", "502", "500", "server error", "service unavailable",
    "timeout", "connection", "reset", "refused", "eof", "broken pipe",
)


def _is_retryable(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(kw in msg for kw in _RETRYABLE_KW)


def _resolve_max_tokens() -> int | None:
    """Resolve max_tokens from env ``LLM_MAX_TOKENS``.

    When the env var is empty / unset and the provider is DeepSeek, we default
    to the maximum supported value (65 536) to minimise output truncation
    that causes "insufficient tool messages following tool_calls" errors.
    """
    env_val = os.environ.get("LLM_MAX_TOKENS", "").strip()
    if env_val:
        try:
            return int(env_val)
        except ValueError:
            pass
    base_url = os.environ.get("LLM_BASE_URL", "")
    if "deepseek" in base_url.lower():
        return 65536
    return None


from .continuation import (
    _format_tool_call, _format_tool_result,
    run_continuation_streaming, run_continuation_ainvoke,
    run_continuation_invoke,
)


# ---------------------------------------------------------------------------
# Skill prompt
# ---------------------------------------------------------------------------

SKILL_DIR = Path(__file__).resolve().parent / "skills" / "HypothesisAnalyst"
_SKILL_FILE = "single_hypothesis_redrock_skill.md"


def _load_skill() -> str:
    skill_path = SKILL_DIR / _SKILL_FILE
    with open(skill_path) as f:
        return f.read()


# ---------------------------------------------------------------------------
# Tool list
# ---------------------------------------------------------------------------

def _observable_doublets(redshift: float, wavelength_min: float, wavelength_max: float):
    """Return registry pairs whose nominal components are both in coverage."""
    from FORMA.core.reasoning.ontology.registry import ONTOLOGY

    line_by_id = ONTOLOGY.line_index()
    for pair in ONTOLOGY.doublets:
        first, second = (line_by_id[item] for item in pair.component_ids)
        positions = (first.rest_wavelength * (1 + redshift),
                     second.rest_wavelength * (1 + redshift))
        if any(position < wavelength_min or position > wavelength_max
               for position in positions):
            continue
        yield pair, first, second, positions


def _build_tools(npz_path: str, redshift: float, *,
                 peaks: list | None = None, troughs: list | None = None,
                 prefit_measurements: list | None = None,
                 masked_regions: list | None = None,
                 strict_catalog: bool = False) -> list:
    """Redrock verification tools; fitting reads the cleaned NPZ via closure."""
    data = np.load(npz_path)
    _wl = data["wavelength"]
    _fl = data["flux"]
    observable_doublets = list(_observable_doublets(
        redshift, float(np.min(_wl)), float(np.max(_wl))))
    fit_measurements = list(prefit_measurements or [])

    @tool("write_lines_csv")
    def _write_sh_lines_csv(file_path: str, lines: list) -> dict:
        """Write the SH catalog using this run's CWT features and fit results.

        Send all predicted lines. The writer corrects measurement provenance and
        values when they can be resolved, and reports the corrections. If a
        centre matches no trusted measurement, repair it and resend all rows.
        """
        if strict_catalog:
            schema_errors = validate_sh_catalog(
                lines, redshift, float(np.min(_wl)), float(np.max(_wl)),
                masked_regions,
            )
            if schema_errors:
                return {"path": None, "n_lines": 0,
                        "flags": ["invalid_sh_catalog"],
                        "rows_to_repair": schema_errors,
                        "message": "Nothing was written. Repair the listed rows and resend the complete catalog."}
        prepared, corrections, errors = prepare_sh_lines(
            lines, peaks or [], troughs or [], fit_measurements)
        if errors:
            return {"path": None, "n_lines": 0,
                    "flags": ["unresolved_measurement_source"],
                    "rows_to_repair": errors,
                    "message": "Nothing was written. Correct these measurements and resend all rows."}
        result = _write_lines_csv_core.func(file_path=file_path, lines=prepared)
        if corrections:
            result["provenance_corrections"] = corrections
        return result

    @tool
    def _fit_peak(
            center_guess: float,
            width_3sigma: float,
            line_type: str = "emission",
            window_half: float | None = None,
        ) -> dict:
            """Fit a single Gaussian + linear baseline around a predicted line.

            Parameters
            ----------
            center_guess : float
                λ_obs from the Predicted Lines table (Å).
            width_3sigma : float
                Choose the class-specific 3σ width supplied in the user message.
            line_type : "emission" or "absorption".
            window_half : float
                Half-width of fitting window (method profile if omitted).
            """
            result = _do_fit_peak(_wl, _fl, center_guess, width_3sigma, line_type, window_half)
            if isinstance(result.get("center"), (int, float)) and math.isfinite(result["center"]):
                fit_measurements.append({"source": "fit_peak", "kind": line_type, **result})
            return result

    @tool
    def _fit_doublet(
            center_guess_1: float,
            center_guess_2: float,
            line_type: str = "emission",
            width_3sigma: float | None = None,
            window_half: float | None = None,
            separation_expected_obs: float = None,
            separation_tolerance: float | None = None,
            amp_ratio_expected: float = None,
        ) -> dict:
            """Fit a *registered* doublet with two Gaussians + linear baseline.

            Use only a complete pair listed under Observable doublets in the
            user message. Its expected separation is a registry prediction,
            never the distance between two observed CWT peaks. The method
            profile owns the separation tolerance; an input value cannot widen it.
            """
            from FORMA.core.reasoning.fuzzy import initial_predicates
            from FORMA.core.config.analysis_method import load_analysis_method
            offset = next(p.membership.parameters for p in initial_predicates()
                          if p.membership.id == "membership:offset-quality")
            max_offset = float(offset["right"])
            configured_tolerance = load_analysis_method().gaussian_fit.doublet_separation_tolerance_angstrom
            for pair, first, second, positions in observable_doublets:
                expected_sep = abs(positions[1] - positions[0])
                if (first.line_type not in (line_type, "both")
                    or second.line_type not in (line_type, "both")
                    or abs(center_guess_1 - positions[0]) > max_offset
                    or abs(center_guess_2 - positions[1]) > max_offset
                    or abs(abs(center_guess_2 - center_guess_1) - expected_sep) > configured_tolerance
                    or separation_expected_obs is None
                    or abs(separation_expected_obs - expected_sep) > 0.1
                    or (amp_ratio_expected is not None and
                        (pair.amplitude_ratio is None or
                         abs(amp_ratio_expected - pair.amplitude_ratio) > 0.01))):
                    continue
                # A model that omits `width_3sigma` gets the matched doublet's
                # declared class rather than one hard-wired default, so the number
                # in the run message and the number the fit starts from agree.
                # 省略 `width_3sigma` 的模型会拿到所匹配双线声明的类别，而不是某个写死的
                # 默认值，使运行消息里的数字与拟合起点一致。
                resolved_width = (width_3sigma if width_3sigma is not None
                                  else build_width3sigma_map()[pair.fit_width_class])
                result = _do_fit_doublet(
                    _wl, _fl, center_guess_1, center_guess_2,
                    line_type, resolved_width, window_half,
                    expected_sep, configured_tolerance, pair.amplitude_ratio)
                for target_name, component in ((first.name, result.get("component_1")),
                                               (second.name, result.get("component_2"))):
                    if isinstance(component, dict) and isinstance(component.get("center"), (int, float)):
                        fit_measurements.append({"source": "fit_doublet", "kind": line_type,
                                                 "target_line": target_name, **component})
                return result
            return {
                "component_1": None, "component_2": None,
                "flags": ["unregistered_doublet"],
                "message": (
                    "Fit rejected: no complete registered doublet matches the "
                    "component positions, line type, and ontology separation. "
                    "Do not infer a doublet separation from CWT peak spacing."
                ),
            }

    return [
        write_report, _write_sh_lines_csv,
        _fit_peak, _fit_doublet,
    ]


# ---------------------------------------------------------------------------
# JSON extraction from LLM response
# ---------------------------------------------------------------------------

def _extract_json_block(text: str) -> Optional[Dict[str, Any]]:
    """Extract the final JSON block from the LLM report."""
    # Try ```json ... ``` fence
    m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    # Try bare { ... } block at end
    m = re.search(r"\{[^{}]*\"consensus_redshift\"[^{}]*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    return None


# ---------------------------------------------------------------------------
# Feature catalog
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _mask_overlap_label(
    lo: float, hi: float, obs_wl: float, masked_regions: list | None,
) -> str:
    """Return a label describing how the z-window [lo, hi] overlaps with masked regions.

    Returns empty string if no overlap. Otherwise a concise label:
      - ``[fully masked]`` — entire z-window falls in masked region(s)
      - ``[λ_pred masked]`` — nominal λ_pred is masked but part of window is clean
      - ``[window partially masked]`` — part of window overlaps mask, λ_pred is clean
    """
    if not masked_regions:
        return ""
    # A masked pair of endpoints does not prove that the interval between
    # them is masked. Advance across the union of closed mask intervals.
    covered_until = lo
    fully_masked = False
    for m_lo, m_hi in sorted(masked_regions):
        if m_hi < covered_until:
            continue
        if m_lo > covered_until:
            break
        covered_until = max(covered_until, m_hi)
        if covered_until >= hi:
            fully_masked = True
            break
    obs_masked = any(m_lo <= obs_wl <= m_hi for m_lo, m_hi in masked_regions)
    any_overlap = any(
        lo <= m_hi and hi >= m_lo for m_lo, m_hi in masked_regions
    )
    if not any_overlap:
        return ""
    if fully_masked:
        return " [fully masked]"
    if obs_masked:
        return " [λ_pred masked]"
    return " [window partially masked]"


def _find_nearby_features(
    rest_wl: float, obs_wl: float, z_min: float, z_max: float,
    peaks: list, troughs: list,
) -> str:
    """Find peaks/troughs whose wavelength falls within the z-verification window
    for a given rest-frame line:  [λ_rest×(1+z_min), λ_rest×(1+z_max)].

    Results are sorted by distance to ``obs_wl`` (closest first).

    Returns brief refs like ``peak@5001.2±0.3(z=0.0085)`` — full feature details
    are in the CWT Features table above the predictions section.
    """
    lo = rest_wl * (1.0 + z_min)
    hi = rest_wl * (1.0 + z_max)
    nearby = []
    for p in (peaks or []):
        pw = p.get('wavelength', 0)
        if lo <= pw <= hi:
            pw_err = p.get('wavelength_err')
            z_implied = pw / rest_wl - 1.0
            err_str = f"±{pw_err:.1f}" if isinstance(pw_err, (int, float)) else ""
            nearby.append((abs(pw - obs_wl), f"peak@{pw:.1f}{err_str}(z={z_implied:.4f})"))
    for t in (troughs or []):
        tw = t.get('wavelength', 0)
        if lo <= tw <= hi:
            tw_err = t.get('wavelength_err')
            z_implied = tw / rest_wl - 1.0
            err_str = f"±{tw_err:.1f}" if isinstance(tw_err, (int, float)) else ""
            nearby.append((abs(tw - obs_wl), f"trough@{tw:.1f}{err_str}(z={z_implied:.4f})"))
    nearby.sort(key=lambda x: x[0])
    return ", ".join(n[1] for n in nearby) if nearby else "—"


def _build_cwt_features_table(peaks: list, troughs: list) -> str:
    """Build a compact table of all CWT-detected features — printed once, above
    the predicted-lines table.  The per-line ``Nearby Features`` column only
    references wavelengths so the LLM can cross-reference this table for
    FWHM / ridge / SNR details."""
    lines = ["## CWT Detected Features\n"]
    col = "| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |"
    sep = "|-------|-----------|-----|----------|-------------|-------|-----|"

    def _row(f: dict) -> str:
        wl = f.get('wavelength', 0)
        wl_err = f.get('wavelength_err', None)
        amp = f.get('amplitude', 0)
        fwhm_a = f.get('FWHM_A', None)
        fwhm_k = f.get('FWHM_km_s', None)
        ridge = f.get('ridge_length', None)
        snr = f.get('snr', None)
        return (
            f"| {wl:.1f} | "
            f"{f'{wl_err:.1f}' if isinstance(wl_err, (int, float)) else '—'} | "
            f"{amp:.1f} | "
            f"{f'{fwhm_a:.1f}' if isinstance(fwhm_a, (int, float)) else '—'} | "
            f"{f'{fwhm_k:.0f}' if isinstance(fwhm_k, (int, float)) else '—'} | "
            f"{f'{ridge}' if isinstance(ridge, (int, float)) else '—'} | "
            f"{f'{snr:.1f}' if isinstance(snr, (int, float)) else '—'} |"
        )

    if peaks:
        lines.append(f"### Emission (peaks) — {len(peaks)} features\n")
        lines.append(col)
        lines.append(sep)
        for p in peaks:
            lines.append(_row(p))
        lines.append("")

    if troughs:
        lines.append(f"### Absorption (troughs) — {len(troughs)} features\n")
        lines.append(col)
        lines.append(sep)
        for t in troughs:
            lines.append(_row(t))
        lines.append("")

    return "\n".join(lines)


def _build_predictions_section(
    redshift: float,
    z_min: float,
    z_max: float,
    wl_min: float,
    wl_max: float,
    peaks: list,
    troughs: list,
    masked_regions: list | None = None,
    authority=None,
) -> str:
    """Pre-compute predicted lines and cross-reference with detected features
    using the z-verification window for each line.

    Always shows nearby CWT features. Mask overlap annotations are appended to
    the features column when the z-window wavelength range overlaps a masked
    region: ``[fully masked]``, ``[λ_pred masked]``, or ``[window partially masked]``.
    """
    rows = []
    from FORMA.core.reasoning.ontology.registry import ONTOLOGY
    registry_lines = {line.name: line for line in ONTOLOGY.lines}

    for name, rest_wl in EMISSION_LINES.items():
        obs_wl = rest_wl * (1.0 + redshift)
        if wl_min is not None and obs_wl < wl_min:
            continue
        if wl_max is not None and obs_wl > wl_max:
            continue
        lo = rest_wl * (1.0 + z_min)
        hi = rest_wl * (1.0 + z_max)
        features = _find_nearby_features(rest_wl, obs_wl, z_min, z_max, peaks, [])
        mask_note = _mask_overlap_label(lo, hi, obs_wl, masked_regions)
        if authority is not None and name in registry_lines:
            authority.value(rest_wl, slot=f"predicted_line.em.{name}.rest_wavelength",
                            owner=f"{registry_lines[name].id}#rest_wavelength")
        rows.append((
            obs_wl,
            f"| {name} | {rest_wl:.1f} | {obs_wl:.1f} | em | "
            f"{EMISSION_LINE_WIDTHS.get(name, 'narrow')} | {features}{mask_note} |",
        ))

    for name, rest_wl in ABSORPTION_LINES.items():
        obs_wl = rest_wl * (1.0 + redshift)
        if wl_min is not None and obs_wl < wl_min:
            continue
        if wl_max is not None and obs_wl > wl_max:
            continue
        lo = rest_wl * (1.0 + z_min)
        hi = rest_wl * (1.0 + z_max)
        features = _find_nearby_features(rest_wl, obs_wl, z_min, z_max, [], troughs)
        mask_note = _mask_overlap_label(lo, hi, obs_wl, masked_regions)
        if authority is not None and name in registry_lines:
            authority.value(rest_wl, slot=f"predicted_line.abs.{name}.rest_wavelength",
                            owner=f"{registry_lines[name].id}#rest_wavelength")
        rows.append((
            obs_wl,
            f"| {name} | {rest_wl:.1f} | {obs_wl:.1f} | abs | "
            f"absorption | {features}{mask_note} |",
        ))

    if not rows:
        return "\n## Predicted Lines\n\n(No predicted lines fall within the observed wavelength range.)\n"

    rows.sort(key=lambda r: r[0])

    header = (
        "| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features "
        "(ref@λ(z); cross-ref CWT table above for details) |\n"
        "|------|-----------|----------|------|-------|----------------------------------------------------------|"
    )
    return "\n## Predicted Lines at z = {:.4f}\n\n{}\n{}\n".format(
        redshift, header, "\n".join(r[1] for r in rows)
    )


def _build_user_message(
    redshift: float,
    fits_path: str,
    npz_path: str,
    *,
    wavelength_min: float = None,
    wavelength_max: float = None,
    snr_median: float = None,
    peaks: list = None,
    troughs: list = None,
    z_min: float = None,
    z_max: float = None,
    masked_regions: list = None,
    report_path: str = None,
    csv_path: str = None,
    authority=None,
    fit_attempts: list | None = None,
    pre_analysis: bool = False,
) -> str:
    # Use the same configured redshift tolerance as the evaluation and VI catalog.
    from FORMA.core.config.analysis_method import load_analysis_method

    _half_window = load_analysis_method().evaluation.redshift_tolerance
    _z_min = z_min if z_min is not None else round(redshift - _half_window, 4)
    _z_max = z_max if z_max is not None else round(redshift + _half_window, 4)

    _peaks = list(peaks or [])
    _troughs = list(troughs or [])

    # ── Spectrum summary (replaces load_spectrum tool call) ──
    spec_lines = [
        f"| Wavelength range | {wavelength_min:.1f} – {wavelength_max:.1f} Å |"
        if wavelength_min is not None and wavelength_max is not None
        else "| Wavelength range | (not provided) |",
    ]
    if snr_median is not None:
        spec_lines.append(f"| Median SNR | {snr_median:.1f} |")

    _masked_msg = ""
    if masked_regions:
        regions_desc = ", ".join(f"[{s:.1f}, {e:.1f}]" for s, e in masked_regions)
        spec_lines.append(f"| Masked regions | {regions_desc} |")
        _masked_msg = (
            f"\nThese regions were removed due to arm overlap or quality cuts. "
            f"The spectrum has NO data in these ranges. "
            f"In the Predicted Lines table, mask overlap is noted in [brackets]:\n"
            f"  - ``[fully masked]`` — entire z-window has no data → assign MASKED\n"
            f"  - ``[λ_pred masked]`` — nominal position masked, but CWT features may\n"
            f"    still exist in the clean part of the z-window → evaluate as usual\n"
            f"  - ``[window partially masked]`` — part of z-window overlapped → flag\n"
            f"    as caution, but evaluate available features normally\n"
        )

    spectrum_summary = (
        "## Spectrum Summary\n\n"
        + "\n".join(spec_lines)
        + "\n"
    )

    predictions_section = _build_predictions_section(
        redshift, _z_min, _z_max, wavelength_min, wavelength_max, _peaks, _troughs,
        masked_regions=masked_regions, authority=authority,
    )

    cwt_table = _build_cwt_features_table(_peaks, _troughs)

    # Only inject facts relevant to this spectrum, rendered from their owners.
    from FORMA.core.reasoning.ontology.registry import ONTOLOGY
    from FORMA.core.reasoning.fuzzy import initial_predicates
    line_by_id = ONTOLOGY.line_index()
    listed_names = {
        name
        for name, rest_wavelength in (*EMISSION_LINES.items(), *ABSORPTION_LINES.items())
        if (wavelength_min is None or rest_wavelength * (1 + redshift) >= wavelength_min)
        and (wavelength_max is None or rest_wavelength * (1 + redshift) <= wavelength_max)
    }
    eligible_anchors = sorted(
        (line for line in ONTOLOGY.lines
         if line.name in listed_names and line.anchor_priority is not None
         and not line.excluded_from_anchor),
        key=lambda line: (line.anchor_priority, line.rest_wavelength),
    ) if not pre_analysis else []
    from FORMA.core.reasoning.ontology.query import build_width3sigma_map
    windows = build_width3sigma_map()
    from FORMA.core.config.analysis_method import load_analysis_method
    gaussian_method = load_analysis_method().gaussian_fit
    doublet_hints = []
    for pair, first, second, positions in _observable_doublets(
        redshift,
        float("-inf") if wavelength_min is None else wavelength_min,
        float("inf") if wavelength_max is None else wavelength_max,
    ):
        # Declared per doublet in the registry (`DoubletRecord.fit_width_class`),
        # not branched on the doublet id here: `doublet:cahk` states `absorption`
        # because its own component lines declare `width_class="absorption"`.
        # 按双线在注册表中声明（`DoubletRecord.fit_width_class`），而不是在此按 id 分支：
        # `doublet:cahk` 声明 `absorption`，因为它的分量线自身声明 `width_class="absorption"`。
        window_class = pair.fit_width_class
        doublet_hints.append(
            f"- {pair.id}: {first.name}/{second.name} "
            f"({first.rest_wavelength:g}/{second.rest_wavelength:g} Å): "
            f"width_3sigma={windows[window_class]:g}, "
            f"separation_expected_obs={abs(positions[1] - positions[0]):g}, "
            f"rest_separation={pair.rest_separation:g}; "
            + (f"amp_ratio_expected={pair.amplitude_ratio:g} (component 2 / component 1); "
               if pair.amplitude_ratio is not None else "")
            + f"amplitude relation: {pair.amplitude_ratio_note or 'unconstrained'}"
        )
    # Resolved per call so a configured payload reaches the rendered message.
    # 每次调用重新解析，使配置载荷能进入渲染出的消息。
    predicates = initial_predicates()
    offset = next(p.membership.parameters for p in predicates
                  if p.membership.id == "membership:offset-quality")
    snr = next(p.membership.parameters for p in predicates
               if p.membership.id == "membership:detection-snr")
    broad_rule = next(r for r in ONTOLOGY.formal_rules
                      if r.id == "rule:formal-qso-broad-width")
    from FORMA.core.reasoning.ontology.rule_parameters import (
        effective_operand_threshold, effective_parameter,
    )
    broad_width = effective_operand_threshold(
        broad_rule.id, "fwhm_kms"
    )["value"]
    edge_rules = {r.id: r for r in ONTOLOGY.formal_rules}
    blue_edge = effective_operand_threshold(
        "rule:formal-blue-edge-risk", "wavelength_obs"
    )["value"]
    red_edge = effective_operand_threshold(
        "rule:formal-oh-zone-risk", "wavelength_obs"
    )["value"]
    outflow = effective_parameter(
        "parameter:outflow-blueshift-window"
    )["parameters"]
    rule_context = (
        f"\n## Relevant ontology parameters ({ONTOLOGY.schema_version})\n\n"
        f"- membership:offset-quality: strong |offset| < {offset['center_right']:g} Å; "
        f"{offset['center_right']:g}–{offset['right']:g} Å is weaker; "
        f"> {offset['right']:g} Å rejects the candidate.\n"
        f"- rule:formal-qso-broad-width: strict broad-line guide FWHM ≥ {broad_width:g} km/s; "
        "width mismatch is a caveat, not sole rejection.\n"
        f"- membership:detection-snr: SNR < {snr['low']:g} weak; "
        f"≥ {snr['high']:g} strong. Evaluate CWT ridge persistence as well.\n"
        f"- edge scrutiny: blue λ < {blue_edge:g} Å; red λ > {red_edge:g} Å.\n"
        f"- high-ionization velocity offset reference: "
        f"{outflow['low']:g} to {outflow['high']:g} km/s; diagnostic only.\n"
        + (
            "- Registry anchor candidates in nominal coverage (lower priority number preferred): "
            + (", ".join(f"{line.name}={line.anchor_priority}" for line in eligible_anchors)
               if eligible_anchors else "none")
            + ".\n"
            if not pre_analysis else ""
        )
        + "- Registry fit widths (width_3sigma Å): "
        + ", ".join(f"{key}={value:g}" for key, value in sorted(windows.items()))
        + ".\n"
        + (f"- Gaussian tool defaults: single window ±{gaussian_method.single_window_half_angstrom:g} Å, "
           f"doublet window ±{gaussian_method.doublet_window_half_angstrom:g} Å, "
           f"doublet separation tolerance {gaussian_method.doublet_separation_tolerance_angstrom:g} Å; "
           "these are fitting method settings, not line detection significance thresholds.\n")
        + ("- Observable doublets:\n" + "\n".join(doublet_hints) + "\n"
           if doublet_hints else "- No complete registered doublet is in nominal coverage.\n")
    )

    if authority is not None:
        for line in eligible_anchors:
            authority.value(line.anchor_priority,
                            slot=f"anchor_priority.{line.id}",
                            owner=f"{line.id}#anchor_priority")
        for pair, first, second, _ in _observable_doublets(
            redshift,
            float("-inf") if wavelength_min is None else wavelength_min,
            float("inf") if wavelength_max is None else wavelength_max,
        ):
            for line in (first, second):
                authority.value(line.rest_wavelength,
                                slot=f"doublet.{pair.id}.{line.id}.rest_wavelength",
                                owner=f"{line.id}#rest_wavelength")
            authority.value(pair.rest_separation,
                            slot=f"doublet.{pair.id}.rest_separation",
                            owner=f"{pair.id}#rest_separation")
            if pair.amplitude_ratio is not None:
                authority.value(pair.amplitude_ratio,
                                slot=f"doublet.{pair.id}.amplitude_ratio",
                                owner=f"{pair.id}#amplitude_ratio")
        for field in ("center_right", "right"):
            authority.value(offset[field], slot=f"offset_quality.{field}",
                            owner=f"membership:offset-quality#{field}")
        for field in ("low", "high"):
            authority.value(snr[field], slot=f"detection_snr.{field}",
                            owner=f"membership:detection-snr#{field}")
            authority.value(outflow[field], slot=f"outflow_window.{field}",
                            owner=f"parameter:outflow-blueshift-window#{field}")
        for slot, value, owner in (
            ("strict_broad_width", broad_width,
             "rule:formal-qso-broad-width:fwhm_kms"),
            ("blue_edge", blue_edge, "rule:formal-blue-edge-risk:wavelength_obs"),
            ("red_edge", red_edge, "rule:formal-oh-zone-risk:wavelength_obs"),
        ):
            authority.value(value, slot=slot, owner=owner)
        for field in ("single_window_half_angstrom", "doublet_window_half_angstrom",
                      "doublet_separation_tolerance_angstrom"):
            authority.value(getattr(gaussian_method, field), slot=f"gaussian.{field}",
                            owner=f"analysis_method.gaussian_fit.{field}")
        for width_class, width in sorted(windows.items()):
            authority.value(width, slot=f"fit_width.{width_class}",
                            owner=f"analysis_method.gaussian_fit.width_3sigma_angstrom_by_class.{width_class}")

    return (
        spectrum_summary
        + f"\nVerify the redshift hypothesis z ≈ {redshift}.\n\n"
        f"Verification window: z ∈ [{_z_min}, {_z_max}]\n"
        "A CWT feature supports the hypothesis only if the implied redshift "
        "shown beside that predicted line falls within this window.\n"
        f"Lines marked [fully masked] have NO data in the entire z-window — assign status MASKED.\n"
        f"Lines with [λ_pred masked] or [window partially masked] can still be evaluated.\n"
        + _masked_msg
        + rule_context
        + f"\nFITS file: {fits_path}\n"
        f"Cleaned spectrum: {npz_path}\n"
        + (f"Output Report file: {report_path}\n" if report_path else "")
        + (f"Output CSV file: {csv_path}\n" if csv_path else "")
        + "\n" + cwt_table + "\n"
        + predictions_section
        + "\n" + render_fit_attempts(fit_attempts or [])
        + "\nThe CWT table lists all pre-detected features with their quality metrics. "
        "The Predicted Lines table references nearby features by wavelength + implied_z — "
        "cross-reference with the CWT table for FWHM, ridge, and SNR details. "
        + ("Evaluate and adopt features per the current system prompt criteria. "
           if pre_analysis else
           "Evaluate and adopt features per the skill prompt criteria. ")
        + "The predicted-line table and ontology parameters above provide the "
        "facts needed for this hypothesis.\n"
        + "\nEvaluate every listed line before writing outputs.\n"
        + ("\nPhases: evaluate all lines → write CSV → write report → wait for the second user message."
           if pre_analysis else
           "\nPhases: evaluate all lines → write CSV → write report → JSON block.")
    )


def _prepare_prefits(npz_path: str, redshift: float, peaks: list | None,
                     troughs: list | None, z_min: float | None,
                     z_max: float | None, masked_regions: list | None,
                     artifact_path: str | None = None) -> tuple[list[dict], list[dict]]:
    """Run targeted fits before model access and archive the attempted measurements."""
    from FORMA.core.config.analysis_method import load_analysis_method

    half = load_analysis_method().evaluation.redshift_tolerance
    lo = z_min if z_min is not None else round(redshift - half, 4)
    hi = z_max if z_max is not None else round(redshift + half, 4)
    with np.load(npz_path) as spectrum:
        wl = spectrum["wavelength"]
        fl = spectrum["flux"]
        pairs = list(_observable_doublets(redshift, float(wl[0]), float(wl[-1])))
        attempts, measurements = run_sh_prefit(
            wl, fl, redshift, peaks or [], troughs or [], lo, hi,
            masked_regions, pairs,
        )
    if artifact_path:
        def clean(value):
            if isinstance(value, dict):
                return {key: clean(item) for key, item in value.items()}
            if isinstance(value, (list, tuple)):
                return [clean(item) for item in value]
            if isinstance(value, np.generic):
                value = value.item()
            if isinstance(value, float) and not math.isfinite(value):
                return None
            return value
        path = Path(artifact_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(clean(attempts), ensure_ascii=False,
                                   indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return attempts, measurements


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run(
    fits_path: str,
    redshift: float,
    npz_path: str,
    *,
    mode: str = "redrock",
    hypothesis_idx: int = 0,
    wavelength_min: float = None,
    wavelength_max: float = None,
    snr_median: float = None,
    peaks: list = None,
    troughs: list = None,
    z_min: float = None,
    z_max: float = None,
    masked_regions: list = None,
    report_path: str = None,
    csv_path: str = None,
    model: str = None,
    api_key: str = None,
    base_url: str = None,
    temperature: float | None = None,
    max_turns: int = 500,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Run the LLM harness for a single redshift hypothesis.

    Parameters
    ----------
    fits_path : str
        Path to the original FITS file (for context — actual data comes from npz_path).
    redshift : float
        The central redshift hypothesis to test.
    npz_path : str
        Path to the cleaned spectrum .npz file (wavelength, flux, snr arrays).
    mode : str
        Only "redrock" is supported.
    z_min, z_max : float, optional
        Verification window. A fitted line is considered to support the
        hypothesis only if its implied redshift falls within [z_min, z_max].
        If not provided, defaults to redshift ± 0.1.
    model : str, optional
        Model name. Defaults to LLM_MODEL env var or "deepseek-v4-pro".
    api_key : str, optional
        API key. Defaults to LLM_API_KEY env var.
    base_url : str, optional
        API base URL. Defaults to LLM_BASE_URL env var.
    temperature : float
        LLM temperature (default 0.1).
    max_turns : int
        Maximum agent turns (recursion_limit). Default 500.
    verbose : bool
        If True, log intermediate messages.

    Returns
    -------
    dict with keys:
        report : str
            Full LLM text response.
        structured_output : dict or None
            Parsed JSON block from the LLM report (redshift, classification, lines, etc.).
        feature_catalog : list[dict]
            Collected tool results.
        messages : list
            Full message history (for debugging).
    """
    if mode != "redrock":
        raise ValueError(f"unsupported hypothesis mode {mode!r}; use redrock")
    model = model or os.environ.get("LLM_MODEL", "deepseek-v4-pro")
    api_key = api_key or os.environ.get("LLM_API_KEY")
    base_url = base_url or os.environ.get("LLM_BASE_URL", "https://api.deepseek.com")

    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Always disable thinking — multi-turn tool calling can't pass back reasoning_content
    _vendor = _detect_vendor(base_url)
    _extra_body = _build_thinking_extra_body("disabled", _vendor) if _vendor != "unknown" else None
    llm = _create_chat_openai(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature if temperature is not None else temperature_for("single_hypothesis"),
        max_tokens=_resolve_max_tokens(),
        extra_body=_extra_body,
    )

    system_prompt = _load_skill()

    prefit_path = (str(Path(report_path).with_name(
        Path(report_path).stem + "_prefit.json")) if report_path else None)
    fit_attempts, fit_measurements = _prepare_prefits(
        npz_path, redshift, peaks, troughs, z_min, z_max,
        masked_regions, prefit_path,
    )

    agent = create_agent(
        model=llm,
        tools=_build_tools(npz_path, redshift, peaks=peaks, troughs=troughs,
                           prefit_measurements=fit_measurements),
        system_prompt=system_prompt,
    )
    from FORMA.core.runtime.telemetry import track_agent_tools
    agent = track_agent_tools(agent)

    user_message = _build_user_message(
        redshift, fits_path, npz_path,
        wavelength_min=wavelength_min, wavelength_max=wavelength_max,
        snr_median=snr_median,
        peaks=peaks, troughs=troughs,
        z_min=z_min, z_max=z_max, masked_regions=masked_regions,
        report_path=report_path, csv_path=csv_path,
        fit_attempts=fit_attempts,
    )
    config = {"recursion_limit": max_turns}

    # ── HTTP-level retry ──────────────────────────────────────
    last_exc = None
    for attempt in range(_HTTP_RETRIES + 1):
        try:
            result = agent.invoke({"messages": [("user", user_message)]}, config=config)
            break
        except Exception as e:
            last_exc = e
            if not _is_retryable(e) or attempt >= _HTTP_RETRIES:
                raise
            delay = _HTTP_DELAYS[min(attempt, len(_HTTP_DELAYS) - 1)]
            logging.warning(f"HTTP retry {attempt + 1}/{_HTTP_RETRIES} in {delay}s: {e} / HTTP重试第{attempt + 1}/{_HTTP_RETRIES}次，等待{delay}秒：{e}")
            time.sleep(delay)
    else:
        raise last_exc

    # ── Truncation detection (shared continuation loop) ─
    messages = result.get("messages", [])
    run_continuation_invoke(
        agent,
        messages,
        config=config,
        continuation_prompt=(
            "Your previous response was truncated by the token limit. "
            "Continue EXACTLY from where you stopped. Do NOT repeat "
            "anything already written."
        ),
        log_prefix="TargetedSearch",
    )

    feature_catalog = []

    # Concatenate ALL AI messages (original + continuation if truncated)
    report = "\n".join(
        msg.content for msg in messages
        if getattr(msg, "type", None) == "ai" and hasattr(msg, "content")
    )
    structured_output = _extract_json_block(report)

    return {
        "hypothesis_idx": hypothesis_idx,
        "redshift": redshift,
        "report": report,
        "structured_output": structured_output,
        "feature_catalog": feature_catalog,
        "messages": messages,
    }


async def arun(
    fits_path: str,
    redshift: float,
    npz_path: str,
    *,
    mode: str = "redrock",
    hypothesis_idx: int = 0,
    wavelength_min: float = None,
    wavelength_max: float = None,
    snr_median: float = None,
    peaks: list = None,
    troughs: list = None,
    z_min: float = None,
    z_max: float = None,
    masked_regions: list = None,
    report_path: str = None,
    csv_path: str = None,
    model: str = None,
    api_key: str = None,
    base_url: str = None,
    temperature: float | None = None,
    max_turns: int = 100,
    verbose: bool = False,
    stream_md_path: str = None,
) -> Dict[str, Any]:
    """Run LLM harness for a single redshift hypothesis (async, optional streaming).

    Parameters
    ----------
    stream_md_path : str, optional
        If set, stream the full conversation (system prompt + every LLM turn +
        tool calls + tool results) to this .md file in real time. Parent
        directories are created if needed.
    """
    if mode != "redrock":
        raise ValueError(f"unsupported hypothesis mode {mode!r}; use redrock")
    model = model or os.environ.get("LLM_MODEL", "deepseek-v4-pro")
    api_key = api_key or os.environ.get("LLM_API_KEY")
    base_url = base_url or os.environ.get("LLM_BASE_URL", "https://api.deepseek.com")

    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Always disable thinking — multi-turn tool calling can't pass back reasoning_content
    _vendor = _detect_vendor(base_url)
    _extra_body = _build_thinking_extra_body("disabled", _vendor) if _vendor != "unknown" else None
    llm = _create_chat_openai(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature if temperature is not None else temperature_for("single_hypothesis"),
        max_tokens=_resolve_max_tokens(),
        extra_body=_extra_body,
    )

    system_prompt = _load_skill()
    prefit_path = (str(Path(stream_md_path).with_name(
        Path(stream_md_path).stem + "_prefit.json")) if stream_md_path else
        str(Path(report_path).with_name(Path(report_path).stem + "_prefit.json"))
        if report_path else None)
    fit_attempts, fit_measurements = await asyncio.to_thread(
        _prepare_prefits, npz_path, redshift, peaks, troughs, z_min, z_max,
        masked_regions, prefit_path,
    )
    agent = create_agent(model=llm, tools=_build_tools(npz_path, redshift,
                                                       peaks=peaks, troughs=troughs,
                                                       prefit_measurements=fit_measurements),
                         system_prompt=system_prompt)
    from FORMA.core.runtime.telemetry import track_agent_tools
    agent = track_agent_tools(agent)

    from FORMA.core.reasoning.ontology.prompt_authority import (
        PromptAuthority, archive_stage_prompt,
    )
    authority = PromptAuthority("single_hypothesis")
    user_message = _build_user_message(
        redshift, fits_path, npz_path,
        wavelength_min=wavelength_min, wavelength_max=wavelength_max,
        snr_median=snr_median,
        peaks=peaks, troughs=troughs,
        z_min=z_min, z_max=z_max, masked_regions=masked_regions,
        report_path=report_path, csv_path=csv_path,
        authority=authority,
        fit_attempts=fit_attempts,
    )
    archive_stage_prompt(stream_md_path, "single_hypothesis", system_prompt,
                         user_message, authority)

    # ── Streaming path ──────────────────────────────────────────
    if stream_md_path:
        os.makedirs(os.path.dirname(stream_md_path) or ".", exist_ok=True)

        config = {"recursion_limit": max_turns}

        # HTTP-level retry for the streaming call
        last_exc = None
        for attempt in range(_HTTP_RETRIES + 1):
            try:
                md = open(stream_md_path, "w", encoding="utf-8")
                md.write(f"# Hypothesis — z={redshift}\n\n")
                md.write(f"**FITS**: `{fits_path}`\n\n")
                md.write(f"**NPZ**: `{npz_path}`\n\n")
                md.write("---\n\n")
                md.write("<details>\n<summary>System Prompt</summary>\n\n")
                md.write(system_prompt)
                md.write("\n</details>\n\n---\n\n")
                md.write(f"### User\n\n{user_message}\n\n")
                if attempt > 0:
                    md.write(f"\n> ⚠ Retry attempt {attempt} after error: {last_exc}\n\n")
                md.flush()

                accumulated_messages = []
                turn = 0

                async for event in agent.astream(
                    {"messages": [("user", user_message)]},
                    config=config,
                    stream_mode="updates",
                ):
                    for _node_name, update in event.items():
                        msgs = update.get("messages", [])
                        for msg in msgs:
                            accumulated_messages.append(msg)
                            msg_type = getattr(msg, "type", None)

                            if msg_type == "ai":
                                turn += 1
                                content = msg.content if hasattr(msg, "content") else ""
                                tool_calls = getattr(msg, "tool_calls", None)
                                lines = []
                                if content:
                                    lines.append(content.strip())
                                if tool_calls:
                                    for tc in tool_calls:
                                        lines.append(_format_tool_call(tc))
                                if lines:
                                    md.write(f"### Assistant (turn {turn})\n\n")
                                    md.write("\n\n".join(lines))
                                    md.write("\n\n")
                                    md.flush()

                            elif msg_type == "tool":
                                md.write(f"### Tool Result\n\n")
                                md.write(_format_tool_result(msg))
                                md.write("\n\n")
                                md.flush()

                md.close()
                break  # success

            except Exception as e:
                last_exc = e
                try:
                    md.close()
                except Exception:
                    pass
                if not _is_retryable(e) or attempt >= _HTTP_RETRIES:
                    raise
                delay = _HTTP_DELAYS[min(attempt, len(_HTTP_DELAYS) - 1)]
                logging.warning(f"HTTP retry {attempt + 1}/{_HTTP_RETRIES} in {delay}s: {e} / HTTP重试第{attempt + 1}/{_HTTP_RETRIES}次，等待{delay}秒：{e}")
                await asyncio.sleep(delay)
        else:
            raise last_exc

        # ── Truncation detection (shared continuation loop) ─
        await run_continuation_streaming(
            agent,
            accumulated_messages,
            config=config,
            stream_md_path=stream_md_path,
            continuation_prompt=(
                "Your previous response was truncated by the token limit. "
                "Continue EXACTLY from where you stopped. Do NOT repeat "
                "anything already written. Be concise — focus on completing "
                "the remaining line evaluations and the report "
                "(sections 3a–3g)."
            ),
            log_prefix="TargetedSearch",
        )

        # Concatenate ALL AI messages (original + continuation if truncated)
        report = "\n".join(
            msg.content for msg in accumulated_messages
            if getattr(msg, "type", None) == "ai" and hasattr(msg, "content")
        )
        feature_catalog = []

        return {
            "hypothesis_idx": hypothesis_idx,
            "redshift": redshift,
            "report": report,
            "structured_output": _extract_json_block(report),
            "feature_catalog": feature_catalog,
            "messages": accumulated_messages,
        }

    # ── Non-streaming path ──────────────────────────────────────
    config = {"recursion_limit": max_turns}

    last_exc = None
    for attempt in range(_HTTP_RETRIES + 1):
        try:
            result = await agent.ainvoke({"messages": [("user", user_message)]}, config=config)
            break
        except Exception as e:
            last_exc = e
            if not _is_retryable(e) or attempt >= _HTTP_RETRIES:
                raise
            delay = _HTTP_DELAYS[min(attempt, len(_HTTP_DELAYS) - 1)]
            logging.warning(f"HTTP retry {attempt + 1}/{_HTTP_RETRIES} in {delay}s: {e} / HTTP重试第{attempt + 1}/{_HTTP_RETRIES}次，等待{delay}秒：{e}")
            await asyncio.sleep(delay)
    else:
        raise last_exc

    # ── Truncation detection (shared continuation loop) ─
    messages = result.get("messages", [])
    await run_continuation_ainvoke(
        agent,
        messages,
        config=config,
        continuation_prompt=(
            "Your previous response was truncated by the token limit. "
            "Continue EXACTLY from where you stopped. Do NOT repeat "
            "anything already written."
        ),
        log_prefix="TargetedSearch",
    )

    feature_catalog = []

    # Concatenate ALL AI messages (original + continuation if truncated)
    report = "\n".join(
        msg.content for msg in messages
        if getattr(msg, "type", None) == "ai" and hasattr(msg, "content")
    )

    return {
        "hypothesis_idx": hypothesis_idx,
        "redshift": redshift,
        "report": report,
        "structured_output": _extract_json_block(report),
        "feature_catalog": feature_catalog,
        "messages": messages,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="LLM-driven targeted line search harness")
    parser.add_argument("fits_path", help="Path to the original FITS file")
    parser.add_argument("redshift", type=float, help="Redshift hypothesis z")
    parser.add_argument("--npz", required=True, help="Path to cleaned spectrum .npz")
    parser.add_argument("--model", default=None, help="Model name override")
    parser.add_argument("--json", action="store_true", help="Output structured JSON only")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    result = run(
        fits_path=args.fits_path,
        redshift=args.redshift,
        npz_path=args.npz,
        model=args.model,
        verbose=args.verbose,
    )

    if args.json:
        output = {
            "report": result["report"],
            "structured_output": result["structured_output"],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(result["report"])


if __name__ == "__main__":
    main()
