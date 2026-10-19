"""Validated, overridable rule-operand thresholds (ontology schema v4).

受校验、可覆盖的规则操作数界（本体 schema v4）。

``OperandRecord.threshold`` declares the registry default for an *empirical*
convention — a velocity or wavelength bound an adapter counts against — and this
module provides the override surface the decision owner asked for: a JSON payload
whose keys are ``<rule_id> → {<operand_id>: <value>}``, loaded through an explicit
path, ``FORMA_RULE_PARAMETERS``, or ``config/rule_parameters.json``, in that order.

``OperandRecord.threshold`` 为*经验*约定（适配器计数所用的速度或波长界）声明注册表默认值；
本模块提供决策人要求的覆盖面：一份 JSON 载荷，键为 ``<rule_id> → {<operand_id>:
<value>}``，按 显式路径 → ``FORMA_RULE_PARAMETERS`` → ``config/rule_parameters.json``
的顺序加载。

Guards, each load-bearing rather than decorative / 守卫（每条都承重）：

* Only operands that **declare** a ``threshold`` are configurable; naming an
  arbitrary operand or rule is an error, so a typo cannot silently override a
  value the registry never declared.
* Values must be finite and positive, and the unit comes from the record — a
  payload cannot change the meaning of a bound by re-unitifying it.
* Every rule evaluation records the effective value, unit, source and payload
  digest in its trace, so two runs that used different bounds remain
  distinguishable after the fact.

只有**声明了** ``threshold`` 的操作数可配置；点名任意操作数或规则即报错，故拼写错误不会
静默覆盖注册表从未声明的值。值必须有限且为正，单位取自记录——载荷不能通过改单位来改变
界的含义。每次规则求值都把生效值、单位、来源与载荷摘要写进 trace，因此使用不同界的两次
运行事后仍可区分。
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field, model_validator

from FORMA.core.reasoning.ontology.registry import ONTOLOGY
from FORMA.core.reasoning.ontology.schema import OntologyRegistry

ENV_PATH = "FORMA_RULE_PARAMETERS"
DEFAULT_PATH = Path("config/rule_parameters.json")

_RULE_ID = r"^[a-z]+:[a-z0-9][a-z0-9_-]*$"
_OPERAND_ID = r"^[a-z][a-z0-9_]*$"
_PARAMETER_ID = r"^(?:membership|parameter):[a-z][a-z0-9_.-]*$"
_PARAMETER_NAME = r"^[a-z][a-z0-9_]*$"

# These records retain their own rule outcomes and trace ids, but the numeric
# width boundary has one writable owner.  Aliases are read-only and resolve to
# that owner's effective value on every call.
_DERIVED_WIDTH_BOUNDS = {
    ("rule:formal-qso2-nev-requirement", "has_broad_lines"):
        ("rule:formal-qso1-no-broad-line", "n_broad_lines_at_or_above_fwhm_limit"),
    ("rule:formal-qso-broad-width", "fwhm_kms"):
        ("rule:formal-width-class-match", "width_consistency_score"),
    ("rule:formal-galaxy-broad-emission-fatal", "broad_emission_fwhm_kms"):
        ("rule:formal-width-class-match", "width_consistency_score"),
}


class RuleParametersConfig(BaseModel):
    """The validated override payload / 受校验的覆盖载荷。"""

    model_config = ConfigDict(extra="forbid")

    #: v1 payloads may only override rule operand bounds.  v2 adds the
    #: ``parameters`` section, which supplies values for empirical parameters the
    #: registry declares (fuzzy memberships and scalar tolerances); a v1 payload
    #: carrying that section is refused rather than silently ignored.
    #: v1 载荷只能覆盖规则操作数界；v2 增加 ``parameters`` 段，为注册表声明的经验参数
    #: （模糊隶属函数与标量容差）提供取值。带该段的 v1 载荷会被拒绝，而不是被静默忽略。
    schema_version: Literal[
        "forma-rule-parameters-v1", "forma-rule-parameters-v2"
    ]
    overrides: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    parameters: Dict[str, Dict[str, float]] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _shape_is_valid(self):
        import re

        if self.parameters and self.schema_version != "forma-rule-parameters-v2":
            raise ValueError(
                "declared parameters need schema_version forma-rule-parameters-v2"
            )
        for parameter_id, values in self.parameters.items():
            if not re.fullmatch(_PARAMETER_ID, parameter_id):
                raise ValueError(f"invalid declared parameter id {parameter_id!r}")
            if not isinstance(values, dict) or not values:
                raise ValueError(
                    f"{parameter_id!r}: parameter overrides must be a nonempty mapping"
                )
            for name, value in values.items():
                if not re.fullmatch(_PARAMETER_NAME, name):
                    raise ValueError(f"invalid parameter name {name!r}")
                if not math.isfinite(float(value)):
                    raise ValueError(f"{parameter_id}.{name}: value must be finite")
        for rule_id, operands in self.overrides.items():
            if not re.fullmatch(_RULE_ID, rule_id):
                raise ValueError(f"invalid rule id {rule_id!r}")
            if not isinstance(operands, dict) or not operands:
                raise ValueError(f"rule {rule_id!r}: overrides must be a nonempty mapping")
            for operand_id, value in operands.items():
                if not re.fullmatch(_OPERAND_ID, operand_id):
                    raise ValueError(f"invalid operand id {operand_id!r}")
                number = float(value)
                if not math.isfinite(number) or number <= 0:
                    raise ValueError(
                        f"{rule_id}.{operand_id}: threshold must be finite and positive"
                    )
        return self


#: Process-level cache; tests reset it with :func:`reset_rule_parameters_cache`.
#: 进程级缓存；测试用 :func:`reset_rule_parameters_cache` 重置。
_CACHE: Optional[Tuple[RuleParametersConfig, Optional[str], Optional[str]]] = None
_CACHE_MARKER = object()


def reset_rule_parameters_cache() -> None:
    global _CACHE
    _CACHE = None


def _find_operand(
    rule_id: str, operand_id: str, registry: OntologyRegistry
):
    rule = next((r for r in registry.formal_rules if r.id == rule_id), None)
    if rule is None:
        raise KeyError(f"unknown rule id {rule_id!r} in rule parameters")
    operand = next((o for o in rule.operands if o.id == operand_id), None)
    if operand is None:
        raise KeyError(f"rule {rule_id!r} has no operand {operand_id!r}")
    return operand


def _find_parameter(parameter_id: str, registry: OntologyRegistry):
    record = next(
        (item for item in registry.empirical_parameters if item.id == parameter_id),
        None,
    )
    if record is None:
        raise KeyError(f"unknown empirical parameter id {parameter_id!r}")
    return record


def _validate_parameter_shape(
    record: Any, values: Dict[str, float]
) -> None:
    """Refuse a value set that breaks the declared membership shape.

    拒绝破坏已声明隶属函数形状的取值集合。
    """
    if record.kind == "scalar":
        if values["value"] <= 0:
            raise ValueError(f"{record.id}: scalar value must be positive")
    elif record.kind == "interval":
        if values["low"] >= values["high"]:
            raise ValueError(f"{record.id}: low must be below high")
        if record.unit == "dimensionless" and values["low"] <= 0:
            raise ValueError(f"{record.id}: ratio bounds must be positive")
        if record.id == "parameter:outflow-blueshift-window" and values["high"] > 0:
            raise ValueError(f"{record.id}: upper velocity offset must not be redshifted")
    elif record.kind == "threshold":
        if values["low"] >= values["high"]:
            raise ValueError(
                f"{record.id}: low must be below high "
                f"({values['low']} >= {values['high']})"
            )
        if values["low"] < 0 or values["high"] <= 0:
            raise ValueError(f"{record.id}: membership bounds must be non-negative")
    elif record.kind == "trapezoid":
        if not (
            values["left"] < values["center_left"] <= values["center_right"]
            < values["right"]
        ):
            raise ValueError(
                f"{record.id}: trapezoid corners must satisfy left < center_left "
                "<= center_right < right"
            )


def _validated_overrides(
    config: RuleParametersConfig, registry: OntologyRegistry
) -> None:
    """Refuse any override the registry does not declare as a knob.

    拒绝任何注册表未声明为旋钮的覆盖。
    """
    for parameter_id, values in config.parameters.items():
        record = _find_parameter(parameter_id, registry)
        unknown = set(values) - set(record.parameters)
        if unknown:
            raise ValueError(
                f"{parameter_id}: undeclared parameter(s) {sorted(unknown)}; "
                "only declared parameters are configurable"
            )
        for name in values:
            source = record.sources.get(name)
            if source is not None and source.kind == "operand_threshold":
                raise ValueError(
                    f"{parameter_id}.{name} derives from "
                    f"{source.rule_id}.{source.operand_id}; override the source "
                    "rule operand instead"
                )
    for rule_id, operands in config.overrides.items():
        for operand_id in operands:
            operand = _find_operand(rule_id, operand_id, registry)
            if operand.threshold is None:
                raise ValueError(
                    f"{rule_id}.{operand_id} has no declared threshold; "
                    "only declared operand bounds are configurable"
                )
            owner = _DERIVED_WIDTH_BOUNDS.get((rule_id, operand_id))
            if owner is not None:
                raise ValueError(
                    f"{rule_id}.{operand_id} derives from {owner[0]}.{owner[1]}; "
                    "override the source rule operand instead"
                )
    # Validate the *effective* shape. A rule override can invert a derived
    # membership ramp even when no membership field is explicitly overridden.
    for record in registry.empirical_parameters:
        merged = dict(record.parameters)
        for name, source in record.sources.items():
            if source.kind == "operand_threshold":
                operand = _find_operand(source.rule_id, source.operand_id, registry)
                merged[name] = float(config.overrides.get(source.rule_id, {}).get(
                    source.operand_id, operand.threshold
                ))
            elif source.value is not None:
                merged[name] = float(source.value)
        merged.update(config.parameters.get(record.id, {}))
        _validate_parameter_shape(record, merged)
    narrow = config.overrides.get(
        "rule:formal-width-class-contradiction", {}
    ).get("claimed_broad_fwhm_kms", _find_operand(
        "rule:formal-width-class-contradiction", "claimed_broad_fwhm_kms", registry
    ).threshold)
    general = config.overrides.get(
        "rule:formal-qso1-no-broad-line", {}
    ).get("n_broad_lines_at_or_above_fwhm_limit", _find_operand(
        "rule:formal-qso1-no-broad-line",
        "n_broad_lines_at_or_above_fwhm_limit", registry
    ).threshold)
    if narrow >= general:
        raise ValueError(
            "width boundaries must satisfy narrow < general broad < strict broad"
        )


def load_rule_parameters(
    path: str | Path | None = None,
    environ: Any = None,
    registry: OntologyRegistry = ONTOLOGY,
) -> Tuple[RuleParametersConfig, Optional[str], Optional[str]]:
    """Load the override payload; absent implicit file means no overrides.

    加载覆盖载荷；隐式默认文件缺失即视为无覆盖。

    Returns ``(config, source_path, sha256)`` where ``source_path`` is None for the
    empty/default case and ``sha256`` is the payload digest (None when empty).
    返回 ``(config, source_path, sha256)``；空/默认时 ``source_path`` 为 None，
    ``sha256`` 为载荷摘要（空时为 None）。
    """
    env = os.environ if environ is None else environ
    specified = path if path is not None else env.get(ENV_PATH)
    from FORMA.core.config.frozen_parameters import current as _frozen_current

    _frozen = _frozen_current()
    if _frozen is not None and path is None and environ is None:
        _frozen_source = _frozen.sources.get("rule_parameters")
        return (
            _frozen.rule_parameters,
            _frozen_source,
            _frozen.digests.get("rule_parameters"),
        )
    target = Path(specified) if specified else DEFAULT_PATH
    if not target.is_file():
        if specified:
            raise FileNotFoundError(f"Rule parameters file not found: {target}")
        empty = RuleParametersConfig(
            schema_version="forma-rule-parameters-v2", overrides={}, parameters={}
        )
        return empty, None, None

    import hashlib

    text = target.read_text(encoding="utf-8")
    config = RuleParametersConfig.model_validate(json.loads(text))
    _validated_overrides(config, registry)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    result = (config, str(target), digest)
    global _CACHE
    _CACHE = result
    return result


def current_rule_parameters(
    registry: OntologyRegistry = ONTOLOGY,
) -> Tuple[RuleParametersConfig, Optional[str], Optional[str]]:
    global _CACHE
    # Process cache predates run scopes.  It must never supersede the active
    # spectrum's snapshot, even when an earlier run populated the cache.
    from FORMA.core.config.frozen_parameters import current as frozen_current
    if frozen_current() is not None:
        return load_rule_parameters(registry=registry)
    if _CACHE is None:
        _CACHE = load_rule_parameters(registry=registry)
    return _CACHE


def effective_operand_threshold(
    rule_id: str,
    operand_id: str,
    registry: OntologyRegistry = ONTOLOGY,
) -> Dict[str, Any]:
    """Return the effective bound for one declared knob, plus its provenance.

    返回某个已声明旋钮的生效界及其来源。

    The result is ``{value, unit, source, source_path, basis, payload_digest}``
    with ``source`` being ``"registry"`` (the record default) or ``"config"`` (an
    override).  Raises for unknown or undeclared knobs so a typo cannot silently
    fall back to a different value.
    结果为 ``{value, unit, source, source_path, basis, payload_digest}``；``source``
    为 ``"registry"``（记录默认）或 ``"config"``（覆盖）。对未知或未声明的旋钮抛错，
    使拼写错误不会静默回退到别的值。
    """
    operand = _find_operand(rule_id, operand_id, registry)
    if operand.threshold is None:
        raise ValueError(
            f"{rule_id}.{operand_id} has no declared threshold; it is not a knob"
        )
    owner = _DERIVED_WIDTH_BOUNDS.get((rule_id, operand_id))
    if owner is not None:
        resolved = effective_operand_threshold(*owner, registry=registry)
        return {
            **resolved,
            "source": f"{resolved['source']}:{owner[0]}.{owner[1]}",
        }
    config, source_path, digest = current_rule_parameters(registry)
    override = config.overrides.get(rule_id, {}).get(operand_id)
    if override is not None:
        return {
            "value": float(override),
            "unit": operand.threshold_unit,
            "source": "config",
            "source_path": source_path,
            "basis": operand.threshold_basis,
            "payload_digest": digest,
        }
    return {
        "value": float(operand.threshold),
        "unit": operand.threshold_unit,
        "source": "registry",
        "source_path": None,
        "basis": operand.threshold_basis,
        "payload_digest": digest,
    }


def effective_parameter(
    parameter_id: str,
    registry: OntologyRegistry = ONTOLOGY,
) -> Dict[str, Any]:
    """Return one declared empirical parameter's effective values and provenance.

    返回某个已声明经验参数的生效取值与来源。

    A literal parameter can be configured directly. A derived parameter always
    reads its source rule operand's *effective* bound; direct overrides of derived
    endpoints are rejected at load. ``sources``
    records which of those supplied each value, and ``payload_digest`` is the
    digest of the payload that produced the set, so a run can state exactly which
    numbers it used.
    字面量参数可以直接覆盖；派生端点只能读取来源规则操作数的*生效*界，加载时拒绝直接覆盖。
    ``sources`` 记录每个值来自哪一层，``payload_digest`` 是产生该
    取值集合的载荷摘要，使每次运行都能说明它究竟用了哪些数值。
    """
    record = _find_parameter(parameter_id, registry)
    config, source_path, digest = current_rule_parameters(registry)
    overrides = config.parameters.get(parameter_id, {})
    effective: Dict[str, float] = {}
    sources: Dict[str, str] = {}
    for name, default in record.parameters.items():
        if name in overrides:
            effective[name] = float(overrides[name])
            sources[name] = "config"
            continue
        source = record.sources.get(name)
        if source is None or source.kind == "literal":
            effective[name] = (
                float(source.value) if source is not None and source.value is not None
                else float(default)
            )
            sources[name] = "registry"
            continue
        resolved = effective_operand_threshold(
            source.rule_id, source.operand_id, registry
        )
        effective[name] = float(resolved["value"])
        sources[name] = f"{resolved['source']}:{source.rule_id}.{source.operand_id}"
    _validate_parameter_shape(record, effective)
    return {
        "id": record.id,
        "name": record.name,
        "kind": record.kind,
        "unit": record.unit,
        "parameters": effective,
        "sources": sources,
        "basis": record.basis,
        "payload_digest": digest,
        "source_path": source_path,
    }


def effective_parameters(
    registry: OntologyRegistry = ONTOLOGY,
) -> Dict[str, Dict[str, Any]]:
    """Every declared empirical parameter, keyed by id / 按 id 索引的全部已声明参数。"""
    return {
        record.id: effective_parameter(record.id, registry)
        for record in registry.empirical_parameters
    }


def rule_operand_thresholds(
    rule: Any, registry: OntologyRegistry = ONTOLOGY
) -> Dict[str, Dict[str, Any]]:
    """Effective bounds for every knob declared by one rule.

    某条规则声明的每个旋钮的生效界。
    """
    return {
        operand.id: effective_operand_threshold(rule.id, operand.id, registry)
        for operand in rule.operands
        if operand.threshold is not None
    }


def operand_thresholds_summary(
    registry: OntologyRegistry = ONTOLOGY,
) -> Dict[str, Any]:
    """The effective value of every declared knob, for the trace header.

    每个已声明旋钮的生效值，供 trace 头部使用。
    """
    config, source_path, digest = current_rule_parameters(registry)
    knobs = {}
    for rule in registry.formal_rules:
        for operand in rule.operands:
            if operand.threshold is None:
                continue
            resolved = effective_operand_threshold(rule.id, operand.id, registry)
            knobs[f"{rule.id}.{operand.id}"] = {
                "value": resolved["value"],
                "unit": resolved["unit"],
                "source": resolved["source"],
                "source_path": resolved["source_path"],
                "basis": resolved["basis"],
            }
    return {
        "schema": config.schema_version,
        "payload_digest": digest,
        "source_path": source_path,
        "overrides": config.overrides,
        "effective": knobs,
    }


def empirical_parameters_summary(
    registry: OntologyRegistry = ONTOLOGY,
) -> Dict[str, Any]:
    """The effective value of every declared empirical parameter.

    每个已声明经验参数的生效值。

    Read by the prompt-authority audit and available to any stage that renders a
    judgement number, so prose and prompts cite the value the run actually used.
    供提示词权威审计读取，也可供任何渲染判断数值的阶段使用，使散文与提示词引用本次运行
    实际使用的取值。
    """
    config, source_path, digest = current_rule_parameters(registry)
    resolved = effective_parameters(registry)
    return {
        "schema": config.schema_version,
        "payload_digest": digest,
        "source_path": source_path,
        "overrides": config.parameters,
        "effective": {
            parameter_id: {
                "kind": item["kind"],
                "unit": item["unit"],
                "parameters": item["parameters"],
                "sources": item["sources"],
            }
            for parameter_id, item in resolved.items()
        },
    }


__all__ = [
    "ENV_PATH",
    "DEFAULT_PATH",
    "RuleParametersConfig",
    "current_rule_parameters",
    "effective_operand_threshold",
    "effective_parameter",
    "effective_parameters",
    "empirical_parameters_summary",
    "load_rule_parameters",
    "operand_thresholds_summary",
    "reset_rule_parameters_cache",
    "rule_operand_thresholds",
]

def rule_condition_bound(
    rule_id: str,
    registry: OntologyRegistry = ONTOLOGY,
) -> Optional[float]:
    """Effective bound of a rule's first numeric condition, or ``None``.

    某条规则首个数值条件的生效界；无法确定时返回 ``None``。

    Shared by the prompt renderers so that a message and the rule it describes
    cannot drift: both read the same declared operand, and a configuration
    override moves the prose and the evaluation together.  `None` means the rule
    does not state a numeric first condition, which is not an error — callers
    decide their own fallback.

    由各提示词渲染处共用，使消息与它所描述的规则不会分叉：二者读取同一个已声明操作数，
    一次配置覆盖同时移动散文与求值。返回 ``None`` 表示该规则没有数值化的首个条件，这并非
    错误——回退由调用方决定。
    """
    rule = next((item for item in registry.formal_rules if item.id == rule_id), None)
    if rule is None or not rule.conditions:
        return None
    condition = rule.conditions[0]
    if not isinstance(condition.rhs, (int, float)):
        return None
    operand = next((item for item in rule.operands if item.id == condition.lhs), None)
    if operand is None or operand.threshold != condition.rhs:
        return float(condition.rhs)
    try:
        return float(effective_operand_threshold(
            rule_id, condition.lhs, registry=registry)["value"])
    except (KeyError, ValueError):
        return float(condition.rhs)
