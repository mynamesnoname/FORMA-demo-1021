import os

from typing import Optional, List
from pydantic import BaseModel, Field

from FORMA.core.config._utils import getenv_int
from FORMA.core.config.analysis_method import AuditMethod, InstrumentMethod, load_analysis_method

DEFAULT_AUDITOR_READ_HALF_ANGSTROM = AuditMethod().feature_read_half_angstrom
DEFAULT_FA_COMPOSITE_READ_HALF_ANGSTROM = AuditMethod().composite_read_half_angstrom


# ------------------------
# 分析参数配置
# ------------------------

class ParamsConfig(BaseModel):
    arm_name: Optional[List[str]]
    arm_wavelength_range: Optional[List[List[float]]]
    ocr: str
    harness_concurrency: int
    hypothesis_label_seed: Optional[str]
    evidence_graph_enabled: bool
    telemetry_enabled: bool
    self_evolve: bool
    failure_batch_size: int
    z_tolerance: float

    # ── Redrock 配置 ──
    rr_template_dir: Optional[str]
    archetype_dir: Optional[str]
    use_archetypes: bool
    rr_nminima: int
    rr_nnearest: int
    rr_omp_num_threads: int
    rr_archetype_legendre_degree: int = Field(default=2, ge=0)
    rr_archetype_legendre_prior_sigma: float = Field(default=0.1, ge=0, allow_inf_nan=False)
    assumed_snr_without_ivar: float = Field(default=InstrumentMethod().missing_noise_effective_snr_placeholder, gt=0, allow_inf_nan=False)

    # ── CWT 特征检测参数 ──
    cwt_snr_thresh: float
    cwt_min_ridge_length: int
    cwt_n_scales: int
    cwt_min_width: float
    cwt_max_width: float

    # JSON-owned read method; scientific line/zone bounds live in the ontology.
    # These values are rendered into each audit run message.
    auditor_read_half_angstrom: float = Field(default=DEFAULT_AUDITOR_READ_HALF_ANGSTROM, gt=0)
    fa_composite_read_half_angstrom: float = Field(
        default=DEFAULT_FA_COMPOSITE_READ_HALF_ANGSTROM, gt=0
    )

    @classmethod
    def from_env(cls) -> "ParamsConfig":
        method = load_analysis_method()
        arm_name = [arm.name for arm in method.instrument.arms] or None
        arm_wavelength_range = [
            [arm.wavelength_min_angstrom, arm.wavelength_max_angstrom]
            for arm in method.instrument.arms
        ] or None

        return cls(
            arm_name=arm_name,
            arm_wavelength_range=arm_wavelength_range,
            ocr=os.getenv("OCR") or "paddle",
            harness_concurrency=getenv_int("HARNESS_CONCURRENCY", 3),
            hypothesis_label_seed=os.getenv("HYPOTHESIS_LABEL_SEED") or None,
            evidence_graph_enabled=os.getenv("EVIDENCE_GRAPH", "false").lower() in ("true", "1", "yes"),
            telemetry_enabled=os.getenv("TELEMETRY_ENABLED", "true").lower() in ("true", "1", "yes"),
            self_evolve=os.getenv("SELF_EVOLVE", "false").lower() in ("true", "1", "yes"),
            failure_batch_size=getenv_int("FAILURE_BATCH_SIZE", 5),
            z_tolerance=method.evaluation.redshift_tolerance,

            # ── Redrock 配置 ──
            rr_template_dir=os.getenv("RR_TEMPLATE_DIR") or None,
            archetype_dir=os.getenv("ARCHETYPE_DIR") or None,
            use_archetypes=os.getenv("USE_ARCHETYPES", "true").lower() in ("true", "1", "yes"),
            rr_nminima=getenv_int("NMINIMA", 9),
            rr_nnearest=getenv_int("NNEAREST", 2),
            rr_omp_num_threads=getenv_int("OMP_NUM_THREADS", 1),
            rr_archetype_legendre_degree=getenv_int("RR_ARCHETYPE_LEGENDRE_DEGREE", 2),
            rr_archetype_legendre_prior_sigma=float(os.getenv("RR_ARCHETYPE_LEGENDRE_PRIOR_SIGMA", "0.1")),
            assumed_snr_without_ivar=method.instrument.missing_noise_effective_snr_placeholder,

            # ── CWT 特征检测参数 ──
            cwt_snr_thresh=method.cwt.wavelet_response_snr_threshold,
            cwt_min_ridge_length=method.cwt.min_ridge_length,
            cwt_n_scales=method.cwt.n_scales,
            cwt_min_width=method.cwt.min_wavelet_scale_pixels,
            cwt_max_width=method.cwt.max_wavelet_scale_pixels,
            auditor_read_half_angstrom=method.audit.feature_read_half_angstrom,
            fa_composite_read_half_angstrom=method.audit.composite_read_half_angstrom,
        )
