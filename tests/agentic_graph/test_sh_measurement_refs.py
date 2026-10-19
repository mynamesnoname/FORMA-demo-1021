"""ID-based SH write boundary: the model never copies measurement floats."""

from __future__ import annotations

import csv
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from FORMA.agentic_graph.sh_measurement_refs import (
    build_catalog, build_id_writer, render_catalog, resolve_judgments,
)


CENTRE = 4960.3123456789


def catalog(fits=None):
    return build_catalog(
        redshift=0.0, wavelength_min=4950.0, wavelength_max=4970.0,
        peaks=[{"wavelength": CENTRE, "wavelength_err": 0.8123456789,
                "amplitude": 2.0, "amplitude_err": 0.1,
                "FWHM_A": 4.0, "FWHM_km_s": 241.9,
                "ridge_length": 12, "snr": 18.0}],
        troughs=[], fits=fits or [],
    )


def decision(line_id, ref, status="LIKELY"):
    return {"line_id": line_id, "measurement_id": ref, "status": status,
            "reason_codes": ["matched"], "comment": "Observed feature matches."}


class SHMeasurementRefsTests(unittest.TestCase):
    def test_catalog_window_reads_shared_redshift_tolerance(self):
        from FORMA.core.config.analysis_method import load_analysis_method

        kwargs = dict(redshift=0.5, wavelength_min=3500.0,
                      wavelength_max=7000.0, peaks=[], troughs=[], fits=[])
        default = build_catalog(**kwargs)
        self.assertEqual((default["z_min"], default["z_max"]), (0.49, 0.51))

        with tempfile.TemporaryDirectory() as directory:
            method = load_analysis_method().model_dump(mode="json")
            method["evaluation"]["redshift_tolerance"] = 0.02
            config_path = Path(directory) / "analysis_method.json"
            config_path.write_text(json.dumps(method), encoding="utf-8")
            with patch.dict(os.environ, {"FORMA_ANALYSIS_METHOD_CONFIG": str(config_path)}):
                overridden = build_catalog(**kwargs)
        self.assertEqual((overridden["z_min"], overridden["z_max"]), (0.48, 0.52))

    def test_id_only_write_keeps_full_precision_and_judgment(self):
        frozen = catalog()
        line_id = frozen["lines"][0]["id"]
        self.assertIn("cwt:em:0000", render_catalog(frozen))
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "lines.csv"
            judgments = Path(directory) / "judgments.json"
            result = build_id_writer(frozen, judgment_path=judgments).invoke({
                "file_path": str(output), "lines": [decision(line_id, "cwt:em:0000")],
            })
            self.assertEqual(result["n_lines"], 1)
            with output.open(newline="") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(float(row["fitted_center"]), CENTRE)
            self.assertEqual(row["source"], "CWT")
            self.assertEqual(float(row["implied_z"]), CENTRE / 4960.3 - 1)
            self.assertEqual(json.loads(judgments.read_text())[0]["reason_codes"], ["matched"])

    def test_bad_id_wrong_kind_and_unselectable_fit_are_repairable(self):
        frozen = catalog(fits=[{
            "source": "fit_peak", "kind": "emission", "target_line": "[O III]a",
            "center": 4960.3, "flags": ["center_at_bound"],
        }, {
            "source": "fit_peak", "kind": "absorption", "target_line": "Ca H_abs",
            "center": 4960.3, "flags": [],
        }])
        line_id = frozen["lines"][0]["id"]
        for ref, expected in (("cwt:em:9999", "known measurement ID"),
                              ("fit:0000", "not selectable"),
                              ("fit:0001", "kind mismatch")):
            with self.subTest(ref=ref):
                _, errors = resolve_judgments(frozen, [decision(line_id, ref)])
                self.assertIn(expected, str(errors))

    def test_clean_nominal_line_cannot_be_masked_even_with_id_interface(self):
        frozen = catalog()
        line_id = frozen["lines"][0]["id"]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "lines.csv"
            result = build_id_writer(frozen, masked_regions=[(4965, 4970)]).invoke({
                "file_path": str(output),
                "lines": [decision(line_id, None, "MASKED")],
            })
            self.assertIsNone(result["path"])
            self.assertFalse(output.exists())
            self.assertIn("MASKED requires", str(result["rows_to_repair"]))

    def test_missing_line_and_numeric_smuggling_are_rejected(self):
        frozen = catalog()
        line_id = frozen["lines"][0]["id"]
        _, errors = resolve_judgments(frozen, [])
        self.assertIn("missing predicted line", str(errors))
        injected = {**decision(line_id, "cwt:em:0000"), "fitted_center": 123.0}
        _, errors = resolve_judgments(frozen, [injected])
        self.assertIn("optional reason_codes/comment only", str(errors))


if __name__ == "__main__":
    unittest.main()
