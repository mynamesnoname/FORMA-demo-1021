"""Per-value authority for rendered prompt numbers (WP-041).

渲染进提示词的数字的逐值权威（WP-041）。

The 2026-10-16 review of WP-041 corrected the design: authority needs a **per-value
manifest**, not two whole-document digests. A prompt digest proves that the text is
unchanged; it cannot say *which declaration* supplied a given number, nor whether a number
that looks like a threshold was rendered from a declaration or typed into a sentence. Two
of the defects found on 2026-10-15 were exactly of that kind — a Lyα section claiming
±300 Å while the configured read window was 100 Å, and a break wavelength typed in prose
that `index:dn4000` owns.

WP-041 的 2026-10-16 review 更正了设计：权威需要**逐值清单**，而不是两个整文档摘要。提示词摘要能
证明文本未变，却无法说明某个数字*由哪条声明*提供，也无法区分"由声明渲染的阈值"与"写进句子里的
数字"。2026-10-15 发现的两处缺陷正是这一类：Lyα 段落声称 ±300 Å 而配置的读取窗口是 100 Å；断点
波长被写在散文里，而它归 `index:dn4000` 所有。

A builder records each rendered declaration value as it writes the sentence:

构建器在写出句子的同时，把每个由声明渲染的值登记下来：

    authority = PromptAuthority("feature_auditor")
    text = f"... ±{authority.value(read_half, owner='analysis_method.audit.feature_read_half_angstrom'):g} Å ..."

and the stage archives `prompt_authority.json` next to its trace:

阶段随后在其 trace 旁归档 `prompt_authority.json`：

    {"schema": "forma-prompt-authority-v1", "stage": "...", "prompt_sha256": "...",
     "frozen_parameters_digest": "...",
     "entries": [{"slot": "...", "value": 100.0, "owner": "...", "kind": "declaration"}]}

Boundaries, recorded rather than hidden:

边界（记录而非隐藏）：

* the manifest covers **declarations only** — measurements shown to the model (fitted
  centres, FWHM, redshifts, SNR) are data, not authority, and are not listed;
* entries are keyed by **slot**, not by value, so a diff says which sentence changed;
* a number typed straight into a prompt string produces **no entry**, so the manifest is
  only as complete as the builders' use of this helper — the rendered-prompt audit
  (`evaluation/baseline/audit_prompt_numbers.py`) is what reports undeclared numbers, and
  the two are meant to be read together.

* 清单只覆盖**声明**——展示给模型的测量值（拟合中心、FWHM、红移、SNR）是数据而非权威，不登记；
* 条目以**槽位**为键而非以数值为键，因此 diff 能说明是哪句话变了；
* 直接写进提示词字符串的数字**不会产生条目**，因此清单的完整性取决于构建器是否使用本助手——未声明
  数字由渲染提示词审计（`evaluation/baseline/audit_prompt_numbers.py`）负责上报，二者应合起来读。
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Dict, List, Optional

SCHEMA = "forma-prompt-authority-v1"


def _declared_value(owner: str) -> Any:
    """Return a directly owned scalar, or None for compound/derived entries."""
    if owner.startswith("analysis_method."):
        from FORMA.core.config.analysis_method import load_analysis_method
        node: Any = load_analysis_method().model_dump(mode="json")
        for part in owner.removeprefix("analysis_method.").split("."):
            node = node[part]
        return node
    if owner.startswith(("parameter:", "membership:")) and "#" in owner:
        from FORMA.core.reasoning.ontology.rule_parameters import effective_parameter
        parameter_id, field = owner.split("#", 1)
        return effective_parameter(parameter_id)["parameters"][field]
    if owner.startswith("rule:") and owner.count(":") >= 2:
        rule_id, operand_id = owner.rsplit(":", 1)
        if operand_id != "condition_rhs":
            from FORMA.core.reasoning.ontology.rule_parameters import effective_operand_threshold
            return effective_operand_threshold(rule_id, operand_id)["value"]
    if owner.startswith(("line:", "doublet:", "skyline:", "index:")) and "#" in owner:
        from FORMA.core.reasoning.ontology.registry import ONTOLOGY
        record_id, field = owner.split("#", 1)
        records = {
            "line:": ONTOLOGY.lines,
            "doublet:": ONTOLOGY.doublets,
            "skyline:": ONTOLOGY.skylines,
            "index:": ONTOLOGY.indices,
        }
        family = next(items for prefix, items in records.items() if record_id.startswith(prefix))
        return getattr(next(item for item in family if item.id == record_id), field)
    return None


def _check_value(value: Any, owner: str) -> None:
    expected = _declared_value(owner)
    if expected is None:
        return
    if isinstance(value, (int, float)) and isinstance(expected, (int, float)):
        if math.isclose(value, expected, rel_tol=1e-12, abs_tol=1e-12):
            return
    elif value == expected:
        return
    raise ValueError(f"prompt value {value!r} disagrees with {owner}: {expected!r}")


def _entry_metadata(owner: str) -> Dict[str, Any]:
    """Resolve the declaration's source without inferring ownership from a number."""
    from FORMA.core.config.frozen_parameters import current

    frozen = current()
    if owner.startswith(("parameter:", "membership:")):
        parameter_id, _, field = owner.partition("#")
        from FORMA.core.reasoning.ontology.rule_parameters import effective_parameter
        resolved = effective_parameter(parameter_id)
        return {
            "unit": resolved.get("unit"),
            "source": resolved.get("sources", {}).get(field, "registry"),
            "payload_digest": resolved.get("payload_digest"),
        }
    if owner.startswith("analysis_method."):
        from FORMA.core.config.analysis_method import load_analysis_method
        node: Any = load_analysis_method().model_dump(mode="json")
        try:
            for part in owner.removeprefix("analysis_method.").split("."):
                node = node[part]
        except (KeyError, TypeError) as exc:
            raise ValueError(f"unknown prompt authority: {owner}") from exc
        unit = "Å" if "angstrom" in owner else ("km/s" if "kms" in owner else None)
        return {
            "unit": unit,
            "source": (frozen.sources.get("analysis_method") if frozen else None)
                      or "analysis_method default",
            "payload_digest": frozen.digests.get("analysis_method") if frozen else None,
        }
    if owner.startswith("rule:") and owner.count(":") >= 2:
        rule_id, _, operand_id = owner.rpartition(":")
        if operand_id != "condition_rhs":
            from FORMA.core.reasoning.ontology.rule_parameters import effective_operand_threshold
            resolved = effective_operand_threshold(rule_id, operand_id)
            return {
                "unit": resolved.get("unit"),
                "source": resolved.get("source"),
                "payload_digest": resolved.get("payload_digest"),
            }
        from FORMA.core.reasoning.ontology.registry import ONTOLOGY
        from FORMA.core.reasoning.ontology.rule_parameters import effective_operand_threshold
        rule = next((item for item in ONTOLOGY.formal_rules if item.id == rule_id), None)
        if rule is not None and rule.conditions:
            condition = rule.conditions[0]
            operand = next((item for item in rule.operands
                            if item.id == condition.lhs and item.threshold is not None), None)
            if operand is not None:
                resolved = effective_operand_threshold(rule_id, operand.id)
                return {
                    "unit": resolved.get("unit"),
                    "source": resolved.get("source"),
                    "payload_digest": resolved.get("payload_digest"),
                }
        return {"unit": None, "source": "ontology rule condition", "payload_digest": None}
    if owner.startswith(("line:", "index:", "doublet:", "skyline:")):
        from FORMA.core.reasoning.ontology.registry import ONTOLOGY
        record_id, _, field = owner.partition("#")
        collections = {
            "line:": ONTOLOGY.lines,
            "index:": ONTOLOGY.indices,
            "doublet:": ONTOLOGY.doublets,
            "skyline:": ONTOLOGY.skylines,
        }
        records = next(items for prefix, items in collections.items()
                       if record_id.startswith(prefix))
        record = next((item for item in records if item.id == record_id), None)
        if record is None or (field and not hasattr(record, field)):
            raise ValueError(f"unknown prompt authority: {owner}")
        unit = "Å"
        if owner.endswith("#anchor_priority"):
            unit = "priority rank"
        elif owner.endswith("#amplitude_ratio"):
            unit = "dimensionless"
        return {"unit": unit, "source": "ontology registry", "payload_digest": None}
    return {"unit": None, "source": "declared runtime", "payload_digest": None}


class PromptAuthority:
    """Collects the declaration values a prompt renders / 收集提示词渲染的声明取值。"""

    def __init__(self, stage: str) -> None:
        self.stage = stage
        self._entries: List[Dict[str, Any]] = []
        self._slots: set = set()

    def value(self, value: Any, *, owner: str, slot: str,
              kind: str = "declaration") -> Any:
        """Record one rendered declaration value and return it for formatting.

        登记一个被渲染的声明取值，并把它返回以便格式化。
        """
        if slot in self._slots:
            raise ValueError(f"slot {slot!r} rendered twice in stage {self.stage!r}")
        metadata = _entry_metadata(owner)
        _check_value(value, owner)
        self._slots.add(slot)
        self._entries.append({
            "slot": slot,
            "value": value if isinstance(value, (int, float, str, bool)) else str(value),
            "owner": owner,
            "kind": kind,
            **metadata,
        })
        return value

    @property
    def entries(self) -> List[Dict[str, Any]]:
        return list(self._entries)

    def extend(self, entries: List[Dict[str, Any]]) -> None:
        """Merge entries rendered elsewhere (e.g. a shared legend).

        合并别处渲染的条目（例如共享的图例）。
        """
        for entry in entries:
            if entry["slot"] in self._slots:
                raise ValueError(
                    f"slot {entry['slot']!r} rendered twice in stage {self.stage!r}"
                )
            _check_value(entry["value"], entry["owner"])
            self._slots.add(entry["slot"])
            self._entries.append({**entry, **_entry_metadata(entry["owner"])})

    def document(self, prompt_text: str,
                 frozen_digest: Optional[str] = None,
                 *, system_prompt: str = "") -> Dict[str, Any]:
        """The artifact written next to the stage's trace / 写在阶段 trace 旁的产物。"""
        return {
            "schema": SCHEMA,
            "stage": self.stage,
            "prompt_sha256": hashlib.sha256(json.dumps(
                {"system": system_prompt, "user": prompt_text},
                ensure_ascii=False, sort_keys=True,
            ).encode("utf-8")).hexdigest(),
            "prompt_characters": len(system_prompt) + len(prompt_text),
            "prompt_parts": ["system", "user"],
            "frozen_parameters_digest": frozen_digest,
            "n_entries": len(self._entries),
            "entries": self.entries,
        }

    def write(self, path: str, prompt_text: str,
              frozen_digest: Optional[str] = None,
              *, system_prompt: str = "") -> Dict[str, Any]:
        """Write the manifest and return it / 写出清单并返回它。"""
        document = self.document(prompt_text, frozen_digest,
                                 system_prompt=system_prompt)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(document, handle, ensure_ascii=False, indent=2)
        return document


def changed_slots(first: Dict[str, Any], second: Dict[str, Any]) -> List[str]:
    """Slots whose value or owner differs between two manifests.

    两个清单之间取值或所有者不同的槽位。

    This is what a digest cannot tell you: *which* rendered declaration moved.
    这正是摘要无法回答的：究竟是哪一个被渲染的声明发生了变化。
    """
    left = {entry["slot"]: entry for entry in first.get("entries", [])}
    right = {entry["slot"]: entry for entry in second.get("entries", [])}
    def identity(entry):
        return None if entry is None else (entry.get("owner"), entry.get("value"))

    return sorted(slot for slot in set(left) | set(right)
                  if identity(left.get(slot)) != identity(right.get(slot)))


def archive_stage_prompt(
    stream_path: str | None, stage: str, system_prompt: str,
    user_prompt: str, authority: PromptAuthority | None = None,
) -> Optional[Dict[str, Any]]:
    """Archive the exact initial model-facing system and user message pair."""
    if not stream_path:
        return None
    from pathlib import Path
    from FORMA.core.config.frozen_parameters import frozen_digest

    stream = Path(stream_path)
    # Several hypothesis streams share one directory; each prompt needs its own
    # authority record. The conventional stream.md keeps the familiar filename.
    name = ("prompt_authority.json" if stream.stem == "stream"
            else f"{stream.stem}_prompt_authority.json")
    destination = stream.with_name(name)
    destination.parent.mkdir(parents=True, exist_ok=True)
    collector = authority or PromptAuthority(stage)
    return collector.write(
        str(destination), user_prompt, frozen_digest(), system_prompt=system_prompt
    )
