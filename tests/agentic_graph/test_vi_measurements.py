"""VI measurement freezing and cross-hypothesis identity handoff."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import numpy as np

from FORMA.agentic_graph.legacy_sh_adapter import run_with_existing_sh_inputs
from FORMA.agentic_graph.sh_measurement_refs import build_catalog
from FORMA.agentic_graph.vi_measurements import (
    assign_cwt_feature_ids, prepare_vi_measurements,
)


class VIMeasurementsTests(unittest.IsolatedAsyncioTestCase):
    def _prepare(self, root: Path):
        spectrum = root / "spectrum.npz"
        np.savez(spectrum, wavelength=np.linspace(4900, 5050, 151),
                 flux=np.ones(151))
        peaks = [{"wavelength": 4960.3123456789, "snr": 12.0}]

        def fitted(_npz, redshift, _peaks, _troughs, _lo, _hi, _mask, artifact):
            attempt = {"target": "[O III]a", "method": "fit_peak",
                       "predicted_obs": [4960.3 * (1 + redshift)],
                       "result": {"center": 4960.3 * (1 + redshift)},
                       "status": "ok"}
            Path(artifact).write_text(json.dumps([attempt]), encoding="utf-8")
            fit = {"source": "fit_peak", "kind": "emission",
                   "target_line": "[O III]a", "center": 4960.3 * (1 + redshift),
                   "flags": []}
            return [attempt], [fit]

        with patch("FORMA.agentic_graph.vi_measurements._prepare_prefits", side_effect=fitted) as runner:
            manifest = prepare_vi_measurements(
                run_id="run-1", spectrum_npz_path=spectrum,
                hypotheses={"H1": 0.0, "H2": 0.001}, peaks=peaks, troughs=[],
                output_dir=root / "vi_measurements",
            )
        self.assertEqual(runner.call_count, 2)
        return spectrum, manifest

    def test_cwt_ids_are_shared_and_fits_are_hypothesis_scoped(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, manifest = self._prepare(root)
            first = json.loads(Path(manifest["hypotheses"]["H1"]["catalog_path"]).read_text())
            second = json.loads(Path(manifest["hypotheses"]["H2"]["catalog_path"]).read_text())
            self.assertEqual(first["measurements"][0]["id"], "cwt:em:0000")
            self.assertEqual(second["measurements"][0]["id"], "cwt:em:0000")
            self.assertEqual(first["measurements"][1]["id"], "fit:H1:0000")
            self.assertEqual(second["measurements"][1]["id"], "fit:H2:0000")
            self.assertEqual(first["measurements"][0]["record"]["wavelength"],
                             4960.3123456789)
            self.assertEqual(manifest["cwt_features"]["emission"][0]["feature_id"],
                             "cwt:em:0000")
            self.assertEqual(first["spectrum_npz_sha256"], second["spectrum_npz_sha256"])
            with self.assertRaises(FileExistsError):
                prepare_vi_measurements(
                    run_id="run-1", spectrum_npz_path=root / "spectrum.npz",
                    hypotheses={"H1": 0.0}, peaks=[], troughs=[],
                    output_dir=root / "vi_measurements",
                )

    def test_existing_cwt_id_cannot_be_silently_rebound(self):
        with self.assertRaisesRegex(ValueError, "does not match"):
            assign_cwt_feature_ids([{"wavelength": 5000, "feature_id": "cwt:em:0001"}], [])
        with self.assertRaisesRegex(ValueError, "VI boundary"):
            build_catalog(
                run_id="run-1", hypothesis_ref="H1", redshift=0.0,
                wavelength_min=4900, wavelength_max=5050,
                peaks=[{"wavelength": 4960.3}], troughs=[], fits=[],
            )

    async def test_sh_uses_frozen_vi_catalog_without_refitting(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spectrum, manifest = self._prepare(root)
            catalog = manifest["hypotheses"]["H1"]["catalog_path"]
            captured = {}

            async def capture(**kwargs):
                captured.update(kwargs)
                return {"ok": True}

            with patch("FORMA.agentic_graph.legacy_sh_adapter.run_sh_line_review",
                       new=AsyncMock(side_effect=capture)), patch(
                "FORMA.agents.multi_agents.harness.single_hypothesis._prepare_prefits",
                side_effect=AssertionError("SH must not fit"),
            ):
                result = await run_with_existing_sh_inputs(
                    llm=object(), run_id="run-1", hypothesis_ref="H1",
                    hypothesis_redshift=0.0, fits_path="example.fits",
                    npz_path=str(spectrum), csv_path=root / "lines.csv",
                    report_path=root / "report.md", vi_catalog_path=catalog,
                )
            self.assertEqual(result, {"ok": True})
            self.assertEqual(captured["measurement_catalog_path"], Path(catalog))
            self.assertIn("cwt:em:0000", captured["sh_context"])

            with self.assertRaisesRegex(ValueError, "does not match"):
                await run_with_existing_sh_inputs(
                    llm=object(), run_id="run-1", hypothesis_ref="H2",
                    hypothesis_redshift=0.0, fits_path="example.fits",
                    npz_path=str(spectrum), csv_path=root / "other.csv",
                    report_path=root / "other.md", vi_catalog_path=catalog,
                )

            np.savez(spectrum, wavelength=np.linspace(4900, 5050, 151),
                     flux=np.zeros(151))
            with self.assertRaisesRegex(ValueError, "spectrum changed"):
                await run_with_existing_sh_inputs(
                    llm=object(), run_id="run-1", hypothesis_ref="H1",
                    hypothesis_redshift=0.0, fits_path="example.fits",
                    npz_path=str(spectrum), csv_path=root / "other.csv",
                    report_path=root / "other.md", vi_catalog_path=catalog,
                )


if __name__ == "__main__":
    unittest.main()
