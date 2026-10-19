"""The measured feature-width vocabulary, declared once with owned boundaries.

实测特征宽度词表：一次声明，边界各有其所有者。

Two different questions were both spelled `width_class`:

两个不同的问题此前都被写作 `width_class`：

* the **line** class (`LineRecord.width_class`: broad / narrow / both /
  absorption) — what a spectral line is;
* the **measured band** of a detected feature (narrow / intermediate / broad) —
  how wide this particular feature measured.

**谱线**类别（`LineRecord.width_class`：broad / narrow / both / absorption）说的是"这条谱线是
什么"；被检出特征的**实测档**（narrow / intermediate / broad）说的是"这一个特征测得有多宽"。

The measured band had no declaration at all: `intermediate` lived only in two code
expressions and one prompt sentence, its lower boundary was read from one rule
operand by the CWT finder and from a condition bound by the matrix, and its upper
boundary was read from the width-consistency pivot by the CWT finder but from the
strict-broad rule by the matrix.  The values agreed by coincidence, so a retune of
either declaration would have split the two producers of the same label.

实测档此前完全没有声明：`intermediate` 只存在于两处代码表达式与一句提示词里；它的下界在 CWT
找特征处读一个规则操作数、在矩阵处读一个条件界；上界在 CWT 找特征处读宽度一致性分界、在矩阵处
读严格宽线规则。数值只是碰巧一致，因此任一声明被重新定标都会让同一标签的两个产出方分道扬镳。

This module declares the band vocabulary and names **one owner for each boundary**,
so both producers read the same declaration and the band names cannot drift from the
numbers that define them.

本模块声明该档位词表，并为**每个边界指定唯一所有者**，使两个产出方读取同一声明，档位名不再
可能与定义它的数值脱节。
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

#: The measured band of a detected feature / 被检出特征的实测档。
NARROW = "narrow"
INTERMEDIATE = "intermediate"
BROAD = "broad"

#: The complete measured vocabulary, in increasing width order.
#: 完整实测词表，按宽度递增排列。
BANDS = (NARROW, INTERMEDIATE, BROAD)

#: Display value for a row whose FWHM could not be measured.  It is not a band.
#: FWHM 无法测量的行所使用的显示值。它不是档位。
UNMEASURED = "—"

#: What each band says about the feature / 每一档就特征所作的陈述。
MEANING: Dict[str, str] = {
    NARROW: "measured below the narrow/intermediate boundary",
    INTERMEDIATE: "wider than the narrow/intermediate boundary and below the strict broad boundary",
    BROAD: "at or above the strict broad boundary",
}

#: Each boundary has exactly one owner: (rule id, operand id) whose declared
#: threshold is the boundary.  The owners are read through the rule-parameter
#: accessor, so a JSON override moves the band with it.
#: 每个边界只有一个所有者：(规则 id, 操作数 id)，其声明的阈值即该边界。所有者经规则参数访问器
#: 读取，因此 JSON 覆盖会连带移动该档位。
NARROW_INTERMEDIATE_OWNER = ("rule:formal-width-class-contradiction",
                            "claimed_broad_fwhm_kms")
INTERMEDIATE_BROAD_OWNER = ("rule:formal-qso-broad-width", "fwhm_kms")

#: What a band means for the width-conflict question.  The executable answer stays
#: with `rule:formal-width-class-match` (it compares the *line's* declared class
#: against the measured FWHM), so these notes describe how the band is to be read
#: and do not add a second decision path.
#: 各档对"宽度冲突"问题意味着什么。可执行判定仍归 `rule:formal-width-class-match`（它把*谱线*
#: 的声明类别与实测 FWHM 相比），因此这些说明只描述该如何阅读该档，不新增第二条判定路径。
CONFLICT_NOTE: Dict[str, str] = {
    NARROW: ("matches a narrow-class line and conflicts with a broad-class line, "
             "which needs a profile at or above the strict broad boundary"),
    INTERMEDIATE: ("is a grey zone: consistent with a narrow-class claim, and not "
                   "enough for a broad-class claim. It is neither a clean match nor "
                   "by itself a conflict; the conflict question is answered by the "
                   "rule from the line's declared class, never from this band alone"),
    BROAD: ("matches a broad-class line and conflicts with a narrow-class line"),
}


def _boundary(owner) -> Optional[float]:
    from FORMA.core.reasoning.ontology.rule_parameters import (
        effective_operand_threshold,
    )

    rule_id, operand_id = owner
    value = effective_operand_threshold(rule_id, operand_id)["value"]
    return None if value is None else float(value)


def boundaries() -> Dict[str, Optional[float]]:
    """The two declared boundaries, each from its single owner.

    两个已声明边界，各自取自其唯一所有者。
    """
    return {
        "narrow_intermediate": _boundary(NARROW_INTERMEDIATE_OWNER),
        "intermediate_broad": _boundary(INTERMEDIATE_BROAD_OWNER),
    }


def _number(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def band_of(fwhm_km_s: Any) -> Optional[str]:
    """The declared band for a measured FWHM, or ``None`` when it cannot be measured.

    实测 FWHM 所属的已声明档位；无法测量时返回 ``None``。

    Both producers (the CWT finder and the contradiction matrix) call this, so the
    label a feature carries no longer depends on which code path wrote the row.
    两个产出方（CWT 找特征与矛盾矩阵）都调用它，因此特征携带的标签不再取决于哪条代码路径写了
    这一行。
    """
    value = _number(fwhm_km_s)
    if value is None:
        return None
    limits = boundaries()
    lower = limits["narrow_intermediate"]
    upper = limits["intermediate_broad"]
    if lower is not None and value < lower:
        return NARROW
    if upper is not None and value < upper:
        return INTERMEDIATE
    return BROAD


def normalize(value: Any) -> str:
    """The canonical band spelling, or ``""`` when the value is not a band.

    档位的规范拼写；不属于词表时返回 ``""``。
    """
    token = str(value if value is not None else "").strip().lower()
    return token if token in BANDS else ""


def is_known(value: Any) -> bool:
    """Whether a value belongs to the declared band vocabulary.

    取值是否属于已声明的档位词表。
    """
    return normalize(value) != ""


def undeclared_bands(values) -> List[str]:
    """The distinct non-empty values outside the vocabulary, in first-seen order.

    词表之外的、非空取值，按首次出现顺序去重返回。
    """
    seen: List[str] = []
    for value in values:
        token = str(value if value is not None else "").strip()
        if token and token not in BANDS and token not in seen:
            seen.append(token)
    return seen


def validate(values) -> None:
    """Refuse a catalog whose band column carries an undeclared value.

    拒绝档位列携带未声明取值的目录。

    The catalog is written by deterministic code, so an undeclared band means a bug
    rather than something a model could repair: it fails loudly instead of writing a
    label that no consumer declares.
    该目录由确定性代码写出，因此未声明的档位是程序缺陷而非模型可修复的问题：它大声失败，而不是
    写下一个没有任何消费者声明的标签。
    """
    bad = undeclared_bands(values)
    if bad:
        raise ValueError(
            f"undeclared feature width band(s) {bad}; the declared vocabulary is "
            f"{list(BANDS)} (see FORMA.core.reasoning.ontology.feature_width)"
        )


def legend_with_authority() -> tuple:
    """The band legend plus the per-value entries it renders (WP-041).

    档位图例，以及它渲染出的逐值条目（WP-041）。

    The legend used to return a sentence whose numbers had no recorded owner; callers that
    build a prompt now take both the text and the entries.
    该图例此前只返回一句文本，其中的数字没有记录所有者；构建提示词的调用方现在同时取文本与条目。
    """
    limits = boundaries()
    lower = limits["narrow_intermediate"]
    upper = limits["intermediate_broad"]
    entries = []
    if lower is not None:
        entries.append({
            "slot": "width_legend.narrow_intermediate",
            "value": float(lower),
            "owner": f"{NARROW_INTERMEDIATE_OWNER[0]}:{NARROW_INTERMEDIATE_OWNER[1]}",
            "kind": "declaration",
        })
    if upper is not None:
        entries.append({
            "slot": "width_legend.intermediate_broad",
            "value": float(upper),
            "owner": f"{INTERMEDIATE_BROAD_OWNER[0]}:{INTERMEDIATE_BROAD_OWNER[1]}",
            "kind": "declaration",
        })
    return legend(), entries


def legend() -> str:
    """The prompt legend for the band vocabulary, rendered from the declaration.

    档位词表的提示词图例，由声明渲染而来。

    The FeatureAuditor prompt used to spell the three bands out by hand next to the
    numbers that define them; rendering it here keeps one authority for both.
    FeatureAuditor 的提示词此前手工写出三档及其数值；在此渲染使二者只有一个权威。
    """
    limits = boundaries()
    lower = limits["narrow_intermediate"]
    upper = limits["intermediate_broad"]
    parts = []
    if lower is not None and upper is not None:
        parts.append(f"{NARROW} < {lower:g} km/s")
        parts.append(f"{INTERMEDIATE} below {upper:g} km/s")
        parts.append(f"{BROAD} at or above {upper:g} km/s")
    else:
        parts.append(", ".join(BANDS))
    note = CONFLICT_NOTE[INTERMEDIATE]
    return ("Width: " + ", ".join(parts) + f". An {INTERMEDIATE} feature {note}.")
