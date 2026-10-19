"""DESI sky-line proximity remains an advisory feature property."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from FORMA.agentic_graph.skyline_risk import _catalog, skyline_risk


class SkylineRiskTests(unittest.TestCase):
    def test_frozen_desi_catalog_and_discrete_match(self):
        lines, digest, version = _catalog()
        self.assertEqual(len(lines), 274)
        self.assertEqual(version, "0.70.0")
        self.assertEqual(len(digest), 64)
        risk = skyline_risk(5578.85)
        self.assertEqual(risk["status"], "near_discrete_skyline")
        self.assertEqual(risk["nearest_line"]["wavelength_angstrom"], 5578.85)
        self.assertEqual(risk["nearest_line"]["offset_angstrom"], 0.0)
        self.assertTrue(risk["within_proximity_threshold"])

    def test_oh_band_is_only_a_region_warning_and_bound_is_configurable(self):
        bound = {"value": 2.0, "source": "config", "source_path": "config/test.json",
                 "payload_digest": "test"}
        with patch("FORMA.agentic_graph.skyline_risk.effective_operand_threshold",
                   return_value=bound):
            region = skyline_risk(7200.0)
            self.assertEqual(region["status"], "oh_band_only")
            self.assertFalse(region["within_proximity_threshold"])
            self.assertIn("skyline:oh-band-7000", region["oh_band_ids"])
            self.assertEqual(region["threshold_angstrom"], 2.0)
            self.assertEqual(region["threshold_source"], "config")
            self.assertEqual(region["threshold_source_path"], "config/test.json")
            clear = skyline_risk(4242.4)
            self.assertEqual(clear["status"], "no_registered_risk")
            self.assertEqual(clear["oh_band_ids"], [])

    def test_nonfinite_feature_center_is_rejected(self):
        with self.assertRaises(ValueError):
            skyline_risk(float("nan"))


if __name__ == "__main__":
    unittest.main()
