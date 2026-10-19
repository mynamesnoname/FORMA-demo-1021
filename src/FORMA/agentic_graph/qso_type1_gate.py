"""Deterministic Type 1 QSO gate selection for the new investigation graph.

This module consumes already validated coverage and per-line judgments. It does
not infer a line identity from pixels or import the legacy evidence graph.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping


LYA = "line:lya-1216"
CIV = "line:civ-1549"
CIII = "line:ciii-1909"
MGII = "line:mgii-2800"
TYPE1_LINES = (LYA, CIV, CIII, MGII)

CoverageState = Literal[
    "outside_range", "fully_masked", "no_usable_data", "partial", "usable"
]
LineState = Literal["paired", "vote_explained", "failed", "unresolved"]
EffectiveLineState = Literal[
    "paired", "vote_explained", "failed", "unresolved", "neutral_masked"
]
GateStatus = Literal["type1_supported", "type1_failed", "type1_unresolved"]

_COVERAGE_STATES = frozenset(CoverageState.__args__)
_LINE_STATES = frozenset(LineState.__args__)
_SUPPORT = frozenset({"paired", "vote_explained"})


@dataclass(frozen=True)
class Type1GateResult:
    selected_line_ids: tuple[str, ...]
    status: GateStatus
    effective_line_states: tuple[tuple[str, EffectiveLineState], ...]


def select_type1_gate_lines(coverage: Mapping[str, CoverageState]) -> tuple[str, ...]:
    """Choose a line group, falling through only if every group line is masked.

    A mask is neutral within a two-line group. A later line is considered only
    when the whole selected group has no line left to judge. Partial masks and
    unavailable IVAR/data do not qualify as proven full-window masks.
    """
    for line_id in TYPE1_LINES:
        state = coverage.get(line_id)
        if state not in _COVERAGE_STATES:
            raise ValueError(f"missing or invalid coverage for {line_id}: {state!r}")

    def in_range(line_id: str) -> bool:
        return coverage[line_id] != "outside_range"

    if in_range(LYA):
        base = (LYA, CIV) if in_range(CIV) else (LYA,)
    elif in_range(CIV):
        base = (CIV, CIII) if in_range(CIII) else (CIV,)
    elif in_range(CIII):
        base = (CIII,)
    elif in_range(MGII):
        base = (MGII,)
    else:
        return ()

    if any(coverage[line_id] != "fully_masked" for line_id in base):
        return base

    selected = list(base)
    for line_id in TYPE1_LINES[TYPE1_LINES.index(base[-1]) + 1:]:
        if not in_range(line_id):
            continue
        selected.append(line_id)
        if coverage[line_id] != "fully_masked":
            break
    return tuple(selected)


def infer_type1_gate(
    coverage: Mapping[str, CoverageState],
    line_states: Mapping[str, LineState],
) -> Type1GateResult:
    """Apply the Type 1 rule to the selected, already reviewed broad lines.

    A proven full-window mask is neutral, not affirmative support. If all
    selected lines are neutral masks, no Type 1 conclusion is possible. Missing
    line results and other unusable in-range windows remain unresolved.
    """
    selected = select_type1_gate_lines(coverage)
    effective: list[tuple[str, EffectiveLineState]] = []
    for line_id in selected:
        if coverage[line_id] == "fully_masked":
            effective_state: EffectiveLineState = "neutral_masked"
        else:
            state = line_states.get(line_id, "unresolved")
            if state not in _LINE_STATES:
                raise ValueError(f"invalid line state for {line_id}: {state!r}")
            effective_state = ("unresolved" if coverage[line_id] == "no_usable_data"
                               else state)
        effective.append((line_id, effective_state))

    if any(state == "failed" for _, state in effective):
        status: GateStatus = "type1_failed"
    elif (not any(state in _SUPPORT for _, state in effective)
          or any(state == "unresolved" for _, state in effective)):
        status = "type1_unresolved"
    elif all(state in _SUPPORT or state == "neutral_masked"
             for _, state in effective):
        status = "type1_supported"
    else:
        raise AssertionError("validated line states did not yield a gate status")

    return Type1GateResult(selected, status, tuple(effective))
