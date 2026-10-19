"""One-feature FA preflight and strict binary submission."""

import tempfile
import json
import unittest
from pathlib import Path

import numpy as np
from langchain_core.messages import AIMessage, ToolMessage

from FORMA.agentic_graph.fa_feature_reality import (
    build_feature_window, measured_feature_width, run_feature_reality)
from FORMA.agentic_graph.execution_artifacts import allocate_execution
from FORMA.agentic_graph.vi_measurements import _sha256


class _FakeAgent:
    def __init__(self, tools, received):
        self.tool = tools[0]
        self.received = received

    async def astream(self, state, *, config, stream_mode):
        self.received.append(state["messages"][0].content)
        yield {"model": {"messages": [AIMessage(
            content="Coherent multi-pixel peak.", tool_calls=[{
                "name": "submit_feature_reality", "args": {"answer": "yes"}, "id": "c1",
            }], response_metadata={"token_usage": {
                "prompt_tokens": 12, "completion_tokens": 3, "total_tokens": 15}},
        )]}}
        result = self.tool.invoke({"answer": "yes"})
        yield {"tools": {"messages": [ToolMessage(
            content=str(result), tool_call_id="c1", name="submit_feature_reality",
        )]}}


class FeatureRealityTests(unittest.IsolatedAsyncioTestCase):
    async def test_one_target_no_identity_leak_and_usage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "spectrum.npz"
            np.savez(path, wavelength=np.arange(4000., 4020.),
                     flux=np.array([0., 0., 1., 2., 3., 4., 3., 2., 1., 0.,
                                    0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]),
                     ivar=np.ones(20))
            seen = []
            catalog_path = root / "catalog.json"
            catalog_path.write_text(json.dumps({
                "run_id": "r", "spectrum_npz_path": str(path),
                "spectrum_npz_sha256": _sha256(path), "masked_regions": [],
                "measurements": [{"id": "cwt:em:0001", "source": "CWT",
                                  "kind": "emission", "adoptable": True,
                                  "record": {"wavelength": 4005., "FWHM_A": 5.5,
                                             "FWHM_km_s": 412.}}],
            }))
            result = await run_feature_reality(
                llm=object(), run_id="r", measurement_id="cwt:em:0001",
                vi_catalog_path=catalog_path,
                session_path=root / "session.md", agent_factory=lambda **kw:
                    _FakeAgent(kw["tools"], seen),
            )
            self.assertEqual(result["node"]["answer"], "yes")
            self.assertNotIn("cwt:em:0001", seen[0])
            self.assertNotIn("[O III]", seen[0])
            self.assertIn("Candidate measured FWHM: `5.5` Å (`412` km/s)", seen[0])
            self.assertIn("| wavelength (Å) | flux | usable |", seen[0])
            self.assertNotIn("| ivar |", seen[0])
            self.assertEqual(result["model_usage"][0]["input_tokens"], 12)
            store = {}
            for branch in ("main", "recheck"):
                allocation = allocate_execution(
                    root / "outputs", run_id="r", branch_id=branch,
                    node_key="fa.real_feature_or_not/r/cwt:em:0001")
                voted = await run_feature_reality(
                    llm=object(), run_id="r", measurement_id="cwt:em:0001",
                    vi_catalog_path=catalog_path, execution=allocation,
                    node_store=store, agent_factory=lambda **kw:
                        _FakeAgent(kw["tools"], seen),
                )
                self.assertEqual(voted["node"]["execution"]["branch_id"], branch)
                self.assertTrue(allocation.path("node.json").is_file())
            self.assertEqual(len(store), 2)
            catalog = json.loads(catalog_path.read_text())
            catalog["spectrum_npz_sha256"] = "stale"
            catalog_path.write_text(json.dumps(catalog))
            with self.assertRaisesRegex(ValueError, "spectrum changed"):
                await run_feature_reality(
                    llm=object(), run_id="r", measurement_id="cwt:em:0001",
                    vi_catalog_path=catalog_path, session_path=root / "unused.md",
                    agent_factory=lambda **kw: self.fail("model must not be called"),
                )

    def test_no_valid_pixels_rejected_before_model(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.npz"
            np.savez(path, wavelength=np.arange(4000., 4010.),
                     flux=np.ones(10), ivar=np.zeros(10))
            with self.assertRaisesRegex(ValueError, "no usable samples"):
                build_feature_window(path, center=4005., kind="emission")

    def test_frozen_width_source_and_internal_ivar(self):
        self.assertEqual(measured_feature_width({
            "source": "CWT", "record": {"FWHM_A": 4.25, "FWHM_km_s": 300}}),
            (4.25, 300.0))
        self.assertEqual(measured_feature_width({
            "source": "fit_peak", "record": {"fwhm": 7.5, "fwhm_km_s": 500}}),
            (7.5, 500.0))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "masked.npz"
            np.savez(path, wavelength=np.array([4000., 4001., 4002.]),
                     flux=np.array([1., 2., 1.]), ivar=np.array([1., 0., 1.]))
            prompt = build_feature_window(path, center=4001., kind="emission",
                                          measured_fwhm_angstrom=2.,
                                          measured_fwhm_km_s=150.)
            self.assertIn("| 4001 | 2 | no |", prompt)
            self.assertIn("2/3 usable", prompt)
            self.assertIn("from positive IVAR", prompt)
            self.assertNotIn("| ivar |", prompt)
