"""Frozen VI and SH measurements drive display artifacts without science mutation."""

from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from FORMA.agentic_graph.spectrum_visualization import (
    plot_sh_adopted_lines, plot_spectrum_overview, plot_vi_features,
)
from FORMA.agentic_graph.browser_visualization import write_browser_bundle


class SpectrumVisualizationTests(unittest.TestCase):
    def test_overview_vi_and_sh_pngs_read_frozen_measurements(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wave = np.linspace(3900, 5100, 301)
            flux = 2 + .1 * (wave - 4500) / 600
            flux += 1.5 * np.exp(-.5 * ((wave - 4300) / 8) ** 2)
            flux -= .9 * np.exp(-.5 * ((wave - 4700) / 10) ** 2)
            npz = root / "spectrum.npz"
            ivar = np.ones(wave.size)
            ivar[0] = 0
            np.savez_compressed(npz, wavelength=wave, flux=flux, ivar=ivar)
            overview = plot_spectrum_overview(
                npz, root / "spectrum.png", bands=[("Blue", 3900, 4500),
                                                    ("Red", 4500, 5100)])
            catalog = root / "catalog.json"
            catalog.write_text(json.dumps({"measurements": [{
                "id": "fit:H1:0000", "source": "fit_peak", "kind": "emission",
                "adoptable": True, "record": {"center": 4300.0}}]}) + "\n",
                               encoding="utf-8")
            manifest = {"cwt_features": {
                "emission": [{"wavelength": 4300.0, "FWHM_A": 18.0}],
                "absorption": [{"wavelength": 4700.0, "FWHM_A": 22.0}]},
                "hypotheses": {"H1": {"catalog_path": str(catalog), "redshift": .1}},
                "run_id": "demo-run"}
            features = plot_vi_features(npz, manifest, root / "VI")
            with np.load(root / "VI/continuum_display.npz") as saved:
                self.assertTrue(np.array_equal(saved["wavelength"], wave))
                self.assertEqual(saved["flux"].shape, wave.shape)
            csv_path = root / "lines.csv"
            with csv_path.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=(
                    "name", "status", "fitted_center", "amplitude", "source"))
                writer.writeheader()
                writer.writerow({"name": "[O II]", "status": "LIKELY",
                                 "fitted_center": 4300, "amplitude": 1.5,
                                 "source": "fit_peak"})
                writer.writerow({"name": "Ca K_abs", "status": "MARGINAL",
                                 "fitted_center": 4700, "amplitude": -.9,
                                 "source": "CWT"})
                writer.writerow({"name": "[O III]", "status": "NOT_FOUND",
                                 "fitted_center": "", "amplitude": "", "source": ""})
            adopted = plot_sh_adopted_lines(
                npz, csv_path, root / "adopted_lines.png",
                root / "VI/continuum_display.npz")
            for path in (overview, features, adopted):
                self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            manifest_file = root / "VI/measurements/manifest.json"
            manifest_file.parent.mkdir()
            manifest_file.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
            sh_csv = root / "SH/H1/pre_analysis/branches/main/attempt/lines.csv"
            sh_csv.parent.mkdir(parents=True)
            sh_csv.write_bytes(csv_path.read_bytes())
            bundle_paths = write_browser_bundle(root)
            bundle = json.loads(bundle_paths["json"].read_text())
            self.assertEqual(bundle["spectrum"]["wavelength_angstrom"], wave.tolist())
            self.assertIsNone(bundle["spectrum"]["flux"][0])
            self.assertEqual(bundle["continuum"]["role"], "display_only")
            self.assertEqual(bundle["sh"]["H1"]["lines"][0]["status"], "LIKELY")
            self.assertNotIn(str(root), bundle_paths["js"].read_text())
            self.assertTrue(bundle_paths["js"].read_text().startswith(
                "window.FORMA_VISUALIZATION_DATA = "))
