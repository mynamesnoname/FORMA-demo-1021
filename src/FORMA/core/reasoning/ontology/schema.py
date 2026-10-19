"""Pydantic schema for the versioned spectral ontology registry (WP-009).

版本化谱线本体注册表的 Pydantic schema（WP-009）。

Identifiers are stable slugs, never display text: a prompt may render a line as
``[O III]b`` but consumers key on ``line:oiii-5008``.  The registry validates
duplicate and dangling identifiers before it is allowed to be used.
标识符是稳定 slug，而非展示文本：prompt 可把谱线渲染为 ``[O III]b``，但消费方以
``line:oiii-5008`` 为键。注册表必须先通过重复与悬空标识符校验才能使用。
"""

from __future__ import annotations

import math
import re
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator

ONTOLOGY_SCHEMA_VERSION = "forma-spectral-ontology-v6"
#: v6 adds signed and dimensionless empirical intervals for diagnostic reference
#: windows. v5 documents remain readable with the same parameter defaults.
#: v5 adds the ``empirical_parameters`` family: judgement numbers that encode a
#: convention rather than a measurement are *declared* here (id, unit, default,
#: basis, consumer) and their values may be supplied by a validated payload, so
#: ontology, prompts, skills and the knowledge base cannot disagree with the value
#: a run actually used.  v4 added the typed, overridable
#: ``OperandRecord.threshold`` bound; v1-v3 documents stay readable with
#: ``threshold=None`` (the adapter then has no declared bound and treats it as
#: unconfigured).  v3 added the defect-grade annotation fields on
#: ``FormalRuleRecord``; v1 and v2 documents stay readable and take the documented
#: defaults.  Documents below v5 load with an empty parameter family.
#: v5 增加 ``empirical_parameters`` 族：编码"约定"而非"测量"的判断数值在此**声明**
#: （id、单位、默认值、依据、消费者），其取值可由受校验的载荷提供，从而使本体、提示词、
#: 技能与知识库不可能与本次运行实际使用的值不一致。v4 增加了 ``OperandRecord.threshold``
#: 类型化可覆盖界；v3 增加了缺陷评级标注字段；更低版本文档继续可读并取默认值，v5 以下的
#: 文档以空参数族载入。
SUPPORTED_ONTOLOGY_SCHEMA_VERSIONS = frozenset(
    {
        ONTOLOGY_SCHEMA_VERSION,
        "forma-spectral-ontology-v5",
        "forma-spectral-ontology-v4",
        "forma-spectral-ontology-v3",
        "forma-spectral-ontology-v2",
        "forma-spectral-ontology-v1",
    }
)
#: Migration rule for v1 documents: v2 added the `skylines`, `width3sigma` and
#: `indices` families and the optional `DoubletRecord.amplitude_ratio` field;
#: a v1 document reads with those lists empty and ratios unset, and all v1
#: records keep their original ids and values.
#: v1 文档的迁移规则：v2 新增 `skylines`、`width3sigma`、`indices` 三个族与可选的
#: `DoubletRecord.amplitude_ratio` 字段；v1 文档以空列表与未设比率读入，全部 v1
#: 记录的 id 与数值保持不变。

_ID_PATTERN = re.compile(r"^[a-z]+:[a-z0-9][a-z0-9_-]*$")

Citation = Dict[str, str]


class LineRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = Field(min_length=1)
    rest_wavelength: float
    transition: Optional[str] = None
    species: Optional[str] = None
    ionization_ev: Optional[float] = None
    line_type: Literal["emission", "absorption", "both"] = "emission"
    width_class: Literal["broad", "narrow", "both", "absorption", "unknown"] = "unknown"
    anchor_priority: Optional[int] = Field(default=None, ge=1)
    excluded_from_anchor: bool = False
    citations: List[Citation] = Field(default_factory=list)

    @model_validator(mode="after")
    def _valid_identifier(self):
        if not _ID_PATTERN.fullmatch(self.id):
            raise ValueError(f"invalid ontology ID {self.id!r}")
        return self


class DoubletRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = Field(min_length=1)
    component_ids: List[str] = Field(min_length=2)
    rest_separation: Optional[float] = None
    amplitude_ratio_note: Optional[str] = None
    #: Numeric amplitude ratio of the *second* component over the *first*
    #: (component_ids order), when the KB states one.  Added in v2.
    #: 当 KB 给出数值时，*第二*分量相对*第一*分量的振幅比（component_ids 顺序）。v2 新增。
    amplitude_ratio: Optional[float] = Field(default=None, gt=0.0)
    #: Inclusive acceptance window for the amplitude ratio of the *first*
    #: component over the *second* (``[low, high]``): the range inside which the
    #: doublet identification is treated as physically consistent.  ``None``
    #: when the KB states no numeric window.
    #: *第一*分量相对*第二*分量振幅比的闭区间接受窗口（``[low, high]``），
    #: 即在该区间内认为双线识别物理自洽。KB 未给出数值窗口时为 ``None``。
    ratio_window: Optional[List[float]] = None
    #: Which fit-width class the doublet's Gaussians start from.  Resolved
    #: against the fit-window map (`analysis_method.gaussian_fit.
    #: width_3sigma_angstrom_by_class`, historically `fitwin:*`) to an initial
    #: sigma, so the *choice* is declared here instead of hard-coded per doublet
    #: in the harness.  Default `narrow` preserves the behaviour of every doublet
    #: that states nothing; a component line's own `width_class="absorption"`
    #: (Ca K/H) is why `doublet:cahk` declares `absorption` rather than `broad`.
    #: 该双线的高斯拟合从哪个宽度类别起步。它经拟合窗口映射（`analysis_method.gaussian_fit.
    #: width_3sigma_angstrom_by_class`，历史上为 `fitwin:*`）解析为初始 sigma，因此这个
    #: *选择*在此声明，而不是在 harness 里按双线硬编码。默认 `narrow` 保持所有未声明双线的
    #: 行为；`doublet:cahk` 声明为 `absorption` 而非 `broad`，依据是其分量线自身已声明
    #: `width_class="absorption"`。
    fit_width_class: Literal["narrow", "broad", "both", "absorption"] = "narrow"
    citations: List[Citation] = Field(default_factory=list)

    @model_validator(mode="after")
    def _valid_identifier(self):
        if not _ID_PATTERN.fullmatch(self.id):
            raise ValueError(f"invalid ontology ID {self.id!r}")
        if len(self.component_ids) != 2:
            raise ValueError(f"doublet {self.id!r} must have exactly two components")
        if self.ratio_window is not None:
            if len(self.ratio_window) != 2:
                raise ValueError(f"doublet {self.id!r} ratio_window needs [low, high]")
            if self.ratio_window[0] > self.ratio_window[1]:
                raise ValueError(f"doublet {self.id!r} ratio_window is inverted")
        return self


class ClassRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    citations: List[Citation] = Field(default_factory=list)

    @model_validator(mode="after")
    def _valid_identifier(self):
        if not _ID_PATTERN.fullmatch(self.id):
            raise ValueError(f"invalid ontology ID {self.id!r}")
        return self


class RuleRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    kind: Literal["coverage", "quality", "ionization", "classification"]
    description: str = Field(min_length=1)
    citations: List[Citation] = Field(default_factory=list)

    @model_validator(mode="after")
    def _valid_identifier(self):
        if not _ID_PATTERN.fullmatch(self.id):
            raise ValueError(f"invalid ontology ID {self.id!r}")
        return self


class SkylineRecord(BaseModel):
    """A fixed-wavelength atmospheric feature (airglow, skyline, O₂ band).

    固定波长的大气特征（气辉、天光线、O₂ 带）。

    Added in v2 so the skyline cross-check table lives in the registry instead
    of only in ``kb/lines.md`` prose.
    v2 新增，使天光线交叉检查表置于注册表而非仅存在于 ``kb/lines.md`` 散文。
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = Field(min_length=1)
    kind: Literal["emission", "absorption", "band"] = "emission"
    wavelength_obs: float
    #: Upper bound for band records; single lines leave it unset.
    #: 带记录的波长上限；单线记录不设。
    wavelength_max: Optional[float] = None
    note: Optional[str] = None
    citations: List[Citation] = Field(default_factory=list)

    @model_validator(mode="after")
    def _valid_identifier(self):
        if not _ID_PATTERN.fullmatch(self.id):
            raise ValueError(f"invalid ontology ID {self.id!r}")
        if self.kind == "band" and self.wavelength_max is None:
            raise ValueError(f"skyline band {self.id!r} requires wavelength_max")
        if (
            self.wavelength_max is not None
            and self.wavelength_max < self.wavelength_obs
        ):
            raise ValueError(
                f"skyline {self.id!r}: wavelength_max must not be below wavelength_obs"
            )
        return self


class Width3SigmaRecord(BaseModel):
    """The 3σ fitting-window default used by ``tools.fit_peak`` per width class.

    ``tools.fit_peak`` 按宽度类别使用的 3σ 拟合窗口默认值。

    Added in v2 so the fit-window lookup computes from the registry
    (`query.build_width3sigma_map`), which resolves the method profile's
    ``gaussian_fit.width_3sigma_angstrom_by_class`` at call time.
    v2 新增，使 ``tools.py::_WIDTH_3SIGMA_MAP`` 由注册表计算。
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    width_class: Literal["broad", "narrow", "both", "absorption"]
    width_3sigma_A: float = Field(gt=0.0)
    citations: List[Citation] = Field(default_factory=list)

    @model_validator(mode="after")
    def _valid_identifier(self):
        if not _ID_PATTERN.fullmatch(self.id):
            raise ValueError(f"invalid ontology ID {self.id!r}")
        return self


class IndexBandRecord(BaseModel):
    """Rest-frame band windows of a spectral index (e.g. Dn4000).

    光谱指数（如 Dn4000）的静止系波段窗口。

    Added in v2; the index *value* thresholds remain reference-only prose in
    the KB, so only the band definition is owned here.
    v2 新增；指数*数值*阈值在 KB 中仅为参考，故此处只收录波段定义。
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = Field(min_length=1)
    blue_low: float
    blue_high: float
    red_low: float
    red_high: float
    unit: str = Field(default="Angstrom")
    citations: List[Citation] = Field(default_factory=list)

    @model_validator(mode="after")
    def _valid_identifier(self):
        if not _ID_PATTERN.fullmatch(self.id):
            raise ValueError(f"invalid ontology ID {self.id!r}")
        if self.blue_high <= self.blue_low or self.red_high <= self.red_low:
            raise ValueError(f"index band {self.id!r} has non-increasing windows")
        return self


class OperandRecord(BaseModel):
    """A named, typed input a formal rule reads from evidence.

    正式规则从证据中读取的具名、带类型的输入。

    ``missing_meaning`` is always treated as *unknown* by the evaluator: a rule
    may never turn a missing measurement into a ``fail`` (absence is not negative
    evidence).
    ``missing_meaning`` 在执行器眼中一律是*未知*：规则绝不把缺失的测量变成 ``fail``
    （缺失不是负面证据）。
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    description: str = Field(min_length=1)
    unit: Optional[str] = None
    missing_meaning: Literal["unknown", "not_applicable"] = "unknown"
    #: Numeric bound the operand is computed against (v4).  An empirical
    #: convention — not a physical constant — so it is declared here for the
    #: registry default but overridable through a validated rule-parameter
    #: payload; every rule evaluation records which effective value it used.
    #: 操作数计算所用的数值界（v4）。这是经验约定而非物理常数，故在此声明为注册表
    #: 默认值，但可通过受校验的规则参数载荷覆盖；每次规则求值都记录所用生效值。
    threshold: Optional[float] = Field(default=None, allow_inf_nan=False, gt=0)
    #: Unit of ``threshold``, distinct from ``unit`` when the operand itself is a
    #: count but its bound is a velocity or wavelength (e.g. a count of lines at
    #: or above a km/s bound).
    #: ``threshold`` 的单位；当操作数本身是计数而其界是速度或波长时，与 ``unit``
    #: 不同（例如"达到某 km/s 界的谱线计数"）。
    threshold_unit: Optional[str] = None
    #: Scientific basis or citation for the bound, when it is a reasoned
    #: convention rather than a measurement.
    #: 该界的科学依据或引用（当其为经过论证的约定而非测量值时）。
    threshold_basis: Optional[str] = None

    @model_validator(mode="after")
    def _valid_identifier(self):
        if not re.fullmatch(r"[a-z][a-z0-9_]*", self.id):
            raise ValueError(f"invalid operand id {self.id!r}")
        return self

    @model_validator(mode="after")
    def _threshold_requires_a_unit(self):
        if self.threshold is not None and not self.threshold_unit:
            raise ValueError(
                f"operand {self.id!r} declares a threshold but no threshold_unit"
            )
        if self.threshold is None and self.threshold_unit:
            raise ValueError(
                f"operand {self.id!r} declares threshold_unit without a threshold"
            )
        return self


class ConditionRecord(BaseModel):
    """One machine-evaluable condition over declared operands.

    对已声明操作数的一条可机检条件。

    ``rhs`` is either a numeric literal or the id of another operand, so a
    relation like "Ca K amplitude ≤ Ca H amplitude" is expressible.  ``rhs_high``
    is required for ``between``.
    ``rhs`` 是数值字面量或另一操作数的 id，因此可以表达 "Ca K 振幅 ≤ Ca H 振幅"
    这类关系；``between`` 要求提供 ``rhs_high``。
    """

    model_config = ConfigDict(extra="forbid")

    lhs: str
    operator: Literal["lt", "le", "gt", "ge", "eq", "between"]
    rhs: Union[float, str]
    rhs_high: Optional[float] = None
    note: Optional[str] = None


class OutcomeSpec(BaseModel):
    """Three-state verdict tags and their evidence polarities.

    三态结论标签及其证据极性。

    Unknown outcomes are always neutral — this is a load-bearing guarantee of the
    evaluator, so it is not configurable here.
    未知结果恒为中性——这是执行器的承重保证，因此此处不可配置。
    """

    model_config = ConfigDict(extra="forbid")

    pass_verdict: str = Field(min_length=1)
    fail_verdict: str = Field(min_length=1)
    unknown_verdict: str = "unknown — no evidence contribution"
    pass_polarity: Literal["positive", "negative", "neutral"] = "positive"
    fail_polarity: Literal["positive", "negative", "neutral"] = "negative"


class FormalRuleRecord(BaseModel):
    """A machine-checkable diagnostic constraint or graded rule.

    可机检的诊断约束或分级规则。

    Hard constraints are physical requirements; graded diagnostics may yield
    ``unknown`` and must say how unknown inputs are handled rather than
    treating absence as negative evidence.
    硬约束是物理要求；分级诊断可产生 ``unknown``，且必须说明未知输入如何处理，不能把
    缺失当作负面证据。

    ``operands`` + ``conditions`` + ``outcomes`` make the rule evaluable against
    observations (2026-10-11 review); ``satisfied_when`` selects conjunctive
    ("all") or disjunctive ("any") satisfaction.  A rule without conditions is
    shape-valid but not machine-evaluable, and the registry validator reports it.
    ``operands`` + ``conditions`` + ``outcomes`` 使规则可针对观测求值（2026-10-11
    评审）；``satisfied_when`` 选择合取（"all"）或析取（"any"）满足方式。没有条件的规则
    形状合法但不可机检，注册表校验器会报告。
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = Field(min_length=1)
    kind: Literal["hard_constraint", "graded_diagnostic"] = "hard_constraint"
    premise_ids: List[str] = Field(default_factory=list)
    applies_to_ids: List[str] = Field(default_factory=list)
    units: Dict[str, str] = Field(default_factory=dict)
    conclusion: str = Field(min_length=1)
    conclusion_polarity: Literal["positive", "negative", "neutral"] = "neutral"
    unknown_handling: Optional[str] = None
    contradiction_group: Optional[str] = None
    provenance: List[Citation] = Field(default_factory=list)
    #: Typed evaluation contract (2026-10-11) / 类型化求值契约（2026-10-11）。
    operands: List[OperandRecord] = Field(default_factory=list)
    conditions: List[ConditionRecord] = Field(default_factory=list)
    outcomes: Optional[OutcomeSpec] = None
    satisfied_when: Literal["all", "any"] = "all"
    #: Which pipeline stage supplies this rule's operands (2026-10-11 deferred
    #: rule review).  ``synthesis`` rules are evaluated by the synthesis-verdict
    #: adapter (`ontology/runtime.py`); ``harness`` rules by the per-hypothesis
    #: adapter (`ontology/harness_rules.py`); ``auditor`` / ``argumentation``
    #: rules are evaluated with stage-local operands and are named by their
    #: stage where no stage adapter runs them yet.
    #: 提供本规则操作数的流水线阶段（2026-10-11 deferred 规则评审）。``synthesis``
    #: 规则由 synthesis 裁决适配器（`ontology/runtime.py`）求值；``harness`` 规则由
    #: 逐假设适配器（`ontology/harness_rules.py`）求值；``auditor`` /
    #: ``argumentation`` 规则以阶段本地操作数求值，并在尚无阶段适配器处按阶段具名。
    runtime_scope: Literal["synthesis", "harness", "auditor", "argumentation"] = "auditor"
    #: Defect-grade annotations (defect-grade contract §5.1).  The weight is
    #: diagnostic information only — it never accumulates into a grade sum —
    #: and a rule may only cap the final grade to LOW when ``fatal_eligible``
    #: is explicitly declared together with its scientific basis.
    #: 缺陷评级标注（缺陷评级契约 §5.1）。权重仅为诊断信息，绝不参与"求和后分档"；
    #: 只有显式声明 ``fatal_eligible`` 并给出科学依据的规则才可把最终评级封顶为 LOW。
    severity_weight: Optional[float] = Field(default=None, ge=0.0)
    severity_basis: Optional[str] = None
    fatal_eligible: bool = False

    @model_validator(mode="after")
    def _valid_identifier(self):
        if not _ID_PATTERN.fullmatch(self.id):
            raise ValueError(f"invalid ontology ID {self.id!r}")
        if self.kind == "graded_diagnostic" and not self.unknown_handling:
            raise ValueError(
                f"graded diagnostic {self.id!r} must declare unknown_handling"
            )
        if not self.provenance:
            raise ValueError(f"formal rule {self.id!r} must carry provenance")
        if self.severity_weight is not None:
            if not math.isfinite(self.severity_weight):
                raise ValueError(
                    f"formal rule {self.id!r}: severity_weight must be finite"
                )
            if not self.severity_basis:
                raise ValueError(
                    f"formal rule {self.id!r}: severity_weight requires "
                    "severity_basis"
                )
        if self.fatal_eligible and not self.severity_basis:
            raise ValueError(
                f"formal rule {self.id!r}: fatal_eligible requires severity_basis"
            )
        operand_ids = [operand.id for operand in self.operands]
        if len(operand_ids) != len(set(operand_ids)):
            raise ValueError(f"formal rule {self.id!r} has duplicate operand ids")
        for condition in self.conditions:
            if condition.lhs not in operand_ids:
                raise ValueError(
                    f"formal rule {self.id!r}: condition lhs "
                    f"{condition.lhs!r} is not a declared operand"
                )
            if isinstance(condition.rhs, str) and condition.rhs not in operand_ids:
                raise ValueError(
                    f"formal rule {self.id!r}: condition rhs operand "
                    f"{condition.rhs!r} is not declared"
                )
            if condition.operator == "between" and condition.rhs_high is None:
                raise ValueError(
                    f"formal rule {self.id!r}: 'between' condition requires rhs_high"
                )
        if self.conditions and self.outcomes is None:
            raise ValueError(
                f"formal rule {self.id!r}: evaluable conditions require an "
                "OutcomeSpec"
            )
        return self


class ParameterSource(BaseModel):
    """Where one declared parameter's value comes from (v5).

    已声明参数取值的来源（v5）。

    ``literal`` carries the registry default.  ``operand_threshold`` reads the
    *effective* bound of a declared operand, so a value that is the same physical
    bound as a rule threshold is derived rather than restated: one override then
    moves the rule, the membership and every rendered message together.  A bound
    that only exists inside a rule condition is given a typed operand threshold
    instead of a second source kind, so there is exactly one derivation path.
    ``literal`` 携带注册表默认值；``operand_threshold`` 读取某个已声明操作数的*生效*界。
    这样"与规则阈值同一物理界"的参数是**派生**而非重述：一次覆盖同时移动规则、隶属函数与所有
    渲染出去的消息。只存在于规则条件里的界应补成类型化操作数界，而不是再开一种来源，从而保持
    只有一条派生路径。
    """

    model_config = ConfigDict(extra="forbid")

    kind: Literal["literal", "operand_threshold"]
    value: Optional[float] = Field(default=None, allow_inf_nan=False)
    rule_id: Optional[str] = None
    operand_id: Optional[str] = None

    @model_validator(mode="after")
    def _fields_match_kind(self):
        if self.kind == "literal":
            if self.value is None:
                raise ValueError("a literal parameter source needs a value")
        elif not (self.rule_id and self.operand_id):
            raise ValueError(
                "an operand_threshold source needs rule_id and operand_id"
            )
        return self


class EmpiricalParameterRecord(BaseModel):
    """A declared empirical judgement number (v5).

    已声明的经验判断数值（v5）。

    Empirical parameters encode a convention — how this pipeline chooses to
    judge — so the registry declares them and a validated payload may supply their
    values.  Physical and structural facts (line wavelengths, doublet separations,
    skyline wavelengths, band edges, unit conversions) are deliberately *not*
    representable here: they are measurements of the world, not choices.
    经验参数编码的是约定——本流水线选择如何判断——因此由注册表声明、由受校验载荷提供取值。
    物理与结构事实（谱线波长、双线间距、天光波长、波段边界、单位换算）刻意**不可**在此表示：
    它们是对世界的测量，不是选择。

    ``parameters`` is the declared default set; ``sources`` overrides the source of
    individual parameters (absent entries stay literal defaults).
    ``parameters`` 是声明的默认值集合；``sources`` 覆盖个别参数的来源（缺省项按字面默认值）。
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    kind: Literal["scalar", "interval", "threshold", "trapezoid"]
    unit: str = Field(min_length=1)
    parameters: Dict[str, float]
    sources: Dict[str, ParameterSource] = Field(default_factory=dict)
    basis: str = Field(min_length=1)
    citations: List[Citation] = Field(default_factory=list)
    consumers: List[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _valid_id_and_shape(self):
        if self.kind in {"scalar", "interval"}:
            if not re.fullmatch(r"parameter:[a-z][a-z0-9_.-]*", self.id):
                raise ValueError(
                    f"a scalar/interval empirical parameter needs a 'parameter:' id, got "
                    f"{self.id!r}"
                )
            expected = {"value"} if self.kind == "scalar" else {"low", "high"}
            if set(self.parameters) != expected:
                raise ValueError(
                    f"{self.kind} parameter {self.id!r} declares {sorted(expected)}"
                )
            if self.kind == "interval" and self.parameters["low"] >= self.parameters["high"]:
                raise ValueError(f"{self.id!r}: low must be below high")
        else:
            if not re.fullmatch(r"membership:[a-z][a-z0-9_.-]*", self.id):
                raise ValueError(
                    f"a {self.kind} membership needs a 'membership:' id, got "
                    f"{self.id!r}"
                )
            expected = (
                {"low", "high"} if self.kind == "threshold"
                else {"left", "center_left", "center_right", "right"}
            )
            if set(self.parameters) != expected:
                raise ValueError(
                    f"{self.id!r} must declare {sorted(expected)}, got "
                    f"{sorted(self.parameters)}"
                )
            values = self.parameters
            if self.kind == "threshold":
                if values["low"] >= values["high"]:
                    raise ValueError(
                        f"{self.id!r}: low must be below high "
                        f"({values['low']} >= {values['high']})"
                    )
            elif not (
                values["left"] < values["center_left"] <= values["center_right"]
                < values["right"]
            ):
                raise ValueError(
                    f"{self.id!r}: trapezoid corners must satisfy left < "
                    "center_left <= center_right < right"
                )
        unknown = set(self.sources) - set(self.parameters)
        if unknown:
            raise ValueError(
                f"{self.id!r}: sources for undeclared parameters {sorted(unknown)}"
            )
        return self


class OntologyRegistry(BaseModel):
    """The initial structured registry / 初始结构化注册表。"""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = ONTOLOGY_SCHEMA_VERSION
    updated: str
    lines: List[LineRecord] = Field(default_factory=list)
    doublets: List[DoubletRecord] = Field(default_factory=list)
    classes: List[ClassRecord] = Field(default_factory=list)
    rules: List[RuleRecord] = Field(default_factory=list)
    formal_rules: List[FormalRuleRecord] = Field(default_factory=list)
    #: v2 families; empty for v1 documents (migration rule above).
    #: v2 族；v1 文档中为空（见上方迁移规则）。
    skylines: List[SkylineRecord] = Field(default_factory=list)
    width3sigma: List[Width3SigmaRecord] = Field(default_factory=list)
    indices: List[IndexBandRecord] = Field(default_factory=list)
    #: v5 family; empty for earlier documents (migration rule above).
    #: v5 族；更早版本文档中为空（见上方迁移规则）。
    empirical_parameters: List[EmpiricalParameterRecord] = Field(default_factory=list)

    @model_validator(mode="after")
    def _reject_unsupported_version(self):
        if self.schema_version not in SUPPORTED_ONTOLOGY_SCHEMA_VERSIONS:
            raise ValueError(
                f"unsupported ontology schema version {self.schema_version!r}"
            )
        return self

    def line_index(self) -> Dict[str, LineRecord]:
        return {line.id: line for line in self.lines}

    def validate(self) -> List[str]:
        """Return every duplicate or dangling-identifier problem.

        返回全部重复或悬空标识符问题。
        """
        problems: List[str] = []
        seen: Dict[str, str] = {}
        for kind, records in (
            ("line", self.lines),
            ("doublet", self.doublets),
            ("class", self.classes),
            ("rule", self.rules),
            ("formal_rule", self.formal_rules),
            ("skyline", self.skylines),
            ("width3sigma", self.width3sigma),
            ("index", self.indices),
            ("empirical_parameter", self.empirical_parameters),
        ):
            for record in records:
                previous = seen.get(record.id)
                if previous is not None:
                    problems.append(
                        f"duplicate ontology id {record.id!r} ({previous} and {kind})"
                    )
                else:
                    seen[record.id] = kind

        line_ids = self.line_index()
        for doublet in self.doublets:
            for component_id in doublet.component_ids:
                if component_id not in line_ids:
                    problems.append(
                        f"doublet {doublet.id!r} references dangling line "
                        f"{component_id!r}"
                    )

        names: Dict[str, str] = {}
        for line in self.lines:
            previous = names.get(line.name)
            if previous is not None:
                problems.append(
                    f"ambiguous line alias {line.name!r}: used by both "
                    f"{previous!r} and {line.id!r}; name resolution would be "
                    "silently order-dependent"
                )
            else:
                names[line.name] = line.id

        for line in self.lines:
            if not line.citations:
                problems.append(f"line {line.id!r} has no citation/provenance")

        known_ids = set(seen)
        for rule in self.formal_rules:
            for premise_id in (*rule.premise_ids, *rule.applies_to_ids):
                if premise_id not in known_ids:
                    problems.append(
                        f"formal rule {rule.id!r} references dangling concept "
                        f"{premise_id!r}"
                    )
            if not rule.conditions:
                problems.append(
                    f"formal rule {rule.id!r} has no machine-evaluable "
                    "conditions; add typed operands/conditions so the evaluator "
                    "can produce pass/fail/unknown against observations"
                )
        hard_by_group: Dict[str, List[FormalRuleRecord]] = {}
        for rule in self.formal_rules:
            if rule.kind == "hard_constraint" and rule.contradiction_group:
                hard_by_group.setdefault(rule.contradiction_group, []).append(rule)
        for group, rules in hard_by_group.items():
            polarities = {rule.conclusion_polarity for rule in rules}
            if polarities - {"neutral"} and len(polarities) > 1:
                problems.append(
                    f"contradictory hard constraints in group {group!r}: "
                    f"{[rule.id for rule in rules]}"
                )

        for record in self.empirical_parameters:
            if not record.citations:
                problems.append(
                    f"empirical parameter {record.id!r} has no citation/provenance"
                )
            for parameter_name, source in record.sources.items():
                if source.kind == "literal":
                    continue
                if source.kind == "operand_threshold":
                    rule = next(
                        (item for item in self.formal_rules
                         if item.id == source.rule_id), None,
                    )
                    operand_ids = {op.id for op in rule.operands} if rule else set()
                    if source.operand_id not in operand_ids:
                        problems.append(
                            f"empirical parameter {record.id!r} derives "
                            f"{parameter_name!r} from dangling operand "
                            f"{source.rule_id!r}/{source.operand_id!r}"
                        )

        for record in (*self.lines, *self.doublets, *self.classes, *self.rules):
            if hasattr(record, "rest_wavelength"):
                value = record.rest_wavelength
                if value != value or value in (float("inf"), float("-inf")):
                    problems.append(f"line {record.id!r} has a non-finite wavelength")

        width_classes: Dict[str, str] = {}
        for record in self.width3sigma:
            previous = width_classes.get(record.width_class)
            if previous is not None:
                problems.append(
                    f"duplicate width3sigma width_class {record.width_class!r}: "
                    f"{previous!r} and {record.id!r}"
                )
            else:
                width_classes[record.width_class] = record.id
            if record.width_3sigma_A != record.width_3sigma_A:
                problems.append(
                    f"width3sigma {record.id!r} has a non-finite width"
                )

        for record in self.skylines:
            if record.wavelength_obs != record.wavelength_obs:
                problems.append(
                    f"skyline {record.id!r} has a non-finite wavelength"
                )
            if not record.citations:
                problems.append(f"skyline {record.id!r} has no citation/provenance")

        for record in self.indices:
            if not record.citations:
                problems.append(f"index band {record.id!r} has no citation/provenance")
        return problems


__all__ = [
    "ClassRecord",
    "EmpiricalParameterRecord",
    "ParameterSource",
    "ConditionRecord",
    "FormalRuleRecord",
    "DoubletRecord",
    "IndexBandRecord",
    "LineRecord",
    "ONTOLOGY_SCHEMA_VERSION",
    "OntologyRegistry",
    "OperandRecord",
    "OutcomeSpec",
    "RuleRecord",
    "SkylineRecord",
    "SUPPORTED_ONTOLOGY_SCHEMA_VERSIONS",
    "Width3SigmaRecord",
]
