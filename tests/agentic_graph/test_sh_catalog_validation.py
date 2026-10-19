"""Deterministic write-boundary checks for the new SH node."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from FORMA.agents.multi_agents.harness.sh_provenance import (
    SH_CSV_FIELDS, validate_sh_catalog,
)
from FORMA.agents.multi_agents.harness.single_hypothesis import _build_tools


def row(status: str = "NOT_FOUND") -> dict:
    result = {field: None for field in SH_CSV_FIELDS}
    result.update(name="[O III]a", rest_wavelength=4960.3,
                  predicted_obs=4960.3, status=status)
    return result


class SHCatalogValidationTests(unittest.TestCase):
    def test_nominally_clean_line_cannot_be_masked_by_distant_overlap(self):
        errors = validate_sh_catalog([row("MASKED")], 0.0, 4950, 4970,
                                     [(4965, 4970)])
        self.assertIn("MASKED requires the nominal predicted wavelength",
                      str(errors))
        self.assertEqual(validate_sh_catalog([row("MASKED")], 0.0, 4950, 4970,
                                             [(4958, 4962)]), [])

    def test_unadopted_status_cannot_carry_failed_fit(self):
        failed = row("NOT_FOUND")
        failed.update(fitted_center=4960.3, source="fit_peak")
        self.assertIn("unadopted line cannot carry a measurement",
                      str(validate_sh_catalog([failed], 0.0, 4950, 4970, [])))

    def test_registry_numbers_and_completeness(self):
        good = row()
        self.assertEqual(validate_sh_catalog([good], 0.0, 4950, 4970, []), [])
        wrong = {**good, "predicted_obs": 4961.0}
        self.assertIn("does not match registry/redshift",
                      str(validate_sh_catalog([wrong], 0.0, 4950, 4970, [])))
        self.assertIn("duplicate line",
                      str(validate_sh_catalog([good, good], 0.0, 4950, 4970, [])))
        self.assertIn("missing predicted line",
                      str(validate_sh_catalog([], 0.0, 4950, 4970, [])))

    def test_strict_writer_rejects_before_file_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            npz = Path(directory) / "spectrum.npz"
            csv = Path(directory) / "lines.csv"
            wavelengths = np.linspace(4950, 4970, 41)
            np.savez(npz, wavelength=wavelengths, flux=np.ones_like(wavelengths))
            writer = {item.name: item for item in _build_tools(
                str(npz), 0.0, masked_regions=[(4965, 4970)],
                strict_catalog=True,
            )}["write_lines_csv"]
            rejected = writer.invoke({"file_path": str(csv),
                                      "lines": [row("MASKED")]})
            self.assertIsNone(rejected["path"])
            self.assertFalse(csv.exists())
            accepted = writer.invoke({"file_path": str(csv),
                                      "lines": [row("NOT_FOUND")]})
            self.assertEqual(accepted["n_lines"], 1)
            self.assertTrue(csv.exists())
