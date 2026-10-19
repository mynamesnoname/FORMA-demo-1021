"""The per-line status vocabulary, declared once, and the questions asked of it.

逐线状态词表：只声明一次，以及围绕它提出的问题。

The SH harness writes one `status` per evaluated line into
`{idx}_lines.csv`; every later stage then asks something *about* that status, and
each used to answer with its own literal set.  Two copies of
`{"LIKELY", "MARGINAL"}` lived in the rule adapters, the graph projection kept a
third mapping, the plot and the summary kept a fourth and fifth order — and two
values (`ESTIMATED`, `SPURIOUS`) survived only in those consumers after their
producers were deleted.  A row could therefore be "kept" for one stage and "not
kept" for another, silently.

SH harness 把每条被评估谱线的 `status` 写进 `{idx}_lines.csv`；此后每个阶段都会就这个状态提
出某个问题，而每一处都曾用自己的字面量集合作答：规则适配器里有两份 `{"LIKELY","MARGINAL"}`
副本，图投影有第三份映射，绘图与摘要有第四、第五种排序，而两个取值（`ESTIMATED`、`SPURIOUS`）
在生产它们的代码删除之后只残留在这些消费者里。于是同一行可以对一个阶段是"保留"、对另一个阶段
是"未保留"，而且是静默的。

The vocabulary is structural, not an empirical knob, so it is declared here rather
than configured.  Each value states what it means and whether it asserts a
measurement; every consumer imports a **named predicate** for the question it
actually asks, so a future difference between two questions has to be written down
and tested instead of appearing by accident.

该词表是结构事实而非经验旋钮，因此在此声明而不是做成配置。每个取值说明其含义以及它是否主张
一次测量；每个消费者为自己真正提出的问题 import 一个**命名谓词**，使两个问题日后的差异必须
被写下并测试，而不是偶然出现。
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

#: A line the harness measured and kept / 被 harness 测量并保留的谱线。
LIKELY = "LIKELY"
MARGINAL = "MARGINAL"
#: Checked and absent / 已检查且不存在。
NOT_FOUND = "NOT_FOUND"
#: Not measured at all — neutral, never a negative claim / 根本没有测量——中性，绝不构成否定主张。
MASKED = "MASKED"

#: The complete vocabulary, in the order the summary reports it.
#: 完整词表，按摘要报告的顺序。
STATUSES = (LIKELY, MARGINAL, NOT_FOUND, MASKED)

#: What each value means, and what it asserts about the measurement.
#: 每个取值的含义，以及它就测量所作的主张。
MEANING: Dict[str, str] = {
    LIKELY: "detected and kept: the centre is measured and the identification holds",
    MARGINAL: "detected and kept with a caveat: weaker or wider than a LIKELY line",
    NOT_FOUND: "checked and absent inside the window",
    MASKED: "no data in the window; unmeasured rather than absent",
}

#: Predicates that answer "does this row assert a measurement?" — one name per
#: question, so a caller cannot accidentally reuse another question's answer.
#: 回答"该行是否主张一次测量"的谓词——一个问题一个名字，避免调用方误用别的问题的答案。
_KEPT = (LIKELY, MARGINAL)


def normalize(value: Any) -> str:
    """The canonical spelling of a status, or ``""`` when it is not one.

    状态的规范拼写；不属于词表时返回 ``""``。
    """
    token = str(value if value is not None else "").strip().upper()
    return token if token in STATUSES else ""


def is_known(value: Any) -> bool:
    """Whether a value belongs to the declared vocabulary / 取值是否属于已声明词表。"""
    return normalize(value) != ""


def unknown_statuses(values: Iterable[Any]) -> List[str]:
    """The distinct values outside the vocabulary, in first-seen order.

    词表之外的取值，按首次出现顺序去重返回。

    Used by the write boundary to refuse such a row by name instead of letting
    three consumers disagree about it later.
    供写入边界按名拒绝这类行，而不是让三处消费者日后各执一词。
    """
    seen: List[str] = []
    for value in values:
        token = str(value if value is not None else "").strip().upper()
        if token and token not in STATUSES and token not in seen:
            seen.append(token)
    return seen


def is_kept_evidence(value: Any) -> bool:
    """Does this row assert a detected feature? (rule adapters, plotting)

    该行是否主张一个已检出的特征？（规则适配器、绘图）

    `NOT_FOUND` is a negative claim about the line and `MASKED` is no claim at all,
    so neither is evidence; the two kept values differ only in their caveat.
    对谱线而言 `NOT_FOUND` 是否定主张、`MASKED` 则不构成主张，两者都不是证据；两个保留值只
    在caveat 上有别。
    """
    return normalize(value) in _KEPT


def is_measured(value: Any) -> bool:
    """Was the window actually measured? (`MASKED` means it was not)

    窗口是否真的被测量过？（`MASKED` 表示没有）
    """
    return normalize(value) in (LIKELY, MARGINAL, NOT_FOUND)


def status_rank(value: Any) -> int:
    """Sort weight for the summary tables; unknown values sort last.

    摘要表的排序权重；未知取值排在最后。
    """
    token = normalize(value)
    return STATUSES.index(token) if token else len(STATUSES)


def claim_assertion(value: Any) -> str:
    """The claim vocabulary of the evidence graph for this status.

    该状态在证据图主张词表中的取值。

    `MASKED` maps to `unknown` deliberately: an unmeasured window is not evidence
    against the line, and the graph must not read it as a negative claim.
    `MASKED` 刻意映射为 `unknown`：未测量的窗口不是反对该谱线的证据，图不得把它读成否定主张。
    """
    token = normalize(value)
    return {
        LIKELY: "keep",
        MARGINAL: "flag",
        NOT_FOUND: "not_found",
        MASKED: "unknown",
    }.get(token, "unknown")


def describe() -> List[Dict[str, str]]:
    """The vocabulary with its meaning, for a prompt or a test to render.

    词表及其含义，供提示词或测试渲染。
    """
    return [{"status": status, "meaning": MEANING[status]} for status in STATUSES]
