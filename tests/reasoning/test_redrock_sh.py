"""Redrock-only single-hypothesis prompt and tool contract."""

from __future__ import annotations

import sys
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from FORMA.agents.multi_agents.harness.single_hypothesis import (
    _build_tools,
    _build_user_message,
    _load_skill,
    _mask_overlap_label,
    _prepare_prefits,
    run,
)
from FORMA.agents.multi_agents.harness.tools import _do_fit_doublet, write_lines_csv
from FORMA.agents.multi_agents.harness.sh_provenance import prepare_sh_lines
from FORMA.agents.multi_agents.harness.sh_prefit import run_sh_prefit, render_fit_attempts
from FORMA.core.constants import FWHM_TO_SIGMA
from FORMA.core.reasoning.ontology.registry import ONTOLOGY


class RedrockOnlySHTests(unittest.TestCase):
    def test_prefit_attempts_only_when_local_cwt_candidate_is_absent(self):
        from FORMA.agents.multi_agents.harness import sh_prefit
        wl = np.linspace(4960, 5040, 321)
        flux = 1 + 3 * np.exp(-0.5 * ((wl - 5000) / 2) ** 2)
        with patch.object(sh_prefit, "EMISSION_LINES", {"test_line": 5000.0}), \
             patch.object(sh_prefit, "ABSORPTION_LINES", {}):
            present, _ = run_sh_prefit(wl, flux, 0, [{"wavelength": 5000.0}],
                                       [], -0.1, 0.1, [], [])
            missing, measurements = run_sh_prefit(wl, flux, 0, [], [],
                                                   -0.1, 0.1, [], [])
        self.assertEqual(present, [])
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0]["target"], "test_line")
        self.assertEqual(missing[0]["method"], "fit_peak")
        self.assertEqual(measurements[0]["source"], "fit_peak")
        self.assertIn("test_line", render_fit_attempts(missing))

    def test_failed_prefit_is_visible_but_not_adoptable(self):
        from FORMA.agents.multi_agents.harness import sh_prefit
        wl = np.linspace(4960, 5040, 321)
        with patch.object(sh_prefit, "EMISSION_LINES", {"test_line": 5000.0}), \
             patch.object(sh_prefit, "ABSORPTION_LINES", {}), \
             patch.object(sh_prefit, "_do_fit_peak", return_value={
                 "center": None, "flags": ["fit_failed"],
                 "message": "optimizer failed", "local_snr": None,
                 "delta_chi2_per_n": None,
             }):
            attempts, measurements = run_sh_prefit(
                wl, np.ones_like(wl), 0, [], [], -0.1, 0.1, [], [])
        self.assertEqual(measurements, [])
        self.assertEqual(attempts[0]["status"], "failed")
        self.assertIn("fit_failed", render_fit_attempts(attempts))

    def test_prefit_display_preserves_measurement_digits_for_provenance(self):
        text = render_fit_attempts([{
            "target": "line", "method": "fit_peak", "predicted_obs": [10000.0],
            "status": "ok", "result": {
                "center": 10000.1234, "center_err": 0.0007,
                "amplitude": 1.234567, "fwhm_km_s": 120.5,
                "local_snr": 8.2, "delta_chi2_per_n": 2.1, "flags": [],
            },
        }])
        self.assertIn("10000.1234±0.0007", text)
        self.assertIn("1.234567", text)

    def test_prefit_archive_and_prompt_keep_cwt_prediction_tables(self):
        from FORMA.agents.multi_agents.harness import sh_prefit
        with tempfile.TemporaryDirectory() as tmp:
            npz = Path(tmp) / "spectrum.npz"
            archive = Path(tmp) / "hypothesis_prefit.json"
            wl = np.linspace(4960.0, 5040.0, 321)
            flux = 1 + 3 * np.exp(-0.5 * ((wl - 5000.0) / 2) ** 2)
            np.savez(npz, wavelength=wl, flux=flux)
            with patch.object(sh_prefit, "EMISSION_LINES", {"test_line": 5000.0}), \
                 patch.object(sh_prefit, "ABSORPTION_LINES", {}):
                attempts, measurements = _prepare_prefits(
                    str(npz), 0.0, [], [], -0.1, 0.1, [], str(archive))
            self.assertEqual(len(attempts), 1)
            self.assertEqual(len(measurements), 1)
            self.assertEqual(len(json.loads(archive.read_text())), 1)
            message = _build_user_message(
                0.0, "input.fits", str(npz), wavelength_min=4960,
                wavelength_max=5040, peaks=[], troughs=[],
                z_min=-0.1, z_max=0.1, fit_attempts=attempts)
            self.assertIn("Nearby Features (ref@λ(z); cross-ref CWT table above for details)", message)
            self.assertLess(message.index("## Predicted Lines at z ="),
                            message.index("## Targeted Gaussian Fit Attempts"))
            self.assertIn("test_line", message)

    def test_prefit_measurement_is_accepted_by_sh_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            npz = Path(tmp) / "spec.npz"
            csv_path = Path(tmp) / "lines.csv"
            np.savez(npz, wavelength=np.linspace(5000, 5020, 21),
                     flux=np.ones(21))
            measurement = {"source": "fit_peak", "kind": "emission",
                           "center": 5010.0, "center_err": 0.2,
                           "amplitude": 2.0, "amplitude_err": 0.1,
                           "sigma": 2.0, "fwhm_km_s": 282.0}
            tool = next(item for item in _build_tools(
                str(npz), 0.0, prefit_measurements=[measurement])
                if item.name == "write_lines_csv")
            from FORMA.agents.multi_agents.harness.tools import EMISSION_LINES
            row = {"name": "[O III]b", "rest_wavelength": EMISSION_LINES["[O III]b"],
                   "predicted_obs": 5010.0, "fitted_center": 5010.0,
                   "source": "fit_peak", "status": "MARGINAL"}
            result = tool.invoke({"file_path": str(csv_path), "lines": [row]})
            self.assertEqual(result["path"], str(csv_path))
            self.assertIn("fit_peak", csv_path.read_text())

    def test_prefit_component_cannot_be_relabelled_as_blended_line(self):
        from FORMA.agents.multi_agents.harness.tools import ABSORPTION_LINES
        centre = 7298.536
        measurement = {"source": "fit_doublet", "kind": "absorption",
                       "target_line": "Na D1_abs", "center": centre,
                       "amplitude": -0.4}
        component = {"name": "Na D1_abs", "rest_wavelength": ABSORPTION_LINES["Na D1_abs"],
                     "fitted_center": centre, "source": "fit_doublet", "status": "MARGINAL"}
        blend = {**component, "name": "Na D_abs",
                 "rest_wavelength": ABSORPTION_LINES["Na D_abs"]}
        accepted, _, errors = prepare_sh_lines([component, blend], [], [], [measurement])
        self.assertEqual([row["name"] for row in accepted], ["Na D1_abs"])
        self.assertEqual(errors[0]["name"], "Na D_abs")

        # A coincident CWT trough must not make the same blended line count as
        # independent evidence alongside its resolved fitted component.
        _, _, duplicate_errors = prepare_sh_lines(
            [component, blend], [], [{"wavelength": centre}], [measurement])
        self.assertTrue(any(error["name"] == "Na D_abs" and
                            "duplicates" in error["reason"]
                            for error in duplicate_errors))

    def test_full_mask_requires_union_to_cover_entire_line_window(self):
        cases = [
            ([(100.0, 120.0), (180.0, 200.0)], " [λ_pred masked]"),
            ([(100.0, 150.0), (150.0, 200.0)], " [fully masked]"),
            ([(140.0, 200.0), (90.0, 160.0)], " [fully masked]"),
            ([(100.0, 149.9), (150.0, 200.0)], " [λ_pred masked]"),
            ([(90.0, 110.0)], " [window partially masked]"),
            ([(201.0, 220.0)], ""),
        ]
        for masks, expected in cases:
            with self.subTest(masks=masks):
                self.assertEqual(_mask_overlap_label(100.0, 200.0, 200.0, masks), expected)
        self.assertEqual(
            _mask_overlap_label(100.0, 200.0, 150.0,
                                [(100.0, 120.0), (180.0, 200.0)]),
            " [window partially masked]",
        )

    def test_old_mode_is_rejected_before_model_or_file_access(self):
        with self.assertRaisesRegex(ValueError, "unsupported hypothesis mode"):
            run("unused.fits", 0.2, "unused.npz", mode="nomad")

    def test_redrock_tools_include_fitting(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spectrum.npz"
            np.savez(path, wavelength=np.array([5000.0, 5001.0]),
                     flux=np.array([1.0, 2.0]))
            names = {tool.name for tool in _build_tools(str(path), 0.2)}
        self.assertEqual(names, {
            "write_report", "write_lines_csv", "_fit_peak", "_fit_doublet",
        })

    def test_sh_rejects_invented_doublet_without_running_optimizer(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spectrum.npz"
            wavelength = np.linspace(3600.0, 9824.0, 200)
            np.savez(path, wavelength=wavelength, flux=np.ones_like(wavelength))
            tools = {item.name: item for item in _build_tools(str(path), 1.6408)}
            result = tools["_fit_doublet"].invoke({
                "center_guess_1": 7384.0,
                "center_guess_2": 7407.2,
                "line_type": "emission",
                "width_3sigma": 90,
                "separation_expected_obs": 23.2,
                "amp_ratio_expected": 1.0,
            })
        self.assertIn("unregistered_doublet", result["flags"])
        self.assertIsNone(result["component_1"])

    def test_sh_accepts_registered_doublet_and_rejects_wrong_prior(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spectrum.npz"
            wavelength = np.linspace(5900.0, 6100.0, 801)
            flux = (1.0
                    + 2.0 * np.exp(-0.5 * ((wavelength - 5952.0) / 3.0) ** 2)
                    + 6.0 * np.exp(-0.5 * ((wavelength - 6009.6) / 3.0) ** 2))
            np.savez(path, wavelength=wavelength, flux=flux)
            tool = next(item for item in _build_tools(str(path), 0.2)
                        if item.name == "_fit_doublet")
            call = {
                "center_guess_1": 5952.0,
                "center_guess_2": 6009.6,
                "line_type": "emission",
                "width_3sigma": 25,
                "separation_expected_obs": 57.48,
                "amp_ratio_expected": 3.0,
            }
            valid = tool.invoke(call)
            invalid = tool.invoke({**call, "separation_expected_obs": 23.2})
            invented_ratio = tool.invoke({**call, "amp_ratio_expected": 1.0})
            widened = tool.invoke({**call, "center_guess_2": 6020.0,
                                   "separation_tolerance": 100.0})
        self.assertNotIn("unregistered_doublet", valid["flags"])
        self.assertTrue(valid["separation_check"]["match"])
        self.assertIn("unregistered_doublet", invalid["flags"])
        self.assertIn("unregistered_doublet", invented_ratio["flags"])
        self.assertIn("unregistered_doublet", widened["flags"])

    def test_runtime_message_injects_relevant_ontology_context(self):
        message = _build_user_message(
            redshift=0.2,
            fits_path="spectrum.fits",
            npz_path="spectrum.npz",
            wavelength_min=3500.0,
            wavelength_max=7000.0,
            peaks=[], troughs=[],
        )
        self.assertIn(ONTOLOGY.schema_version, message)
        self.assertIn("membership:offset-quality", message)
        self.assertIn("rule:formal-qso-broad-width", message)
        self.assertIn("doublet:oiii", message)
        self.assertIn("separation_expected_obs=", message)
        self.assertIn("amp_ratio_expected=3", message)
        self.assertIn("Registry anchor candidates", message)
        self.assertIn("[O III]b=7", message)
        self.assertNotIn("excluded-from-anchor", message)
        self.assertNotIn("doublet:na-d", message)  # outside nominal coverage
        self.assertIn("Predicted Lines", message)
        self.assertNotIn("Nomad", _load_skill())

    def test_qso_only_uv_lines_remain_ranked_anchor_candidates(self):
        message = _build_user_message(
            redshift=3.0, fits_path="spectrum.fits", npz_path="spectrum.npz",
            wavelength_min=3600.0, wavelength_max=9900.0,
        )
        self.assertIn("C III]=8", message)
        self.assertIn("C IV=10", message)
        self.assertIn("Lyα=12", message)
        self.assertNotIn("excluded-from-anchor", message)

    def test_doublet_separation_checks_observed_frame_difference(self):
        wavelength = np.linspace(5900.0, 6100.0, 801)
        flux = (1.0
                + 2.0 * np.exp(-0.5 * ((wavelength - 5952.0) / 3.0) ** 2)
                + 6.0 * np.exp(-0.5 * ((wavelength - 6009.6) / 3.0) ** 2))
        result = _do_fit_doublet(
            wavelength, flux, 5952.0, 6009.6,
            separation_expected_obs=57.6, separation_tolerance=1.0,
        )
        self.assertTrue(result["separation_check"]["match"])
        self.assertAlmostEqual(result["separation_check"]["expected_sep_A"], 57.6)


class DeclaredWindowTests(unittest.TestCase):
    """The run message's verification window comes from the declaration (WP-040).

    运行消息的校验窗口取自声明（WP-040）。
    """

    def test_fallback_window_uses_shared_redshift_tolerance(self):
        message = _build_user_message(
            redshift=0.5, fits_path="s.fits", npz_path="s.npz",
            wavelength_min=3500.0, wavelength_max=7000.0,
        )
        self.assertIn("Verification window: z ∈ [0.49, 0.51]", message)

        with tempfile.TemporaryDirectory() as tmp:
            from FORMA.core.config.analysis_method import load_analysis_method
            method = load_analysis_method().model_dump(mode="json")
            method["evaluation"]["redshift_tolerance"] = 0.025
            payload = Path(tmp) / "analysis_method.json"
            payload.write_text(json.dumps(method), encoding="utf-8")
            with patch.dict(os.environ, {"FORMA_ANALYSIS_METHOD_CONFIG": str(payload)}):
                widened = _build_user_message(
                    redshift=0.5, fits_path="s.fits", npz_path="s.npz",
                    wavelength_min=3500.0, wavelength_max=7000.0,
                )
        self.assertIn("Verification window: z ∈ [0.475, 0.525]", widened)

    def test_predicted_line_nearby_column_uses_shared_tolerance(self):
        message = _build_user_message(
            redshift=0.0, fits_path="s.fits", npz_path="s.npz",
            wavelength_min=3400.0, wavelength_max=3500.0,
            peaks=[{"wavelength": 3456.0}, {"wavelength": 3470.0}],
            troughs=[],
        )
        row = next(line for line in message.splitlines() if line.startswith("| [Ne V] |"))
        self.assertIn("peak@3456.0", row)
        self.assertNotIn("peak@3470.0", row)
        self.assertIn("| 3470.0 |", message)  # Full CWT table still lists it.


class LineCsvProvenanceTests(unittest.TestCase):
    """The SH CSV must declare where each adopted measurement came from.

    SH 的 CSV 必须声明每行采用的测量来源（WP-035 后续修订）。
    """

    def _write(self, rows):
        import csv

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "1_lines.csv"
            write_lines_csv.invoke({"file_path": str(path), "lines": rows})
            with path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                return reader.fieldnames, list(reader)

    def test_source_and_implied_z_are_persisted(self):
        fields, rows = self._write([
            {"name": "[O II]", "rest_wavelength": 3727.0, "predicted_obs": 4174.2,
             "fitted_center": 4193.6, "amplitude": 11.6, "status": "LIKELY",
             "source": "CWT", "implied_z": 0.0, "cwt_snr": 9.4},
            {"name": "Ca K_abs", "rest_wavelength": 3933.7, "predicted_obs": 6576.5,
             "fitted_center": 6574.2, "amplitude": -1.2, "status": "MARGINAL",
             "source": "fit_peak", "implied_z": None},
            {"name": "[O II]", "rest_wavelength": 3727.0,
             "fitted_center": None, "status": "NOT_FOUND", "source": None,
             "implied_z": 0.1252},
        ])
        self.assertIn("source", fields)
        self.assertIn("implied_z", fields)
        self.assertEqual([row["source"] for row in rows], ["CWT", "fit_peak", ""])
        self.assertAlmostEqual(float(rows[0]["implied_z"]), 4193.6 / 3727.0 - 1)
        self.assertAlmostEqual(float(rows[1]["implied_z"]), 6574.2 / 3933.7 - 1)
        self.assertEqual(rows[2]["implied_z"], "")

    def test_fit_derived_row_cannot_claim_cwt_metrics(self):
        """The rule holds, and it is repairable rather than fatal.

        规则成立，且可修复而非致命。

        Raising here destroyed whole hypotheses on the 2026-10-15 boundary
        execution (12 of 16 runs, 23 rows); the tool now refuses the write and
        names the fields to null, so the model can re-send the same rows.
        在此抛异常曾于 2026-10-15 的边界执行中毁掉整个假设（16 轮中 12 轮、23 行）；
        工具现在拒绝写入并指明需置空的字段，使模型能重发同样的行。
        """
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "1_lines.csv"
            result = write_lines_csv.invoke({"file_path": str(path), "lines": [{
                "name": "Mg II", "source": "fit_doublet", "status": "LIKELY",
                "fitted_center": 7395.33, "ridge_length": 7, "cwt_snr": 15.5,
            }]})
            self.assertFalse(path.exists())
            self.assertIsNone(result["path"])
            self.assertEqual(result["n_lines"], 0)
            self.assertIn("cwt_metrics_on_fit_derived_row", result["flags"])
            self.assertEqual(
                result["rows_to_repair"],
                [{"name": "Mg II", "source": "fit_doublet",
                  "set_to_null": ["ridge_length", "cwt_snr"]}],
            )
            self.assertIn("cannot carry CWT metrics", result["message"])

    def test_the_repaired_row_then_writes(self):
        """The same rows with the named fields nulled are accepted.

        把被指名的字段置空后，同样的行会被接受。
        """
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "1_lines.csv"
            result = write_lines_csv.invoke({"file_path": str(path), "lines": [{
                "name": "Mg II", "rest_wavelength": 2798.8,
                "source": "fit_doublet", "status": "LIKELY",
                "fitted_center": 7395.33, "ridge_length": None, "cwt_snr": None,
            }]})
            self.assertEqual(result["n_lines"], 1)
            self.assertTrue(path.exists())
            self.assertNotIn("flags", result)



class SHTrustedProvenanceTests(unittest.TestCase):
    """The SH tool binds CSV measurements to the catalog or a returned fit."""

    def _tools(self, tmp, *, peaks=None, troughs=None):
        path = Path(tmp) / "spectrum.npz"
        np.savez(path, wavelength=np.array([3600.0, 9824.0]),
                 flux=np.array([1.0, 1.0]))
        return {item.name: item for item in _build_tools(
            str(path), 1.0, peaks=peaks, troughs=troughs)}

    def test_fit_center_claiming_cwt_is_corrected_before_write(self):
        import csv

        peak = {"wavelength": 7471.2, "wavelength_err": 0.8,
                "amplitude": 0.7, "amplitude_err": 0.1,
                "FWHM_km_s": 1204.0, "ridge_length": 18, "snr": 20.1}
        fit = {"center": 7471.096, "center_err": 0.12,
               "amplitude": 0.82, "amplitude_err": 0.06,
               "sigma": 2.3, "fwhm_km_s": 217.0, "flags": []}
        with tempfile.TemporaryDirectory() as tmp:
            tools = self._tools(tmp, peaks=[peak])
            with patch("FORMA.agents.multi_agents.harness.single_hypothesis._do_fit_peak",
                       return_value=fit):
                tools["_fit_peak"].invoke({"center_guess": 7467.4,
                                           "width_3sigma": 25})
            path = Path(tmp) / "lines.csv"
            result = tools["write_lines_csv"].invoke({"file_path": str(path), "lines": [{
                "name": "[O II]", "rest_wavelength": 3727.0,
                "fitted_center": 7471.096, "source": "CWT",
                "ridge_length": 18, "cwt_snr": 20.1, "status": "LIKELY",
            }]})
            with path.open(newline="") as handle:
                row = next(csv.DictReader(handle))
        self.assertEqual(result["n_lines"], 1)
        self.assertEqual(row["source"], "fit_peak")
        self.assertEqual(row["fitted_center"], "7471.096")
        self.assertEqual(row["amplitude"], "0.82")
        self.assertEqual(row["ridge_length"], "")
        self.assertEqual(row["cwt_snr"], "")
        self.assertEqual(result["provenance_corrections"][0]["source_to"], "fit_peak")

    def test_fit_source_with_cwt_metrics_is_canonicalized(self):
        import csv

        fit = {"center": 7471.096, "center_err": 0.12,
               "amplitude": 0.82, "amplitude_err": 0.06,
               "sigma": 2.3, "fwhm_km_s": 217.0, "flags": []}
        with tempfile.TemporaryDirectory() as tmp:
            tools = self._tools(tmp)
            with patch("FORMA.agents.multi_agents.harness.single_hypothesis._do_fit_peak",
                       return_value=fit):
                tools["_fit_peak"].invoke({"center_guess": 7467.4,
                                           "width_3sigma": 25})
            path = Path(tmp) / "lines.csv"
            result = tools["write_lines_csv"].invoke({"file_path": str(path), "lines": [{
                "name": "[O II]", "rest_wavelength": 3727.0,
                "fitted_center": 7471.096, "source": "fit_peak",
                "ridge_length": 18, "cwt_snr": 20.1, "status": "LIKELY",
            }]})
            with path.open(newline="") as handle:
                row = next(csv.DictReader(handle))
        self.assertEqual(result["n_lines"], 1)
        self.assertEqual(row["source"], "fit_peak")
        self.assertEqual(row["ridge_length"], "")
        self.assertEqual(row["cwt_snr"], "")

    def test_emission_cannot_claim_cwt_trough(self):
        with tempfile.TemporaryDirectory() as tmp:
            tools = self._tools(tmp, troughs=[{"wavelength": 6674.4,
                                              "amplitude": -0.5,
                                              "ridge_length": 5, "snr": 9.2}])
            path = Path(tmp) / "lines.csv"
            result = tools["write_lines_csv"].invoke({"file_path": str(path), "lines": [{
                "name": "Hε", "rest_wavelength": 3970.1,
                "fitted_center": 6674.4, "source": "CWT", "status": "MARGINAL",
            }]})
            self.assertFalse(path.exists())
        self.assertIn("unresolved_measurement_source", result["flags"])

    def test_doublet_fit_center_cannot_claim_nearby_cwt(self):
        prepared, corrections, errors = prepare_sh_lines(
            [{"name": "[O III]b", "rest_wavelength": 5008.2,
              "fitted_center": 6622.166, "source": "CWT",
              "ridge_length": 4, "cwt_snr": 8.9, "status": "LIKELY"}],
            [{"wavelength": 6621.6, "ridge_length": 4, "snr": 8.9}], [],
            [{"source": "fit_doublet", "kind": "emission", "center": 6622.166,
              "amplitude": 1.2, "sigma": 2.0, "fwhm_km_s": 213.0}],
        )
        self.assertFalse(errors)
        self.assertEqual(prepared[0]["source"], "fit_doublet")
        self.assertIsNone(prepared[0]["ridge_length"])
        self.assertIsNone(prepared[0]["cwt_snr"])
        self.assertEqual(corrections[0]["source_to"], "fit_doublet")

    def test_cwt_copy_uses_upstream_precision_and_metrics(self):
        prepared, _, errors = prepare_sh_lines(
            [{"name": "[O II]", "rest_wavelength": 3727.0,
              "fitted_center": 7471.2, "source": "CWT", "cwt_snr": 99.0}],
            [{"wavelength": 7471.24, "amplitude": 0.7, "snr": 20.1,
              "ridge_length": 18, "FWHM_A": 30.0}], [], [],
        )
        self.assertFalse(errors)
        self.assertEqual(prepared[0]["fitted_center"], 7471.24)
        self.assertEqual(prepared[0]["cwt_snr"], 20.1)
        self.assertAlmostEqual(prepared[0]["fitted_sigma"], 30.0 * FWHM_TO_SIGMA)


if __name__ == "__main__":
    unittest.main()
