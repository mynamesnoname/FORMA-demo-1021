"""LRG/BGS graph gates, advisory votes, Ne V handoff and branch provenance."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from langchain_core.messages import AIMessage, ToolMessage

from FORMA.agentic_graph.fa_doublet import review_doublet
from FORMA.core.constants import SIGMA_TO_FWHM, SPEED_OF_LIGHT_KMS
from FORMA.agentic_graph.feature_registry import _digest, build_feature_registry
from FORMA.agentic_graph.lrg_bgs_path import (_absorption_sample, run_lrg_bgs_path,
                                               run_lrg_bgs_path_through_report)
from FORMA.agentic_graph.qso_entry import run_qso_entry
from FORMA.agentic_graph.reasoning_trace import (fork_branch, new_trace, record_analysis,
                                                 record_fa_vote, bind_artifact_root,
                                                 write_trace)
from evaluation.agentic_graph.run_lrg_bgs_paths import run as run_lrg_archive

from test_feature_registry_and_trace import _Q11Model, _fixture, _json


def _fixture_lrg(root: Path, *, mode: str = "two", strong: bool = True,
                 mask_blue: bool = False, mask_ca: bool = False,
                 ca_absorption: bool = False, mask_dn_red: bool = False) -> dict:
    nev = mode == "nev"
    first = "line:nev-3426" if nev else "line:cak-3934-abs"
    manifest_file, nodes = _fixture(root, classification="LRG/BGS",
                                    first_line_id=first, redshift=0.0)
    manifest = json.loads(manifest_file.read_text())
    npz = Path(manifest["spectrum_npz_path"])
    wl = np.arange(3300.0, 5101.0)
    flux = np.ones_like(wl)
    if strong:
        flux[(wl >= 4000) & (wl < 4100)] = 2.0
    if ca_absorption:
        flux[wl == 3935.0] = 0.5
        flux[wl == 3970.0] = 0.5
    ivar = np.ones_like(wl)
    if mask_dn_red:
        ivar[(wl >= 4000) & (wl < 4100)] = 0.0
    np.savez(npz, wavelength=wl, flux=flux, ivar=ivar)
    manifest["spectrum_npz_sha256"] = _digest(npz)
    first_center = 3426.0 if nev else 3934.8
    cwt = {"feature_id": "cwt:em:0000", "wavelength": first_center}
    if nev:
        manifest["cwt_features"] = {"emission": [cwt], "absorption": []}
    else:
        manifest["cwt_features"] = {"emission": [], "absorption": [cwt]}
    _json(root / "vi/cwt_features.json", manifest["cwt_features"])
    for node_file in nodes:
        node = json.loads(node_file.read_text())
        catalog_file = Path(node["measurement_catalog_path"])
        catalog = json.loads(catalog_file.read_text())
        catalog.update({"spectrum_npz_sha256": _digest(npz),
                        "wavelength_min": float(wl[0]), "wavelength_max": float(wl[-1]),
                        "masked_regions": ([[3850., 3950.]] if mask_blue else
                                           [[3919., 3950.]] if mask_ca else [])})
        catalog["lines"] = [
            {"id": first, "kind": "emission" if nev else "absorption",
             "predicted_obs": first_center},
            {"id": "line:cah-3969-abs" if not nev else "line:other",
             "kind": "absorption" if not nev else "emission",
             "predicted_obs": 3969.6 if not nev else 4500.},
        ]
        catalog["measurements"][0].update({"kind": catalog["lines"][0]["kind"],
                                            "record": cwt})
        catalog["measurements"][1].update({
            "kind": catalog["lines"][1]["kind"],
            "record": {"center": 3969.6 if not nev else 4500.}})
        _json(catalog_file, catalog)
        judgment_file = Path(node["judgment_path"])
        judgments = json.loads(judgment_file.read_text())
        judgments[0]["line_id"] = first
        judgments[1]["line_id"] = catalog["lines"][1]["id"]
        if mode == "zero":
            for item in judgments:
                item.update({"measurement_id": None, "status": "NOT_FOUND"})
        elif mode == "one":
            judgments[1].update({"measurement_id": None, "status": "NOT_FOUND"})
        elif mode == "one_masked":
            judgments[1].update({"measurement_id": None, "status": "MASKED"})
        elif mode == "masked_ca":
            for item in judgments:
                item.update({"measurement_id": None, "status": "MASKED"})
        _json(judgment_file, judgments)
        node["measurement_catalog_sha256"] = _digest(catalog_file)
        node["judgment_sha256"] = _digest(judgment_file)
        _json(node_file, node)
    _json(manifest_file, manifest)
    trace = new_trace(build_feature_registry(manifest_file, nodes))
    record_analysis(trace, "main", kind="sh_pre_analysis_import",
                    analysis_ref="h1", artifact_refs=["sh/h1/node"])
    return trace


def _accept(trace: dict, feature: str) -> None:
    for seat in range(3):
        record_fa_vote(trace, "main", feature,
                       vote_id=f"{feature}:{seat}", reviewer_id=f"r{seat}",
                       answer="yes", origin="model")


class _VoteAgent:
    def __init__(self, writer, answer: str, tool_name: str = "submit_cahk_vote"):
        self.writer = writer
        self.answer = answer
        self.tool_name = tool_name

    async def astream(self, state, *, config, stream_mode):
        args = {"answer": self.answer,
                "reason": "Both predicted component regions have usable local pixels."}
        yield {"model": {"messages": [AIMessage(
            content="Reviewed the two supplied local windows.",
            tool_calls=[{"name": self.tool_name, "args": args, "id": "v1"}],
            response_metadata={"token_usage": {
                "prompt_tokens": 12, "completion_tokens": 5,
                "total_tokens": 17}})]}}
        value = self.writer.invoke(args)
        yield {"tools": {"messages": [ToolMessage(
            content=str(value), tool_call_id="v1", name=self.tool_name)]}}


class _SampleModel:
    def __init__(self, offsets: tuple[int, ...] = (2,)):
        self.calls = 0
        self.offsets = offsets

    async def ainvoke(self, messages):
        self.calls += 1
        payload = json.loads(messages[-1].content)
        samples = payload["samples"]
        trough = min(samples, key=lambda item: item["flux"] if item["valid"] else float("inf"))
        if trough["flux"] >= 1.0:
            answer = {"no_valid_trough": True, "reason": "No resolved local depression."}
        else:
            index = samples.index(trough)
            offset = self.offsets[(self.calls - 1) % len(self.offsets)]
            answer = {"left_sample_id": samples[index - offset]["sample_id"],
                      "trough_sample_id": trough["sample_id"],
                      "right_sample_id": samples[index + offset]["sample_id"],
                      "reason": "A local minimum lies between two higher continuum samples."}
        return AIMessage(content=json.dumps(answer),
                         response_metadata={"token_usage": {"prompt_tokens": 10,
                                                              "completion_tokens": 8,
                                                              "total_tokens": 18}})


class LRGBGSPathTests(unittest.IsolatedAsyncioTestCase):
    async def test_two_adopted_ca_and_strong_dn_survive_without_vote(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root)
            _accept(trace, "cwt:em:0000")
            _accept(trace, "fit:h1:0000")
            before = copy.deepcopy(trace["branches"]["main"]["state"]["registry"])
            result = await run_lrg_bgs_path(trace, branch_id="main", hypothesis_ref="h1",
                                            output_root=root / "out")
            self.assertEqual((result["path_status"], result["candidate_type"]),
                             ("survive", "LRG/BGS"))
            inventory = next(item["node"]["output"] for item in result["nodes"]
                             if item["node"]["node_type"] == "lrg_bgs.cahk_inventory")
            self.assertEqual(inventory["adopted_count"], 2)
            self.assertFalse(any(item["node"]["node_type"] == "lrg_bgs.cahk_targeted_review"
                                 for item in result["nodes"]))
            self.assertEqual(trace["branches"]["main"]["state"]["registry"], before)
            write_trace(trace, root / "out/tree.json")

    async def test_zero_ca_uses_targeted_vote_and_no_vote_changes_route(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="zero")
            answers = iter(["no", "no", "yes"])
            result = await run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out",
                llm=object(), concurrency=1,
                agent_factory=lambda **kw: _VoteAgent(kw["tools"][0], next(answers)))
            review = next(item["node"]["output"] for item in result["nodes"]
                          if item["node"]["node_type"] == "lrg_bgs.cahk_targeted_review")
            self.assertEqual(review["status"], "complete")
            self.assertFalse(review["pair_supported"])
            self.assertEqual(review["vote_summary"]["no"], 2)
            self.assertEqual(review["model_usage"]["calls"], 3)
            self.assertEqual(result["path_status"], "survive")
            self.assertIn(result["report_ref"], trace["artifacts"])
            write_trace(trace, root / "out/tree.json")

    async def test_strong_dn_zero_ca_positive_vote_samples_both_components(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="zero", ca_absorption=True)
            model = _SampleModel()
            result = await run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out",
                llm=model,
                agent_factory=lambda **kw: _VoteAgent(kw["tools"][0], "yes"))
            review = next(item["node"]["output"] for item in result["nodes"]
                          if item["node"]["node_type"] == "lrg_bgs.cahk_targeted_review")
            self.assertEqual(result["path_status"], "survive")
            self.assertTrue(review["consultative_only"])
            self.assertEqual(review["sampled_observation"]["status"], "complete")
            self.assertEqual(len(review["sampled_observation"]["candidates"]), 2)
            self.assertEqual(model.calls, 6)
            write_trace(trace, root / "out/tree.json")

    async def test_one_adopted_ca_has_pending_advice_without_model(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="one")
            _accept(trace, "cwt:em:0000")
            result = await run_lrg_bgs_path(trace, branch_id="main",
                                            hypothesis_ref="h1", output_root=root / "out")
            review = next(item["node"]["output"] for item in result["nodes"]
                          if item["node"]["node_type"] == "lrg_bgs.cahk_targeted_review")
            self.assertEqual(review["status"], "pending")
            self.assertEqual(result["path_status"], "survive")

    async def test_fa_doublet_is_not_reused_as_type_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="one")
            _accept(trace, "cwt:em:0000")
            advisory = await review_doublet(
                trace=trace, branch_id="main", hypothesis_ref="h1",
                doublet_id="doublet:cahk", output_root=root / "out", llm=object(),
                concurrency=1,
                agent_factory=lambda **kw: _VoteAgent(
                    kw["tools"][0], "yes", "submit_doublet_vote"))
            result = await run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out")
            review = next(item["node"]["output"] for item in result["nodes"]
                          if item["node"]["node_type"] == "lrg_bgs.cahk_targeted_review")
            self.assertEqual(review["status"], "pending")
            self.assertEqual(review["source"], "targeted_window")
            self.assertNotIn(advisory["node_ref"], [ref for item in result["nodes"]
                                                    for ref in item["node"]["input_refs"]])
            self.assertEqual(result["path_status"], "survive")
            write_trace(trace, root / "out/tree.json")

    async def test_masked_ca_window_is_unreviewable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="zero", mask_ca=True)
            result = await run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out",
                llm=object(), agent_factory=lambda **kw: self.fail("model must not run"))
            review = next(item["node"]["output"] for item in result["nodes"]
                          if item["node"]["node_type"] == "lrg_bgs.cahk_targeted_review")
            self.assertEqual(review["status"], "unreviewable")
            self.assertEqual(result["path_status"], "survive")

    async def test_weak_and_missing_dn_are_distinct(self):
        for mask_blue, expected in ((False, "dead"), (True, "unresolved")):
            with self.subTest(mask_blue=mask_blue), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                trace = _fixture_lrg(root, mode="zero", strong=False, mask_blue=mask_blue)
                result = await run_lrg_bgs_path(trace, branch_id="main",
                                                hypothesis_ref="h1", output_root=root / "out")
                self.assertEqual(result["path_status"], expected)
                self.assertFalse(any(item["node"]["node_type"] == "lrg_bgs.cahk_inventory"
                                     for item in result["nodes"]))

    async def test_masked_ca_is_unknown_but_strong_dn_keeps_canvas_route(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="masked_ca")
            result = await run_lrg_bgs_path(trace, branch_id="main",
                                            hypothesis_ref="h1", output_root=root / "out")
            inventory = next(item["node"]["output"] for item in result["nodes"]
                             if item["node"]["node_type"] == "lrg_bgs.cahk_inventory")
            self.assertEqual(inventory["inventory_status"], "unknown")
            self.assertEqual(result["path_status"], "survive")
            route = result["nodes"][-2]["node"]["output"]
            self.assertIn("cahk_inventory_unknown", route["unresolved_reasons"])
            self.assertTrue(any(item["node"]["node_type"] == "lrg_bgs.cahk_targeted_review"
                                for item in result["nodes"]))

    async def test_adopted_ca_center_inside_frozen_mask_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mask_ca=True)
            _accept(trace, "cwt:em:0000")
            _accept(trace, "fit:h1:0000")
            with self.assertRaisesRegex(ValueError, "falls in a frozen mask"):
                await run_lrg_bgs_path(trace, branch_id="main", hypothesis_ref="h1",
                                       output_root=root / "out")
            self.assertFalse(any(key.startswith("sh2.lrg_bgs/") for key in
                                 trace["branches"]["main"]["state"]["analysis_results"]))

    async def test_weak_dn_with_two_adopted_ca_survives(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, strong=False)
            _accept(trace, "cwt:em:0000")
            _accept(trace, "fit:h1:0000")
            result = await run_lrg_bgs_path(trace, branch_id="main",
                                            hypothesis_ref="h1", output_root=root / "out")
            route = result["nodes"][-2]["node"]["output"]
            self.assertEqual((result["path_status"], route["reason_code"]),
                             ("survive", "cahk_pair_adopted"))

    async def test_weak_dn_one_ca_requires_positive_vote_and_sampled_second_component(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="one", strong=False, ca_absorption=True)
            _accept(trace, "cwt:em:0000")
            model = _SampleModel()
            result = await run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out",
                llm=model, concurrency=2,
                agent_factory=lambda **kw: _VoteAgent(kw["tools"][0], "yes"))
            review = next(item["node"]["output"] for item in result["nodes"]
                          if item["node"]["node_type"] == "lrg_bgs.cahk_targeted_review")
            route = result["nodes"][-2]["node"]["output"]
            self.assertEqual((result["path_status"], route["reason_code"]),
                             ("survive", "cahk_sampled_pair"))
            self.assertEqual(model.calls, 3)
            self.assertEqual(review["sampled_observation"]["status"], "complete")
            self.assertEqual(len(review["sampled_observation"]["candidates"]), 1)
            self.assertEqual(route["sampled_candidate_ids"], [
                review["sampled_observation"]["candidates"][0]["candidate_id"]])
            report = Path(trace["artifacts"][result["report_ref"]]["path"]).read_text()
            self.assertIn("sampled trough", report)
            self.assertIn("FWHM proxy", report)
            self.assertIn(route["sampled_candidate_ids"][0], report)
            self.assertEqual(trace["branches"]["main"]["state"]["registry"]
                             ["hypotheses"]["h1"]["classification"], "LRG/BGS")
            write_trace(trace, root / "out/tree.json")

    async def test_ca_representative_is_complete_median_fwhm_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="one", strong=False, ca_absorption=True)
            _accept(trace, "cwt:em:0000")
            model = _SampleModel(offsets=(1, 3, 2))
            result = await run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out",
                llm=model,
                agent_factory=lambda **kw: _VoteAgent(kw["tools"][0], "yes"))
            review = next(item["node"]["output"] for item in result["nodes"]
                          if item["node"]["node_type"] == "lrg_bgs.cahk_targeted_review")
            candidate = review["sampled_observation"]["candidates"][0]
            self.assertEqual([pick["outer_reference_span_angstrom"]
                              for pick in candidate["selections"]], [2., 6., 4.])
            self.assertEqual(candidate["representative"]["outer_reference_span_angstrom"], 4.)
            self.assertEqual(candidate["representative"]["seat"], 2)
            self.assertEqual(result["path_status"], "survive")

    async def test_weak_dn_one_ca_rejected_vote_is_dead(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="one", strong=False)
            _accept(trace, "cwt:em:0000")
            result = await run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out",
                llm=object(), agent_factory=lambda **kw: _VoteAgent(kw["tools"][0], "no"))
            self.assertEqual(result["path_status"], "dead")
            self.assertEqual(result["nodes"][-2]["node"]["output"]["reason_code"],
                             "cahk_review_rejected")

    async def test_weak_dn_one_ca_unfinished_vote_remains_unresolved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="one", strong=False)
            _accept(trace, "cwt:em:0000")
            result = await run_lrg_bgs_path(trace, branch_id="main",
                                            hypothesis_ref="h1", output_root=root / "out")
            self.assertEqual(result["path_status"], "unresolved")

    async def test_weak_dn_positive_vote_without_a_trough_is_unresolved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="one", strong=False)
            _accept(trace, "cwt:em:0000")
            model = _SampleModel()
            result = await run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out",
                llm=model,
                agent_factory=lambda **kw: _VoteAgent(kw["tools"][0], "yes"))
            review = next(item["node"]["output"] for item in result["nodes"]
                          if item["node"]["node_type"] == "lrg_bgs.cahk_targeted_review")
            self.assertEqual(review["sampled_observation"]["status"], "pending")
            self.assertEqual(result["path_status"], "unresolved")
            self.assertEqual(model.calls, 3)

    async def test_rejected_fa_measurement_is_not_restored_by_targeted_ca_vote(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, strong=False, ca_absorption=True)
            _accept(trace, "cwt:em:0000")
            for seat in range(3):
                record_fa_vote(trace, "main", "fit:h1:0000", vote_id=f"no:{seat}",
                               reviewer_id=f"r{seat}", answer="no", origin="model")
            result = await run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out",
                llm=_SampleModel(),
                agent_factory=lambda **kw: _VoteAgent(kw["tools"][0], "yes"))
            route = result["nodes"][-2]["node"]["output"]
            self.assertEqual(result["path_status"], "unresolved")
            self.assertIn("cahk_requires_fa_recheck", route["unresolved_reasons"])

    async def test_masked_sh_component_is_not_restored_by_targeted_ca_vote(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="one_masked", strong=False,
                                 ca_absorption=True)
            _accept(trace, "cwt:em:0000")
            result = await run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out",
                llm=_SampleModel(),
                agent_factory=lambda **kw: _VoteAgent(kw["tools"][0], "yes"))
            self.assertEqual(result["path_status"], "unresolved")
            self.assertIn("cahk_masked_sh_requires_reconciliation",
                          result["nodes"][-2]["node"]["output"]["unresolved_reasons"])

    async def test_unknown_dn_with_adopted_ca_can_use_pair(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mask_dn_red=True)
            _accept(trace, "cwt:em:0000")
            _accept(trace, "fit:h1:0000")
            result = await run_lrg_bgs_path(trace, branch_id="main",
                                            hypothesis_ref="h1", output_root=root / "out")
            self.assertEqual(result["path_status"], "survive")
            self.assertIn("insufficient_usable_band_data",
                          result["nodes"][-2]["node"]["output"]["unresolved_reasons"])

    async def test_unknown_dn_one_ca_rejected_vote_stays_unresolved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="one", mask_dn_red=True)
            _accept(trace, "cwt:em:0000")
            result = await run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out",
                llm=object(), agent_factory=lambda **kw: _VoteAgent(kw["tools"][0], "no"))
            self.assertEqual(result["path_status"], "unresolved")
            review = next(item["node"]["output"] for item in result["nodes"]
                          if item["node"]["node_type"] == "lrg_bgs.cahk_targeted_review")
            self.assertEqual(review["status"], "complete")
            self.assertFalse(review["pair_supported"])
            self.assertIn("insufficient_usable_band_data",
                          result["nodes"][-2]["node"]["output"]["unresolved_reasons"])

    async def test_offline_runner_preserves_pending_advice(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="zero")
            out = root / "out"
            out.mkdir()
            bind_artifact_root(trace, out)
            before = write_trace(trace, out / "before.json")
            summary = await run_lrg_archive(before, out / "after.json")
            self.assertEqual(summary["hypotheses"]["h1"]["path_status"], "survive")
            archived = json.loads((out / "after.json").read_text())
            refs = [ref for ref, item in archived["artifacts"].items()
                    if item["kind"] == "lrg_bgs_node"]
            review = next(node for ref in refs
                          if (node := json.loads(Path(archived["artifacts"][ref]["path"]).read_text()))
                          ["node_type"] == "lrg_bgs.cahk_targeted_review")
            self.assertEqual(review["output"]["status"], "pending")

    async def test_nev_handoff_reaches_qso_q2_and_preserves_initial_type(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="nev")
            _accept(trace, "cwt:em:0000")
            result = await run_lrg_bgs_path(trace, branch_id="main",
                                            hypothesis_ref="h1", output_root=root / "out")
            self.assertEqual(result["path_status"], "transfer")
            self.assertEqual(result["qso_entry"]["candidate_type"], "Type 2 QSO")
            self.assertEqual(trace["branches"]["main"]["state"]["registry"]
                             ["hypotheses"]["h1"]["classification"], "LRG/BGS")
            handoff_event = result["handoff_event"]
            fork_branch(trace, parent_branch_id="main", fork_event_id=handoff_event["event_id"],
                        branch_id="recheck", purpose="replay LRG/BGS transfer")
            child = run_qso_entry(trace, branch_id="recheck", hypothesis_ref="h1",
                                  output_root=root / "out",
                                  handoff_ref=handoff_event["payload"]["route_ref"])
            self.assertEqual(child["candidate_type"], "Type 2 QSO")
            write_trace(trace, root / "out/tree.json")

    async def test_changed_source_and_duplicate_node_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root)
            changed = copy.deepcopy(trace)
            changed["artifacts"]["spectrum_npz"]["sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "changed"):
                await run_lrg_bgs_path(changed, branch_id="main",
                                       hypothesis_ref="h1", output_root=root / "other")
            await run_lrg_bgs_path(trace, branch_id="main",
                                   hypothesis_ref="h1", output_root=root / "out")
            with self.assertRaisesRegex(ValueError, "already active"):
                await run_lrg_bgs_path(trace, branch_id="main",
                                       hypothesis_ref="h1", output_root=root / "out")


class LRGBGSHandoffReportTests(unittest.IsolatedAsyncioTestCase):
    async def test_qso_report_from_lrg_bgs_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="nev")
            _accept(trace, "cwt:em:0000")
            model = _Q11Model()
            result = await run_lrg_bgs_path_through_report(
                trace, branch_id="main", hypothesis_ref="h1", output_root=root / "out",
                llm=model)
            self.assertEqual(result["qso_report"]["node"]["output"]
                             ["candidate_type"], "Type 2 QSO")
            self.assertEqual(model.calls, 1)
            write_trace(trace, root / "out/tree.json")


class CaSamplingContractTests(unittest.TestCase):
    def test_ca_absorption_width_is_explicit_fwhm_proxy(self):
        window = {"samples": [
            {"sample_id": 1, "wavelength_angstrom": 3967., "flux": 1., "valid": True},
            {"sample_id": 2, "wavelength_angstrom": 3969., "flux": 0.5, "valid": True},
            {"sample_id": 3, "wavelength_angstrom": 3971., "flux": 1., "valid": True}]}
        answer = {"left_sample_id": 1, "trough_sample_id": 2,
                  "right_sample_id": 3, "reason": "Resolved local absorption trough"}
        sample = _absorption_sample(answer, window, 3969., 15., edge_sigma=3.)
        self.assertEqual(sample["absorption_depth_proxy"], 0.5)
        self.assertEqual(sample["outer_reference_span_angstrom"], 4.)
        self.assertEqual(sample["outer_reference_sigma_assumption"], 3.)
        self.assertAlmostEqual(sample["fwhm_proxy_angstrom"], 4 * SIGMA_TO_FWHM / 6)
        self.assertAlmostEqual(sample["fwhm_proxy_km_s"],
                               sample["fwhm_proxy_angstrom"] / 3969 * SPEED_OF_LIGHT_KMS)

    def test_rejects_masked_or_non_trough_pixel_ids(self):
        window = {"samples": [
            {"sample_id": 1, "wavelength_angstrom": 3968., "flux": 1., "valid": True},
            {"sample_id": 2, "wavelength_angstrom": 3969., "flux": 0.5, "valid": False},
            {"sample_id": 3, "wavelength_angstrom": 3970., "flux": 1., "valid": True}]}
        answer = {"left_sample_id": 1, "trough_sample_id": 2,
                  "right_sample_id": 3, "reason": "Candidate trough at expected position"}
        with self.assertRaisesRegex(ValueError, "masked"):
            _absorption_sample(answer, window, 3969., 15.)
        window["samples"][1]["valid"] = True
        window["samples"][1]["flux"] = 1.
        with self.assertRaisesRegex(ValueError, "does not show"):
            _absorption_sample(answer, window, 3969., 15.)
