"""Freeze run-scoped CWT observations and hypothesis-scoped fits at the VI boundary.

The resulting catalogs are the sole measurement input to the new SH adapter.
This boundary runs after Redrock has supplied the hypotheses and before any
SH model session starts. It does not import the legacy Evidence Graph.
"""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Mapping

import numpy as np

from FORMA.agents.multi_agents.harness.single_hypothesis import _prepare_prefits

from .sh_measurement_refs import build_catalog


def assign_cwt_feature_ids(peaks: list[dict], troughs: list[dict]) -> tuple[list[dict], list[dict]]:
    """Assign one immutable, run-local ID to each VI CWT detection.

    The VI detection order is preserved. An existing ID must agree with that
    order, so a resumed run cannot silently change the referent of an ID.
    """
    def assign(items: list[dict], prefix: str) -> list[dict]:
        result = []
        for index, feature in enumerate(items):
            expected = f"{prefix}:{index:04d}"
            existing = feature.get("feature_id")
            if existing is not None and existing != expected:
                raise ValueError(f"CWT feature ID {existing!r} does not match {expected!r}")
            result.append({**feature, "feature_id": expected})
        return result

    return assign(peaks, "cwt:em"), assign(troughs, "cwt:abs")


def _write_json(path: Path, value: dict | list) -> None:
    path.write_text(json.dumps(
        value, ensure_ascii=False, indent=2, allow_nan=False,
        default=lambda item: item.item() if isinstance(item, np.generic) else _unsupported(item),
    ) + "\n", encoding="utf-8")


def _unsupported(value):
    raise TypeError(f"cannot freeze value of type {type(value).__name__}")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def prepare_vi_measurements(
    *, run_id: str, spectrum_npz_path: str | Path,
    hypotheses: Mapping[str, float], peaks: list[dict], troughs: list[dict],
    output_dir: str | Path, masked_regions: list | None = None,
    z_bounds: Mapping[str, tuple[float, float]] | None = None,
) -> dict:
    """Fit uncovered predicted lines once per Redrock hypothesis, then freeze.

    ``hypotheses`` maps stable hypothesis references to their Redrock redshift.
    The returned manifest points to one catalog per hypothesis. Catalogs share
    CWT IDs and carry distinct fit IDs; no SH model call is made here.
    """
    if not isinstance(run_id, str) or not run_id or not hypotheses:
        raise ValueError("run_id and at least one hypothesis are required")
    if any(not isinstance(ref, str) or not ref for ref in hypotheses):
        raise ValueError("each hypothesis needs a nonempty reference")
    npz_path = Path(spectrum_npz_path).resolve(strict=True)
    target_dir = Path(output_dir).resolve()
    if target_dir.exists():
        raise FileExistsError(f"VI measurement directory already exists: {target_dir}")

    vi_peaks, vi_troughs = assign_cwt_feature_ids(peaks, troughs)
    with np.load(npz_path) as spectrum:
        wavelength = spectrum["wavelength"]
        if wavelength.size == 0:
            raise ValueError("spectrum has no wavelength samples")
        wavelength_min = float(np.min(wavelength))
        wavelength_max = float(np.max(wavelength))

    target_dir.mkdir(parents=True)
    spectrum_sha256 = _sha256(npz_path)
    manifest = {"run_id": run_id, "spectrum_npz_path": str(npz_path),
                "spectrum_npz_sha256": spectrum_sha256,
                "cwt_features": {"emission": vi_peaks, "absorption": vi_troughs},
                "hypotheses": {}}
    _write_json(target_dir / "cwt_features.json", manifest["cwt_features"])
    for index, (hypothesis_ref, redshift) in enumerate(hypotheses.items()):
        if not isinstance(redshift, (int, float)) or not np.isfinite(redshift):
            raise ValueError(f"invalid redshift for {hypothesis_ref!r}")
        bounds = (z_bounds or {}).get(hypothesis_ref)
        z_min, z_max = bounds if bounds is not None else (None, None)
        attempts_path = target_dir / f"hypothesis_{index:03d}_fit_attempts.json"
        attempts, fits = _prepare_prefits(
            str(npz_path), float(redshift), vi_peaks, vi_troughs,
            z_min, z_max, masked_regions, str(attempts_path),
        )
        for fit_index, fit in enumerate(fits):
            fit["measurement_id"] = f"fit:{hypothesis_ref}:{fit_index:04d}"
        catalog = build_catalog(
            run_id=run_id, hypothesis_ref=hypothesis_ref,
            redshift=float(redshift), wavelength_min=wavelength_min,
            wavelength_max=wavelength_max, peaks=vi_peaks, troughs=vi_troughs,
            fits=fits, z_min=z_min, z_max=z_max,
        )
        catalog["fit_attempts"] = attempts
        catalog["masked_regions"] = masked_regions or []
        catalog["spectrum_npz_path"] = str(npz_path)
        catalog["spectrum_npz_sha256"] = spectrum_sha256
        catalog_path = target_dir / f"hypothesis_{index:03d}_measurement_catalog.json"
        _write_json(catalog_path, catalog)
        manifest["hypotheses"][hypothesis_ref] = {
            "redshift": float(redshift), "catalog_path": str(catalog_path),
            "fit_attempts_path": str(attempts_path),
        }
    if _sha256(npz_path) != spectrum_sha256:
        raise RuntimeError("spectrum changed while VI measurements were prepared")
    _write_json(target_dir / "manifest.json", manifest)
    return manifest
