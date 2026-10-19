"""Versioned instrument, detection, fitting, audit and evaluation methods."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


ENV_PATH = "FORMA_ANALYSIS_METHOD_CONFIG"
DEFAULT_PATH = Path("config/analysis_method.json")


class ArmRange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    wavelength_min_angstrom: float = Field(gt=0, allow_inf_nan=False)
    wavelength_max_angstrom: float = Field(gt=0, allow_inf_nan=False)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        name = value.strip()
        if not name:
            raise ValueError("arm name must be nonempty")
        return name

    @model_validator(mode="after")
    def ordered(self):
        if self.wavelength_min_angstrom >= self.wavelength_max_angstrom:
            raise ValueError("arm wavelength minimum must be below maximum")
        return self


class InstrumentMethod(BaseModel):
    model_config = ConfigDict(extra="forbid")

    arms: list[ArmRange] = Field(default_factory=list)
    missing_noise_effective_snr_placeholder: float = Field(default=5.0, gt=0, allow_inf_nan=False)

    @model_validator(mode="after")
    def unique_arms(self):
        names = [arm.name.strip() for arm in self.arms]
        if len(set(names)) != len(names) or any(not name for name in names):
            raise ValueError("arm names must be nonempty and unique")
        return self


class CwtMethod(BaseModel):
    model_config = ConfigDict(extra="forbid")

    wavelet_response_snr_threshold: float = Field(default=5.0, gt=0, allow_inf_nan=False)
    min_ridge_length: int = Field(default=4, ge=1)
    n_scales: int = Field(default=24, ge=2)
    min_wavelet_scale_pixels: float = Field(default=1.0, gt=0, allow_inf_nan=False)
    max_wavelet_scale_pixels: float = Field(default=80.0, gt=0, allow_inf_nan=False)
    local_noise_half_window_pixels: int = Field(default=50, ge=1)
    local_noise_floor_fraction: float = Field(default=0.1, gt=0, le=1, allow_inf_nan=False)
    ridge_link_max_drift_pixels: int = Field(default=10, ge=0)
    reported_fwhm_min_pixels: float = Field(default=2.0, gt=0, allow_inf_nan=False)
    baseline_median_min_pixels: int = Field(default=51, ge=3)
    baseline_median_fraction_of_spectrum: float = Field(default=0.05, gt=0, le=1, allow_inf_nan=False)
    amplitude_error_estimate_fraction: float = Field(default=0.15, ge=0, allow_inf_nan=False)

    @model_validator(mode="after")
    def check_range(self):
        if self.min_wavelet_scale_pixels >= self.max_wavelet_scale_pixels:
            raise ValueError("CWT minimum width must be below maximum width")
        if self.min_ridge_length > self.n_scales:
            raise ValueError("CWT minimum ridge length exceeds number of scales")
        return self


class EvaluationMethod(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Shared by evaluation and the SH candidate search half-window.  Keep one
    # source so prompt rendering, pre-fitting and write validation agree.
    # 评估与 SH 候选搜索半窗口共用；提示词、预拟合和写入校验读取同一来源。
    redshift_tolerance: float = Field(default=0.01, ge=0, allow_inf_nan=False)
    implied_redshift_scatter_min_measured_lines: int = Field(default=2, ge=2)
    strong_feature_reference_fraction: float = Field(default=0.25, gt=0, lt=1, allow_inf_nan=False)
    dn4000_min_samples_per_band: int = Field(default=3, ge=1)


class GaussianFitMethod(BaseModel):
    model_config = ConfigDict(extra="forbid")

    single_window_half_angstrom: float = Field(default=200.0, gt=0, allow_inf_nan=False)
    doublet_window_half_angstrom: float = Field(default=300.0, gt=0, allow_inf_nan=False)
    doublet_separation_tolerance_angstrom: float = Field(default=5.0, ge=0, allow_inf_nan=False)
    single_min_samples: int = Field(default=10, ge=6)
    doublet_min_samples: int = Field(default=20, ge=9)
    initial_width_sigma_min_angstrom: float = Field(default=2.0, gt=0, allow_inf_nan=False)
    fitted_width_sigma_min_angstrom: float = Field(default=1.0, gt=0, allow_inf_nan=False)
    center_bound_half_angstrom: float = Field(default=50.0, gt=0, allow_inf_nan=False)
    single_max_function_evaluations: int = Field(default=5000, ge=1)
    doublet_max_function_evaluations: int = Field(default=10000, ge=1)
    width_3sigma_angstrom_by_class: dict[Literal["broad", "narrow", "both", "absorption"], float] = Field(default_factory=lambda: {
        "broad": 90.0, "narrow": 25.0, "both": 50.0, "absorption": 20.0,
    })

    @model_validator(mode="after")
    def consistent(self):
        if set(self.width_3sigma_angstrom_by_class) != {"broad", "narrow", "both", "absorption"}:
            raise ValueError("all four fitting width classes are required")
        if any(not (0 < value < float("inf")) for value in self.width_3sigma_angstrom_by_class.values()):
            raise ValueError("fitting widths must be positive and finite")
        if self.initial_width_sigma_min_angstrom < self.fitted_width_sigma_min_angstrom:
            raise ValueError("initial width sigma floor must not be below fitted floor")
        if min(self.single_window_half_angstrom, self.doublet_window_half_angstrom) <= 2 * self.initial_width_sigma_min_angstrom:
            raise ValueError("fit windows must exceed twice the initial width sigma floor")
        if self.center_bound_half_angstrom >= min(self.single_window_half_angstrom, self.doublet_window_half_angstrom):
            raise ValueError("center bound must fit within both windows")
        return self


class ContinuumMethod(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chebyshev_min_degree: int = Field(default=1, ge=0)
    chebyshev_max_degree: int = Field(default=10, ge=0)
    residual_clip_percentile: float = Field(default=95.0, gt=0, lt=100, allow_inf_nan=False)
    score_mad_weight: float = Field(default=10.0, ge=0, allow_inf_nan=False)
    score_abs_skew_target: float = Field(default=0.5, ge=0, allow_inf_nan=False)
    score_skew_weight: float = Field(default=5.0, ge=0, allow_inf_nan=False)
    score_degree_weight: float = Field(default=0.2, ge=0, allow_inf_nan=False)
    mask_half_width_in_fitted_sigma: float = Field(default=3.0, gt=0, allow_inf_nan=False)
    min_unmasked_samples: int = Field(default=20, ge=2)

    @model_validator(mode="after")
    def ordered(self):
        if self.chebyshev_min_degree > self.chebyshev_max_degree:
            raise ValueError("Chebyshev degree minimum exceeds maximum")
        return self


class LyalphaForestMethod(BaseModel):
    model_config = ConfigDict(extra="forbid")

    blueward_span_angstrom: float = Field(default=200.0, gt=0, allow_inf_nan=False)
    redward_reference_span_angstrom: float = Field(default=80.0, gt=0, allow_inf_nan=False)
    min_valid_blue_samples: int = Field(default=10, ge=2)
    vote_quorum: int = Field(default=3, ge=1)
    max_attempts_per_vote_seat: int = Field(default=2, ge=1)

    @model_validator(mode="after")
    def odd_vote_quorum(self):
        if self.vote_quorum % 2 == 0:
            raise ValueError("Lyα forest vote quorum must be odd")
        return self


class DoubletReviewMethod(BaseModel):
    model_config = ConfigDict(extra="forbid")

    context_margin_angstrom: float = Field(default=80.0, gt=0, allow_inf_nan=False)
    component_check_half_angstrom: float = Field(default=15.0, gt=0, allow_inf_nan=False)
    cahk_outer_reference_sigma: float = Field(default=3.0, gt=0, allow_inf_nan=False)
    min_valid_component_samples: int = Field(default=5, ge=2)
    vote_quorum: int = Field(default=3, ge=1)
    max_attempts_per_vote_seat: int = Field(default=2, ge=1)

    @model_validator(mode="after")
    def valid_review_window(self):
        if self.vote_quorum % 2 == 0:
            raise ValueError("doublet review vote quorum must be odd")
        if self.context_margin_angstrom < self.component_check_half_angstrom:
            raise ValueError("doublet context margin must cover the component check window")
        return self


class LineAlignmentMethod(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vote_quorum: int = Field(default=3, ge=1)
    max_attempts_per_vote_seat: int = Field(default=2, ge=1)
    outer_reference_sigma: float = Field(default=3.0, gt=0, allow_inf_nan=False)

    @model_validator(mode="after")
    def odd_vote_quorum(self):
        if self.vote_quorum % 2 == 0:
            raise ValueError("line alignment vote quorum must be odd")
        return self


class AuditMethod(BaseModel):
    model_config = ConfigDict(extra="forbid")

    feature_read_half_angstrom: float = Field(default=100.0, gt=0, allow_inf_nan=False)
    composite_read_half_angstrom: float = Field(default=200.0, gt=0, allow_inf_nan=False)
    verified_feature_merge_max_distance_angstrom: float = Field(default=2.0, ge=0, allow_inf_nan=False)
    missing_line_assessment_match_max_distance_angstrom: float = Field(default=1.0, ge=0, allow_inf_nan=False)
    oii_slope_search_half_angstrom: float = Field(default=25.0, gt=0, allow_inf_nan=False)
    lyalpha_forest: LyalphaForestMethod = Field(default_factory=LyalphaForestMethod)
    doublet_review: DoubletReviewMethod = Field(default_factory=DoubletReviewMethod)
    line_alignment: LineAlignmentMethod = Field(default_factory=LineAlignmentMethod)


class QsoType1Method(BaseModel):
    model_config = ConfigDict(extra="forbid")

    local_read_half_angstrom: float = Field(default=150.0, gt=0, allow_inf_nan=False)
    envelope_edge_sigma: float = Field(default=3.0, gt=0, allow_inf_nan=False)
    strength_vote_quorum: int = Field(default=3, ge=1)
    max_attempts_per_vote_seat: int = Field(default=2, ge=1)

    @model_validator(mode="after")
    def odd_vote_quorum(self):
        if self.strength_vote_quorum % 2 == 0:
            raise ValueError("QSO strength vote quorum must be odd")
        return self


class AnalysisMethodConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["forma-analysis-method-v2"]
    instrument: InstrumentMethod
    cwt: CwtMethod
    evaluation: EvaluationMethod
    gaussian_fit: GaussianFitMethod
    continuum: ContinuumMethod
    audit: AuditMethod
    qso_type1: QsoType1Method = Field(default_factory=QsoType1Method)


def load_analysis_method(path: str | Path | None = None) -> AnalysisMethodConfig:
    """Load explicit/env/default JSON; absent implicit file keeps prior code defaults.

    While a run's frozen set is installed and this call asks for that same source, the
    frozen snapshot is returned instead of re-reading the file, so an edit during the run
    cannot change a value (`core/config/frozen_parameters.py`).
    当本次运行的冻结集合已安装且这次调用请求的是同一来源时，直接返回冻结快照而不再读文件，因此
    运行中途的编辑无法改变取值（`core/config/frozen_parameters.py`）。
    """
    specified = path if path is not None else os.getenv(ENV_PATH)
    from FORMA.core.config.frozen_parameters import current as _frozen_current

    _frozen = _frozen_current()
    if _frozen is not None and path is None:
        return _frozen.analysis_method
    target = Path(specified) if specified else DEFAULT_PATH
    if not target.is_file():
        if specified or target.exists():
            raise FileNotFoundError(f"Analysis method config is not a file: {target}")
        return AnalysisMethodConfig(
            schema_version="forma-analysis-method-v2",
            instrument=InstrumentMethod(),
            cwt=CwtMethod(),
            evaluation=EvaluationMethod(),
            gaussian_fit=GaussianFitMethod(),
            continuum=ContinuumMethod(),
            audit=AuditMethod(),
        )
    return AnalysisMethodConfig.model_validate(json.loads(target.read_text(encoding="utf-8")))


def analysis_method_from_form_values(
    arm_name: str, arm_wavelength_range: str,
    cwt_snr_thresh: float, cwt_min_ridge: int,
    cwt_min_width: float, cwt_max_width: float, cwt_n_scales: int,
) -> AnalysisMethodConfig:
    """Build a validated per-session method payload from the WebUI fields."""
    names = [name.strip() for name in arm_name.split(",")]
    ranges = [item.strip() for item in arm_wavelength_range.split(",")]
    if not names or len(names) != len(ranges):
        raise ValueError("Arm names and wavelength ranges must have equal nonzero lengths")
    arms = []
    for name, item in zip(names, ranges):
        bounds = item.split("-")
        if len(bounds) != 2:
            raise ValueError(f"Invalid arm wavelength range: {item}")
        arms.append({
            "name": name,
            "wavelength_min_angstrom": float(bounds[0]),
            "wavelength_max_angstrom": float(bounds[1]),
        })
    base = load_analysis_method().model_dump(mode="json")
    base["instrument"]["arms"] = arms
    base["cwt"].update({
        "wavelet_response_snr_threshold": float(cwt_snr_thresh),
        "min_ridge_length": int(cwt_min_ridge),
        "n_scales": int(cwt_n_scales),
        "min_wavelet_scale_pixels": float(cwt_min_width),
        "max_wavelet_scale_pixels": float(cwt_max_width),
    })
    return AnalysisMethodConfig.model_validate(base)
