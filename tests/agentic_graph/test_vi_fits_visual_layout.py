"""New graph FITS outputs keep all VI products under the readable VI folder."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from FORMA.agentic_graph.vi_fits_adapter import prepare_fits_inputs


class _Rows:
    def __init__(self, rows):
        self.rows = rows

    def to_dict(self, _orientation):
        return self.rows


class VIFitsVisualLayoutTests(unittest.TestCase):
    def test_graph_vi_and_overview_have_new_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fits = root / "demo.fits"
            fits.touch()
            output = root / "sample"
            wave = np.linspace(3900, 5100, 301)
            flux = 2 + np.exp(-.5 * ((wave - 4300) / 8) ** 2)

            def detect(**kwargs):
                self.assertEqual(kwargs["artifact_subdir"], "VI")
                vi = Path(kwargs["output_dir"]) / "VI"
                (vi / "demo_emission.csv").write_text("wavelength\n", encoding="utf-8")
                (vi / "demo_absorption.csv").write_text("wavelength\n", encoding="utf-8")
                return {"df_emission": _Rows([{"wavelength": 4300., "FWHM_A": 18.}]),
                        "df_absorption": _Rows([])}

            def freeze(**kwargs):
                target = Path(kwargs["output_dir"])
                self.assertEqual(target, output / "VI/measurements")
                target.mkdir()
                catalog = target / "H1.json"
                catalog.write_text(json.dumps({"measurements": []}) + "\n", encoding="utf-8")
                manifest = {"cwt_features": {"emission": kwargs["peaks"],
                                             "absorption": kwargs["troughs"]},
                            "hypotheses": {"H1": {"catalog_path": str(catalog)}}}
                (target / "manifest.json").write_text(json.dumps(manifest) + "\n",
                                                      encoding="utf-8")
                return manifest

            params = SimpleNamespace(
                arm_name=["Blue", "Red"],
                arm_wavelength_range=[[3900, 4500], [4500, 5100]],
                assumed_snr_without_ivar=1., cwt_snr_thresh=5.,
                cwt_min_ridge_length=2, cwt_n_scales=8,
                cwt_min_width=1., cwt_max_width=20.,
                rr_template_dir="templates", use_archetypes=False,
                archetype_dir=None, rr_nminima=2, rr_nnearest=1,
                rr_omp_num_threads=1, rr_archetype_legendre_degree=2,
                rr_archetype_legendre_prior_sigma=.1,
                hypothesis_label_seed="demo")
            with patch("FORMA.agentic_graph.vi_fits_adapter._load_spectrum_from_fits",
                       return_value={"wavelength": wave, "flux": flux,
                                     "snr": np.ones(wave.size),
                                     "ivar": np.ones(wave.size)}), patch(
                "FORMA.agentic_graph.vi_fits_adapter.run_cwt_feature_detection",
                side_effect=detect), patch(
                "FORMA.agentic_graph.vi_fits_adapter.run_redrock_pipeline",
                return_value={"hypotheses": [{"z_representative": .1,
                                               "_redrock": {"znum": 0}}]}), patch(
                "FORMA.agentic_graph.vi_fits_adapter.prepare_vi_measurements",
                side_effect=freeze):
                prepared = prepare_fits_inputs(fits_path=fits, run_id="r",
                                               output_root=output, params=params)
            self.assertEqual(Path(prepared["manifest_path"]),
                             output / "VI/measurements/manifest.json")
            for path in (output / "spectrum.png", output / "VI/features.png",
                         output / "VI/continuum_display.npz"):
                self.assertTrue(path.is_file(), path)
            self.assertFalse((output / "visual_interpreter").exists())
            self.assertFalse((output / "vi_measurements").exists())
