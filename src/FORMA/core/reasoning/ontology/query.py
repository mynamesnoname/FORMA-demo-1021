"""Typed ontology query API and Markdown KB compatibility view (WP-010).

类型化本体查询 API 与 Markdown KB 兼容视图（WP-010）。
"""

from __future__ import annotations

from typing import List, Optional

from FORMA.core.reasoning.ontology.registry import ONTOLOGY
from FORMA.core.reasoning.ontology.schema import (
    DoubletRecord,
    LineRecord,
    OntologyRegistry,
)


def query_lines(
    *,
    name: Optional[str] = None,
    line_id: Optional[str] = None,
    line_type: Optional[str] = None,
    registry: OntologyRegistry = ONTOLOGY,
) -> List[LineRecord]:
    """Return line records matching the filters / 返回匹配过滤条件的谱线记录。"""
    lines = registry.lines
    if line_id is not None:
        record = registry.line_index().get(line_id)
        return [record] if record is not None else []
    if name is not None:
        lines = [line for line in lines if line.name == name]
    if line_type is not None:
        lines = [line for line in lines if line.line_type == line_type]
    return lines


def resolve_line_id(name: str, registry: OntologyRegistry = ONTOLOGY) -> Optional[str]:
    """Resolve a prompt-facing line name to a stable ontology ID.

    将 prompt 展示名解析为稳定本体 ID。

    An ambiguous alias — two line records sharing one name — is refused rather
    than resolved by list order (2026-10-11 review: silent first-match is an
    aliasing bug).
    歧义别名——两条谱线记录共用一名——被拒绝而非按列表顺序解析（2026-10-11 评审：
    静默取首个匹配是别名缺陷）。
    """
    matches = [line.id for line in registry.lines if line.name == name]
    if len(matches) > 1:
        raise ValueError(
            f"ambiguous line alias {name!r}: matches {sorted(matches)}; "
            "the registry must disambiguate names before resolution"
        )
    return matches[0] if matches else None


def line_rest_wavelength(name: str, registry: OntologyRegistry = ONTOLOGY) -> Optional[float]:
    """KB-compatible lookup used by the existing pipeline / 现有流水线使用的兼容查询。"""
    line_id = resolve_line_id(name, registry)
    if line_id is None:
        return None
    return registry.line_index()[line_id].rest_wavelength


def doublets_for_line(line_id: str, registry: OntologyRegistry = ONTOLOGY) -> List[DoubletRecord]:
    return [d for d in registry.doublets if line_id in d.component_ids]


def build_width3sigma_map(registry: OntologyRegistry = ONTOLOGY):
    """Resolve 3σ fit windows from the method profile for the active registry.

    自定义 registry 保留其自身 fitwin 默认值，活动 registry 使用方法配置。
    """
    defaults = {
        record.width_class: record.width_3sigma_A
        for record in registry.width3sigma
    }
    if registry is ONTOLOGY:
        from FORMA.core.config.analysis_method import load_analysis_method
        return dict(load_analysis_method().gaussian_fit.width_3sigma_angstrom_by_class)
    return defaults


def get_index_band(index_id: str, registry: OntologyRegistry = ONTOLOGY):
    """Return an index band record by ID, or None (WP-023).

    按 ID 返回指数波段记录，找不到为 None（WP-023）。
    """
    for record in registry.indices:
        if record.id == index_id:
            return record
    return None


def dn4000_break_angstrom() -> float | None:
    """The 4000 Å break's rest wavelength, from the declared Dn4000 band.

    4000 Å 断点的静止波长，取自已声明的 Dn4000 波段。

    The break sits at the red band's lower edge, so the number prose quotes and the
    number the index measures have one owner (`index:dn4000`).
    断点位于红侧波段的下沿，因此文本引用的数字与指标测量的数字只有一个所有者
    （`index:dn4000`）。
    """
    band = get_index_band("index:dn4000")
    return None if band is None else float(band.red_low)


def dn4000_interpretation_bands(registry: OntologyRegistry = ONTOLOGY) -> dict:
    """Return the Dn4000 interpretation bounds owned by the registry (WP-029).

    返回由注册表拥有的 Dn4000 判读边界（WP-029）。

    The rule declares the diagnostic; the effective reference bounds come from
    ``parameter:dn4000-reference-bands``. A missing rule is a hard error.
    规则声明诊断；生效参考界来自参数记录。规则缺失直接报错。
    """
    rule = next(
        (item for item in registry.formal_rules
         if item.id == "rule:formal-dn4000-interpretation"),
        None,
    )
    if rule is None:
        raise RuntimeError(
            "ontology registry lacks rule:formal-dn4000-interpretation"
        )
    strong = None
    moderate_low = None
    moderate_high = None
    for condition in rule.conditions:
        if condition.operator == "gt" and isinstance(condition.rhs, (int, float)):
            strong = float(condition.rhs)
        if condition.operator == "between" and isinstance(condition.rhs, (int, float)):
            moderate_low = float(condition.rhs)
            moderate_high = float(condition.rhs_high) if condition.rhs_high is not None else None
    if strong is None or moderate_low is None or moderate_high is None:
        raise RuntimeError(
            "rule:formal-dn4000-interpretation does not declare both bands"
        )
    from FORMA.core.reasoning.ontology.rule_parameters import effective_parameter
    bounds = effective_parameter("parameter:dn4000-reference-bands", registry)["parameters"]
    return {
        "strong": bounds["high"],
        "moderate_low": bounds["low"],
        "moderate_high": bounds["high"],
    }


def nearest_skyline_offset(
    wavelength_obs: float,
    registry: OntologyRegistry = ONTOLOGY,
):
    """Return the offset to the nearest registered skyline and its record.

    返回与最近注册天光线的偏移量及其记录。

    Only discrete airglow emission lines contribute. OH bands are risk regions,
    not a measured distance to an individual skyline; atmospheric absorption
    bands are not narrow emission-line contaminants.
    只计算离散天光发射线；OH 波段是风险区域，不是单条天光线距离。
    """
    best: Optional[float] = None
    best_record = None
    for record in registry.skylines:
        if record.kind != "emission" or record.wavelength_max is not None:
            continue
        offset = abs(wavelength_obs - record.wavelength_obs)
        if best is None or offset < best:
            best = offset
            best_record = record
    return {"offset_A": best, "skyline": best_record}


def oiii_ratio_window_a_over_b() -> list[float]:
    """Convert the effective b:a acceptance interval to the FA a:b convention."""
    from FORMA.core.reasoning.ontology.rule_parameters import effective_parameter

    bounds = effective_parameter("parameter:oiii-ratio-b-over-a")["parameters"]
    return [1.0 / bounds["high"], 1.0 / bounds["low"]]


def build_runtime_line_tables(
    registry: OntologyRegistry = ONTOLOGY,
):
    """Registry-backed prompt/runtime line catalogs (WP-023).

    由注册表支撑的 prompt/运行时谱线目录（WP-023）。

    These dictionaries are compatibility shims for the legacy module-level
    tables.  They are computed from the ontology rather than hand-maintained,
    so there is no second authoritative numeric source.
    这些字典是旧模块级线表的兼容垫片。它们由本体计算而非手工维护，因此不存在第二个权威
    数值来源。
    """
    emission = {}
    absorption = {}
    widths = {}
    for line in registry.lines:
        if line.line_type == "emission":
            emission[line.name] = line.rest_wavelength
            widths[line.name] = line.width_class
        elif line.line_type == "absorption":
            absorption[line.name] = line.rest_wavelength
    return emission, absorption, widths


def render_kb_compatibility_view(registry: OntologyRegistry = ONTOLOGY) -> str:
    """Render structured facts back into Markdown compatible with the KB prompts.

    将结构化事实渲染回与 KB prompt 兼容的 Markdown。
    """
    sections = [
        "# Ontology-generated Line Reference",
        "",
        f"schema_version: {registry.schema_version}",
        f"updated: {registry.updated}",
        "",
        "| ID | Name | λ_rest (Å) | Type | Width | Anchor priority |",
        "|----|------|-----------|------|-------|-----------------|",
    ]
    for line in registry.lines:
        sections.append(
            f"| `{line.id}` | {line.name} | {line.rest_wavelength:.4f} "
            f"| {line.line_type} | {line.width_class} | "
            f"{line.anchor_priority if line.anchor_priority is not None else '—'} |"
        )
    return "\n".join(sections) + "\n"


def render_rules_compatibility_view(registry: OntologyRegistry = ONTOLOGY) -> str:
    """Render the machine-evaluable formal rules into a grep_kb-served page.

    将可机检正式规则渲染为 grep_kb 服务的参考页。

    This is the single registry-backed rule source the agents search: every
    row carries the rule ID, its three-state verdict tags, operand units and
    provenance, so prompt-side thresholds are cited against the registry
    instead of acting as a second authoritative table.
    这是代理检索的唯一注册表支撑规则来源：每行携带规则 ID、三态 verdict 标签、
    操作数单位与出处，使 prompt 侧阈值以注册表为引用，而非充当第二权威表。
    """
    sections = [
        "# Ontology-generated Formal Rule Reference",
        "",
        f"schema_version: {registry.schema_version}",
        f"updated: {registry.updated}",
        "",
        "| Rule ID | Name | Kind | Scope | Conclusion | Pass | Fail | Unknown | Provenance |",
        "|---------|------|------|-------|------------|------|------|---------|------------|",
    ]
    for rule in sorted(registry.formal_rules, key=lambda r: r.id):
        outcomes = rule.outcomes
        pass_verdict = outcomes.pass_verdict if outcomes else rule.conclusion
        fail_verdict = outcomes.fail_verdict if outcomes else "—"
        unknown_verdict = outcomes.unknown_verdict if outcomes else "—"
        provenance = "; ".join(
            citation.get("source", "") for citation in rule.provenance
        )
        sections.append(
            f"| `{rule.id}` | {rule.name} | {rule.kind} | {rule.runtime_scope} | "
            f"{rule.conclusion} | {pass_verdict} | {fail_verdict} | "
            f"{unknown_verdict} | {provenance} |"
        )
    return "\n".join(sections) + "\n"


def write_rules_compatibility_view(
    path: str = "src/FORMA/agents/multi_agents/harness/kb/ontology_rules.generated.md",
    registry: OntologyRegistry = ONTOLOGY,
) -> None:
    from pathlib import Path
    Path(path).write_text(render_rules_compatibility_view(registry), encoding="utf-8")


def write_kb_compatibility_view(
    path: str = "src/FORMA/agents/multi_agents/harness/kb/ontology_lines.generated.md",
    registry: OntologyRegistry = ONTOLOGY,
) -> None:
    from pathlib import Path
    Path(path).write_text(render_kb_compatibility_view(registry), encoding="utf-8")


__all__ = [
    "build_runtime_line_tables",
    "build_width3sigma_map",
    "doublets_for_line",
    "get_index_band",
    "line_rest_wavelength",
    "nearest_skyline_offset",
    "oiii_ratio_window_a_over_b",
    "query_lines",
    "render_kb_compatibility_view",
    "render_rules_compatibility_view",
    "resolve_line_id",
    "write_kb_compatibility_view",
    "write_rules_compatibility_view",
]
