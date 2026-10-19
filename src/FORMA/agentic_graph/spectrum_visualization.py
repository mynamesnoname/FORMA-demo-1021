"""Read-only PNG views of frozen graph spectrum, VI measurements and SH lines."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from numpy.polynomial import Chebyshev

from FORMA.core.config.analysis_method import load_analysis_method
from FORMA.core.line_status import is_kept_evidence


INK = "#17263d"
FLUX = "#334b68"
GRID = "#d9e2e9"
PEAK = "#d46732"
TROUGH = "#694c9b"
FIT = "#008e87"
CONTINUUM = "#cb4d68"


def _read_spectrum(path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    with np.load(path) as spectrum:
        wave = np.asarray(spectrum["wavelength"], dtype=float)
        flux = np.asarray(spectrum["flux"], dtype=float)
        if "ivar" in spectrum:
            ivar = np.asarray(spectrum["ivar"], dtype=float)
            flux = np.where(np.isfinite(ivar) & (ivar > 0), flux, np.nan)
    if (wave.ndim != 1 or flux.shape != wave.shape or wave.size < 3
            or not np.isfinite(wave).all() or not np.all(np.diff(wave) > 0)):
        raise ValueError("plot needs an ordered one-dimensional spectrum")
    return wave, flux


def _style(ax, title: str, *, xlabel: bool = False) -> None:
    ax.set_title(title, loc="left", fontsize=11, color=INK, weight="semibold", pad=9)
    ax.set_ylabel("Flux", color=INK)
    if xlabel:
        ax.set_xlabel("Observed wavelength (Å)", color=INK)
    ax.grid(axis="y", color=GRID, linewidth=.7, alpha=.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(GRID)
    ax.tick_params(colors=INK, labelsize=9)


def _finish(fig, destination: str | Path) -> Path:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=165, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def plot_spectrum_overview(npz_path: str | Path, destination: str | Path,
                           *, bands: list[tuple[str, float, float]] | None = None) -> Path:
    """One whole-spectrum row plus one row for each configured arm/band."""
    wave, flux = _read_spectrum(npz_path)
    if not bands:
        edges = np.linspace(wave[0], wave[-1], 4)
        bands = [(f"Band {index + 1}", float(edges[index]), float(edges[index + 1]))
                 for index in range(3)]
    bands = [(name, lo, hi) for name, lo, hi in bands
             if hi > wave[0] and lo < wave[-1]]
    fig, axes = plt.subplots(len(bands) + 1, 1, figsize=(16, 3.0 * (len(bands) + 1)),
                             constrained_layout=True)
    axes = np.atleast_1d(axes)
    fig.suptitle(f"{Path(npz_path).parent.name}  ·  observed spectrum", fontsize=17,
                 color=INK, weight="bold")
    axes[0].plot(wave, flux, color=FLUX, lw=.65, rasterized=True)
    _style(axes[0], f"Full range  ·  {wave[0]:.0f}–{wave[-1]:.0f} Å")
    for ax, (name, lo, hi) in zip(axes[1:], bands):
        selection = (wave >= lo) & (wave <= hi)
        ax.plot(wave[selection], flux[selection], color=FLUX, lw=.8, rasterized=True)
        ax.set_xlim(max(lo, wave[0]), min(hi, wave[-1]))
        _style(ax, f"{name}  ·  {max(lo, wave[0]):.0f}–{min(hi, wave[-1]):.0f} Å",
               xlabel=ax is axes[-1])
    return _finish(fig, destination)


def _display_continuum(wave: np.ndarray, flux: np.ndarray,
                       features: list[dict]) -> tuple[np.ndarray, int]:
    """Robust Chebyshev display fit; never fed back into CWT or scientific decisions."""
    method = load_analysis_method().continuum
    degree = max(method.chebyshev_min_degree,
                 min(5, method.chebyshev_max_degree))
    usable = np.isfinite(flux)
    for feature in features:
        center, fwhm = feature.get("wavelength"), feature.get("FWHM_A")
        if (isinstance(center, (float, int)) and isinstance(fwhm, (float, int))
                and math.isfinite(center) and math.isfinite(fwhm) and fwhm > 0):
            usable &= np.abs(wave - center) > 1.5 * fwhm
    if usable.sum() < max(30, 3 * (degree + 1)):
        usable = np.isfinite(flux)
    if usable.sum() <= degree:
        raise ValueError("too few finite spectrum pixels for a display continuum")
    for _ in range(3):
        fit = Chebyshev.fit(wave[usable], flux[usable], deg=degree,
                            domain=[float(wave[0]), float(wave[-1])])
        residual = flux - fit(wave)
        scale = 1.4826 * np.median(np.abs(residual[usable] - np.median(residual[usable])))
        if not np.isfinite(scale) or scale <= 0:
            break
        updated = usable & (np.abs(residual - np.median(residual[usable])) < 4 * scale)
        if updated.sum() <= degree or np.array_equal(updated, usable):
            break
        usable = updated
    return np.asarray(fit(wave), dtype=float), degree


def _number(value) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _mark_features(ax, wave, residual, features: list[dict], *, color: str,
                   label: str, hollow: bool = False) -> None:
    centers = [_number(item.get("wavelength", item.get("center"))) for item in features]
    centers = np.asarray([center for center in centers
                          if center is not None and wave[0] <= center <= wave[-1]])
    if not centers.size:
        return
    values = np.interp(centers, wave, np.nan_to_num(residual, nan=0.0))
    ax.scatter(centers, values, s=33 if hollow else 27, marker="o", zorder=4,
               facecolors="none" if hollow else color, edgecolors=color,
               linewidths=1.2 if hollow else .4, label=f"{label} ({len(centers)})")
    for center in centers:
        ax.axvline(center, color=color, lw=.55, alpha=.20)


def plot_vi_features(npz_path: str | Path, manifest: dict,
                     vi_directory: str | Path) -> Path:
    """Flux/continuum, emission residual and absorption residual in three rows."""
    wave, flux = _read_spectrum(npz_path)
    cwt = manifest["cwt_features"]
    continuum, degree = _display_continuum(wave, flux,
                                           cwt["emission"] + cwt["absorption"])
    vi = Path(vi_directory)
    vi.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(vi / "continuum_display.npz", wavelength=wave,
                        flux=continuum, chebyshev_degree=degree)
    residual = flux - continuum
    fits = {"emission": [], "absorption": []}
    for info in manifest["hypotheses"].values():
        catalog = json.loads(Path(info["catalog_path"]).read_text(encoding="utf-8"))
        for measurement in catalog["measurements"]:
            if measurement["source"] != "CWT" and measurement["adoptable"]:
                fits[measurement["kind"]].append(measurement["record"])
    fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True,
                             constrained_layout=True)
    fig.suptitle("VI  ·  frozen CWT and Gaussian measurements", fontsize=17,
                 color=INK, weight="bold")
    axes[0].plot(wave, flux, color=FLUX, lw=.65, label="Observed flux", rasterized=True)
    axes[0].plot(wave, continuum, color=CONTINUUM, lw=1.4,
                 label=f"Chebyshev display fit (degree {degree})")
    _style(axes[0], "Spectrum and display-only continuum")
    axes[0].legend(frameon=False, loc="upper right", fontsize=8)
    for ax, kind, color, title in ((axes[1], "emission", PEAK, "Peaks"),
                                   (axes[2], "absorption", TROUGH, "Troughs")):
        ax.plot(wave, residual, color=FLUX, lw=.65, alpha=.8, rasterized=True)
        ax.axhline(0, color=GRID, lw=.9)
        _mark_features(ax, wave, residual, cwt[kind], color=color, label="CWT")
        _mark_features(ax, wave, residual, fits[kind], color=FIT,
                       label="Gaussian fits · hypothesis-local", hollow=True)
        _style(ax, f"{title}  ·  residual from display continuum", xlabel=ax is axes[-1])
        if ax.get_legend_handles_labels()[0]:
            ax.legend(frameon=False, loc="upper right", fontsize=8)
    axes[-1].set_xlim(wave[0], wave[-1])
    return _finish(fig, vi / "features.png")


def plot_sh_adopted_lines(npz_path: str | Path, csv_path: str | Path,
                          destination: str | Path,
                          continuum_path: str | Path | None = None) -> Path:
    """Plot exactly the measured LIKELY/MARGINAL rows frozen in lines.csv."""
    wave, flux = _read_spectrum(npz_path)
    continuum = np.zeros_like(flux)
    if continuum_path is not None and Path(continuum_path).is_file():
        with np.load(continuum_path) as saved:
            if not np.array_equal(saved["wavelength"], wave):
                raise ValueError("display continuum wavelength grid differs from spectrum")
            continuum = np.asarray(saved["flux"], dtype=float)
    residual = flux - continuum
    with Path(csv_path).open(newline="", encoding="utf-8") as stream:
        rows = [row for row in csv.DictReader(stream)
                if is_kept_evidence(row.get("status"))]
    fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True,
                             constrained_layout=True)
    hypothesis = Path(csv_path).parents[4].name if len(Path(csv_path).parents) > 4 else "hypothesis"
    fig.suptitle(f"SH  ·  {hypothesis} adopted lines",
                 fontsize=17, color=INK, weight="bold")
    axes[0].plot(wave, flux, color=FLUX, lw=.65, rasterized=True)
    _style(axes[0], f"Observed spectrum  ·  {len(rows)} adopted line rows")
    axes[0].legend(handles=[
        Line2D([], [], color=PEAK, lw=1.5, label="Emission"),
        Line2D([], [], color=TROUGH, lw=1.5, label="Absorption"),
        Line2D([], [], color=INK, marker="o", linestyle="None", markersize=5,
               label="LIKELY"),
        Line2D([], [], color=INK, marker="s", linestyle="None", markersize=5,
               label="MARGINAL")], frameon=False, loc="upper right", ncol=4, fontsize=8)
    for ax, title in ((axes[1], "Emission lines"), (axes[2], "Absorption lines")):
        ax.plot(wave, residual, color=FLUX, lw=.65, alpha=.8, rasterized=True)
        ax.axhline(0, color=GRID, lw=.8)
        _style(ax, title, xlabel=ax is axes[-1])
    for index, row in enumerate(rows):
        center = _number(row.get("fitted_center"))
        amplitude = _number(row.get("amplitude"))
        if center is None or amplitude is None or not wave[0] <= center <= wave[-1]:
            raise ValueError("adopted SH line lacks an in-range measured center and amplitude")
        kind = 1 if amplitude >= 0 else 2
        color = PEAK if kind == 1 else TROUGH
        for ax in (axes[0], axes[kind]):
            ax.axvline(center, color=color, lw=.85, alpha=.52)
        ax = axes[kind]
        y = float(np.interp(center, wave, np.nan_to_num(residual, nan=0.0)))
        marker = "o" if row["status"] == "LIKELY" else "s"
        ax.scatter([center], [y], s=31, marker=marker, color=color, zorder=4)
        ax.annotate(f"{row['name']}  {center:.1f}", xy=(center, y),
                    xytext=(0, 13 + 13 * (index % 3)), textcoords="offset points",
                    rotation=62, fontsize=7, color=color, ha="left", va="bottom")
    axes[-1].set_xlim(wave[0], wave[-1])
    return _finish(fig, destination)
