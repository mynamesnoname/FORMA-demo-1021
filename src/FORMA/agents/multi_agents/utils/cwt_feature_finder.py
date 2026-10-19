"""
CWT-based feature detector using Ricker (Mexican hat) wavelet.
Multi-scale ridge detection replaces the Gaussian consensus voting in
simple_feature_finder.

The Ricker wavelet (second derivative of Gaussian) is a natural matched
filter for Gaussian-like spectral lines. At each scale the CWT coefficients
form a scale-space representation where:
  - Positive coefficients -> emission-like features
  - Negative coefficients -> absorption-like features

Ridge detection in this scale-space identifies features that persist across
multiple scales, providing a principled confidence metric.
"""

import os
import numpy as np
import pandas as pd
import pywt
from scipy.signal import find_peaks
from scipy.ndimage import median_filter
from FORMA.core.constants import (
    SIGMA_TO_FWHM as _SIGMA_TO_FWHM,
    SPEED_OF_LIGHT_KMS,
)

SIGMA_TO_FWHM = _SIGMA_TO_FWHM  # declared in FORMA.core.constants (2·√(2·ln 2))


# ---------------------------------------------------------------------------
# Local noise estimation (same as simple_feature_finder)
# ---------------------------------------------------------------------------

def _local_noise_mad(signal, half_window=None):
    """Sliding-window MAD noise estimate, robust against line features."""
    from FORMA.core.config.analysis_method import load_analysis_method
    method = load_analysis_method().cwt
    if half_window is None:
        half_window = method.local_noise_half_window_pixels
    n = len(signal)
    noise = np.zeros(n, dtype=np.float64)
    for i in range(n):
        lo = max(0, i - half_window)
        hi = min(n, i + half_window + 1)
        noise[i] = 1.4826 * np.median(np.abs(signal[lo:hi] - np.median(signal[lo:hi])))
    return np.maximum(noise, np.median(noise) * method.local_noise_floor_fraction)


# ---------------------------------------------------------------------------
# CWT ridge detection core
# ---------------------------------------------------------------------------

def _cwt_ridge_detection(signal, wavelength, scales, snr_thresh=None,
                         min_ridge_length=None, tol_pix=None):
    """
    Multi-scale CWT ridge detection using the Ricker wavelet.

    Parameters
    ----------
    signal : ndarray
        For emission pass ``residual = flux - continuum``.
        For absorption pass ``-residual`` (troughs become peaks).
    wavelength : ndarray
    scales : ndarray
        Wavelet scales in pixel units (log-spaced recommended).
    snr_thresh : float
        Minimum |CWT| / local_noise ratio.
    min_ridge_length : int
        Minimum number of scales a feature must persist across.
    tol_pix : int
        Max pixel drift allowed when linking detections across adjacent scales.

    Returns
    -------
    list of dict with keys: wavelength, amplitude, fwhm_pix,
                             ridge_length, snr
    """
    n = len(signal)
    if n < 10:
        return []

    from FORMA.core.config.analysis_method import load_analysis_method
    method = load_analysis_method().cwt
    if snr_thresh is None:
        snr_thresh = method.wavelet_response_snr_threshold
    if min_ridge_length is None:
        min_ridge_length = method.min_ridge_length
    if tol_pix is None:
        tol_pix = method.ridge_link_max_drift_pixels
    noise = _local_noise_mad(signal, half_window=method.local_noise_half_window_pixels)

    # ---- CWT with Ricker (Mexican hat) wavelet via PyWavelets ----
    cwt_mat, _ = pywt.cwt(signal, scales, 'mexh')  # (n_scales, n_pixels)

    # ---- Find local maxima at each scale ----
    detections = []  # (pixel_idx, scale_idx, cwt_value, snr)
    for i in range(len(scales)):
        row = cwt_mat[i, :]
        peaks_idx, _ = find_peaks(row, width=1)
        for pi in peaks_idx:
            local_snr = float(row[pi]) / noise[pi] if noise[pi] > 0 else 0.0
            if local_snr >= snr_thresh:
                detections.append((int(pi), i, float(row[pi]), local_snr))

    if not detections:
        return []

    # ---- Build ridges by linking detections across adjacent scales ----
    detections.sort(key=lambda x: (x[1], x[0]))  # sort by (scale_idx, pixel)

    ridges = []  # list of [(pixel, scale_idx, val, snr), ...]
    for det in detections:
        pi, si, val, snr = det
        matched = False
        for ridge in ridges:
            last_pi, last_si, _, _ = ridge[-1]
            if last_si == si - 1 and abs(pi - last_pi) <= tol_pix:
                ridge.append(det)
                matched = True
                break
            # Same-scale collision (should be rare with width=1):
            # keep the higher-SNR detection
            if last_si == si and abs(pi - last_pi) <= tol_pix:
                if snr > ridge[-1][3]:
                    ridge[-1] = det
                matched = True
                break
        if not matched:
            ridges.append([det])

    # ---- Extract representative parameters from each ridge ----
    results = []
    for ridge in ridges:
        if len(ridge) < min_ridge_length:
            continue

        pixels = [d[0] for d in ridge]
        scales_detected = [scales[d[1]] for d in ridge]

        rep_idx = int(np.median(pixels))
        rep_wave = float(wavelength[rep_idx])
        rep_amp = float(signal[rep_idx])

        med_scale = float(np.median(scales_detected))
        fwhm_pix = max(med_scale * SIGMA_TO_FWHM, method.reported_fwhm_min_pixels)

        max_snr = max(d[3] for d in ridge)

        results.append({
            'wavelength': rep_wave,
            'amplitude': rep_amp,
            'fwhm_pix': fwhm_pix,
            'ridge_length': len(ridge),
            'snr': max_snr,
        })

    return results


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def find_features_cwt(wavelength, flux, snr_thresh=None, min_ridge_length=None,
                      n_scales=None, min_scale=None, max_scale=None,
                      verbose=True):
    """
    CWT-based emission and absorption line detection.

    Parameters
    ----------
    wavelength : ndarray
    flux : ndarray
        Original spectrum flux (NOT residual).
    snr_thresh : float
        Minimum CWT SNR to keep a detection.
    min_ridge_length : int
        Minimum number of scales for a valid ridge (≥ 2).
    n_scales : int
        Number of logarithmically-spaced wavelet scales.
    min_scale, max_scale : float
        Scale range in pixel units.  min_scale ≈ narrowest line FWHM / 2·√(2·ln 2).
    verbose : bool

    Returns
    -------
    records_emission, records_absorption : list[dict]
    """
    n = len(flux)
    if n < 10:
        return [], []

    # Rough continuum via wide median filter -> residual
    from FORMA.core.config.analysis_method import load_analysis_method
    method = load_analysis_method().cwt
    if snr_thresh is None:
        snr_thresh = method.wavelet_response_snr_threshold
    if min_ridge_length is None:
        min_ridge_length = method.min_ridge_length
    if n_scales is None:
        n_scales = method.n_scales
    if min_scale is None:
        min_scale = method.min_wavelet_scale_pixels
    if max_scale is None:
        max_scale = method.max_wavelet_scale_pixels
    median_width = max(
        method.baseline_median_min_pixels,
        int(n * method.baseline_median_fraction_of_spectrum),
    )
    if median_width % 2 == 0:
        median_width += 1
    baseline = median_filter(flux, size=median_width)
    residual = flux - baseline  # emission > 0, absorption < 0

    scales = np.logspace(np.log10(min_scale), np.log10(max_scale), n_scales)
    mean_dwave = np.median(np.diff(wavelength))

    # Emission: positive features in residual
    em_candidates = _cwt_ridge_detection(
        residual, wavelength, scales,
        snr_thresh=snr_thresh, min_ridge_length=min_ridge_length)

    # Absorption: positive features in -residual (troughs -> peaks)
    ab_candidates = _cwt_ridge_detection(
        -residual, wavelength, scales,
        snr_thresh=snr_thresh, min_ridge_length=min_ridge_length)

    def _build_records(candidates, feature_type):
        # The measured band and its two boundaries are declared once, with one owner
        # per boundary (`core/reasoning/ontology/feature_width.py`); the matrix and
        # this finder therefore label a feature identically.  The upper boundary is
        # the strict-broad rule, not the width-consistency pivot the finder used to
        # read: both held 2000 km/s, but only one of them owns that boundary.
        # 实测档及其两个边界只声明一次，每个边界只有一个所有者
        # （`core/reasoning/ontology/feature_width.py`），因此矩阵与本处给同一特征打同一标签。
        # 上界属于严格宽线规则，而不是本处此前读取的宽度一致性分界：两者数值都是 2000 km/s，
        # 但只有前者拥有该边界。
        from FORMA.core.reasoning.ontology.feature_width import band_of
        records = []
        for c in candidates:
            amp = c['amplitude']
            if feature_type == 'absorption':
                amp = -abs(amp)
            fwhm_a = c['fwhm_pix'] * mean_dwave
            fwhm_km_s = fwhm_a / c['wavelength'] * SPEED_OF_LIGHT_KMS if c['wavelength'] > 0 else 0
            records.append({
                'wavelength': c['wavelength'],
                'wavelength_err': float(mean_dwave),
                'FWHM_A': float(fwhm_a),
                'FWHM_km_s': float(fwhm_km_s),
                'amplitude': float(amp),
                # Uncertainties are magnitudes and must never carry the sign
                # of an absorption-line amplitude.
                'amplitude_err': float(abs(amp) * method.amplitude_error_estimate_fraction),
                'width_class': band_of(fwhm_km_s),
                'feature_type': feature_type,
                'ridge_length': c['ridge_length'],
                'snr': c['snr'],
                'left_neighbor': 'None',
                'right_neighbor': 'None',
                'is_pseudo_peak': False,
                'pseudo_reason': '',
                'covered_troughs': 0,
                'trough_centers': '',
            })
        return records

    records_em = _build_records(em_candidates, 'emission')
    records_ab = _build_records(ab_candidates, 'absorption')

    if verbose:
        print(f"[cwt_finder] CWT ridge detection "
              f"(SNR≥{snr_thresh}, ridge≥{min_ridge_length}, "
              f"scales={n_scales}×[{min_scale:.0f}..{max_scale:.0f}]px): "
              f"{len(records_em)} peaks, {len(records_ab)} troughs")
        if records_em:
            rl_dist = {}
            for r in records_em:
                rl = r['ridge_length']
                rl_dist[rl] = rl_dist.get(rl, 0) + 1
            print(f"  peak ridge_length distribution: {rl_dist}")
        if records_ab:
            rl_dist = {}
            for r in records_ab:
                rl = r['ridge_length']
                rl_dist[rl] = rl_dist.get(rl, 0) + 1
            print(f"  trough ridge_length distribution: {rl_dist}")

    return records_em, records_ab


# ---------------------------------------------------------------------------
# Drop-in replacement for run_simple_feature_detection
# ---------------------------------------------------------------------------

def run_cwt_feature_detection(
    output_dir, file_name, wavelength, flux,
    ivar=None, effective_snr=None,
    absorption_detection_params=None,
    emission_detection_params=None,
    verbose=True,
    artifact_subdir="visual_interpreter",
):
    """
    CWT-based feature detection -- drop-in replacement for
    ``run_simple_feature_detection``.  Interface fully compatible.

    Returns
    -------
    dict with keys: df_emission, df_absorption, records_emission,
                    records_absorption, wave_remaining, flux_remaining
    """
    wavelength = np.asarray(wavelength, dtype=np.float64)
    flux = np.asarray(flux, dtype=np.float64)

    # `None` means "use the validated declaration", which the block below reads.
    # The literals that used to sit here (5.0, 2, 24, 1.0, 80.0) disagreed with
    # the declared detection threshold and ridge length while looking like
    # defaults, so an override could not reach the detector.
    # `None` 表示"使用已校验的声明"，由下方代码块读取。此前这里的字面量（5.0、2、24、1.0、
    # 80.0）看起来像默认值，却与已声明的检测门槛和 ridge 长度不一致，使覆盖无法到达检测器。
    snr_thresh = None
    min_ridge_length = None
    n_scales = None
    min_scale = None
    max_scale = None

    if emission_detection_params:
        snr_thresh = emission_detection_params.get('snr_thresh', snr_thresh)
        min_ridge_length = emission_detection_params.get('min_ridge_length', min_ridge_length)
        n_scales = emission_detection_params.get('n_scales', n_scales)
        min_scale = emission_detection_params.get('min_scale', min_scale)
        max_scale = emission_detection_params.get('max_scale', max_scale)

    records_em, records_ab = find_features_cwt(
        wavelength, flux,
        snr_thresh=snr_thresh,
        min_ridge_length=min_ridge_length,
        n_scales=n_scales,
        min_scale=min_scale,
        max_scale=max_scale,
        verbose=verbose)

    # ---- Build DataFrames (columns aligned with simple_feature_finder output) ----
    def _to_df(records):
        if not records:
            return pd.DataFrame()
        df = pd.DataFrame(records)
        # Rank by feature strength.  Absorption amplitudes are negative, so a
        # signed descending rank would incorrectly put the shallowest trough first.
        df['amplitude_rank'] = df['amplitude'].abs().rank(
            ascending=False, method='min'
        ).astype(int)
        df = df.sort_values('wavelength').reset_index(drop=True)
        return df

    df_em = _to_df(records_em)
    df_ab = _to_df(records_ab)

    def _save_csv(df, suffix):
        # Both catalogs are always written, even when a kind has no features.
        # Returning early left a run with no `_emission.csv` at all, and the
        # evidence-graph builder requires both files, so a spectrum with no
        # emission feature crashed the whole analysis under EVIDENCE_GRAPH=true
        # (reproduced on `.test_set/DESI/BGS/fits_input/54.fits`, 2026-10-14).
        # The header-only file keeps the artifact set deterministic, and every
        # reader already treats "no rows" as "no features".
        # 两类目录始终写出，即使某一类没有任何特征。此前的提前返回会让一次运行完全没有
        # `_emission.csv`，而证据图构建器要求两个文件都在，因此在 EVIDENCE_GRAPH=true 下
        # 没有发射特征的光谱会让整轮分析崩溃（2026-10-14 在
        # `.test_set/DESI/BGS/fits_input/54.fits` 复现）。只含表头的文件使产物集合确定，
        # 而所有读取方本就把"没有行"当作"没有特征"。
        out_cols = ['index', 'amplitude_rank', 'wavelength', 'wavelength_err',
                    'FWHM_A', 'FWHM_km_s', 'amplitude', 'amplitude_err',
                    'integrated_flux', 'flux_at_center',
                    'ridge_length', 'snr',
                    'width_class', 'feature_type',
                    'left_neighbor', 'right_neighbor',
                    'is_pseudo_peak', 'pseudo_reason',
                    'covered_troughs', 'trough_centers']
        df_out = pd.DataFrame(index=range(len(df)))
        for col in out_cols:
            if col in df.columns:
                df_out[col] = df[col]
            elif col == 'index':
                df_out[col] = range(len(df))
            elif col == 'amplitude_rank' and 'amplitude' in df.columns:
                df_out[col] = df['amplitude'].abs().rank(
                    ascending=False, method='min'
                ).astype(int)
            elif col == 'integrated_flux' and {'amplitude', 'FWHM_A'} <= set(df.columns):
                df_out[col] = df['amplitude'] * df['FWHM_A'] / SIGMA_TO_FWHM * np.sqrt(2 * np.pi)
            elif col == 'flux_at_center' and 'amplitude' in df.columns:
                df_out[col] = df['amplitude']
            else:
                # An empty catalog has no source columns at all; every derived
                # column still has to exist so the header-only file keeps the
                # full schema its readers validate against.
                # 空目录根本没有任何来源列；派生列仍须存在，使只含表头的文件保留读取方校验
                # 所需的完整 schema。
                df_out[col] = df[col] if col in df.columns else ''
        # The band column carries a declared vocabulary; an undeclared value means
        # this deterministic producer has a bug, so it fails loudly instead of
        # writing a label no consumer declares.
        # 档位列携带已声明词表；未声明取值意味着这个确定性产出方存在缺陷，因此大声失败，而不是写
        # 下一个没有任何消费者声明的标签。
        from FORMA.core.reasoning.ontology.feature_width import validate as validate_bands
        if 'width_class' in df_out.columns:
            validate_bands(df_out['width_class'].tolist())
        if not artifact_subdir or os.path.basename(artifact_subdir) != artifact_subdir:
            raise ValueError("CWT artifact_subdir must be one directory name")
        path = os.path.join(output_dir, artifact_subdir, f"{file_name}_{suffix}.csv")
        df_out.to_csv(path, index=False)

    _save_csv(df_em, 'emission')
    _save_csv(df_ab, 'absorption')

    return {
        'df_emission': df_em,
        'df_absorption': df_ab,
        'records_emission': records_em,
        'records_absorption': records_ab,
        'wave_remaining': wavelength.copy(),
        'flux_remaining': flux.copy(),
    }
