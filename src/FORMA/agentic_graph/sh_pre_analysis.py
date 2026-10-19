"""Two-stage SH pre-analysis and validated preliminary-class injection.

This is a node boundary, not an implementation of the future investigation
graph. Callers own the node store and the hypothesis referent. The legacy SH
context and measurement tools may be supplied through a separate adapter;
``FORMA.core.evidence`` is never an input to this module.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from contextlib import aclosing
from pathlib import Path
from typing import Any, Callable, MutableMapping

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, ConfigDict, StrictStr

from .session_markdown import MarkdownSessionRecorder
from .execution_artifacts import ExecutionAllocation, validate_execution
from .node_keys import sh_node_key as node_key


CLASSES = ("Type 1 QSO", "Type 2 QSO", "ELG", "LRG/BGS")
REPORT_HEADINGS = (
    "### 3a. Spectrum Summary", "### 3b. Overall Verdict",
    "### 3c. Per-Line Results", "### 3d. Key Findings",
    "### 3e. Classification", "### 3f. Caveats",
)
# Re-exported: FA, SH line review, QSO report and LRG/BGS read prompts from here.
from .prompts import PROMPT_DIR  # noqa: F401


class PreAnalysisError(RuntimeError):
    """The node could not reach a validated, injectable state."""


class _SubmissionArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    classification: StrictStr | None


def _render(name: str, replacements: dict[str, str], prompt_dir: Path) -> str:
    text = (prompt_dir / name).read_text(encoding="utf-8")
    for marker, value in replacements.items():
        token = "{{" + marker + "}}"
        if token not in text:
            raise PreAnalysisError(f"prompt {name} lacks {token}")
        text = text.replace(token, value)
    if re.search(r"\{\{[A-Z_]+\}\}", text):
        raise PreAnalysisError(f"prompt {name} has unresolved placeholders")
    return text


def _report_class(content: str, z_text: str) -> str | None:
    """Read only the two declared machine-readable report lines."""
    lines = content.splitlines()

    def first_nonempty_after(position: int) -> str | None:
        index = position + 1
        while index < len(lines) and not lines[index].strip():
            index += 1
        return lines[index] if index < len(lines) else None

    positions = []
    for heading in REPORT_HEADINGS:
        hits = [index for index, line in enumerate(lines) if line == heading]
        if len(hits) != 1:
            raise ValueError(f"报告必须恰有一个 `{heading}` 标题")
        positions.append(hits[0])
    if positions != sorted(positions):
        raise ValueError("报告 3a–3f 标题顺序错误")
    z_lines = [line for line in lines if line.startswith("Hypothesis redshift:")]
    if (z_lines != [f"Hypothesis redshift: {z_text}"]
            or first_nonempty_after(positions[0]) != z_lines[0]):
        raise ValueError(f"报告必须恰有一行 `Hypothesis redshift: {z_text}`；不能由 anchor 重算")
    class_lines = [line for line in lines if line.startswith("Preliminary classification:")]
    if (len(class_lines) != 1
            or first_nonempty_after(positions[4]) != class_lines[0]):
        raise ValueError("报告必须恰有一行 `Preliminary classification: <类型或 null>`")
    value = class_lines[0].removeprefix("Preliminary classification: ")
    if (class_lines[0] != "Preliminary classification: " + value
            or value not in (*CLASSES, "null")):
        raise ValueError("初步类型只能逐字写为 Type 1 QSO、Type 2 QSO、ELG、LRG/BGS 或 null")
    return None if value == "null" else value


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _expected_path(actual: str, expected: Path) -> bool:
    return Path(actual).resolve() == expected


def _writer_result(value: Any, expected: Path) -> bool:
    return (
        isinstance(value, dict)
        and isinstance(value.get("path"), str)
        and _expected_path(value["path"], expected)
        and expected.is_file()
    )


async def _run_until(agent: Any, messages: list[Any], *, config: dict,
                     completed: Callable[[], bool],
                     on_event: Callable[[Any], None] | None = None) -> list[Any]:
    """Stop immediately after the successful tool result enters the transcript."""
    seen = list(messages)
    async with aclosing(agent.astream({"messages": messages}, config=config,
                                     stream_mode="updates")) as stream:
        async for event in stream:
            if on_event is not None:
                on_event(event)
            if isinstance(event, dict):
                for update in event.values():
                    if isinstance(update, dict):
                        seen.extend(update.get("messages") or [])
            if completed():
                break
    return seen


async def _repair_incomplete_stage(agent: Any, messages: list[Any], *, config: dict,
                                   completed: Callable[[], bool],
                                   recorder: MarkdownSessionRecorder,
                                   instruction: str) -> list[Any]:
    """Give one incomplete tool phase a bounded, archived continuation turn."""
    if completed():
        return messages
    followup = HumanMessage(content=instruction)
    recorder.record_event({"continuation_input": {"messages": [followup]}})
    return await _run_until(agent, [*messages, followup], config=config,
                            completed=completed, on_event=recorder.record_event)


async def run_sh_pre_analysis(
    *,
    llm: Any,
    run_id: str,
    hypothesis_ref: str,
    hypothesis_redshift: float,
    sh_context: str,
    csv_path: str | Path,
    report_path: str | Path,
    csv_writer: Any,
    report_writer: Any,
    measurement_catalog_path: str | Path | None = None,
    judgment_path: str | Path | None = None,
    session_stage1_path: str | Path | None = None,
    session_stage2_path: str | Path | None = None,
    execution: ExecutionAllocation | None = None,
    node_store: MutableMapping[str, dict[str, Any]] | None = None,
    prompt_dir: Path = PROMPT_DIR,
    agent_factory: Callable[..., Any] = create_agent,
    recursion_limit: int = 100,
) -> dict[str, Any]:
    """Run SH, append a second user turn, and commit one validated node value.

    ``csv_writer`` and ``report_writer`` are the trusted tool implementations
    selected by the caller. Only their expected-path wrappers are model-facing.
    The second agent sees the first transcript but has only the submission tool.
    """
    key = node_key(run_id, hypothesis_ref)
    if execution is not None:
        validate_execution(execution)
        if (execution.run_id != run_id or execution.node_key != key
                or Path(csv_path).resolve() != execution.path("lines.csv")
                or Path(report_path).resolve() != execution.path("report.md")):
            raise ValueError("SH output paths or node key differ from allocated execution")
        if session_stage1_path is not None or session_stage2_path is not None:
            raise ValueError("allocated SH execution owns its session paths")
        session_stage1_path = execution.path("stage1_session.md")
        session_stage2_path = execution.path("stage2_session.md")
    store_key = execution.node_execution_id if execution is not None else key
    store = node_store if node_store is not None else {}
    if store_key in store:
        raise PreAnalysisError(f"node {key!r} already exists; revisions need a separate contract")
    if not sh_context.strip():
        raise ValueError("sh_context must be non-empty")
    if recursion_limit < 2:
        raise ValueError("recursion_limit must be at least 2")
    if not math.isfinite(hypothesis_redshift):
        raise ValueError("hypothesis_redshift must be finite")
    csv_expected = Path(csv_path).resolve()
    report_expected = Path(report_path).resolve()
    stage1_expected = (Path(session_stage1_path).resolve() if session_stage1_path else
                       report_expected.with_name(report_expected.stem + "_stage1_session.md"))
    stage2_expected = (Path(session_stage2_path).resolve() if session_stage2_path else
                       report_expected.with_name(report_expected.stem + "_stage2_session.md"))
    if len({csv_expected, report_expected, stage1_expected, stage2_expected}) != 4:
        raise ValueError("CSV, report and session paths must all differ")
    if stage1_expected.exists() or stage2_expected.exists():
        raise PreAnalysisError("本节点的会话记录路径已存在；需使用新的运行目录")
    catalog_expected = Path(measurement_catalog_path).resolve() if measurement_catalog_path else None
    judgment_expected = Path(judgment_path).resolve() if judgment_path else None
    if (catalog_expected is None) != (judgment_expected is None):
        raise ValueError("measurement catalog and judgments must be supplied together")
    if catalog_expected is not None and (not catalog_expected.is_file() or judgment_expected.exists()):
        raise PreAnalysisError("measurement catalog must exist and judgment output must be new")
    catalog_digest = _digest(catalog_expected) if catalog_expected else None
    if csv_expected == report_expected:
        raise ValueError("CSV and report paths must differ")
    if csv_expected.exists() or report_expected.exists():
        raise PreAnalysisError("本节点的 CSV 或报告路径已存在；需使用新的运行目录")
    z_text = repr(float(hypothesis_redshift))
    system = _render("sh_pre_analysis_system.md", {}, prompt_dir)
    user1 = _render("sh_pre_analysis_user_1.md", {
        "HYPOTHESIS_REDSHIFT": z_text,
        "CSV_PATH": str(csv_expected),
        "REPORT_PATH": str(report_expected),
        "SH_CONTEXT": sh_context,
    }, prompt_dir)
    user2 = _render("sh_pre_analysis_user_2.md", {}, prompt_dir)

    csv_digest: str | None = None
    judgment_digest: str | None = None
    report_digest: str | None = None
    report_csv_digest: str | None = None
    report_classification: str | None = None
    report_written = False

    @tool("write_lines_csv")
    def guarded_csv(file_path: str, lines: list) -> dict:
        """Write all predicted-line rows to the fixed CSV path."""
        nonlocal csv_digest, judgment_digest
        if not _expected_path(file_path, csv_expected):
            return {"ok": False, "path": None, "error": f"CSV 路径必须是 {csv_expected}"}
        result = csv_writer.invoke({"file_path": str(csv_expected), "lines": lines})
        if (_writer_result(result, csv_expected)
                and type(result.get("n_lines")) is int and result["n_lines"] >= 0):
            csv_digest = _digest(csv_expected)
            if judgment_expected is not None and judgment_expected.is_file():
                judgment_digest = _digest(judgment_expected)
        return result

    @tool("write_report")
    def guarded_report(file_path: str, content: str) -> dict:
        """Write the report after CSV success; verify locked z and class line."""
        nonlocal report_digest, report_csv_digest, report_classification, report_written
        if not _expected_path(file_path, report_expected):
            return {"ok": False, "path": None, "error": f"报告路径必须是 {report_expected}"}
        if csv_digest is None or not csv_expected.is_file() or _digest(csv_expected) != csv_digest:
            return {"ok": False, "path": None, "error": "先成功写入本次 CSV，再写报告"}
        try:
            parsed_class = _report_class(content, z_text)
        except ValueError as exc:
            return {"ok": False, "path": None, "error": str(exc)}
        result = report_writer.invoke({"file_path": str(report_expected), "content": content})
        if (_writer_result(result, report_expected)
                and result.get("size_bytes") == len(content.encode("utf-8"))
                and report_expected.read_text(encoding="utf-8") == content):
            report_digest = _digest(report_expected)
            report_csv_digest = csv_digest
            report_classification = parsed_class
            report_written = True
        return result

    config = {"recursion_limit": recursion_limit}
    phase1_input = [HumanMessage(content=user1)]
    stage1_record = MarkdownSessionRecorder(
        stage1_expected, run_id=run_id, hypothesis_ref=hypothesis_ref,
        stage="spectral review", system_prompt=system,
        input_messages=phase1_input, tools=["write_lines_csv", "write_report"],
    )
    try:
        phase1_agent = agent_factory(
            model=llm, tools=[guarded_csv, guarded_report],
            system_prompt=system,
        )
        phase1_messages = await _run_until(
            phase1_agent, phase1_input, config=config,
            completed=lambda: report_written, on_event=stage1_record.record_event,
        )
        if not report_written:
            if csv_digest is not None and csv_expected.is_file() and _digest(csv_expected) != csv_digest:
                raise PreAnalysisError("CSV 在第一阶段结束后发生变化，拒绝续写")
            phase1_messages = await _repair_incomplete_stage(
                phase1_agent, phase1_messages, config=config,
                completed=lambda: report_written, recorder=stage1_record,
                instruction=(
                    "The first phase is incomplete. "
                    + ("The CSV was written successfully; do not rewrite it. "
                       if csv_digest is not None else
                       "The CSV has not been written successfully. Write it first. ")
                    + "Call write_report with the complete report at the required path now. "
                    "A statement that you will write it is not completion. "
                    "Do not attempt preliminary classification yet."
                ),
            )
        if (not report_written or csv_digest is None or report_digest is None
                or report_csv_digest != csv_digest):
            raise PreAnalysisError("第一阶段未成功写入本次 CSV 和报告；未追加第二阶段提示词")
        if judgment_expected is not None and judgment_digest is None:
            raise PreAnalysisError("ID 判读记录未写入；未追加第二阶段提示词")
        if _digest(csv_expected) != csv_digest or _digest(report_expected) != report_digest:
            raise PreAnalysisError("第一阶段产物在分类注入前发生变化")
    except Exception as exc:
        stage1_record.finish(status="failed", error_type=type(exc).__name__)
        raise
    stage1_record.finish(status="complete")

    submitted: dict[str, Any] | None = None

    @tool("submit_preliminary_classification", args_schema=_SubmissionArgs)
    def submit_classification(classification: str | None) -> dict:
        """Inject exactly the report's preliminary class into this hypothesis node."""
        nonlocal submitted
        if submitted is not None:
            return {"ok": False, "error": "本节点已经完成注入"}
        if classification not in (*CLASSES, None):
            return {"ok": False, "error": "classification 只能是四种精确类型或 JSON null"}
        if _digest(csv_expected) != csv_digest or _digest(report_expected) != report_digest:
            return {"ok": False, "error": "CSV 或报告已变化，拒绝注入"}
        if (catalog_expected is not None and
                (_digest(catalog_expected) != catalog_digest
                 or not judgment_expected.is_file()
                 or _digest(judgment_expected) != judgment_digest)):
            return {"ok": False, "error": "测量目录或 ID 判读记录已变化，拒绝注入"}
        try:
            current_class = _report_class(report_expected.read_text(encoding="utf-8"), z_text)
        except ValueError as exc:
            return {"ok": False, "error": f"报告格式错误：{exc}"}
        if classification != current_class or classification != report_classification:
            expected = "null" if current_class is None else current_class
            return {"ok": False, "error": f"与报告 `Preliminary classification:` 不一致；报告值为 {expected}"}
        candidate = {
            "key": key,
            "hypothesis_ref": hypothesis_ref,
            "hypothesis_redshift": float(hypothesis_redshift),
            "classification": classification,
            "status": "unresolved" if classification is None else "complete",
            "classification_unavailable_reason": (
                "not_classifiable_at_this_stage" if classification is None else None
            ),
            "csv_path": str(csv_expected),
            "csv_sha256": csv_digest,
            "report_path": str(report_expected),
            "report_sha256": report_digest,
        }
        if execution is not None:
            candidate["execution"] = execution.metadata()
        if catalog_expected is not None:
            candidate.update({
                "measurement_catalog_path": str(catalog_expected),
                "measurement_catalog_sha256": catalog_digest,
                "judgment_path": str(judgment_expected),
                "judgment_sha256": judgment_digest,
            })
        store[store_key] = candidate
        submitted = candidate
        return {"ok": True, "node_key": key, "status": candidate["status"]}

    phase2_input = [*phase1_messages, HumanMessage(content=user2)]
    stage2_record = MarkdownSessionRecorder(
        stage2_expected, run_id=run_id, hypothesis_ref=hypothesis_ref,
        stage="classification injection", system_prompt=system,
        input_messages=phase2_input, tools=["submit_preliminary_classification"],
    )
    try:
        phase2_agent = agent_factory(
            model=llm, tools=[submit_classification], system_prompt=system,
        )
        messages = await _run_until(
            phase2_agent, phase2_input,
            config=config, completed=lambda: submitted is not None,
            on_event=stage2_record.record_event,
        )
        if submitted is None:
            messages = await _repair_incomplete_stage(
                phase2_agent, messages, config=config,
                completed=lambda: submitted is not None, recorder=stage2_record,
                instruction=(
                    "The classification has not been submitted. "
                    "Call submit_preliminary_classification with the exact value "
                    "already written in the report, or JSON null if the report says null. "
                    "A statement that you will submit it is not completion."
                ),
            )
        if submitted is None:
            raise PreAnalysisError("第二阶段未成功注入分类；节点未写入")
        stage2_record.finish(status="complete")
        submitted.update({
            "session_stage1_path": str(stage1_expected),
            "session_stage1_sha256": _digest(stage1_expected),
            "session_stage2_path": str(stage2_expected),
            "session_stage2_sha256": _digest(stage2_expected),
        })
        if execution is not None:
            with execution.path("node.json").open("x", encoding="utf-8") as stream:
                json.dump(submitted, stream, ensure_ascii=False, indent=2, allow_nan=False)
                stream.write("\n")
    except Exception as exc:
        store.pop(store_key, None)
        if submitted is None:
            stage2_record.finish(status="failed", error_type=type(exc).__name__)
        raise
    return {
        "node": submitted,
        "messages": messages,
        "model_usage": {"stage1": stage1_record.model_calls,
                        "stage2": stage2_record.model_calls},
        "system_prompt": system,
        "first_user_prompt": user1,
        "second_user_prompt": user2,
    }
