"""Galaxy graph handoffs use adopted SH/FA pairs and preserve their provenance."""

from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from FORMA.agentic_graph.elg_path import run_elg_path, run_elg_path_through_report
from FORMA.agentic_graph.feature_registry import _digest, build_feature_registry
from FORMA.agentic_graph.lrg_bgs_path import (run_lrg_bgs_path,
                                               run_lrg_bgs_path_through_report)
from FORMA.agentic_graph.qso_entry import run_qso_entry
from FORMA.agentic_graph.qso_transfer_guard import type1_transfer_evidence
from FORMA.agentic_graph.reasoning_trace import (fork_branch, new_trace,
                                                 record_analysis, record_fa_vote)

from test_feature_registry_and_trace import _Q11Model, _fixture, _json


def _trace(root: Path, classification: str, *, pair: str = "civ_ciii",
           accepted: tuple[bool, bool] = (True, True)) -> dict:
    first, second, z, centers, kinds = (
        ("line:civ-1549", "line:ciii-1909", 1.2, (3407.8, 4199.8),
         ("emission", "emission")) if pair == "civ_ciii" else
        ("line:mgii-2800", "line:mgii-2800-abs", 0.4, (3920.0, 3920.0),
         ("emission", "absorption")))
    manifest_path, nodes = _fixture(root, classification=classification,
                                    first_line_id=first, redshift=z,
                                    first_fwhm_km_s=2200)
    manifest = json.loads(manifest_path.read_text())
    npz = Path(manifest["spectrum_npz_path"])
    wl = np.arange(3300., 5101.)
    flux = np.ones_like(wl)
    for center in centers:
        flux += np.exp(-.5 * ((wl - center) / 5.) ** 2)
    np.savez(npz, wavelength=wl, flux=flux, ivar=np.ones_like(wl))
    cwt = {"feature_id": "cwt:em:0000", "wavelength": centers[0],
           "FWHM_km_s": 2200}
    manifest["spectrum_npz_sha256"] = _digest(npz)
    manifest["cwt_features"] = {"emission": [cwt], "absorption": []}
    _json(root / "vi/cwt_features.json", manifest["cwt_features"])
    for node_path in nodes:
        node = json.loads(node_path.read_text())
        catalog_path = Path(node["measurement_catalog_path"])
        catalog = json.loads(catalog_path.read_text())
        catalog.update(spectrum_npz_sha256=_digest(npz),
                       wavelength_min=float(wl[0]), wavelength_max=float(wl[-1]))
        catalog["lines"][0].update(id=first, kind=kinds[0], predicted_obs=centers[0])
        catalog["lines"][1].update(id=second, kind=kinds[1], predicted_obs=centers[1])
        catalog["measurements"][0]["record"] = cwt
        catalog["measurements"][1]["kind"] = kinds[1]
        catalog["measurements"][1]["record"] = {"center": centers[1],
                                                   "fwhm_km_s": 2200}
        _json(catalog_path, catalog)
        judgment_path = Path(node["judgment_path"])
        judgments = json.loads(judgment_path.read_text())
        judgments[1]["line_id"] = second
        _json(judgment_path, judgments)
        node["measurement_catalog_sha256"] = _digest(catalog_path)
        node["judgment_sha256"] = _digest(judgment_path)
        _json(node_path, node)
    _json(manifest_path, manifest)
    trace = new_trace(build_feature_registry(manifest_path, nodes))
    record_analysis(trace, "main", kind="sh_pre_analysis_import",
                    analysis_ref="h1", artifact_refs=["sh/h1/node"])
    for feature, yes in zip(("cwt:em:0000", "fit:h1:0000"), accepted, strict=True):
        if yes:
            for seat in range(3):
                record_fa_vote(trace, "main", feature,
                               vote_id=f"{feature}:{seat}", reviewer_id=f"r{seat}",
                               answer="yes", origin="model")
    return trace


class GalaxyQSOTransferTests(unittest.TestCase):
    def test_guard_four_lines_and_mgii_absorption_exception(self):
        for line_id in ("line:lya-1216", "line:civ-1549", "line:ciii-1909",
                        "line:mgii-2800"):
            row = {"line_id": line_id, "measurement_id": "feature:1",
                   "cleaned_pairing": "adopted", "line_kind": "emission",
                   "fa_vote_artifact_refs": []}
            result = type1_transfer_evidence([row])
            self.assertEqual(result["trigger_pairs"],
                             [{"line_id": line_id, "measurement_id": "feature:1"}])
        mgii = {"line_id": "line:mgii-2800", "measurement_id": "feature:1",
                "cleaned_pairing": "adopted", "line_kind": "emission",
                "fa_vote_artifact_refs": []}
        absorption = {**mgii, "line_id": "line:mgii-2800-abs",
                      "measurement_id": "feature:2", "line_kind": "absorption"}
        self.assertEqual(type1_transfer_evidence([mgii, absorption])["trigger_pairs"], [])
        civ = {**mgii, "line_id": "line:civ-1549", "measurement_id": "feature:3"}
        retained = type1_transfer_evidence([mgii, absorption, civ])
        self.assertEqual(retained["trigger_pairs"], [])
        self.assertTrue(retained["galaxy_retention_by_mgii_pair"])
        self.assertEqual({item["line_id"] for item in retained["retained_diagnostic_pairs"]},
                         {"line:mgii-2800", "line:civ-1549"})
        for state in ("pending_review", "rejected_measurement", "unreviewable_data"):
            self.assertEqual(type1_transfer_evidence([{**civ, "cleaned_pairing": state}])
                             ["trigger_pairs"], [])

    def test_both_galaxy_graphs_transfer_diagnostic_and_finish_type1(self):
        for classification, run in (("ELG", run_elg_path_through_report),
                                    ("LRG/BGS", run_lrg_bgs_path_through_report)):
            with self.subTest(classification=classification), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                trace = _trace(root, classification)
                result = asyncio.run(run(trace, branch_id="main", hypothesis_ref="h1",
                                         output_root=root / "out", llm=_Q11Model()))
                self.assertEqual(result["path_status"], "transfer")
                self.assertEqual(result["qso_entry"]["path_status"], "in_progress")
                self.assertEqual(result["qso_type1"]["candidate_type"], "Type 1 QSO")
                self.assertEqual(result["qso_report"]["node"]["output"]
                                 ["candidate_type"], "Type 1 QSO")
                route = next(item["node"]["output"] for item in result["nodes"]
                             if item["node"]["node_type"].endswith("route_result"))
                self.assertEqual(route["qso_transfer_mode"], "type1")
                self.assertEqual(len(route["qso_trigger_pairs"]), 2)

    def test_mgii_with_absorption_stays_in_galaxy_graph(self):
        for classification, run in (("ELG", run_elg_path),
                                    ("LRG/BGS", run_lrg_bgs_path)):
            with self.subTest(classification=classification), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                trace = _trace(root, classification, pair="mgii_abs")
                kwargs = dict(branch_id="main", hypothesis_ref="h1", output_root=root / "out")
                result = (run(trace, **kwargs) if classification == "ELG" else
                          asyncio.run(run(trace, **kwargs)))
                self.assertNotEqual(result["path_status"], "transfer")
                self.assertIsNone(result["qso_entry"])
                guard = next(item["node"]["output"] for item in result["nodes"]
                             if item["node"]["node_type"].endswith("qso_type1_guard"))
                self.assertTrue(guard["galaxy_retention_by_mgii_pair"])
                self.assertEqual(guard["trigger_pairs"], [])

    def test_mgii_without_adopted_absorption_transfers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _trace(root, "ELG", pair="mgii_abs", accepted=(True, False))
            result = run_elg_path(trace, branch_id="main", hypothesis_ref="h1",
                                  output_root=root / "out")
            self.assertEqual(result["path_status"], "transfer")
            self.assertEqual(result["qso_entry"]["path_status"], "in_progress")
            self.assertEqual(result["qso_entry"]["nodes"][-1]["node"]["node_type"],
                             "qso.broad_line_inventory")
            handoff = result["handoff_event"]
            fork_branch(trace, parent_branch_id="main", fork_event_id=handoff["event_id"],
                        branch_id="review", purpose="replay transferred Type 1 path")
            child = run_qso_entry(trace, branch_id="review", hypothesis_ref="h1",
                                  output_root=root / "out",
                                  handoff_ref=handoff["payload"]["route_ref"])
            self.assertEqual(child["path_status"], "in_progress")


if __name__ == "__main__":
    unittest.main()
