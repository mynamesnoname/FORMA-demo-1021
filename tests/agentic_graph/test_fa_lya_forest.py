"""Forest information must remain scoped, replayable, and outside QSO gates."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from langchain_core.messages import AIMessage, ToolMessage

from FORMA.agentic_graph.fa_lya_forest import (
    build_lya_forest_window, read_lya_forest_information, review_lya_forest,
)
from FORMA.agentic_graph.hs_comparison import _advisory_rows
from FORMA.agentic_graph.feature_registry import build_feature_registry
from FORMA.agentic_graph.reasoning_trace import (
    fork_branch, new_trace, record_analysis, write_trace,
)
from FORMA.core.config.analysis_method import LyalphaForestMethod, load_analysis_method

from test_feature_registry_and_trace import _fixture


class _ForestAgent:
    def __init__(self, tool, answer, seen):
        self.tool, self.answer, self.seen = tool, answer, seen

    async def astream(self, state, *, config, stream_mode):
        self.seen.append(state["messages"][0].content)
        args = {"answer": self.answer, "reason": "Several blueward dips are visible."}
        yield {"model": {"messages": [AIMessage(
            content="I see repeated blueward structure.",
            tool_calls=[{"name": "submit_lya_forest_vote", "args": args, "id": "forest1"}],
            response_metadata={"token_usage": {
                "prompt_tokens": 10, "completion_tokens": 4, "total_tokens": 14}},
        )]}}
        result = self.tool.invoke(args)
        yield {"tools": {"messages": [ToolMessage(
            content=str(result), tool_call_id="forest1", name="submit_lya_forest_vote",
        )]}}


class ForestReviewTests(unittest.IsolatedAsyncioTestCase):
    async def test_three_votes_are_advisory_and_trace_replays(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root, first_line_id="line:lya-1216",
                                       classification="Type 1 QSO")
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            before = copy.deepcopy(trace["branches"]["main"]["state"]["registry"])
            answers = iter(["yes", "no", "yes"])
            seen = []
            result = await review_lya_forest(
                trace=trace, branch_id="main", hypothesis_ref="h1",
                output_root=root / "outputs", llm=object(), concurrency=1,
                agent_factory=lambda **kw: _ForestAgent(kw["tools"][0], next(answers), seen),
            )
            node = result["node"]
            self.assertEqual(node["status"], "complete")
            self.assertEqual(node["visibility"], "visible")
            self.assertEqual(node["vote_summary"]["yes"], 2)
            self.assertEqual(node["model_usage"]["cache_hit_unreported_calls"], 3)
            self.assertIsNotNone(node["prompt_identity"])
            self.assertEqual(node["vote_summary"]["assurance"], "contested")
            self.assertTrue(node["consultative_only"])
            self.assertEqual(trace["branches"]["main"]["state"]["registry"], before)
            self.assertEqual(len(seen), 3)
            self.assertTrue(all("blueward" in message.lower() for message in seen))
            self.assertTrue(all("h1" not in message for message in seen))
            self.assertFalse(node["coverage"]["requested_blue_interval_within_spectrum_bounds"])
            info = read_lya_forest_information(trace, branch_id="main", hypothesis_ref="h1")
            self.assertEqual(info["visibility"], "visible")
            sources = set()
            dossier = _advisory_rows(trace, "main", ["h1"], sources)
            self.assertEqual(dossier[0]["lya_forest"]["visibility"], "visible")
            self.assertIn(result["node_ref"], sources)
            fork_branch(trace, parent_branch_id="main",
                        fork_event_id=trace["branches"]["main"]["events"][-1]["event_id"],
                        branch_id="followup", purpose="independent HS review")
            self.assertEqual(read_lya_forest_information(
                trace, branch_id="followup", hypothesis_ref="h1")["node_ref"],
                result["node_ref"])
            write_trace(trace, root / "outputs/tree.json")
            with self.assertRaisesRegex(ValueError, "not-yet-reviewed"):
                await review_lya_forest(trace=trace, branch_id="main", hypothesis_ref="h1",
                                        output_root=root / "outputs", llm=object())

    async def test_insufficient_blue_data_creates_unreviewable_information_without_model(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root, first_line_id="line:lya-1216")
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            method_config = load_analysis_method().model_copy(deep=True)
            method_config.audit.lyalpha_forest.min_valid_blue_samples = 1000
            with patch("FORMA.agentic_graph.fa_lya_forest.load_analysis_method",
                       return_value=method_config):
                result = await review_lya_forest(
                    trace=trace, branch_id="main", hypothesis_ref="h1",
                    output_root=root / "outputs", llm=object(),
                    agent_factory=lambda **kw: self.fail("model should not be called"),
                )
            self.assertEqual(result["node"]["status"], "unreviewable")
            self.assertIsNone(result["node"]["forest_visible"])
            self.assertEqual(result["model_usage"]["calls"], 0)
            write_trace(trace, root / "outputs/tree.json")

    async def test_exhausted_sessions_stay_pending_and_keep_attempts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root, first_line_id="line:lya-1216")
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])

            def fail(**kwargs):
                raise RuntimeError("temporary service failure")

            result = await review_lya_forest(
                trace=trace, branch_id="main", hypothesis_ref="h1",
                output_root=root / "outputs", llm=object(),
                agent_factory=fail, concurrency=2,
            )
            node = result["node"]
            self.assertEqual(node["status"], "pending")
            self.assertIsNone(node["forest_visible"])
            self.assertEqual(node["failed_seats"], 3)
            self.assertEqual(len([ref for ref in node["attempt_refs"]
                                  if ref.endswith("failure.json")]), 6)
            write_trace(trace, root / "outputs/tree.json")

    def test_window_masks_and_blue_red_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            npz = Path(directory) / "s.npz"
            wl = np.arange(4000., 4111.)
            np.savez(npz, wavelength=wl, flux=np.ones_like(wl), ivar=np.ones_like(wl))
            method = LyalphaForestMethod(blueward_span_angstrom=20,
                                         redward_reference_span_angstrom=10,
                                         min_valid_blue_samples=10)
            data = build_lya_forest_window(npz, lya_wavelength=4100,
                                           masked_regions=[[4080, 4085]], method=method)
            coverage = data["coverage"]
            self.assertEqual(coverage["blue_samples"], 20)
            self.assertEqual(coverage["blue_masked_samples"], 6)
            self.assertEqual(coverage["blue_valid_samples"], 14)
            self.assertEqual(coverage["red_valid_samples"], 11)
            self.assertTrue(coverage["assessable"])
            self.assertIn("| 4080 | 1 | 1 | no |", data["user_prompt"])
            with self.assertRaisesRegex(ValueError, "invalid forest mask"):
                build_lya_forest_window(npz, lya_wavelength=4100,
                                        masked_regions=[[4100, 4000]], method=method)
