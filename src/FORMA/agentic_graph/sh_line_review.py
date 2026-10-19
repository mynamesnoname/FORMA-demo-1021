"""Single-stage SH line review; type decisions belong to the downstream graph."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Callable, MutableMapping

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from .execution_artifacts import ExecutionAllocation, validate_execution
from .node_keys import sh_node_key
from .session_markdown import MarkdownSessionRecorder
from .spectrum_visualization import plot_sh_adopted_lines
from .sh_pre_analysis import (PROMPT_DIR, PreAnalysisError, _digest, _expected_path,
                              _render, _repair_incomplete_stage, _run_until,
                              _writer_result)


async def run_sh_line_review(
    *, llm: Any, run_id: str, hypothesis_ref: str,
    hypothesis_redshift: float, sh_context: str,
    csv_path: str | Path, csv_writer: Any,
    measurement_catalog_path: str | Path, judgment_path: str | Path,
    execution: ExecutionAllocation | None = None,
    node_store: MutableMapping[str, dict] | None = None,
    prompt_dir: Path = PROMPT_DIR,
    agent_factory: Callable[..., Any] = create_agent,
    recursion_limit: int = 100,
) -> dict:
    """Commit a source-bound line table and its model-facing transcript."""
    if not sh_context.strip() or not math.isfinite(hypothesis_redshift):
        raise ValueError("SH context and finite hypothesis redshift are required")
    key = sh_node_key(run_id, hypothesis_ref)
    csv = Path(csv_path).resolve()
    catalog = Path(measurement_catalog_path).resolve(strict=True)
    judgments = Path(judgment_path).resolve()
    if execution is not None:
        validate_execution(execution)
        if (execution.run_id != run_id or execution.node_key != key
                or execution.path("lines.csv") != csv
                or execution.path("lines_judgments.json") != judgments):
            raise ValueError("SH line-review paths differ from allocated execution")
        session = execution.path("stage1_session.md")
    else:
        session = csv.with_name("stage1_session.md")
    if len({csv, catalog, judgments, session}) != 4:
        raise ValueError("SH line-review artifact paths must differ")
    if csv.exists() or judgments.exists() or session.exists():
        raise FileExistsError("SH line-review output already exists")
    if recursion_limit < 2:
        raise ValueError("recursion_limit must be at least 2")
    store = node_store if node_store is not None else {}
    store_key = execution.node_execution_id if execution else key
    if store_key in store:
        raise PreAnalysisError("SH line-review node already exists")
    catalog_digest = _digest(catalog)
    catalog_data = json.loads(catalog.read_text(encoding="utf-8"))
    spectrum_path = Path(catalog_data["spectrum_npz_path"]).resolve(strict=True)
    plot_path = execution.path("adopted_lines.png") if execution else csv.with_name("adopted_lines.png")
    z = repr(float(hypothesis_redshift))
    system = _render("sh_line_review_system.md", {}, prompt_dir)
    user = _render("sh_line_review_user.md", {
        "HYPOTHESIS_REDSHIFT": z,
        "CSV_PATH": str(csv), "SH_CONTEXT": sh_context,
    }, prompt_dir)
    csv_digest = judgment_digest = None

    @tool("write_lines_csv")
    def guarded_csv(file_path: str, lines: list) -> dict:
        """Write exactly one ID-based judgment for each predicted line."""
        nonlocal csv_digest, judgment_digest
        if not _expected_path(file_path, csv):
            return {"ok": False, "path": None, "error": "CSV path differs from allocated path"}
        if _digest(catalog) != catalog_digest:
            return {"ok": False, "path": None, "error": "VI catalog changed"}
        result = csv_writer.invoke({"file_path": str(csv), "lines": lines})
        if (_writer_result(result, csv) and type(result.get("n_lines")) is int
                and judgments.is_file()):
            csv_digest, judgment_digest = _digest(csv), _digest(judgments)
        return result

    first = [HumanMessage(content=user)]
    recorder = MarkdownSessionRecorder(
        session, run_id=run_id, hypothesis_ref=hypothesis_ref,
        stage="line review", system_prompt=system,
        input_messages=first,
        tools=["write_lines_csv"],
    )
    try:
        agent = agent_factory(model=llm, tools=[guarded_csv], system_prompt=system)
        messages = await _run_until(
            agent, first, config={"recursion_limit": recursion_limit},
            completed=lambda: csv_digest is not None,
            on_event=recorder.record_event)
        if csv_digest is None:
            await _repair_incomplete_stage(
                agent, messages, config={"recursion_limit": recursion_limit},
                completed=lambda: csv_digest is not None, recorder=recorder,
                instruction="The line table is incomplete. Call write_lines_csv with all required lines now. A promise to write it is not completion.")
        if (csv_digest is None or judgment_digest is None
                or _digest(csv) != csv_digest or _digest(judgments) != judgment_digest
                or _digest(catalog) != catalog_digest):
            raise PreAnalysisError("SH line review did not commit a frozen CSV and judgment set")
        plot_sh_adopted_lines(
            spectrum_path, csv, plot_path,
            spectrum_path.parent / "VI" / "continuum_display.npz")
    except Exception as exc:
        recorder.finish(status="failed", error_type=type(exc).__name__)
        raise
    recorder.finish(status="complete")
    node = {
        "schema_version": "forma-sh-line-review-v1",
        "key": key, "hypothesis_ref": hypothesis_ref,
        "hypothesis_redshift": float(hypothesis_redshift),
        "status": "complete", "csv_path": str(csv), "csv_sha256": csv_digest,
        "measurement_catalog_path": str(catalog),
        "measurement_catalog_sha256": catalog_digest,
        "judgment_path": str(judgments), "judgment_sha256": judgment_digest,
        "session_stage1_path": str(session),
        "session_stage1_sha256": _digest(session),
        "adopted_lines_plot_path": str(plot_path),
        "adopted_lines_plot_sha256": _digest(plot_path),
    }
    if execution is not None:
        node["execution"] = execution.metadata()
        with execution.path("node.json").open("x", encoding="utf-8") as stream:
            json.dump(node, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
    store[store_key] = node
    return {"node": node, "model_usage": {"stage1": recorder.model_calls},
            "system_prompt": system, "first_user_prompt": user}
