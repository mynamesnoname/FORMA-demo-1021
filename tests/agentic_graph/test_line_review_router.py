"""New SH line-only contract and replayable code-owned entry routing."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from langchain_core.tools import tool

from FORMA.agentic_graph.execution_artifacts import allocate_execution
from FORMA.agentic_graph.feature_registry import build_feature_registry
from FORMA.agentic_graph.reasoning_trace import (fork_branch, new_trace, record_analysis,
                                                record_fa_vote, state_at_event)
from FORMA.agentic_graph.sh_line_review import run_sh_line_review
from FORMA.agentic_graph.type_entry_router import route_type_entry

from test_lrg_bgs_path import _fixture_lrg
from test_sh_pre_analysis import _FakeAgent


@tool("fake_id_writer")
def _writer(file_path: str, lines: list) -> dict:
    """Write a frozen judgment table for the node contract test."""
    path = Path(file_path)
    path.write_text("name,status,fitted_center,amplitude,source\n"
                    "Ca K_abs,MARGINAL,4561.0,-1.2,fit_peak\n", encoding="utf-8")
    path.with_name("lines_judgments.json").write_text(json.dumps(lines) + "\n", encoding="utf-8")
    return {"path": file_path, "n_lines": len(lines)}


class LineReviewRouterTests(unittest.IsolatedAsyncioTestCase):
    async def test_line_review_writes_csv_and_session_without_report_or_class(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            allocation = allocate_execution(root, run_id="r", branch_id="main",
                                            node_key="sh.pre_analysis/r/H1")
            catalog = root / "catalog.json"
            spectrum = root / "spectrum.npz"
            np.savez_compressed(spectrum, wavelength=np.linspace(4500, 4600, 101),
                                flux=np.ones(101))
            catalog.write_text(json.dumps({"spectrum_npz_path": str(spectrum)}) + "\n",
                               encoding="utf-8")
            rows = [{"line_id": "line:cak-3934-abs", "measurement_id": "fit:H1:0000",
                     "status": "MARGINAL", "reason_codes": ["depth_uncertain"],
                     "comment": "Centre aligned; depth order uncertain"}]
            def factory(*, model, tools, system_prompt):
                self.assertEqual([item.name for item in tools], ["write_lines_csv"])
                self.assertNotIn("Overall Verdict", system_prompt)
                return _FakeAgent(tools, [("write_lines_csv", {
                    "file_path": str(allocation.path("lines.csv")), "lines": rows})], [])
            result = await run_sh_line_review(
                llm=object(), run_id="r", hypothesis_ref="H1",
                hypothesis_redshift=.159, sh_context="frozen line and measurement table",
                csv_path=allocation.path("lines.csv"), csv_writer=_writer,
                measurement_catalog_path=catalog,
                judgment_path=allocation.path("lines_judgments.json"),
                execution=allocation, agent_factory=factory)
            node = result["node"]
            self.assertEqual(node["schema_version"], "forma-sh-line-review-v1")
            self.assertNotIn("classification", node)
            self.assertFalse(allocation.path("report.md").exists())
            self.assertFalse(allocation.path("stage2_session.md").exists())
            self.assertTrue(allocation.path("node.json").exists())
            self.assertTrue(allocation.path("adopted_lines.png").is_file())
            self.assertEqual(len(node["adopted_lines_plot_sha256"]), 64)
            self.assertIn("depth order uncertain", allocation.path("lines_judgments.json").read_text())

    async def test_ca_pair_opens_lrg_bgs_and_route_replays(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _fixture_lrg(root, strong=False)
            for ref in ("h1", "h2"):
                path = root / ref / "node.json"
                node = json.loads(path.read_text())
                node["schema_version"] = "forma-sh-line-review-v1"
                node.pop("classification")
                path.write_text(json.dumps(node) + "\n")
            trace = new_trace(build_feature_registry(
                root / "vi/manifest.json", [root / "h1/node.json", root / "h2/node.json"]))
            for ref in ("h1", "h2"):
                record_analysis(trace, "main", kind="sh_pre_analysis_import",
                                analysis_ref=ref, artifact_refs=[f"sh/{ref}/node"])
            for feature_id in trace["branches"]["main"]["state"]["registry"]["features"]:
                for seat in range(3):
                    record_fa_vote(trace, "main", feature_id,
                                   vote_id=f"{feature_id}:{seat}", reviewer_id=f"r{seat}",
                                   answer="yes", origin="model")
            result = route_type_entry(trace, branch_id="main", hypothesis_ref="h1",
                                      output_root=root / "out")
            self.assertEqual(result["node"]["output"]["selected_initial_graph"], "LRG/BGS")
            self.assertEqual(result["node"]["output"]["selected_reason"], "old_population_candidate")
            self.assertEqual(trace["branches"]["main"]["state"]["registry"]["hypotheses"]["h1"]["classification"], "LRG/BGS")
            event = trace["branches"]["main"]["events"][-1]
            replay = state_at_event(trace, "main", event["event_id"])
            self.assertEqual(replay["registry"]["hypotheses"]["h1"]["entry_route_ref"], result["artifact_ref"])
            fork_branch(trace, parent_branch_id="main", fork_event_id=event["event_id"],
                        branch_id="check", purpose="route replay")
            self.assertEqual(trace["branches"]["check"]["state"]["registry"]["hypotheses"]["h1"]["classification"], "LRG/BGS")


if __name__ == "__main__":
    unittest.main()
