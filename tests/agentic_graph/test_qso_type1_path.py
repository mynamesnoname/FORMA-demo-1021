"""Meaningful Type 1 path guards: coverage, routing, and independent vote sessions."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from langchain_core.messages import AIMessage

from FORMA.agentic_graph.feature_registry import _digest, build_feature_registry
from FORMA.agentic_graph.qso_entry import run_qso_entry
from FORMA.agentic_graph.qso_report import (build_qso_report_context,
                                             render_qso_line_table,
                                             run_qso_entry_through_report,
                                             run_qso_report)
from FORMA.agentic_graph.qso_type1_gate import CIV, LYA
from FORMA.agentic_graph.qso_type1_path import (
    _point_measurement, _strength_vote, local_window, run_qso_type1_path,
)
from FORMA.agentic_graph.reasoning_trace import new_trace, record_analysis, record_fa_vote, write_trace
from FORMA.agentic_graph.execution_artifacts import allocate_execution

from test_feature_registry_and_trace import _fixture, _Q11Model


class _InspectionModel:
    def __init__(self, finding="no_coherent_signal_seen"):
        self.finding = finding
        self.calls = 0

    async def ainvoke(self, messages):
        self.calls += 1
        return AIMessage(content=json.dumps({
            "finding": self.finding,
            "broad_envelope": self.finding == "plausible_uncatalogued_signal",
            "absorption_fragmentation": False,
            "reason": "Local samples do not show a continuous broad envelope."}))


class _VoteModel:
    def __init__(self):
        self.calls = []

    async def ainvoke(self, messages):
        system, user = messages
        self.calls.append((system.content, user.content))
        data = json.loads(user.content)
        if "samples" in data:
            valid = [row for row in data["samples"] if row["valid"]]
            peak = max(valid, key=lambda row: row["flux"])
            sides = []
            for side in (-1, 1):
                options = [row for row in valid
                           if (row["wavelength_angstrom"] - peak["wavelength_angstrom"]) * side > 0
                           and row["flux"] <= peak["flux"] * 0.02]
                if not options:
                    return AIMessage(content=json.dumps({
                        "no_valid_pair": True, "reason": "no outer baseline on both sides"}))
                sides.append(min(options, key=lambda row: abs(
                    row["wavelength_angstrom"] - peak["wavelength_angstrom"])))
            return AIMessage(content=json.dumps({
                "left_sample_id": sides[0]["sample_id"],
                "peak_sample_id": peak["sample_id"],
                "right_sample_id": sides[1]["sample_id"],
                "reason": "outer baseline and local contrast"}))
        return AIMessage(content=json.dumps({"vote": "accept", "reason": "acceptable ratio"}))


def _type1_trace(root: Path, *, paired_civ=False, candidate_civ=False):
    manifest_path, nodes = _fixture(root, classification="Type 1 QSO",
                                    first_line_id=LYA, redshift=2.5,
                                    first_fwhm_km_s=2000)
    manifest = json.loads(manifest_path.read_text())
    npz = Path(manifest["spectrum_npz_path"])
    wavelength = np.arange(4000., 5900.)
    flux = np.exp(-.5 * ((wavelength - 4256.) / 14.) ** 2)
    if candidate_civ:
        flux += 0.7 * np.exp(-.5 * ((wavelength - 5421.5) / 19.) ** 2)
    np.savez(npz, wavelength=wavelength, flux=flux, ivar=np.ones_like(flux))
    manifest["spectrum_npz_sha256"] = _digest(npz)
    for node_path in nodes:
        node = json.loads(node_path.read_text())
        catalog_path = Path(node["measurement_catalog_path"])
        catalog = json.loads(catalog_path.read_text())
        catalog["spectrum_npz_sha256"] = _digest(npz)
        catalog["wavelength_min"] = float(wavelength[0])
        catalog["wavelength_max"] = float(wavelength[-1])
        catalog["lines"][1]["id"] = CIV
        catalog["lines"][1]["predicted_obs"] = 1549.0 * 3.5
        if paired_civ:
            catalog["measurements"][1]["record"]["fwhm_km_s"] = 2200
        catalog_path.write_text(json.dumps(catalog) + "\n")
        judgment_path = Path(node["judgment_path"])
        judgments = json.loads(judgment_path.read_text())
        judgments[1]["line_id"] = CIV
        if not paired_civ:
            judgments[1]["measurement_id"] = None
            judgments[1]["status"] = "NOT_FOUND"
        judgment_path.write_text(json.dumps(judgments) + "\n")
        node["measurement_catalog_sha256"] = _digest(catalog_path)
        node["judgment_sha256"] = _digest(judgment_path)
        node_path.write_text(json.dumps(node) + "\n")
    manifest_path.write_text(json.dumps(manifest) + "\n")
    trace = new_trace(build_feature_registry(manifest_path, nodes))
    record_analysis(trace, "main", kind="sh_pre_analysis_import",
                    analysis_ref="h1", artifact_refs=["sh/h1/node"])
    for feature_id in (["cwt:em:0000", "fit:h1:0000"] if paired_civ else ["cwt:em:0000"]):
        for index in range(3):
            record_fa_vote(trace, "main", feature_id,
                           vote_id=f"{feature_id}:{index}", reviewer_id=f"r{index}",
                           answer="yes", origin="model")
    return trace


class QsoType1PathTests(unittest.IsolatedAsyncioTestCase):
    def test_full_mask_requires_continuous_explicit_window_cover(self):
        wl = np.arange(4200., 4301.)
        flux = np.ones_like(wl)
        ivar = np.ones_like(wl)
        full = local_window(wl, flux, ivar, center=4250., half_width=20.,
                            masked_regions=[[4230., 4270.]])
        self.assertEqual(full["coverage"], "fully_masked")
        partial = local_window(wl, flux, ivar, center=4250., half_width=20.,
                               masked_regions=[[4230., 4249.], [4251., 4270.]])
        self.assertEqual(partial["coverage"], "partial")
        ivar_bad = local_window(wl, flux, np.zeros_like(wl), center=4250.,
                                half_width=20., masked_regions=[])
        self.assertEqual(ivar_bad["coverage"], "no_usable_data")
        self.assertFalse(ivar_bad["full_window_explicit_mask_proof"])

    def test_q8_rejects_masked_or_invalid_point_ids(self):
        wl = np.arange(10., 15.)
        window = local_window(wl, np.array([0., 2., 1., 0., 0.]),
                              np.ones(5), center=12., half_width=2.,
                              masked_regions=[[11., 11.]])
        with self.assertRaisesRegex(ValueError, "not a valid"):
            _point_measurement({"left_sample_id": 1, "peak_sample_id": 2,
                                "right_sample_id": 3, "reason": "masked left"}, window)
        with self.assertRaisesRegex(ValueError, "not a valid"):
            _point_measurement({"left_sample_id": 0, "peak_sample_id": 99,
                                "right_sample_id": 3,
                                "reason": "invented ID"}, window)
        with self.assertRaisesRegex(ValueError, "not a valid"):
            _point_measurement({"left_sample_id": 3, "peak_sample_id": 2,
                                "right_sample_id": 0,
                                "reason": "reversed points"}, window)

    def test_q8_two_sided_baseline_and_width_proxy(self):
        wl = np.arange(10., 15.)
        window = local_window(wl, np.array([1., 2., 5., 4., 3.]),
                              np.ones(5), center=12., half_width=2., masked_regions=[])
        result = _point_measurement({"left_sample_id": 0, "peak_sample_id": 2,
                                     "right_sample_id": 4, "reason": "outer references"},
                                    window, edge_sigma=3)
        self.assertEqual(result["baseline_at_peak"], 2)
        self.assertEqual(result["amplitude_proxy"], 3)
        self.assertEqual(result["envelope_span_angstrom"], 4)
        self.assertAlmostEqual(result["fwhm_proxy_angstrom"],
                               4 * 2.3548200450309493 / 6)

    async def test_q4_through_q10_marks_inspected_missing_civ_dead(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _type1_trace(root)
            entry = run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                                  output_root=root / "out")
            self.assertEqual(entry["path_status"], "in_progress")
            model = _InspectionModel()
            result = await run_qso_type1_path(
                trace, branch_id="main", hypothesis_ref="h1",
                output_root=root / "out", llm=model)
            self.assertEqual(model.calls, 1)
            self.assertEqual(result["path_status"], "dead")
            q9 = result["nodes"][-2]["node"]["output"]
            self.assertEqual(q9["effective_line_states"], [[LYA, "paired"], [CIV, "failed"]])
            self.assertEqual(result["nodes"][0]["node"]["output"]["queue"][0]["line_id"], CIV)
            write_trace(trace, root / "out/tree.json")

    async def test_q4_through_q10_paired_lines_survive_without_model(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _type1_trace(root, paired_civ=True)
            run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                          output_root=root / "out")
            model = _InspectionModel()
            result = await run_qso_type1_path(trace, branch_id="main", hypothesis_ref="h1",
                                               output_root=root / "out", llm=model)
            self.assertEqual(model.calls, 0)
            self.assertEqual(result["path_status"], "survive")
            self.assertEqual(result["candidate_type"], "Type 1 QSO")
            write_trace(trace, root / "out/tree.json")

    async def test_fresh_type1_route_dispatches_q9_q10_and_q11(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _type1_trace(root, paired_civ=True)
            result = await run_qso_entry_through_report(
                trace, branch_id="main", hypothesis_ref="h1",
                output_root=root / "out", llm=_Q11Model())
            self.assertEqual(result["type1"]["path_status"], "survive")
            self.assertEqual(result["report"]["node"]["output"]["candidate_type"],
                             "Type 1 QSO")
            self.assertIn("Graph path status: survive",
                          Path(result["report"]["report_path"]).read_text())
            write_trace(trace, root / "out/tree.json")

    async def test_q8_uses_independent_anonymous_point_sessions_and_fresh_votes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            allocation = allocate_execution(root, run_id="r", branch_id="main",
                                            node_key="qso.relative_strength/test")
            wl = np.arange(4200., 4210.)
            ivar = np.ones_like(wl)
            target = local_window(wl, np.array([0., 1., 4., 1., 0., 0., 0., 0., 0., 0.]),
                                  ivar, center=4204., half_width=4., masked_regions=[])
            reference = local_window(wl, np.array([0., 1., 2., 1., 0., 0., 0., 0., 0., 0.]),
                                     ivar, center=4204., half_width=4., masked_regions=[])
            model = _VoteModel()
            result, files = await _strength_vote(
                model, {"run_id": "r"}, "h", allocation, target, reference,
                CIV, LYA, "possible narrow absorption")
            self.assertEqual(result["status"], "accepted")
            self.assertEqual(result["p_accept"], 1)
            self.assertEqual(len(model.calls), 9)
            self.assertEqual(len(result["pairings"]), 3)
            self.assertEqual(result["representative_target_measurement"]["selection_rule"],
                             "median_target_width")
            self.assertEqual(result["target_picks"][0]["amplitude_proxy"], 4)
            self.assertTrue(all("target_line_id" not in user and
                                "reference_line_id" not in user
                                for _, user in model.calls[:6]))
            self.assertTrue(all("target_line_id" in user and
                                "local contrast" not in user and
                                "fwhm_proxy_km_s" not in user
                                for _, user in model.calls[6:]))
            self.assertEqual(len(files), 10)

    async def test_q8_representative_uses_whole_median_width_pick(self):
        class WidthModel:
            def __init__(self):
                self.pick_count = 0
                self.compare_count = 0

            async def ainvoke(self, messages):
                data = json.loads(messages[1].content)
                if "samples" not in data:
                    seat = self.compare_count
                    self.compare_count += 1
                    return AIMessage(content=json.dumps({
                        "vote": "reject" if seat == 1 else "accept",
                        "reason": "one pair disputed"}))
                seat = self.pick_count
                self.pick_count += 1
                radius = (1, 2, 3)[seat] if seat < 3 else 2
                return AIMessage(content=json.dumps({
                    "left_sample_id": 6 - radius, "peak_sample_id": 6,
                    "right_sample_id": 6 + radius, "reason": "outer boundaries"}))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            allocation = allocate_execution(root, run_id="r", branch_id="main",
                                            node_key="qso.relative_strength/median")
            wl = np.arange(13.)
            flux = np.zeros(13)
            flux[6] = 10
            window = local_window(wl, flux, np.ones(13), center=6.,
                                  half_width=6., masked_regions=[])
            result, _ = await _strength_vote(WidthModel(), {"run_id": "r"}, "h",
                                             allocation, window, window, CIV, LYA, "test")
            representative = result["representative_target_measurement"]
            self.assertEqual(result["status"], "accepted")
            self.assertAlmostEqual(result["p_accept"], 2 / 3)
            self.assertEqual(representative["target_seat"], 1)
            self.assertEqual(representative["amplitude_proxy"], 10)
            self.assertEqual(representative["left_sample_id"], 4)
            self.assertEqual(representative["right_sample_id"], 8)

    async def test_q8_no_valid_pair_never_becomes_a_comparison_vote(self):
        class NoPairModel(_VoteModel):
            async def ainvoke(self, messages):
                if not self.calls:
                    self.calls.append((messages[0].content, messages[1].content))
                    return AIMessage(content=json.dumps({
                        "no_valid_pair": True, "reason": "no local saddle"}))
                return await super().ainvoke(messages)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            allocation = allocate_execution(root, run_id="r", branch_id="main",
                                            node_key="qso.relative_strength/no-pair")
            wl = np.arange(4200., 4210.)
            window = local_window(wl, np.array([0., 1., 4., 1., 0., 0., 0., 0., 0., 0.]),
                                  np.ones_like(wl), center=4204., half_width=4.,
                                  masked_regions=[])
            model = NoPairModel()
            result, _ = await _strength_vote(model, {"run_id": "r"}, "h", allocation,
                                             window, window, CIV, LYA, "test")
            self.assertEqual(result["status"], "measurement_unavailable")
            self.assertIsNone(result["p_accept"])
            self.assertEqual(result["votes"], [])
            self.assertEqual(len(model.calls), 6)

    async def test_q6_fragmented_candidate_q7_registration_q8_vote_reaches_q9(self):
        class CombinedModel(_VoteModel):
            async def ainvoke(self, messages):
                if "Inspect one predicted" in messages[0].content:
                    self.calls.append((messages[0].content, messages[1].content))
                    return AIMessage(content=json.dumps({
                        "finding": "plausible_uncatalogued_signal",
                        "broad_envelope": True, "absorption_fragmentation": True,
                        "reason": "a broad coherent envelope is visible"}))
                return await super().ainvoke(messages)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _type1_trace(root, candidate_civ=True)
            run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                          output_root=root / "out")
            model = CombinedModel()
            result = await run_qso_type1_path(trace, branch_id="main", hypothesis_ref="h1",
                                               output_root=root / "out", llm=model)
            kinds = [node["node"]["node_type"] for node in result["nodes"]]
            self.assertIn(f"qso.proposed_observation/{CIV}", kinds)
            self.assertIn(f"qso.relative_strength/{CIV}", kinds)
            self.assertEqual(result["path_status"], "survive")
            q7 = next(item["node"]["output"] for item in result["nodes"]
                      if item["node"]["node_type"] == f"qso.proposed_observation/{CIV}")
            q8 = next(item["node"]["output"] for item in result["nodes"]
                      if item["node"]["node_type"] == f"qso.relative_strength/{CIV}")
            self.assertEqual(q7["measurement_status"], "awaiting_q8_point_selection")
            self.assertTrue(q7["absorption_fragmentation"])
            self.assertEqual(q8["representative_broadness"], "supported_proxy")
            self.assertEqual(q8["candidate_id"], q7["candidate_id"])
            context = build_qso_report_context(trace, "main", "h1")
            self.assertEqual(context["targeted_measurements"][0]["candidate_id"],
                             q7["candidate_id"])
            self.assertEqual(context["targeted_measurements"][0]["fwhm_proxy_angstrom"],
                             q8["representative_target_measurement"]["fwhm_proxy_angstrom"])
            self.assertIn("Q8 envelope proxies", render_qso_line_table(context))
            self.assertIn("FWHM proxy (Å)", render_qso_line_table(context))
            self.assertEqual(len(model.calls), 10)
            report = await run_qso_report(trace, branch_id="main", hypothesis_ref="h1",
                                          output_root=root / "out", llm=_Q11Model())
            self.assertIn(q7["candidate_id"], Path(report["report_path"]).read_text())
            write_trace(trace, root / "out/tree.json")

    async def test_accepted_ratio_without_broad_proxy_stays_unresolved(self):
        class NarrowPickModel(_VoteModel):
            async def ainvoke(self, messages):
                if "Inspect one predicted" in messages[0].content:
                    return AIMessage(content=json.dumps({
                        "finding": "plausible_uncatalogued_signal",
                        "broad_envelope": True, "absorption_fragmentation": True,
                        "reason": "possible fragmented envelope"}))
                data = json.loads(messages[1].content)
                if "samples" not in data:
                    return AIMessage(content=json.dumps({
                        "vote": "accept", "reason": "ratio accepted"}))
                valid = [row for row in data["samples"] if row["valid"]]
                peak = max(valid, key=lambda row: row["flux"])
                by_wavelength = {row["wavelength_angstrom"]: row for row in valid}
                left = by_wavelength[peak["wavelength_angstrom"] - 3]
                right = by_wavelength[peak["wavelength_angstrom"] + 3]
                return AIMessage(content=json.dumps({
                    "left_sample_id": left["sample_id"],
                    "peak_sample_id": peak["sample_id"],
                    "right_sample_id": right["sample_id"],
                    "reason": "narrow selected envelope"}))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _type1_trace(root, candidate_civ=True)
            run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                          output_root=root / "out")
            result = await run_qso_type1_path(trace, branch_id="main", hypothesis_ref="h1",
                                              output_root=root / "out", llm=NarrowPickModel())
            q8 = next(item["node"]["output"] for item in result["nodes"]
                      if item["node"]["node_type"] == f"qso.relative_strength/{CIV}")
            self.assertEqual(q8["status"], "accepted")
            self.assertEqual(q8["representative_broadness"], "not_supported_proxy")
            self.assertEqual(result["path_status"], "unresolved")


if __name__ == "__main__":
    unittest.main()
