"""Validated model-call sampling policy; scientific thresholds do not live here."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


DEFAULT_PATH = Path("config/model_calls.json")
ENV_PATH = "FORMA_MODEL_CALL_CONFIG"


class ModelCallConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["forma-model-calls-v1"] = "forma-model-calls-v1"
    single_hypothesis_temperature: float = Field(default=0.1, ge=0, le=2, allow_inf_nan=False)
    feature_audit_temperature: float = Field(default=0.1, ge=0, le=2, allow_inf_nan=False)
    hypothesis_synthesis_temperature: float = Field(default=0.1, ge=0, le=2, allow_inf_nan=False)
    result_audit_temperature: float = Field(default=0.3, ge=0, le=2, allow_inf_nan=False)
    report_writer_temperature: float = Field(default=0.3, ge=0, le=2, allow_inf_nan=False)
    extraction_temperature: float = Field(default=0.0, ge=0, le=2, allow_inf_nan=False)
    self_evolve_temperature: float = Field(default=0.0, ge=0, le=2, allow_inf_nan=False)


def load_model_calls(path: str | Path | None = None) -> ModelCallConfig:
    """Load the model-call profile, honouring the run's frozen set (WP-041).

    加载模型调用档案；本次运行的冻结集合优先（WP-041）。
    """
    specified = path if path is not None else os.getenv(ENV_PATH)
    from FORMA.core.config.frozen_parameters import current as _frozen_current

    _frozen = _frozen_current()
    if _frozen is not None and path is None:
        return _frozen.model_calls
    target = Path(specified) if specified else DEFAULT_PATH
    if not target.is_file():
        if specified or target.exists():
            raise FileNotFoundError(f"Model call config is not a file: {target}")
        return ModelCallConfig()
    return ModelCallConfig.model_validate(json.loads(target.read_text(encoding="utf-8")))


def temperature_for(stage: str) -> float:
    field = f"{stage}_temperature"
    if field not in ModelCallConfig.model_fields:
        raise KeyError(f"Unknown model-call stage: {stage}")
    return getattr(load_model_calls(), field)
