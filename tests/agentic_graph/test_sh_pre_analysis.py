"""Behavioral tests for the two-turn SH node boundary."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool

from FORMA.agentic_graph.sh_pre_analysis import (
    PreAnalysisError, _report_class, node_key, run_sh_pre_analysis,
)
from FORMA.agentic_graph.execution_artifacts import allocate_execution
from FORMA.agents.multi_agents.harness.single_hypothesis import _build_user_message


def _report(z: float, classification: str | None) -> str:
    value = "null" if classification is None else classification
    return (f"### 3a. Spectrum Summary\nHypothesis redshift: {repr(z)}\n待检查\n"
            "### 3b. Overall Verdict\n待检查\n"
            "### 3c. Per-Line Results\n待检查\n"
            "### 3d. Key Findings\n待检查\n"
            f"### 3e. Classification\nPreliminary classification: {value}\n"
            "### 3f. Caveats\n待检查\n")


@tool("csv_writer")
def _csv_writer(file_path: str, lines: list) -> dict:
    """Fake a successful CSV writer."""
    Path(file_path).write_text("name,status\nOII,LIKELY\n", encoding="utf-8")
    return {"path": file_path, "n_lines": len(lines)}


@tool("report_writer")
def _report_writer(file_path: str, content: str) -> dict:
    """Fake a successful report writer."""
    Path(file_path).write_text(content, encoding="utf-8")
    return {"path": file_path, "size_bytes": len(content.encode("utf-8"))}


class _FakeAgent:
    def __init__(self, tools, script, received):
        self.tools = {item.name: item for item in tools}
        self.script = script
        self.received = received

    async def astream(self, state, *, config, stream_mode):
        assert stream_mode == "updates"
        self.received.append(state["messages"])
        for index, (name, args) in enumerate(self.script):
            call_id = f"call-{index}"
            yield {"agent": {"messages": [AIMessage(
                content="", tool_calls=[{"name": name, "args": args, "id": call_id}],
            )]}}
            result = self.tools[name].invoke(args)
            yield {"tools": {"messages": [ToolMessage(
                content=json.dumps(result, ensure_ascii=False),
                tool_call_id=call_id, name=name,
            )]}}


class PreAnalysisTests(unittest.IsolatedAsyncioTestCase):
    async def test_stage1_premature_finish_gets_one_archived_completion_turn(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inputs, store, _, _ = await self._run(root)
            stage1_calls = []
            factory_calls = 0

            class RepairAgent:
                def __init__(self, tools):
                    self.tools = tools

                async def astream(self, state, *, config, stream_mode):
                    stage1_calls.append(state["messages"])
                    script = ([
                        ("write_lines_csv", {"file_path": str(root / "lines.csv"),
                                             "lines": [{"name": "OII"}]}),
                    ] if len(stage1_calls) == 1 else [
                        ("write_report", {"file_path": str(root / "report.md"),
                                          "content": _report(1.2, "Type 2 QSO")}),
                    ])
                    async for event in _FakeAgent(self.tools, script, []).astream(
                            state, config=config, stream_mode=stream_mode):
                        yield event

            def factory(*, model, tools, system_prompt):
                nonlocal factory_calls
                factory_calls += 1
                if factory_calls == 1:
                    return RepairAgent(tools)
                return _FakeAgent(tools, [
                    ("submit_preliminary_classification",
                     {"classification": "Type 2 QSO"})], [])

            inputs["agent_factory"] = factory
            result = await run_sh_pre_analysis(**inputs)
            self.assertEqual(result["node"]["classification"], "Type 2 QSO")
            self.assertEqual(len(stage1_calls), 2)
            self.assertIsInstance(stage1_calls[1][-1], HumanMessage)
            self.assertIn("do not rewrite it", stage1_calls[1][-1].content)
            archive = (root / "report_stage1_session.md").read_text()
            self.assertIn("continuation_input", archive)
            self.assertIn("Status: `complete`", archive)

    async def test_same_logical_sh_node_on_two_branches_has_distinct_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store = {}
            for branch in ("main", "recheck"):
                allocation = allocate_execution(
                    root, run_id="run/1", branch_id=branch,
                    node_key=node_key("run/1", "H1"))
                inputs, _, _, _ = await self._run(allocation.directory)
                inputs["node_store"] = store
                inputs["execution"] = allocation
                result = await run_sh_pre_analysis(**inputs)
                self.assertEqual(result["node"]["execution"]["branch_id"], branch)
                self.assertTrue(allocation.path("node.json").is_file())
                self.assertTrue(allocation.path("stage1_session.md").is_file())
            self.assertEqual(len(store), 2)
            self.assertEqual(len({item["key"] for item in store.values()}), 1)

    def test_report_allows_markdown_spacing_before_machine_lines(self):
        report = _report(1.2, "Type 2 QSO")
        report = report.replace(
            "### 3a. Spectrum Summary\nHypothesis redshift:",
            "### 3a. Spectrum Summary\n\nHypothesis redshift:",
        ).replace(
            "### 3e. Classification\nPreliminary classification:",
            "### 3e. Classification\n\nPreliminary classification:",
        )
        self.assertEqual(_report_class(report, "1.2"), "Type 2 QSO")

    def test_legacy_context_adapter_does_not_request_anchor_or_old_json(self):
        context = _build_user_message(
            1.2, "input.fits", "spectrum.npz", peaks=[], troughs=[],
            wavelength_min=3600, wavelength_max=9800, pre_analysis=True,
        )
        self.assertNotIn("Registry anchor candidates", context)
        self.assertNotIn("write report → JSON block", context)
        self.assertIn("wait for the second user message", context)

    async def _run(self, tmp: Path, *, classification="Type 2 QSO",
                   report_z=1.2, phase1_order=None, submissions=None):
        csv_path = tmp / "lines.csv"
        report_path = tmp / "report.md"
        phase1 = phase1_order or [
            ("write_lines_csv", {"file_path": str(csv_path), "lines": [{"name": "OII"}]}),
            ("write_report", {"file_path": str(report_path),
                              "content": _report(report_z, classification)}),
        ]
        phase2 = [("submit_preliminary_classification", {"classification": value})
                  for value in (submissions if submissions is not None else [classification])]
        stages = [phase1, phase2]
        received = []
        created = []

        def factory(*, model, tools, system_prompt):
            created.append([item.name for item in tools])
            return _FakeAgent(tools, stages[len(created) - 1], received)

        store = {}
        inputs = dict(llm=object(), run_id="run/1", hypothesis_ref="H1",
                      hypothesis_redshift=1.2, sh_context="CWT 与预测谱线数据",
                      csv_path=csv_path, report_path=report_path,
                      csv_writer=_csv_writer, report_writer=_report_writer,
                      node_store=store, agent_factory=factory)
        return inputs, store, created, received

    async def test_successful_two_stage_injection_uses_same_transcript(self):
        with tempfile.TemporaryDirectory() as directory:
            inputs, store, created, received = await self._run(Path(directory))
            result = await run_sh_pre_analysis(**inputs)
            key = node_key("run/1", "H1")
            self.assertEqual(result["node"]["key"], key)
            self.assertEqual(result["node"]["hypothesis_redshift"], 1.2)
            self.assertEqual(store[key]["classification"], "Type 2 QSO")
            self.assertEqual(created[0], ["write_lines_csv", "write_report"])
            self.assertEqual(created[1], ["submit_preliminary_classification"])
            self.assertEqual(len(received[1]), 6)
            self.assertIsInstance(received[1][-1], HumanMessage)
            self.assertIn('{"classification":null}', received[1][-1].content)
            self.assertIn("Hypothesis redshift: 1.2", result["first_user_prompt"])
            self.assertEqual(len(result["messages"]), 8)
            first = Path(result["node"]["session_stage1_path"])
            second = Path(result["node"]["session_stage2_path"])
            self.assertTrue(first.is_file())
            self.assertTrue(second.is_file())
            self.assertIn("Hypothesis redshift: 1.2", first.read_text())
            self.assertIn("write_lines_csv", first.read_text())
            self.assertIn("Tool: `write_report`", first.read_text())
            self.assertIn("submit_preliminary_classification", second.read_text())
            self.assertIn("Input message 6: human", second.read_text())
            self.assertIn("Provider reasoning field returned: no", second.read_text())

    async def test_rejected_class_can_be_corrected_without_rewriting_report(self):
        with tempfile.TemporaryDirectory() as directory:
            inputs, store, _, _ = await self._run(
                Path(directory), submissions=["ELG", "Type 2 QSO"])
            result = await run_sh_pre_analysis(**inputs)
            errors = [message.content for message in result["messages"]
                      if isinstance(message, ToolMessage)]
            self.assertTrue(any("不一致" in item for item in errors))
            self.assertEqual(len(store), 1)

    async def test_failed_second_session_keeps_trace_without_committing_node(self):
        with tempfile.TemporaryDirectory() as directory:
            inputs, store, _, _ = await self._run(
                Path(directory), submissions=["ELG"])
            with self.assertRaisesRegex(PreAnalysisError, "未成功注入分类"):
                await run_sh_pre_analysis(**inputs)
            self.assertEqual(store, {})
            second = Path(directory) / "report_stage2_session.md"
            self.assertTrue(second.is_file())
            self.assertIn("Status: `failed`", second.read_text())
            self.assertIn("与报告", second.read_text())

    async def test_wrong_redshift_never_reaches_second_user_turn(self):
        with tempfile.TemporaryDirectory() as directory:
            inputs, store, created, _ = await self._run(Path(directory), report_z=1.3)
            with self.assertRaisesRegex(PreAnalysisError, "未成功写入"):
                await run_sh_pre_analysis(**inputs)
            self.assertEqual(len(created), 1)
            self.assertEqual(store, {})
            first = Path(directory) / "report_stage1_session.md"
            self.assertTrue(first.is_file())
            self.assertIn("Status: `failed`", first.read_text())
            self.assertFalse((Path(directory) / "report_stage2_session.md").exists())

    async def test_report_before_csv_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            inputs, store, created, _ = await self._run(tmp)
            inputs["agent_factory"] = lambda *, model, tools, system_prompt: _FakeAgent(
                tools, [("write_report", {"file_path": str(tmp / "report.md"),
                                          "content": _report(1.2, "ELG")})], [])
            with self.assertRaises(PreAnalysisError):
                await run_sh_pre_analysis(**inputs)
            self.assertEqual(store, {})

    async def test_null_is_unresolved_and_duplicate_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            inputs, store, _, _ = await self._run(Path(directory), classification=None)
            result = await run_sh_pre_analysis(**inputs)
            self.assertIsNone(result["node"]["classification"])
            self.assertEqual(result["node"]["status"], "unresolved")
            with self.assertRaisesRegex(PreAnalysisError, "already exists"):
                await run_sh_pre_analysis(**inputs)
            self.assertEqual(len(store), 1)


if __name__ == "__main__":
    unittest.main()
