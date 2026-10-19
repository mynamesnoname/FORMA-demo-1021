"""The workflow schedules FA advice for kept claims without a type gate."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from FORMA.agentic_graph.fa_advisory import review_fa_advisories


class AdvisorySchedulingTests(unittest.IsolatedAsyncioTestCase):
    async def test_kept_lya_and_claimed_doublet_are_scheduled_and_summarized(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = {"run_id": "r", "artifact_root": str(root),
                     "branches": {"main": {"state": {
                         "active_pre_analysis": ["H1", "H2"]}}}}
            calls = []

            async def forest(**kwargs):
                calls.append(("forest", kwargs["hypothesis_ref"]))
                return {"node_ref": "fa_forest/one/node",
                        "node": {"status": "complete"}}

            async def doublet(**kwargs):
                calls.append(("doublet", kwargs["hypothesis_ref"],
                              kwargs["doublet_id"]))
                return {"node_ref": "fa_doublet/one/node",
                        "node": {"status": "unreviewable"}}

            def judgments(trace, ref):
                return ([{"line_id": "line:lya-1216", "status": "LIKELY"}]
                        if ref == "sh/H1/judgments" else [])

            with patch("FORMA.agentic_graph.fa_advisory._read_artifact",
                       side_effect=judgments), patch(
                       "FORMA.agentic_graph.fa_advisory.claimed_doublet_ids",
                       side_effect=lambda trace, branch, ref:
                       ["doublet:oiii"] if ref == "H1" else []), patch(
                       "FORMA.agentic_graph.fa_advisory.review_lya_forest",
                       side_effect=forest), patch(
                       "FORMA.agentic_graph.fa_advisory.review_doublet",
                       side_effect=doublet):
                summary = await review_fa_advisories(
                    trace=trace, branch_id="main", output_root=root, llm=object())
            self.assertEqual(calls, [("forest", "H1"),
                                     ("doublet", "H1", "doublet:oiii")])
            self.assertIsNone(summary["hypotheses"][1]["lya_forest"])
            self.assertEqual(summary["hypotheses"][0]["doublets"][0]["status"],
                             "unreviewable")
            self.assertEqual(json.loads((root / "fa_advisory_summary.json").read_text()),
                             summary)
