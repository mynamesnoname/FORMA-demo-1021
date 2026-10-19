"""Reviewed FITS/Redrock inputs for the independent investigation graph.

This adapter reuses only the spectrum reader, CWT detector and Redrock runner.
It never constructs or imports the legacy Evidence Graph or agent state.
"""

from __future__ import annotations

import json
import math
import random
import secrets
from pathlib import Path

import numpy as np

from FORMA.agents.multi_agents.utils.VI import (
    _load_spectrum_from_fits, run_redrock_pipeline,
)
from FORMA.agents.multi_agents.utils.cwt_feature_finder import run_cwt_feature_detection

from .vi_measurements import prepare_vi_measurements
from .spectrum_visualization import plot_spectrum_overview, plot_vi_features


def _redrock_labels(result: dict, seed: str) -> tuple[dict[str, float], dict]:
    """Assign neutral H labels from distinct Redrock znum referents."""
    rows = result.get("hypotheses") or []
    if not isinstance(rows, list) or not rows:
        raise ValueError("Redrock produced no usable hypotheses")
    keyed = []
    for row in rows:
        meta = row.get("_redrock") or {}
        znum = meta.get("znum")
        z = row.get("z_representative")
        if z is None:
            z = row.get("z_center")
        if type(znum) is not int or not isinstance(z, (int, float)) or not math.isfinite(z):
            raise ValueError("Redrock hypothesis lacks a finite redshift or integer znum")
        keyed.append((znum, float(z), meta))
    keyed.sort(key=lambda item: item[0])
    if len({item[0] for item in keyed}) != len(keyed):
        raise ValueError("Redrock hypothesis znum must be unique")
    random.Random(seed).shuffle(keyed)
    hypotheses = {}
    labels = []
    for index, (znum, z, meta) in enumerate(keyed, 1):
        ref = f"H{index}"
        hypotheses[ref] = z
        labels.append({"hypothesis_ref": ref, "znum": znum, "redshift": z,
                       "spectype": meta.get("spectype"),
                       "subtype": meta.get("subtype")})
    return hypotheses, {"schema_version": "forma-agentic-redrock-labels-v1",
                        "seed": seed, "entries": labels}


def prepare_fits_inputs(*, fits_path: str | Path, run_id: str,
                        output_root: str | Path, params) -> dict:
    """Freeze a graph-ready VI manifest and a blinded Redrock label map."""
    fits = Path(fits_path).resolve(strict=True)
    if fits.suffix.lower() != ".fits":
        raise ValueError("the graph FITS adapter accepts only .fits inputs")
    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    spectrum = _load_spectrum_from_fits(
        str(fits), arm_names=params.arm_name,
        arm_wavelength_ranges=params.arm_wavelength_range,
        assumed_snr_without_ivar=params.assumed_snr_without_ivar)
    wl = np.asarray(spectrum["wavelength"])
    flux = np.asarray(spectrum["flux"])
    if (wl.ndim != 1 or len(wl) == 0 or flux.shape != wl.shape
            or not np.isfinite(wl).all() or not np.all(np.diff(wl) > 0)):
        raise ValueError("FITS reader did not produce an ordered one-dimensional spectrum")
    npz = root / "spectrum.npz"
    if npz.exists():
        raise FileExistsError("graph spectrum artifact already exists")
    arrays = {"wavelength": wl, "flux": flux,
              "snr": np.asarray(spectrum["snr"]),
              "snr_is_assumed": bool(spectrum.get("snr_is_assumed", False))}
    if spectrum.get("ivar") is not None:
        arrays["ivar"] = np.asarray(spectrum["ivar"])
    np.savez_compressed(npz, **arrays)
    vi_dir = root / "VI"
    vi_dir.mkdir(exist_ok=True)
    bands = [(name, float(bounds[0]), float(bounds[1]))
             for name, bounds in zip(params.arm_name or [],
                                     params.arm_wavelength_range or [])]
    overview = plot_spectrum_overview(npz, root / "spectrum.png", bands=bands)
    detection = run_cwt_feature_detection(
        output_dir=str(root), file_name=fits.stem,
        wavelength=wl, flux=flux,
        ivar=np.asarray(spectrum["ivar"]) if spectrum.get("ivar") is not None else None,
        effective_snr=(np.asarray(spectrum["snr"])
                       if spectrum.get("ivar") is None else None),
        emission_detection_params={
            "snr_thresh": params.cwt_snr_thresh,
            "min_ridge_length": params.cwt_min_ridge_length,
            "n_scales": params.cwt_n_scales,
            "min_scale": params.cwt_min_width,
            "max_scale": params.cwt_max_width,
        }, verbose=False, artifact_subdir="VI")
    peaks = detection["df_emission"].to_dict("records")
    troughs = detection["df_absorption"].to_dict("records")
    if params.rr_template_dir is None:
        raise ValueError("RR_TEMPLATE_DIR is required for graph Redrock runs")
    if params.use_archetypes and params.archetype_dir is None:
        raise ValueError("ARCHETYPE_DIR is required when USE_ARCHETYPES=true")
    redrock = run_redrock_pipeline(
        input_fits=str(fits), output_dir=str(root), file_name=fits.stem,
        rr_template_dir=params.rr_template_dir,
        archetype_dir=params.archetype_dir,
        use_archetypes=params.use_archetypes,
        nminima=params.rr_nminima, nnearest=params.rr_nnearest,
        omp_num_threads=params.rr_omp_num_threads,
        legendre_degree=params.rr_archetype_legendre_degree,
        legendre_prior=params.rr_archetype_legendre_prior_sigma)
    seed = params.hypothesis_label_seed or secrets.token_hex(16)
    hypotheses, labels = _redrock_labels(redrock, seed)
    (root / "hypothesis_labels.json").write_text(
        json.dumps(labels, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8")
    manifest = prepare_vi_measurements(
        run_id=run_id, spectrum_npz_path=npz, hypotheses=hypotheses,
        peaks=peaks, troughs=troughs, output_dir=vi_dir / "measurements",
        masked_regions=[])
    features_plot = plot_vi_features(npz, manifest, vi_dir)
    snr = np.asarray(spectrum["snr"], dtype=float)
    finite_snr = snr[np.isfinite(snr)]
    return {"manifest_path": str(vi_dir / "measurements/manifest.json"),
            "manifest": manifest, "hypotheses": hypotheses,
            "labels_path": str(root / "hypothesis_labels.json"),
            "npz_path": str(npz), "fits_path": str(fits),
            "spectrum_plot_path": str(overview),
            "vi_features_plot_path": str(features_plot),
            "snr_median": float(np.median(finite_snr)) if finite_snr.size else None}
