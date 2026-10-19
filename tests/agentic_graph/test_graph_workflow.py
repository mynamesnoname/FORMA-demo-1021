"""The controller routes frozen SH/FA state without inventing a final verdict."""

from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from FORMA.agentic_graph.graph_workflow import GraphWorkflow, SHBatchIncompleteError
from FORMA.agentic_graph.feature_registry import _digest
from FORMA.agentic_graph.lrg_bgs_path import run_lrg_bgs_path_through_report
from FORMA.agentic_graph.reasoning_trace import (record_fa_vote, record_type_fallback,
                                                 state_at_event)
from FORMA.agentic_graph.vi_fits_adapter import _redrock_labels

from test_lrg_bgs_path import _VoteAgent, _fixture_lrg
from test_feature_registry_and_trace import _Q11Model


async def _model_votes(**kwargs):
    trace = kwargs["trace"]
    registry = trace["branches"]["main"]["state"]["registry"]
    count = 0
    for feature_id in registry["features"]:
        for seat in range(3):
            record_fa_vote(trace, "main", feature_id,
                           vote_id=f"{feature_id}:{seat}",
                           reviewer_id=f"reviewer:{feature_id}:{seat}",
                           answer="yes", origin="model")
            count += 1
    return {"successful_votes": count}


class GraphWorkflowTests(unittest.IsolatedAsyncioTestCase):
    async def test_dead_lrg_entry_continues_into_eligible_elg_graph(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _fixture_lrg(root, mode="one", strong=False)
            manifest_file = root / "vi/manifest.json"
            manifest = json.loads(manifest_file.read_text())
            oii = {"feature_id": "cwt:em:0001", "wavelength": 3727.0}
            manifest["cwt_features"]["emission"].append(oii)
            (root / "vi/cwt_features.json").write_text(
                json.dumps(manifest["cwt_features"]) + "\n")
            manifest_file.write_text(json.dumps(manifest) + "\n")
            for ref in ("h1", "h2"):
                node_file = root / ref / "node.json"
                node = json.loads(node_file.read_text())
                node["schema_version"] = "forma-sh-line-review-v1"
                node.pop("classification")
                catalog_file = Path(node["measurement_catalog_path"])
                catalog = json.loads(catalog_file.read_text())
                catalog["lines"].append({"id": "line:oii-3727", "kind": "emission",
                                         "predicted_obs": 3727.0})
                catalog["measurements"].append({"id": "cwt:em:0001", "source": "CWT",
                                                "kind": "emission", "adoptable": True,
                                                "record": oii})
                catalog_file.write_text(json.dumps(catalog) + "\n")
                judgment_file = Path(node["judgment_path"])
                judgments = json.loads(judgment_file.read_text())
                judgments.append({"line_id": "line:oii-3727",
                                  "measurement_id": "cwt:em:0001", "status": "LIKELY"})
                judgment_file.write_text(json.dumps(judgments) + "\n")
                node["measurement_catalog_sha256"] = _digest(catalog_file)
                node["judgment_sha256"] = _digest(judgment_file)
                node_file.write_text(json.dumps(node) + "\n")

            async def rejected_lrg(*args, **kwargs):
                return await run_lrg_bgs_path_through_report(
                    *args, **kwargs,
                    agent_factory=lambda **items: _VoteAgent(items["tools"][0], "no"))

            workflow = GraphWorkflow(SimpleNamespace(), model_factory=lambda stage: object(),
                                     fa_reviewer=_model_votes)
            with patch("FORMA.agentic_graph.graph_workflow.run_lrg_bgs_path_through_report",
                       side_effect=rejected_lrg):
                summary = await workflow.run_from_sh(
                    manifest_path=manifest_file,
                    sh_node_paths=[root / "h1/node.json", root / "h2/node.json"],
                    output_root=root / "out")
            self.assertEqual(summary["surviving_hypotheses"], ["h1", "h2"])
            for ref in ("h1", "h2"):
                row = summary["hypotheses"][ref]
                self.assertEqual(row["preliminary_classification"], "LRG/BGS")
                self.assertEqual(row["candidate_type"], "ELG")
                self.assertEqual(row["initial_graph_status"], "dead")
                self.assertEqual(row["eligible_graphs"], ["LRG/BGS", "ELG"])
                self.assertTrue(row["initial_graph_report_ref"])
            tree = json.loads((root / "out/reasoning_tree.json").read_text())
            self.assertEqual(len([event for event in tree["branches"]["main"]["events"]
                                  if event["kind"] == "type_graph_fallback"]), 2)
            for ref in ("h1", "h2"):
                entry_key = f"sh2.elg/{ref}/elg.entry"
                entry = next(event for event in tree["branches"]["main"]["events"]
                             if event["kind"] == "analysis_result"
                             and event["payload"]["analysis_ref"] == entry_key)
                entry_node = json.loads(Path(tree["artifacts"][entry["artifact_refs"][0]]
                                             ["path"]).read_text())
                self.assertEqual(entry_node["output"]["entry_mode"], "fallback")
                self.assertEqual(entry_node["output"]["preliminary_classification"],
                                 "LRG/BGS")
                row = summary["hypotheses"][ref]
                fallback_event = next(
                    event for event in tree["branches"]["main"]["events"]
                    if event["kind"] == "type_graph_fallback"
                    and event["payload"]["hypothesis_ref"] == ref)
                replayed = state_at_event(tree, "main", fallback_event["event_id"])
                self.assertEqual(replayed["registry"]["hypotheses"][ref]
                                 ["classification"], "LRG/BGS")
                with self.assertRaisesRegex(ValueError, "already active"):
                    record_type_fallback(
                        tree, "main", hypothesis_ref=ref, from_graph="LRG/BGS",
                        to_graph="ELG", route_ref=row["fallback_source_route_ref"],
                        entry_route_ref=row["entry_route_ref"])

    async def test_line_only_sh_is_code_routed_after_fa(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _fixture_lrg(root, strong=False)
            for ref in ("h1", "h2"):
                path = root / ref / "node.json"
                node = json.loads(path.read_text())
                node["schema_version"] = "forma-sh-line-review-v1"
                node.pop("classification")
                path.write_text(json.dumps(node) + "\n")
            workflow = GraphWorkflow(SimpleNamespace(), model_factory=lambda stage: object(),
                                     fa_reviewer=_model_votes)
            summary = await workflow.run_from_sh(
                manifest_path=root / "vi/manifest.json",
                sh_node_paths=[root / "h1/node.json", root / "h2/node.json"],
                output_root=root / "out")
            self.assertEqual(summary["surviving_hypotheses"], ["h1", "h2"])
            self.assertEqual(summary["hypotheses"]["h1"]["candidate_type"], "LRG/BGS")
            self.assertEqual(summary["hypotheses"]["h1"]["eligible_graphs"], ["LRG/BGS"])
            self.assertIn("entry_route/", summary["hypotheses"]["h1"]["entry_route_ref"])
            self.assertTrue((root / "out/reasoning_tree.json").exists())

    async def test_one_sh_failure_does_not_cancel_successful_sibling(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _fixture_lrg(root)
            manifest_file = root / "vi/manifest.json"
            manifest = json.loads(manifest_file.read_text())
            for item in manifest["hypotheses"].values():
                item["redshift"] = 0.0
            manifest_file.write_text(json.dumps(manifest) + "\n")
            fits = root / "input.fits"
            fits.write_bytes(b"frozen SH test path")

            async def one_sh(**kwargs):
                ref = kwargs["hypothesis_ref"]
                if ref == "h1":
                    raise ValueError("planned SH failure")
                await asyncio.sleep(0.01)
                kwargs["execution"].path("node.json").write_bytes(
                    (root / ref / "node.json").read_bytes())

            workflow = GraphWorkflow(SimpleNamespace(), model_factory=lambda stage: object(),
                                     sh_runner=one_sh, fa_reviewer=_model_votes)
            output = root / "out"
            with self.assertRaises(SHBatchIncompleteError):
                await workflow.run_prepared(
                    manifest_path=manifest_file, fits_path=fits,
                    output_root=output)
            summary = json.loads((output / "sh_batch_summary.json").read_text())
            self.assertEqual(summary["failed"], {"h1": "ValueError"})
            self.assertIn("h2", summary["completed"])
            self.assertTrue(Path(summary["completed"]["h2"]).is_file())

    async def test_lrg_route_from_frozen_sh_keeps_candidate_and_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _fixture_lrg(root)
            advisory_calls = []

            async def advisory(**kwargs):
                registry = kwargs["trace"]["branches"]["main"]["state"]["registry"]
                self.assertTrue(all(entry["observed_signal_state"] == "signal_present"
                                    for entry in registry["features"].values()))
                advisory_calls.append(kwargs["branch_id"])
                return {"hypotheses": []}

            workflow = GraphWorkflow(
                SimpleNamespace(), model_factory=lambda stage: object(),
                fa_reviewer=_model_votes, fa_advisory_reviewer=advisory)
            output = root / "out"
            summary = await workflow.run_from_sh(
                manifest_path=root / "vi/manifest.json",
                sh_node_paths=[root / "h1/node.json", root / "h2/node.json"],
                output_root=output)
            self.assertEqual(summary["status"], "hs_comparison_complete")
            self.assertFalse(summary["final_classification_available"])
            self.assertEqual(summary["surviving_hypotheses"], ["h1", "h2"])
            self.assertEqual(summary["hypotheses"]["h1"]["candidate_type"], "LRG/BGS")
            self.assertEqual(len(summary["hs_groups"]), 1)
            self.assertEqual(summary["hs_groups"][0]["member_hypotheses"], ["h1", "h2"])
            self.assertEqual(summary["hs_groups"][0]["merge_status"], "merged")
            self.assertEqual(summary["hs_comparison"]["winner_group_id"],
                             summary["hs_groups"][0]["group_id"])
            self.assertTrue(summary["hs_comparison"]["ra_review_pending"])
            self.assertIn(summary["hs_comparison_ref"],
                          json.loads((output / "reasoning_tree.json").read_text())["artifacts"])
            self.assertIn(summary["hs_merge_ref"],
                          json.loads((output / "reasoning_tree.json").read_text())["artifacts"])
            self.assertTrue((output / "reasoning_tree.json").is_file())
            self.assertEqual(advisory_calls, ["main"])
            self.assertTrue((output / "trace_after_fa_advisory.json").is_file())
            self.assertTrue((output / "trace_after_h1.json").is_file())
            self.assertFalse((output / "final_report.md").exists())
            self.assertFalse((output / "in_brief.csv").exists())
            with self.assertRaises(FileExistsError):
                await workflow.run_from_sh(
                    manifest_path=root / "vi/manifest.json",
                    sh_node_paths=[root / "h1/node.json", root / "h2/node.json"],
                    output_root=output)

    async def test_null_classification_is_pruned_without_type_agent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _fixture_lrg(root)
            for ref in ("h1", "h2"):
                path = root / ref / "node.json"
                node = json.loads(path.read_text())
                node["classification"] = None
                path.write_text(json.dumps(node) + "\n")
            workflow = GraphWorkflow(
                SimpleNamespace(), model_factory=lambda stage: object(),
                fa_reviewer=_model_votes)
            summary = await workflow.run_from_sh(
                manifest_path=root / "vi/manifest.json",
                sh_node_paths=[root / "h1/node.json", root / "h2/node.json"],
                output_root=root / "out")
            self.assertEqual(summary["surviving_hypotheses"], [])
            self.assertEqual(summary["hs_groups"], [])
            self.assertIsNone(summary["hs_comparison"]["winner_group_id"])
            self.assertTrue(all(row["path_status"] == "pruned"
                                for row in summary["hypotheses"].values()))

    async def test_prepared_run_submits_independent_bounded_sh_sessions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _fixture_lrg(root)
            manifest_path = root / "vi/manifest.json"
            manifest = json.loads(manifest_path.read_text())
            for item in manifest["hypotheses"].values():
                item["redshift"] = 0.0
            manifest_path.write_text(json.dumps(manifest) + "\n")
            fits = root / "input.fits"
            fits.write_bytes(b"synthetic FITS path for the mocked SH boundary")
            active = peak = 0

            async def frozen_sh(**kwargs):
                nonlocal active, peak
                active += 1
                peak = max(peak, active)
                await asyncio.sleep(0.01)
                ref = kwargs["hypothesis_ref"]
                kwargs["execution"].path("node.json").write_bytes(
                    (root / ref / "node.json").read_bytes())
                active -= 1

            workflow = GraphWorkflow(
                SimpleNamespace(), model_factory=lambda stage: object(),
                sh_runner=frozen_sh, fa_reviewer=_model_votes)
            summary = await workflow.run_prepared(
                manifest_path=manifest_path, fits_path=fits,
                output_root=root / "out", sh_concurrency=2)
            self.assertEqual(peak, 2)
            self.assertEqual(summary["surviving_hypotheses"], ["h1", "h2"])

    async def test_handoff_counts_qso_survival_and_bound_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _fixture_lrg(root, mode="nev")
            model = _Q11Model()
            workflow = GraphWorkflow(
                SimpleNamespace(), model_factory=lambda stage: model,
                fa_reviewer=_model_votes)
            summary = await workflow.run_from_sh(
                manifest_path=root / "vi/manifest.json",
                sh_node_paths=[root / "h1/node.json", root / "h2/node.json"],
                output_root=root / "out")
            self.assertEqual(summary["surviving_hypotheses"], ["h1", "h2"])
            for row in summary["hypotheses"].values():
                self.assertEqual(row["source_path_status"], "transfer")
                self.assertEqual(row["candidate_type"], "Type 2 QSO")
                self.assertTrue(row["qso_report_ref"])
            self.assertEqual(model.calls, 2)

    async def test_missing_fits_preserves_failure_boundary(self):
        workflow = GraphWorkflow(SimpleNamespace(io=SimpleNamespace(input_format="fits")))
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                await workflow.run_fits(Path(directory) / "missing.fits",
                                        Path(directory) / "out")
            self.assertFalse((Path(directory) / "out").exists())


class RedrockLabelTests(unittest.TestCase):
    def test_znum_binds_neutral_labels_and_rejects_duplicate(self):
        rows = {"hypotheses": [
            {"z_representative": 0.4, "_redrock": {"znum": 2, "spectype": "GALAXY"}},
            {"z_representative": 1.7, "_redrock": {"znum": 1, "spectype": "QSO"}},
        ]}
        a, labels = _redrock_labels(rows, "fixed")
        b, other = _redrock_labels({"hypotheses": list(reversed(rows["hypotheses"]))}, "fixed")
        self.assertEqual(a, b)
        self.assertEqual(labels, other)
        self.assertEqual({item["znum"] for item in labels["entries"]}, {1, 2})
        with self.assertRaisesRegex(ValueError, "unique"):
            _redrock_labels({"hypotheses": [rows["hypotheses"][0]] * 2}, "fixed")
