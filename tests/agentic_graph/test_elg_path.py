"""ELG branch gates, advisory continuum and source-bound QSO handoff."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from FORMA.agentic_graph.elg_path import run_elg_path, run_elg_path_through_report
from FORMA.agentic_graph.feature_registry import _digest, build_feature_registry
from FORMA.agentic_graph.qso_entry import run_qso_entry
from FORMA.agentic_graph.reasoning_trace import (
    bind_artifact_root, fork_branch, new_trace, record_analysis, record_fa_vote, state_at_event,
    write_trace,
)
from evaluation.agentic_graph.run_elg_paths import run as run_elg_archive

from test_feature_registry_and_trace import _Q11Model, _fixture, _json


def _elg_fixture(root: Path, *, first_line: str,
                 reuse_first_measurement: bool = False,
                 mask_blue_band: bool = False) -> dict:
    manifest_file, nodes = _fixture(root, classification="ELG",
                                    first_line_id=first_line, redshift=0.0)
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    npz = Path(manifest["spectrum_npz_path"])
    wl = np.arange(3300.0, 5101.0)
    flux = np.ones_like(wl)
    flux[(wl >= 4000) & (wl < 4100)] = 2.0
    center = {"line:nev-3426": 3426.0,
              "line:oii-3727": 3727.0,
              "line:oiii-4960": 4960.3}[first_line]
    flux += np.exp(-0.5 * ((wl - center) / 2.0) ** 2)
    np.savez(npz, wavelength=wl, flux=flux, ivar=np.ones_like(wl))
    cwt = {"feature_id": "cwt:em:0000", "wavelength": center}
    manifest["spectrum_npz_sha256"] = _digest(npz)
    manifest["cwt_features"]["emission"] = [cwt]
    _json(root / "vi/cwt_features.json", manifest["cwt_features"])
    for node_file in nodes:
        node = json.loads(node_file.read_text(encoding="utf-8"))
        catalog_file = Path(node["measurement_catalog_path"])
        catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
        catalog["spectrum_npz_sha256"] = _digest(npz)
        catalog["wavelength_min"] = float(wl[0])
        catalog["wavelength_max"] = float(wl[-1])
        if mask_blue_band:
            catalog["masked_regions"] = [[3850.0, 3950.0]]
        catalog["lines"][0]["predicted_obs"] = center
        catalog["lines"][1]["id"] = "line:oiii-5008"
        catalog["lines"][1]["predicted_obs"] = 5008.2
        catalog["measurements"][0]["record"] = cwt
        catalog["measurements"][1]["record"]["center"] = 5008.0
        _json(catalog_file, catalog)
        judgment_file = Path(node["judgment_path"])
        judgments = json.loads(judgment_file.read_text(encoding="utf-8"))
        judgments[1]["line_id"] = "line:oiii-5008"
        if reuse_first_measurement:
            judgments[1]["measurement_id"] = "cwt:em:0000"
        _json(judgment_file, judgments)
        node["measurement_catalog_sha256"] = _digest(catalog_file)
        node["judgment_sha256"] = _digest(judgment_file)
        _json(node_file, node)
    _json(manifest_file, manifest)
    trace = new_trace(build_feature_registry(manifest_file, nodes))
    record_analysis(trace, "main", kind="sh_pre_analysis_import",
                    analysis_ref="h1", artifact_refs=["sh/h1/node"])
    return trace


def _complete_fa(trace: dict, feature_id: str) -> None:
    for seat in range(3):
        record_fa_vote(trace, "main", feature_id,
                       vote_id=f"{feature_id}:{seat}", reviewer_id=f"r{seat}",
                       answer="yes", origin="model")


class ELGPathTests(unittest.TestCase):
    def test_oii_survives_without_false_old_population_transfer(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _elg_fixture(root, first_line="line:oii-3727")
            _complete_fa(trace, "cwt:em:0000")
            with patch("FORMA.agentic_graph.fa_doublet.read_doublet_information",
                       side_effect=AssertionError("ELG must not read FA doublet advice")):
                result = run_elg_path(trace, branch_id="main", hypothesis_ref="h1",
                                      output_root=root / "out")
            self.assertEqual(result["path_status"], "survive")
            self.assertEqual(result["candidate_type"], "ELG")
            self.assertIsNone(result["qso_entry"])
            by_type = {item["node"]["node_type"]: item["node"]["output"]
                       for item in result["nodes"]}
            self.assertEqual(by_type["elg.emission_evidence"]["B"], "yes")
            self.assertEqual(by_type["elg.emission_evidence"]["A"], "unknown")
            self.assertEqual(by_type["elg.old_population_guard"]["dn4000"]
                             ["reference_strength"], "strong")
            self.assertFalse(by_type["elg.old_population_guard"]["classification_gate"])
            self.assertIn("old_population_hint_not_a_hard_gate",
                          by_type["elg.route_result"]["unresolved_reasons"])
            self.assertTrue(result["report_ref"] in trace["artifacts"])
            write_trace(trace, root / "out/reasoning_branches.json")

    def test_nev_handoff_reaches_qso_q2_and_rejects_unbound_reentry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _elg_fixture(root, first_line="line:nev-3426")
            _complete_fa(trace, "cwt:em:0000")
            result = run_elg_path(trace, branch_id="main", hypothesis_ref="h1",
                                  output_root=root / "out")
            self.assertEqual(result["path_status"], "transfer")
            self.assertEqual(result["qso_entry"]["path_status"], "survive")
            self.assertEqual(result["qso_entry"]["candidate_type"], "Type 2 QSO")
            entry = next(item["node"] for item in result["qso_entry"]["nodes"]
                         if item["node"]["node_type"] == "qso.entry")
            self.assertEqual(entry["output"]["entry_mode"], "handoff")
            self.assertEqual(entry["output"]["route_history"], ["ELG", "QSO"])
            self.assertEqual(trace["branches"]["main"]["state"]["registry"]
                             ["hypotheses"]["h1"]["classification"], "ELG")
            self.assertEqual(len([event for event in trace["branches"]["main"]["events"]
                                  if event["kind"] == "type_graph_handoff"]), 1)
            fork_event = next(event for event in trace["branches"]["main"]["events"]
                              if event["kind"] == "type_graph_handoff")
            fork_branch(trace, parent_branch_id="main",
                        fork_event_id=fork_event["event_id"],
                        branch_id="handoff-child", purpose="revisit QSO")
            child = run_qso_entry(trace, branch_id="handoff-child",
                                  hypothesis_ref="h1", output_root=root / "out",
                                  handoff_ref=fork_event["payload"]["route_ref"])
            self.assertEqual(child["candidate_type"], "Type 2 QSO")
            with self.assertRaises(ValueError):
                run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                              output_root=root / "other")
            write_trace(trace, root / "out/reasoning_branches.json")

    def test_pending_features_do_not_prove_emission_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _elg_fixture(root, first_line="line:oii-3727")
            result = run_elg_path(trace, branch_id="main", hypothesis_ref="h1",
                                  output_root=root / "out")
            self.assertEqual(result["path_status"], "unresolved")
            self.assertIsNone(result["candidate_type"])
            self.assertIn("emission_absence_not_established",
                          result["nodes"][-2]["node"]["output"]["unresolved_reasons"])

    def test_both_oiii_components_count_as_a(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _elg_fixture(root, first_line="line:oiii-4960")
            _complete_fa(trace, "cwt:em:0000")
            _complete_fa(trace, "fit:h1:0000")
            result = run_elg_path(trace, branch_id="main", hypothesis_ref="h1",
                                  output_root=root / "out")
            self.assertEqual(result["path_status"], "survive")
            emission = next(item["node"]["output"] for item in result["nodes"]
                            if item["node"]["node_type"] == "elg.emission_evidence")
            self.assertEqual(emission["A"], "yes")
            self.assertEqual(emission["B"], "unknown")

    def test_same_measurement_cannot_satisfy_both_oiii_components(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _elg_fixture(root, first_line="line:oiii-4960",
                                 reuse_first_measurement=True)
            _complete_fa(trace, "cwt:em:0000")
            result = run_elg_path(trace, branch_id="main", hypothesis_ref="h1",
                                  output_root=root / "out")
            emission = next(item["node"]["output"] for item in result["nodes"]
                            if item["node"]["node_type"] == "elg.emission_evidence")
            self.assertEqual(emission["A"], "unknown")
            self.assertTrue(emission["oiii_component_id_conflict"])
            self.assertEqual(result["path_status"], "unresolved")

    def test_masked_dn4000_band_is_unknown(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _elg_fixture(root, first_line="line:oii-3727",
                                 mask_blue_band=True)
            result = run_elg_path(trace, branch_id="main", hypothesis_ref="h1",
                                  output_root=root / "out")
            old = next(item["node"]["output"] for item in result["nodes"]
                       if item["node"]["node_type"] == "elg.old_population_guard")
            self.assertIsNone(old["dn4000"]["value"])
            self.assertEqual(old["dn4000"]["reference_strength"], "unknown")
            self.assertFalse(old["old_population_hint"])

    def test_changed_source_is_rejected_and_parent_branch_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _elg_fixture(root, first_line="line:oii-3727")
            imported = trace["branches"]["main"]["events"][-1]
            fork_branch(trace, parent_branch_id="main", fork_event_id=imported["event_id"],
                        branch_id="child", purpose="ELG recheck")
            parent = copy.deepcopy(trace["branches"]["main"]["state"])
            run_elg_path(trace, branch_id="child", hypothesis_ref="h1",
                         output_root=root / "out")
            self.assertEqual(trace["branches"]["main"]["state"], parent)
            self.assertEqual(state_at_event(trace, "child",
                             trace["branches"]["child"]["events"][-1]["event_id"]),
                             trace["branches"]["child"]["state"])
            changed = copy.deepcopy(trace)
            changed["artifacts"]["sh/h1/catalog"]["sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "changed"):
                run_elg_path(changed, branch_id="main", hypothesis_ref="h1",
                             output_root=root / "other")

    def test_offline_runner_writes_new_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _elg_fixture(root, first_line="line:oii-3727")
            out = root / "out"
            out.mkdir()
            bind_artifact_root(trace, out)
            source = write_trace(trace, out / "before.json")
            summary = run_elg_archive(source, out / "after.json")
            self.assertEqual(summary["hypotheses"]["h1"]["path_status"], "unresolved")
            archived = json.loads((out / "after.json").read_text(encoding="utf-8"))
            self.assertTrue(any("elg.analysis_report" in key for key in archived
                                ["branches"]["main"]["state"]["analysis_results"]))


class ELGHandoffReportTests(unittest.IsolatedAsyncioTestCase):
    async def test_nev_transfer_has_source_bound_qso_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _elg_fixture(root, first_line="line:nev-3426")
            _complete_fa(trace, "cwt:em:0000")
            model = _Q11Model()
            result = await run_elg_path_through_report(
                trace, branch_id="main", hypothesis_ref="h1",
                output_root=root / "out", llm=model)
            self.assertEqual(result["qso_report"]["node"]["output"]
                             ["candidate_type"], "Type 2 QSO")
            self.assertEqual(model.calls, 1)
            self.assertIn("Preliminary classification: ELG",
                          Path(result["qso_report"]["report_path"]).read_text())
            write_trace(trace, root / "out/tree.json")


if __name__ == "__main__":
    unittest.main()
