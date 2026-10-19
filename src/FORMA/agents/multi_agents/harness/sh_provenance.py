"""Resolve single-hypothesis CSV measurements against trusted run results."""

from __future__ import annotations

from FORMA.core.constants import FWHM_TO_SIGMA
import math

from .tools import ABSORPTION_LINES, EMISSION_LINES
from FORMA.core.line_status import STATUSES

# The SH message prints CWT wavelengths to 0.1 Å. Fit results normally print
# 0.001 Å; models sometimes copy fit centres to 0.01 Å. These are copy bounds,
# not physical association tolerances.
_CWT_COPY_EPS = 0.050001
_FIT_COPY_EPS = 0.005001

SH_CSV_FIELDS = frozenset({
    "name", "rest_wavelength", "predicted_obs", "fitted_center",
    "fitted_center_err", "amplitude", "amplitude_err", "fitted_sigma",
    "fwhm_km_s", "ridge_length", "cwt_snr", "source", "implied_z", "status",
})
MEASUREMENT_FIELDS = (
    "fitted_center", "fitted_center_err", "amplitude", "amplitude_err",
    "fitted_sigma", "fwhm_km_s", "ridge_length", "cwt_snr", "source",
)


def validate_sh_catalog(
    lines: list, redshift: float, wavelength_min: float, wavelength_max: float,
    masked_regions: list | None,
) -> list[dict]:
    """Validate deterministic SH catalog facts before writing any CSV bytes.

    This cannot establish a line identity or prove an absent line was detectable.
    It checks the registry, prediction arithmetic, row state, and declared masks.
    """
    registry = {**EMISSION_LINES, **ABSORPTION_LINES}
    expected = {name for name, rest in registry.items()
                if wavelength_min <= rest * (1 + redshift) <= wavelength_max}
    errors: list[dict] = []
    if not isinstance(lines, list):
        return [{"reason": "lines must be a list"}]
    seen: set[str] = set()
    for index, row in enumerate(lines):
        if not isinstance(row, dict):
            errors.append({"row": index, "reason": "row must be an object"})
            continue
        name = row.get("name")
        if not isinstance(name, str) or name not in expected:
            errors.append({"row": index, "name": name, "reason": "unknown or out-of-coverage line"})
            continue
        if name in seen:
            errors.append({"row": index, "name": name, "reason": "duplicate line"})
        seen.add(name)
        missing = sorted(SH_CSV_FIELDS - row.keys())
        if missing:
            errors.append({"row": index, "name": name, "reason": "missing fields", "fields": missing})
            continue

        rest = registry[name]
        nominal = rest * (1 + redshift)
        for field, expected_value, tolerance in (
            ("rest_wavelength", rest, 1e-6),
            ("predicted_obs", nominal, 0.050001),
        ):
            value = row[field]
            if (isinstance(value, bool) or not isinstance(value, (int, float))
                    or not math.isfinite(value) or abs(value - expected_value) > tolerance):
                errors.append({"row": index, "name": name, "field": field,
                               "reason": "does not match registry/redshift"})
        status = row["status"]
        if not isinstance(status, str) or status not in STATUSES:
            errors.append({"row": index, "name": name, "field": "status",
                           "reason": "unknown status"})
            continue
        for field in SH_CSV_FIELDS - {"name", "rest_wavelength", "predicted_obs", "status", "source"}:
            value = row[field]
            if value is not None and (isinstance(value, bool)
                                      or not isinstance(value, (int, float))
                                      or not math.isfinite(value)):
                errors.append({"row": index, "name": name, "field": field,
                               "reason": "must be a finite number or null"})
        if row["implied_z"] is not None:
            errors.append({"row": index, "name": name, "field": "implied_z",
                           "reason": "send null; writer derives this field"})
        if status in {"NOT_FOUND", "MASKED"}:
            claimed = [field for field in MEASUREMENT_FIELDS if row[field] is not None]
            if claimed:
                errors.append({"row": index, "name": name,
                               "reason": "unadopted line cannot carry a measurement",
                               "fields": claimed})
        elif (row["fitted_center"] is None or not isinstance(row["source"], str)
              or row["source"] not in {"CWT", "fit_peak", "fit_doublet"}):
            errors.append({"row": index, "name": name,
                           "reason": "kept line needs an adopted centre and source"})
        # A broad redshift-search window overlapping a distant mask does not
        # make a clean nominal line position unobservable.
        if status == "MASKED" and not any(
            lo <= nominal <= hi for lo, hi in (masked_regions or [])
        ):
            errors.append({"row": index, "name": name,
                           "reason": "MASKED requires the nominal predicted wavelength inside a declared mask"})
    for name in sorted(expected - seen):
        errors.append({"name": name, "reason": "missing predicted line"})
    return errors


def blended_labels_for_pair(first, second) -> set[str]:
    """Find ontology lines denoting the same unresolved feature as a pair."""
    if not first.species or first.species != second.species:
        return set()
    from FORMA.core.reasoning.ontology.registry import ONTOLOGY
    low, high = sorted((first.rest_wavelength, second.rest_wavelength))
    return {line.name for line in ONTOLOGY.lines
            if line.id not in (first.id, second.id)
            and line.species == first.species
            and low <= line.rest_wavelength <= high}


def prepare_sh_lines(
    lines: list[dict], peaks: list[dict], troughs: list[dict],
    fit_measurements: list[dict],
) -> tuple[list[dict], list[dict], list[dict]]:
    """Return canonical rows, recorded corrections, and unresolved measurements.

    The agent chooses a line identity and status. The adopted measurement and
    its provenance come from the CWT catalog or a fit returned in this run.
    """
    observations = [("emission", feature) for feature in peaks]
    observations += [("absorption", feature) for feature in troughs]
    prepared, corrections, errors = [], [], []
    for row in lines:
        output = dict(row)
        name = row.get("name")
        value = row.get("fitted_center")
        if value in (None, ""):
            output.update({field: None for field in (
                "source", "fitted_center_err", "amplitude", "amplitude_err",
                "fitted_sigma", "fwhm_km_s", "ridge_length", "cwt_snr")})
        else:
            try:
                center = float(value)
            except (TypeError, ValueError):
                center = float("nan")
            if not math.isfinite(center):
                errors.append({"name": name, "reason": "invalid fitted_center"})
                continue

            if name in EMISSION_LINES:
                kind = "emission"
            elif name in ABSORPTION_LINES:
                kind = "absorption"
            else:
                errors.append({"name": name, "reason": "unknown line name"})
                continue
            cwt = [feature for feature_kind, feature in observations
                   if feature_kind == kind and
                   abs(float(feature["wavelength"]) - center) <= _CWT_COPY_EPS]
            fits = [measurement for measurement in fit_measurements
                    if measurement.get("kind") == kind and
                   measurement.get("target_line") in (None, name) and
                    abs(float(measurement["center"]) - center) <= _FIT_COPY_EPS]

            if cwt and fits:
                # Coincident measured centres cannot identify their origin on
                # their own. Honor source only when both candidates really exist.
                source = row.get("source")
                if source == "CWT":
                    fits = []
                elif source in {"fit_peak", "fit_doublet"}:
                    fits = [fit for fit in fits if fit["source"] == source]
                    if fits:
                        cwt = []
                else:
                    errors.append({"name": name, "reason": "ambiguous CWT/fit centre"})
                    continue

            if len(cwt) == 1:
                feature = cwt[0]
                output.update({
                    "source": "CWT",
                    "fitted_center": feature["wavelength"],
                    "fitted_center_err": feature.get("wavelength_err"),
                    "amplitude": feature.get("amplitude"),
                    "amplitude_err": feature.get("amplitude_err"),
                    "fitted_sigma": (
                        float(feature["FWHM_A"]) * FWHM_TO_SIGMA
                        if isinstance(feature.get("FWHM_A"), (int, float)) else None
                    ),
                    "fwhm_km_s": feature.get("FWHM_km_s"),
                    "ridge_length": feature.get("ridge_length"),
                    "cwt_snr": feature.get("snr"),
                })
            elif not cwt and fits:
                fit = min(fits, key=lambda item: abs(float(item["center"]) - center))
                output.update({
                    "source": fit["source"],
                    "fitted_center": fit["center"],
                    "fitted_center_err": fit.get("center_err"),
                    "amplitude": fit.get("amplitude"),
                    "amplitude_err": fit.get("amplitude_err"),
                    "fitted_sigma": fit.get("sigma"),
                    "fwhm_km_s": fit.get("fwhm_km_s"),
                    "ridge_length": None,
                    "cwt_snr": None,
                })
            else:
                errors.append({"name": name, "fitted_center": center,
                               "reason": "centre matches no unique CWT or fit result"})
                continue

        changed = [field for field in output if output[field] != row.get(field)]
        if changed:
            corrections.append({"name": name, "source_from": row.get("source"),
                                "source_to": output.get("source"),
                                "fields_replaced": changed})
        prepared.append(output)
    # A resolved component and a blended label of that same registered pair
    # cannot both be independent evidence, even when the blend can match CWT.
    adopted = {row.get("name") for row in prepared
               if row.get("fitted_center") not in (None, "")}
    from FORMA.core.reasoning.ontology.registry import ONTOLOGY
    line_by_id = ONTOLOGY.line_index()
    for pair in ONTOLOGY.doublets:
        if len(pair.component_ids) != 2:
            continue
        first, second = (line_by_id[line_id] for line_id in pair.component_ids)
        if first.name not in adopted and second.name not in adopted:
            continue
        for blend_name in blended_labels_for_pair(first, second) & adopted:
            errors.append({"name": blend_name,
                           "reason": "blended label duplicates an adopted registered doublet component"})
    return prepared, corrections, errors
