"""Portable, browser-readable view of frozen VI and SH artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np


SCHEMA = "forma-browser-visualization-v1"


def _inside(root: Path, path: str | Path) -> Path:
    candidate = Path(path).resolve(strict=True)
    if not candidate.is_relative_to(root):
        raise ValueError("visualization source is outside the sample directory")
    return candidate


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _finite_array(array) -> list[float | None]:
    values = np.asarray(array, dtype=float)
    if values.ndim != 1:
        raise ValueError("browser spectrum arrays must be one-dimensional")
    return [float(value) if math.isfinite(value) else None for value in values]


def write_browser_bundle(sample_root: str | Path, *,
                         manifest_path: str | Path | None = None) -> dict[str, Path]:
    """Write standalone JSON and file://-loadable JS, without absolute data paths.

    All scientific arrays retain their Python/JSON round-trip float values. The
    Chebyshev continuum is explicitly marked display-only; CSV cells remain
    strings so this projection never becomes an alternative SH authority.
    """
    root = Path(sample_root).resolve(strict=True)
    if manifest_path is None:
        manifest_path = next((path for path in (
            root / "VI/measurements/manifest.json",
            root / "vi_measurements/manifest.json") if path.is_file()), None)
    if manifest_path is None:
        raise FileNotFoundError("sample has no VI measurement manifest")
    manifest_file = _inside(root, manifest_path)
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    spectrum_file = _inside(root, root / "spectrum.npz")
    continuum_file = _inside(root, root / "VI/continuum_display.npz")
    hashes = {str(path.relative_to(root)): _hash(path)
              for path in (manifest_file, spectrum_file, continuum_file)}
    with np.load(spectrum_file) as spectrum, np.load(continuum_file) as display:
        wave = np.asarray(spectrum["wavelength"], dtype=float)
        continuum_wave = np.asarray(display["wavelength"], dtype=float)
        if not np.array_equal(wave, continuum_wave):
            raise ValueError("VI display continuum does not match the spectrum wavelength grid")
        flux = np.asarray(spectrum["flux"], dtype=float)
        ivar = np.asarray(spectrum["ivar"], dtype=float) if "ivar" in spectrum else None
        valid = np.isfinite(flux) & (np.isfinite(ivar) & (ivar > 0)
                                     if ivar is not None else True)
        spectrum_data = {"wavelength_angstrom": _finite_array(wave),
                         "flux": _finite_array(np.where(valid, flux, np.nan)),
                         "valid_pixel": valid.tolist(),
                         "ivar": _finite_array(ivar) if ivar is not None else None,
                         "snr": _finite_array(spectrum["snr"])
                         if "snr" in spectrum else None}
        continuum_data = {
            "role": "display_only", "method": "Chebyshev",
            "degree": int(display["chebyshev_degree"]),
            "flux": _finite_array(display["flux"])}
    fits = []
    for ref, info in sorted(manifest["hypotheses"].items()):
        catalog_file = _inside(root, info["catalog_path"])
        hashes[str(catalog_file.relative_to(root))] = _hash(catalog_file)
        catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
        for item in catalog["measurements"]:
            if item["source"] == "CWT":
                continue
            fits.append({"hypothesis_ref": ref, "id": item["id"],
                         "source": item["source"], "kind": item["kind"],
                         "target_line": item.get("target_line"),
                         "adoptable": item["adoptable"],
                         "flags": item.get("flags", []), "record": item["record"]})
    sh = {}
    for csv_file in sorted(root.glob("SH/*/pre_analysis/**/lines.csv")):
        csv_file = _inside(root, csv_file)
        ref = csv_file.relative_to(root).parts[1]
        if ref in sh:
            raise ValueError(f"multiple SH CSV attempts for {ref}; choose an active attempt")
        with csv_file.open(newline="", encoding="utf-8") as stream:
            sh[ref] = {"redshift": manifest["hypotheses"][ref]["redshift"],
                       "lines": list(csv.DictReader(stream))}
        hashes[str(csv_file.relative_to(root))] = _hash(csv_file)
    bundle = {"schema_version": SCHEMA, "sample_id": root.name,
              "run_id": manifest.get("run_id"),
              "units": {"wavelength": "angstrom", "flux": "native FITS flux"},
              "spectrum": spectrum_data, "continuum": continuum_data,
              "vi": {"cwt_features": manifest["cwt_features"],
                     "gaussian_measurements": fits},
              "sh": sh, "source_sha256": hashes}
    payload = json.dumps(bundle, ensure_ascii=True, allow_nan=False,
                         separators=(",", ":"))
    json_path = root / "visualization_data.json"
    js_path = root / "visualization_data.js"
    json_path.write_text(payload + "\n", encoding="utf-8")
    js_path.write_text("window.FORMA_VISUALIZATION_DATA = " + payload + ";\n",
                       encoding="utf-8")
    return {"json": json_path, "js": js_path}
