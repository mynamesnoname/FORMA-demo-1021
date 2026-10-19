"""Measurement reference resolution for the new SH pre-analysis node.

The model chooses references and judgments. Only this module copies measured
numbers into the legacy-compatible CSV. Scoped catalogs receive IDs from the
VI boundary, never from rounded wavelengths or model-supplied numeric strings.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from langchain_core.tools import tool

from FORMA.agents.multi_agents.harness.sh_provenance import (
    blended_labels_for_pair, validate_sh_catalog,
)
from FORMA.agents.multi_agents.harness.tools import (
    ABSORPTION_LINES, EMISSION_LINES, write_lines_csv as write_csv_core,
)
from FORMA.core.constants import FWHM_TO_SIGMA
from FORMA.core.line_status import STATUSES, is_kept_evidence
from FORMA.core.reasoning.ontology.registry import ONTOLOGY


def build_catalog(
    *, redshift: float, wavelength_min: float, wavelength_max: float,
    peaks: list[dict], troughs: list[dict], fits: list[dict],
    z_min: float | None = None, z_max: float | None = None,
    run_id: str | None = None, hypothesis_ref: str | None = None,
) -> dict[str, Any]:
    """Freeze one hypothesis's selectable observations and predicted lines."""
    if (run_id is None) != (hypothesis_ref is None):
        raise ValueError("run_id and hypothesis_ref must be provided together")
    if run_id is not None and (any(not item.get("feature_id") for item in [*peaks, *troughs])
                               or any(not item.get("measurement_id") for item in fits)):
        raise ValueError("scoped catalogs require IDs assigned at the VI boundary")
    if z_min is None or z_max is None:
        from FORMA.core.config.analysis_method import load_analysis_method
        half = load_analysis_method().evaluation.redshift_tolerance
        z_min = z_min if z_min is not None else round(redshift - half, 4)
        z_max = z_max if z_max is not None else round(redshift + half, 4)
    known = {**EMISSION_LINES, **ABSORPTION_LINES}
    registry = {line.name: line for line in ONTOLOGY.lines}
    lines = [{"id": registry[name].id, "name": name,
              "rest_wavelength": rest, "predicted_obs": rest * (1 + redshift),
              "kind": "emission" if name in EMISSION_LINES else "absorption"}
             for name, rest in known.items()
             if wavelength_min <= rest * (1 + redshift) <= wavelength_max]
    lines.sort(key=lambda row: (row["predicted_obs"], row["id"]))

    measurements = []
    for kind, items, prefix in (("emission", peaks, "cwt:em"),
                                ("absorption", troughs, "cwt:abs")):
        for index, feature in enumerate(items):
            measurement_id = feature.get("feature_id") or f"{prefix}:{index:04d}"
            measurements.append({"id": measurement_id, "source": "CWT",
                                 "kind": kind, "target_line": None,
                                 "adoptable": True, "flags": [],
                                 "record": dict(feature)})
    for index, fit in enumerate(fits):
        flags = list(fit.get("flags") or [])
        measurements.append({
            "id": fit.get("measurement_id") or f"fit:{index:04d}",
            "source": fit["source"],
            "kind": fit["kind"], "target_line": fit.get("target_line"),
            "adoptable": (fit.get("center") is not None
                          and not {"fit_failed", "center_at_bound"}.intersection(flags)),
            "flags": flags, "record": dict(fit),
        })
    ids = [item["id"] for item in measurements]
    if any(not isinstance(item, str) or not item for item in ids) or len(set(ids)) != len(ids):
        raise ValueError("measurement IDs must be nonempty and unique within a catalog")
    return {"run_id": run_id, "hypothesis_ref": hypothesis_ref,
            "redshift": redshift, "z_min": z_min, "z_max": z_max,
            "wavelength_min": wavelength_min,
            "wavelength_max": wavelength_max, "lines": lines,
            "measurements": measurements}


def render_catalog(catalog: dict) -> str:
    """Give the model exact ID tokens beside concise, human-readable values."""
    rows = ["## Authoritative line and measurement IDs", "",
            "Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; "
            "the tool copies full-precision values from the frozen catalog.", "",
            "| Line ID | Name | Predicted λ (Å) | Kind |",
            "|---|---|---:|---|"]
    for line in catalog["lines"]:
        rows.append(f"| {line['id']} | {line['name']} | {line['predicted_obs']:.1f} | {line['kind']} |")
    rows.extend(["", "| Measurement ID | Source | Kind | Centre (Å) | Target | Selectable | Flags |",
                 "|---|---|---|---:|---|---|---|"])
    for measurement in catalog["measurements"]:
        record = measurement["record"]
        center = record.get("wavelength") if measurement["source"] == "CWT" else record.get("center")
        rows.append(
            f"| {measurement['id']} | {measurement['source']} | {measurement['kind']} | "
            f"{center:.3f} | {measurement['target_line'] or '—'} | "
            f"{'yes' if measurement['adoptable'] else 'no'} | "
            f"{', '.join(measurement['flags']) or '—'} |"
        )
    return "\n".join(rows) + "\n"


def _measurement_fields(measurement: dict) -> dict:
    record = measurement["record"]
    if measurement["source"] == "CWT":
        fwhm = record.get("FWHM_A")
        return {
            "fitted_center": record["wavelength"],
            "fitted_center_err": record.get("wavelength_err"),
            "amplitude": record.get("amplitude"),
            "amplitude_err": record.get("amplitude_err"),
            "fitted_sigma": fwhm * FWHM_TO_SIGMA if isinstance(fwhm, (int, float)) else None,
            "fwhm_km_s": record.get("FWHM_km_s"),
            "ridge_length": record.get("ridge_length"),
            "cwt_snr": record.get("snr"),
            "source": "CWT",
        }
    return {
        "fitted_center": record["center"],
        "fitted_center_err": record.get("center_err"),
        "amplitude": record.get("amplitude"),
        "amplitude_err": record.get("amplitude_err"),
        "fitted_sigma": record.get("sigma"),
        "fwhm_km_s": record.get("fwhm_km_s"),
        "ridge_length": None, "cwt_snr": None,
        "source": measurement["source"],
    }


def resolve_judgments(catalog: dict, judgments: list) -> tuple[list[dict], list[dict]]:
    """Resolve ID-only judgments; return canonical CSV rows and repair errors."""
    by_line = {line["id"]: line for line in catalog["lines"]}
    by_measurement = {item["id"]: item for item in catalog["measurements"]}
    errors, rows = [], []
    seen: set[str] = set()
    if not isinstance(judgments, list):
        return [], [{"reason": "lines must be a list"}]
    for index, judgment in enumerate(judgments):
        if not isinstance(judgment, dict):
            errors.append({"row": index, "reason": "row must be an object"})
            continue
        allowed = {"line_id", "measurement_id", "status", "reason_codes", "comment"}
        if set(judgment) - allowed or not {"line_id", "measurement_id", "status"} <= set(judgment):
            errors.append({"row": index, "reason": "use line_id, measurement_id, status, optional reason_codes/comment only"})
            continue
        line_id = judgment["line_id"]
        if not isinstance(line_id, str) or line_id not in by_line:
            errors.append({"row": index, "line_id": line_id, "reason": "unknown line ID"})
            continue
        if line_id in seen:
            errors.append({"row": index, "line_id": line_id, "reason": "duplicate line ID"})
        seen.add(line_id)
        line = by_line[line_id]
        ref = judgment["measurement_id"]
        status = judgment["status"]
        if not isinstance(status, str) or status not in STATUSES:
            errors.append({"row": index, "line_id": line_id, "reason": "unknown status"})
            continue
        if is_kept_evidence(status) and (not isinstance(ref, str) or ref not in by_measurement):
            errors.append({"row": index, "line_id": line_id, "reason": "kept line needs a known measurement ID"})
            continue
        if not is_kept_evidence(status) and ref is not None:
            errors.append({"row": index, "line_id": line_id, "reason": "unadopted line needs null measurement_id"})
            continue
        codes = judgment.get("reason_codes", [])
        if not isinstance(codes, list) or any(not isinstance(item, str) for item in codes):
            errors.append({"row": index, "line_id": line_id, "reason": "reason_codes must be a string list"})
        if not isinstance(judgment.get("comment", ""), str):
            errors.append({"row": index, "line_id": line_id, "reason": "comment must be text"})
        row = {"name": line["name"], "rest_wavelength": line["rest_wavelength"],
               "predicted_obs": line["predicted_obs"], "status": status,
               "implied_z": None}
        if ref is None:
            row.update({key: None for key in (
                "fitted_center", "fitted_center_err", "amplitude", "amplitude_err",
                "fitted_sigma", "fwhm_km_s", "ridge_length", "cwt_snr", "source")})
        else:
            measurement = by_measurement[ref]
            if not measurement["adoptable"]:
                errors.append({"row": index, "line_id": line_id, "measurement_id": ref,
                               "reason": "measurement is not selectable"})
            if measurement["kind"] != line["kind"]:
                errors.append({"row": index, "line_id": line_id, "measurement_id": ref,
                               "reason": "emission/absorption kind mismatch"})
            if measurement["target_line"] not in (None, line["name"]):
                errors.append({"row": index, "line_id": line_id, "measurement_id": ref,
                               "reason": "fit belongs to another line"})
            center = (measurement["record"].get("wavelength")
                      if measurement["source"] == "CWT" else measurement["record"].get("center"))
            if center is not None and not (catalog["z_min"] <= center / line["rest_wavelength"] - 1
                                           <= catalog["z_max"]):
                errors.append({"row": index, "line_id": line_id, "measurement_id": ref,
                               "reason": "measurement is outside this line's redshift window"})
            row.update(_measurement_fields(measurement))
        rows.append(row)
    for line_id in by_line.keys() - seen:
        errors.append({"line_id": line_id, "reason": "missing predicted line"})

    # An unresolved blend and its resolved components must not count twice.
    adopted = {row["name"] for row in rows if row["fitted_center"] is not None}
    by_registry_id = ONTOLOGY.line_index()
    for pair in ONTOLOGY.doublets:
        if len(pair.component_ids) != 2:
            continue
        first, second = (by_registry_id[item] for item in pair.component_ids)
        if first.name not in adopted and second.name not in adopted:
            continue
        for blend_name in blended_labels_for_pair(first, second) & adopted:
            errors.append({"name": blend_name,
                           "reason": "blended label duplicates an adopted doublet component"})
    return rows, errors


def build_id_writer(catalog: dict, *, masked_regions: list | None = None,
                    judgment_path: str | Path | None = None):
    """Expose one ID-only tool while keeping the established CSV artifact."""
    @tool("write_lines_csv")
    def write_by_id(file_path: str, lines: list) -> dict:
        """Write judgments by line_id and measurement_id; measured numbers are resolved by code."""
        rows, errors = resolve_judgments(catalog, lines)
        if not errors:
            errors = validate_sh_catalog(
                rows, catalog["redshift"], catalog["wavelength_min"],
                catalog["wavelength_max"], masked_regions,
            )
        if errors:
            return {"path": None, "n_lines": 0, "flags": ["invalid_id_judgments"],
                    "rows_to_repair": errors,
                    "message": "Nothing was written. Repair and resend every predicted line."}
        result = write_csv_core.func(file_path=file_path, lines=rows)
        if result.get("path") and judgment_path is not None:
            path = Path(judgment_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(lines, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result["judgment_path"] = str(path.resolve())
        return result

    return write_by_id
