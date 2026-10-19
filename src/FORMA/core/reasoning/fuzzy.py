"""Calibrated fuzzy membership functions for spectral evidence (WP-012, WP-040).

光谱证据的校准模糊隶属函数（WP-012、WP-040）。

The membership **shapes** live here; the **numbers** are declared by the ontology
registry as empirical parameters and their values are resolved on every call by
:func:`FORMA.core.reasoning.ontology.rule_parameters.effective_parameter`.  An
endpoint that is the same physical bound as a rule threshold is derived from that
rule's operand, so one override moves the rule, this membership, the prompt that
renders it and the knowledge-base audit together.  Nothing in this module may
hard-code a judgement number again.

隶属函数的**形状**在此定义；**数值**由本体注册表声明为经验参数，并在每次调用时通过
``effective_parameter`` 解析。若某个端点与规则阈值为同一物理界，则它派生自该规则的操作数，
因此一次覆盖会同时移动规则、本隶属函数、渲染它的提示词与知识库审计。本模块不得再硬编码任何
判断数值。
"""

from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from FORMA.core.reasoning.ontology.rule_parameters import effective_parameter


def trapezoid_membership(
    x: float,
    left: float,
    center_left: float,
    center_right: float,
    right: float,
) -> float:
    """Trapezoidal membership in [0, 1] / [0, 1] 梯形隶属度。"""
    if x <= left or x >= right:
        return 0.0
    if center_left <= x <= center_right:
        return 1.0
    if x < center_left:
        return (x - left) / (center_left - left)
    return (right - x) / (right - center_right)


def threshold_membership(x: float, *, low: float = 0.0, high: float = 1.0) -> float:
    """Hard threshold expressed as a fuzzy step for numeric mixing.

    以模糊阶跃表达硬阈值，便于数值混合。
    """
    if x <= low:
        return 0.0
    if x >= high:
        return 1.0
    return (x - low) / (high - low)


class MembershipFunction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    kind: Literal["trapezoid", "threshold"]
    description: str
    parameters: Dict[str, float]
    justification: List[str] = Field(default_factory=list)

    def evaluate(self, x: float) -> float:
        if self.kind == "threshold":
            return threshold_membership(
                x,
                low=self.parameters.get("low", 0.0),
                high=self.parameters.get("high", 1.0),
            )
        return trapezoid_membership(
            x,
            left=self.parameters["left"],
            center_left=self.parameters["center_left"],
            center_right=self.parameters["center_right"],
            right=self.parameters["right"],
        )


class FuzzyPredicate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    membership: MembershipFunction
    input_path: str = Field(min_length=1)

    def evaluate(self, value: float) -> float:
        return self.membership.evaluate(value)


# ---------------------------------------------------------------------------
# Predicate definitions: which evidence field feeds which declared membership
# 谓词定义：哪个证据字段喂给哪个已声明隶属函数
# ---------------------------------------------------------------------------

#: ``membership id -> (predicate id, evidence input path, description)``.  The
#: *shapes* are structural and stay in code; every number comes from the registry.
#: ``隶属函数 id -> (谓词 id, 证据输入路径, 描述)``。形状属结构信息，留在代码中；所有数值
#: 来自注册表。
_PREDICATE_DEFINITIONS: Dict[str, tuple] = {
    "membership:offset-quality": (
        "predicate:offset-quality",
        "evidence.offset_angstrom",
        "wavelength offset quality",
    ),
    "membership:broad-qso": (
        "predicate:broad-qso",
        "evidence.fwhm_kms",
        "broad-line QSO width membership",
    ),
    "membership:detection-snr": (
        "predicate:detection-snr",
        "evidence.detection_snr",
        "detection SNR confidence",
    ),
    "membership:line-inventory": (
        "predicate:line-inventory",
        "evidence.n_likely_lines",
        "line inventory sufficiency",
    ),
}


def membership(membership_id: str) -> MembershipFunction:
    """Resolve one declared membership with its effective values.

    解析一个已声明隶属函数及其生效取值。

    Raises for a membership the registry does not declare, so a typo cannot
    silently fall back to a code constant.
    对注册表未声明的隶属函数抛错，使拼写错误不会静默回退到代码常量。
    """
    resolved = effective_parameter(membership_id)
    definition = _PREDICATE_DEFINITIONS[membership_id]
    return MembershipFunction(
        id=membership_id,
        kind=resolved["kind"],
        description=definition[2],
        parameters=resolved["parameters"],
        justification=[
            resolved["basis"],
            *(
                f"derived from {source}"
                for source in resolved["sources"].values()
                if source != "registry" and source != "config"
            ),
        ],
    )


def initial_predicates() -> List[FuzzyPredicate]:
    """The initial justified predicate set, resolved from the registry.

    初始论证过的谓词集合，取自注册表解析结果。

    Resolved on every call rather than frozen at import: a configuration payload
    loaded later in the process must be visible to every consumer (the
    single-hypothesis run message, the harness tools and the prompt audit).
    每次调用都重新解析而非在导入时冻结：进程后续加载的配置载荷必须对所有消费者可见
    （单假设运行消息、harness 工具与提示词审计）。
    """
    predicates: List[FuzzyPredicate] = []
    for membership_id, (predicate_id, input_path, _description) in (
        _PREDICATE_DEFINITIONS.items()
    ):
        predicates.append(
            FuzzyPredicate(
                id=predicate_id,
                membership=membership(membership_id),
                input_path=input_path,
            )
        )
    return predicates


def _evaluate(membership_id: str, value: float) -> float:
    return membership(membership_id).evaluate(value)


def offset_quality(offset_angstrom: float) -> float:
    """|offset| quality, shaped by the declared offset-quality trapezoid.

    |offset| 质量，形状由已声明的 offset-quality 梯形给出。
    """
    return _evaluate("membership:offset-quality", abs(offset_angstrom))


def broad_line_qso_membership(fwhm_kms: float) -> float:
    """Broad-line QSO membership, ramping between the declared width bounds.

    宽线 QSO 隶属度，在已声明的宽度界之间过渡。
    """
    return _evaluate("membership:broad-qso", fwhm_kms)


def snr_confidence(snr: float) -> float:
    """Detection SNR confidence, ramping up to the declared detection floor.

    检测 SNR 置信度，上升到已声明的检测下限。
    """
    return _evaluate("membership:detection-snr", snr)


def line_inventory_confidence(n_likely: int) -> float:
    """Line-inventory confidence, saturating above the declared floor.

    谱线清单置信度，在已声明下限之上饱和。
    """
    return _evaluate("membership:line-inventory", n_likely)


__all__ = [
    "FuzzyPredicate",
    "MembershipFunction",
    "broad_line_qso_membership",
    "initial_predicates",
    "line_inventory_confidence",
    "membership",
    "offset_quality",
    "snr_confidence",
    "threshold_membership",
    "trapezoid_membership",
]
