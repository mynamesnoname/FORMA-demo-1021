"""Doublet advisory results must preserve feature states and branch lineage."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from langchain_core.messages import AIMessage, ToolMessage

from FORMA.agentic_graph.fa_doublet import (
    _numeric_metrics, _record, build_doublet_window, claimed_doublet_ids,
    read_doublet_information, review_doublet,
)
from FORMA.agentic_graph.feature_registry import _digest, build_feature_registry
from FORMA.agentic_graph.hs_comparison import _advisory_rows
from FORMA.agentic_graph.reasoning_trace import (
    fork_branch, new_trace, record_analysis, write_trace,
)
from FORMA.core.config.analysis_method import DoubletReviewMethod, load_analysis_method
from FORMA.core.reasoning.ontology.query import oiii_ratio_window_a_over_b

from test_feature_registry_and_trace import _fixture, _json


def _doublet_fixture(root: Path, *, orphan: bool = False,
                     outside: bool = False) -> dict:
    manifest_file, nodes = _fixture(root, redshift=0.0)
    manifest = json.loads(manifest_file.read_text())
    npz = Path(manifest["spectrum_npz_path"])
    wl = np.arange(4900.0, 5072.0 if not outside else 4980.0)
    flux = (np.exp(-0.5 * ((wl - 4960) / 2.0) ** 2)
            + 3 * np.exp(-0.5 * ((wl - 5008) / 2.0) ** 2))
    np.savez(npz, wavelength=wl, flux=flux, ivar=np.ones_like(wl))
    manifest["spectrum_npz_sha256"] = _digest(npz)
    cwt = {"feature_id": "cwt:em:0000", "wavelength": 4960.0, "amplitude": 1.0}
    manifest["cwt_features"]["emission"] = [cwt]
    _json(root / "vi/cwt_features.json", manifest["cwt_features"])
    for node_file in nodes:
        node = json.loads(node_file.read_text())
        catalog_file = Path(node["measurement_catalog_path"])
        catalog = json.loads(catalog_file.read_text())
        catalog.update({"spectrum_npz_sha256": _digest(npz),
                        "wavelength_min": float(wl[0]), "wavelength_max": float(wl[-1])})
        catalog["lines"] = [
            {"id": "line:oiii-4960", "kind": "emission", "predicted_obs": 4960.3},
            {"id": "line:oiii-5008", "kind": "emission", "predicted_obs": 5008.2},
        ]
        catalog["measurements"][0]["record"] = cwt
        catalog["measurements"][1]["record"] = {"center": 5008.0, "amplitude": 3.0}
        _json(catalog_file, catalog)
        judgment_file = Path(node["judgment_path"])
        judgments = json.loads(judgment_file.read_text())
        judgments[0]["line_id"] = "line:oiii-4960"
        judgments[1]["line_id"] = "line:oiii-5008"
        if orphan:
            judgments[1].update({"measurement_id": None, "status": "NOT_FOUND"})
        _json(judgment_file, judgments)
        node["measurement_catalog_sha256"] = _digest(catalog_file)
        node["judgment_sha256"] = _digest(judgment_file)
        _json(node_file, node)
    _json(manifest_file, manifest)
    trace = new_trace(build_feature_registry(manifest_file, nodes))
    record_analysis(trace, "main", kind="sh_pre_analysis_import",
                    analysis_ref="h1", artifact_refs=["sh/h1/node"])
    return trace


class _DoubletAgent:
    def __init__(self, writer, answer, seen):
        self.writer, self.answer, self.seen = writer, answer, seen

    async def astream(self, state, *, config, stream_mode):
        self.seen.append(state["messages"][0].content)
        args = {"answer": self.answer,
                "reason": "Both local peaks have usable pixels at the expected positions."}
        yield {"model": {"messages": [AIMessage(
            content="The two local windows support the pair.",
            tool_calls=[{"name": "submit_doublet_vote", "args": args, "id": "doublet1"}],
            response_metadata={"token_usage": {
                "prompt_tokens": 10, "completion_tokens": 4, "total_tokens": 14}},
        )]}}
        value = self.writer.invoke(args)
        yield {"tools": {"messages": [ToolMessage(
            content=str(value), tool_call_id="doublet1", name="submit_doublet_vote",
        )]}}


class DoubletReviewTests(unittest.IsolatedAsyncioTestCase):
    async def test_pair_votes_and_ratio_are_advisory_and_replayable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _doublet_fixture(root)
            self.assertEqual(claimed_doublet_ids(trace, "main", "h1"), ["doublet:oiii"])
            before = copy.deepcopy(trace["branches"]["main"]["state"]["registry"])
            answers = iter(["yes", "no", "yes"])
            seen = []
            result = await review_doublet(
                trace=trace, branch_id="main", hypothesis_ref="h1",
                doublet_id="doublet:oiii", output_root=root / "outputs",
                llm=object(), concurrency=1,
                agent_factory=lambda **kw: _DoubletAgent(
                    kw["tools"][0], next(answers), seen))
            node = result["node"]
            self.assertEqual(node["status"], "complete")
            self.assertTrue(node["pair_supported"])
            self.assertEqual(node["claim_mode"], "complete_pair")
            self.assertEqual(node["metrics"]["measured_separation_angstrom"], 48.0)
            self.assertAlmostEqual(node["metrics"]["amplitude_ratio_a_over_b"], 1 / 3)
            self.assertEqual(node["metrics"]["reference_ratio_window_a_over_b"],
                             oiii_ratio_window_a_over_b())
            self.assertTrue(node["metrics"]["reference_ratio_within_window"])
            self.assertEqual(node["vote_summary"]["yes"], 2)
            self.assertEqual(node["model_usage"]["cache_hit_unreported_calls"], 3)
            self.assertIsNotNone(node["prompt_identity"])
            self.assertEqual(trace["branches"]["main"]["state"]["registry"], before)
            self.assertTrue(all("line:oiii-5008" in prompt for prompt in seen))
            info = read_doublet_information(trace, branch_id="main", hypothesis_ref="h1",
                                            doublet_id="doublet:oiii")
            self.assertEqual(info["node_ref"], result["node_ref"])
            sources = set()
            dossier = _advisory_rows(trace, "main", ["h1"], sources)
            self.assertEqual(dossier[0]["doublets"][0]["pair_supported"], True)
            self.assertEqual(dossier[0]["doublets"][0]["doublet_id"], "doublet:oiii")
            self.assertIn(result["node_ref"], sources)
            fork_branch(trace, parent_branch_id="main",
                        fork_event_id=trace["branches"]["main"]["events"][-1]["event_id"],
                        branch_id="followup", purpose="separate analysis")
            self.assertEqual(read_doublet_information(
                trace, branch_id="followup", hypothesis_ref="h1",
                doublet_id="doublet:oiii")["node_ref"], result["node_ref"])
            write_trace(trace, root / "outputs/tree.json")
            changed_index = copy.deepcopy(trace)
            changed_index["artifacts"]["sh/h1/catalog"]["sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "source changed"):
                read_doublet_information(changed_index, branch_id="main",
                                         hypothesis_ref="h1", doublet_id="doublet:oiii")

    async def test_orphan_exposes_unpaired_partner_without_fabricated_ratio(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _doublet_fixture(root, orphan=True)
            seen = []
            result = await review_doublet(
                trace=trace, branch_id="main", hypothesis_ref="h1",
                doublet_id="doublet:oiii", output_root=root / "outputs",
                llm=object(), concurrency=1,
                agent_factory=lambda **kw: _DoubletAgent(kw["tools"][0], "no", seen))
            node = result["node"]
            self.assertEqual(node["claim_mode"], "orphan")
            self.assertFalse(node["pair_supported"])
            self.assertIsNone(node["components"][1]["measurement_id"])
            self.assertIsNone(node["metrics"]["amplitude_ratio_a_over_b"])
            self.assertIsNone(node["metrics"]["reference_ratio_within_window"])
            self.assertIn("measurement=none", seen[0])
            write_trace(trace, root / "outputs/tree.json")

    async def test_outside_partner_is_unreviewable_without_model_call(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _doublet_fixture(root, orphan=True, outside=True)
            result = await review_doublet(
                trace=trace, branch_id="main", hypothesis_ref="h1",
                doublet_id="doublet:oiii", output_root=root / "outputs",
                llm=object(),
                agent_factory=lambda **kw: self.fail("model should not run"))
            node = result["node"]
            self.assertEqual(node["status"], "unreviewable")
            self.assertEqual(node["coverage"]["unreviewable_reason"],
                             "component_outside_spectrum")
            self.assertIsNone(node["pair_supported"])
            write_trace(trace, root / "outputs/tree.json")

    async def test_failed_seats_remain_pending_with_attempt_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _doublet_fixture(root)
            result = await review_doublet(
                trace=trace, branch_id="main", hypothesis_ref="h1",
                doublet_id="doublet:oiii", output_root=root / "outputs",
                llm=object(), agent_factory=lambda **kw: (_ for _ in ()).throw(
                    RuntimeError("service unavailable")))
            node = result["node"]
            self.assertEqual(node["status"], "pending")
            self.assertEqual(node["failed_seats"], 3)
            self.assertEqual(len([ref for ref in node["attempt_refs"]
                                  if ref.endswith("failure.json")]), 6)
            write_trace(trace, root / "outputs/tree.json")

    def test_coverage_requires_each_core_and_rejects_bad_masks(self):
        with tempfile.TemporaryDirectory() as directory:
            npz = Path(directory) / "s.npz"
            wl = np.arange(4900.0, 5070.0)
            np.savez(npz, wavelength=wl, flux=np.ones_like(wl), ivar=np.ones_like(wl))
            components = [{"line_id": "a", "expected_obs_angstrom": 4960.0},
                          {"line_id": "b", "expected_obs_angstrom": 5008.0}]
            method = DoubletReviewMethod(min_valid_component_samples=5)
            window = build_doublet_window(npz, components=components,
                                          masked_regions=[[4993, 5023]], method=method)
            self.assertFalse(window["coverage"]["assessable"])
            self.assertEqual(window["coverage"]["component_cores"][1]["valid_samples"], 0)
            with self.assertRaisesRegex(ValueError, "invalid doublet mask"):
                build_doublet_window(npz, components=components,
                                     masked_regions=[[5000, 4900]], method=method)

    def test_legacy_ratio_conventions_remain_advisory(self):
        components = [
            {"expected_obs_angstrom": 3934.0, "measured_center_angstrom": 3934.0,
             "amplitude": -3.0},
            {"expected_obs_angstrom": 3969.0, "measured_center_angstrom": 3969.0,
             "amplitude": -2.0},
        ]
        ca = _numeric_metrics(_record("doublet:cahk"), components)
        self.assertTrue(ca["reference_ratio_within_window"])
        self.assertTrue(ca["reference_ratio_is_advisory"])
        components[0]["amplitude"] = -1.0
        self.assertFalse(_numeric_metrics(_record("doublet:cahk"), components)
                         ["reference_ratio_within_window"])
        components[1]["amplitude"] = 0.0
        self.assertIsNone(_numeric_metrics(_record("doublet:cahk"), components)
                          ["reference_ratio_within_window"])

    async def test_cannot_review_unclaimed_doublet(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _doublet_fixture(root)
            with self.assertRaisesRegex(ValueError, "at least one kept"):
                await review_doublet(trace=trace, branch_id="main", hypothesis_ref="h1",
                                     doublet_id="doublet:sii", output_root=root / "outputs",
                                     llm=object())
