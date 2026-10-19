"""Attach DESI sky-line proximity to an observed feature without changing FA votes."""

from __future__ import annotations

import hashlib
import json
import math
from bisect import bisect_left
from functools import lru_cache
from importlib.resources import files

from FORMA.core.reasoning.ontology.registry import ONTOLOGY
from FORMA.core.reasoning.ontology.rule_parameters import effective_operand_threshold


_RULE_ID = "rule:formal-skyline-contamination"
_OPERAND_ID = "nearest_skyline_offset"
_CATALOG_NAME = "data/desi_sky_lines.json"


@lru_cache(maxsize=1)
def _catalog() -> tuple[tuple[float, ...], str, str]:
    raw = files("FORMA.agentic_graph").joinpath(_CATALOG_NAME).read_bytes()
    payload = json.loads(raw)
    if (payload.get("schema_version") != "forma-desi-sky-lines-v1"
            or payload.get("wavelength_medium") != "vacuum"
            or payload.get("wavelength_frame") != "earth"
            or payload.get("wavelength_unit") != "Angstrom"):
        raise ValueError("DESI sky-line catalog has an unsupported coordinate system")
    values = payload.get("wavelengths_angstrom")
    if not isinstance(values, list) or not values:
        raise ValueError("DESI sky-line catalog is empty")
    lines = tuple(float(value) for value in values)
    if (not all(math.isfinite(value) for value in lines)
            or tuple(sorted(set(lines))) != lines):
        raise ValueError("DESI sky-line catalog must contain sorted unique finite wavelengths")
    return lines, hashlib.sha256(raw).hexdigest(), str(payload["source_version"])


def skyline_risk(center_angstrom: float) -> dict:
    """Return a proximity warning, never an atmospheric-origin verdict or mask.

    DESI's list gives bright sky-line positions without species labels. OH bands
    remain separate region warnings; a position inside a band is not an
    individual sky-line match. The existing configurable rule owns the match
    tolerance and its provenance.
    """
    if not isinstance(center_angstrom, (int, float)) or not math.isfinite(center_angstrom):
        raise ValueError("feature center must be finite")
    lines, catalog_digest, source_version = _catalog()
    bound = effective_operand_threshold(_RULE_ID, _OPERAND_ID)
    threshold = bound["value"]
    position = bisect_left(lines, center_angstrom)
    candidates = [i for i in (position - 1, position) if 0 <= i < len(lines)]
    nearest_index = min(candidates, key=lambda i: (abs(lines[i] - center_angstrom), i))
    nearest_wavelength = lines[nearest_index]
    offset = abs(nearest_wavelength - center_angstrom)
    bands = [record.id for record in ONTOLOGY.skylines
             if record.kind == "band" and record.wavelength_max is not None
             and record.wavelength_obs <= center_angstrom <= record.wavelength_max]
    matched = offset <= threshold
    return {
        "status": ("near_discrete_skyline" if matched else
                   "oh_band_only" if bands else "no_registered_risk"),
        "nearest_line": {"id": f"desi-sky:{nearest_index:04d}",
                         "wavelength_angstrom": nearest_wavelength,
                         "offset_angstrom": offset},
        "within_proximity_threshold": matched,
        "oh_band_ids": bands,
        "threshold_angstrom": threshold,
        "threshold_source": bound["source"],
        "threshold_source_path": bound["source_path"],
        "threshold_payload_sha256": bound["payload_digest"],
        "catalog_sha256": catalog_digest,
        "catalog_source": f"desispec {source_version} get_sky_lines()",
    }
