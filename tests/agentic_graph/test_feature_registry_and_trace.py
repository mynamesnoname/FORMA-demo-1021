"""Scoped feature identity, FA quorum, and historical branch replay."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from langchain_core.messages import AIMessage, ToolMessage

from FORMA.agentic_graph.fa_review import review_feature_reality
from FORMA.agentic_graph.feature_registry import _digest, build_feature_registry, cast_vote
from FORMA.agentic_graph.execution_artifacts import allocate_execution
from FORMA.agentic_graph.qso_entry import _save_node, run_qso_entry
from FORMA.agentic_graph.qso_report import run_qso_entry_through_report, run_qso_report
from FORMA.core.reasoning.ontology.registry import ONTOLOGY
from FORMA.agentic_graph.reasoning_trace import (
    fork_branch, new_trace, record_analysis, record_fa_vote, register_artifact,
    register_execution,
    select_branch, state_at_event, write_trace,
)
from FORMA.agentic_graph.type_entry_router import route_type_entry


def _json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n", encoding="utf-8")


def _fixture(root: Path, *, classification=None, first_line_id="line:one",
             redshift=0.2, first_fwhm_km_s=None):
    npz = root / "spectrum.npz"
    wavelength = np.arange(4200., 4520.)
    np.savez(npz, wavelength=wavelength,
             flux=np.exp(-0.5 * ((wavelength - 4242.4) / 3) ** 2)
                  + np.exp(-0.5 * ((wavelength - 4500) / 3) ** 2),
             ivar=np.ones_like(wavelength))
    cwt = {"feature_id": "cwt:em:0000", "wavelength": 4242.4}
    if first_fwhm_km_s is not None:
        cwt["FWHM_km_s"] = first_fwhm_km_s
    _json(root / "vi/cwt_features.json", {"emission": [cwt], "absorption": []})
    manifest = {"run_id": "r", "spectrum_npz_path": str(npz),
                "spectrum_npz_sha256": _digest(npz),
                "cwt_features": {"emission": [cwt], "absorption": []},
                "hypotheses": {}}
    nodes = []
    for hyp in ("h1", "h2"):
        directory = root / hyp
        fit_id = f"fit:{hyp}:0000"
        catalog = {
            "run_id": "r", "hypothesis_ref": hyp, "redshift": redshift,
            "spectrum_npz_path": str(npz), "masked_regions": [],
            "spectrum_npz_sha256": _digest(npz), "fit_attempts": [],
            "wavelength_min": 4200.0, "wavelength_max": 4520.0,
            "lines": [{"id": first_line_id, "kind": "emission",
                       "predicted_obs": 4242.4},
                      {"id": "line:two", "kind": "emission",
                       "predicted_obs": 4500.0}],
            "measurements": [
                {"id": "cwt:em:0000", "source": "CWT", "kind": "emission",
                 "adoptable": True, "record": cwt},
                {"id": fit_id, "source": "Gaussian", "kind": "emission",
                 "adoptable": True, "record": {"center": 4500.0}},
            ],
        }
        catalog_file = directory / "catalog.json"
        attempts_file = directory / "fit_attempts.json"
        _json(catalog_file, catalog)
        _json(attempts_file, [])
        manifest["hypotheses"][hyp] = {"catalog_path": str(catalog_file),
                                        "fit_attempts_path": str(attempts_file)}
        judgments = [
            {"line_id": first_line_id, "measurement_id": "cwt:em:0000", "status": "LIKELY"},
            {"line_id": "line:two", "measurement_id": fit_id, "status": "MARGINAL"},
        ]
        judgment_file = directory / "judgments.json"
        _json(judgment_file, judgments)
        files = {"measurement_catalog": catalog_file, "judgment": judgment_file}
        for name in ("csv", "report", "session_stage1", "session_stage2"):
            path = directory / (name + ".txt")
            path.write_text(name, encoding="utf-8")
            files[name] = path
        node = {"hypothesis_ref": hyp, "hypothesis_redshift": redshift,
                "classification": classification, "status": "unresolved"}
        for name, path in files.items():
            key = "judgment" if name == "judgment" else name
            node[key + "_path"] = str(path)
            node[key + "_sha256"] = _digest(path)
        node_file = directory / "node.json"
        _json(node_file, node)
        nodes.append(node_file)
    manifest_file = root / "vi/manifest.json"
    _json(manifest_file, manifest)
    return manifest_file, nodes


class RegistryAndTraceTests(unittest.TestCase):
    def test_fork_and_retry_get_unique_paths_and_tree_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root)
            trace = new_trace(build_feature_registry(manifest, nodes))
            imported = record_analysis(trace, "main", kind="sh_pre_analysis_import",
                                       analysis_ref="h1", artifact_refs=["sh/h1/node"])
            fork_branch(trace, parent_branch_id="main", fork_event_id=imported["event_id"],
                        branch_id="recheck", purpose="review again")
            logical_key = "fa.real_feature_or_not/r/fit:h1:0000"
            first = allocate_execution(root / "outputs", run_id="r", branch_id="main",
                                       node_key=logical_key)
            retry = allocate_execution(root / "outputs", run_id="r", branch_id="main",
                                       node_key=logical_key)
            child = allocate_execution(root / "outputs", run_id="r", branch_id="recheck",
                                       node_key=logical_key)
            self.assertEqual(len({first.directory, retry.directory, child.directory}), 3)
            self.assertEqual(first.node_key, child.node_key)
            self.assertNotEqual(first.node_execution_id, retry.node_execution_id)
            with self.assertRaises(FileExistsError):
                allocate_execution(root / "outputs", run_id="r", branch_id="main",
                                   node_key=logical_key,
                                   node_execution_id=first.node_execution_id,
                                   attempt_id=first.attempt_id)
            for allocation in (first, retry, child):
                register_execution(trace, allocation)
                allocation.path("node.json").write_text('{"answer":"yes"}\n')
                register_artifact(trace, f"node/{allocation.node_execution_id}",
                                  allocation.path("node.json"), "fa_node",
                                  node_execution_id=allocation.node_execution_id)
            wrong = allocate_execution(root / "outputs", run_id="r", branch_id="main",
                                       node_key="fa.real_feature_or_not/r/other")
            register_execution(trace, wrong)
            wrong.path("node.json").write_text('{"answer":"yes"}\n')
            register_artifact(trace, "wrong-node", wrong.path("node.json"), "fa_node",
                              node_execution_id=wrong.node_execution_id)
            with self.assertRaisesRegex(ValueError, "another logical node"):
                record_fa_vote(trace, "main", "fit:h1:0000", vote_id="wrong",
                               reviewer_id="wrong", answer="yes", origin="model",
                               artifact_ref="wrong-node",
                               node_execution_id=wrong.node_execution_id)
            with self.assertRaisesRegex(ValueError, "outside"):
                register_artifact(trace, "bad", nodes[0], "fa_node",
                                  node_execution_id=first.node_execution_id)
            main_vote = record_fa_vote(
                trace, "main", "fit:h1:0000", vote_id="v1", reviewer_id="a",
                answer="yes", origin="model",
                artifact_ref=f"node/{retry.node_execution_id}",
                node_execution_id=retry.node_execution_id,
            )
            record_fa_vote(trace, "recheck", "fit:h1:0000", vote_id="v2",
                           reviewer_id="b", answer="no", origin="model",
                           artifact_ref=f"node/{child.node_execution_id}",
                           node_execution_id=child.node_execution_id)
            self.assertEqual(main_vote["execution"]["attempt_id"], retry.attempt_id)
            with self.assertRaisesRegex(ValueError, "on this branch"):
                record_fa_vote(trace, "recheck", "fit:h1:0000", vote_id="v3",
                               reviewer_id="c", answer="yes", origin="model",
                               artifact_ref=f"node/{first.node_execution_id}",
                               node_execution_id=first.node_execution_id)
            path = write_trace(trace, root / "tree.json")
            exported = json.loads(path.read_text())
            self.assertEqual(len(exported["executions"]), 4)
            self.assertEqual(exported["branches"]["recheck"]["events"][0]
                             ["execution"]["branch_id"], "recheck")
            self.assertEqual(exported["artifacts"][f"node/{child.node_execution_id}"]
                             ["relative_path"],
                             f"{child.relative_dir}/node.json")

    def test_scope_and_completed_vote_without_line_identity_promotion(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest, nodes = _fixture(Path(directory))
            registry = build_feature_registry(manifest, nodes)
            self.assertEqual(len(registry["features"]), 3)
            shared = registry["features"]["cwt:em:0000"]
            self.assertEqual(shared["scope"], "run")
            self.assertEqual(shared["skyline_risk"]["status"], "no_registered_risk")
            self.assertEqual(shared["skyline_risk"]["nearest_line"]["wavelength_angstrom"],
                             4359.55)
            self.assertEqual({r["hypothesis_ref"] for r in shared["references"]}, {"h1", "h2"})
            self.assertEqual(registry["features"]["fit:h1:0000"]["scope"], "hypothesis")
            self.assertEqual(registry["features"]["fit:h2:0000"]["hypothesis_ref"], "h2")
            cast_vote(registry, "fit:h1:0000", vote_id="v1", reviewer_id="a",
                      answer="yes", origin="model")
            self.assertEqual(registry["features"]["fit:h1:0000"]["observed_signal_state"], "pending")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                cast_vote(registry, "fit:h1:0000", vote_id="v2", reviewer_id="a",
                          answer="yes", origin="model")
            cast_vote(registry, "fit:h1:0000", vote_id="v2", reviewer_id="b",
                      answer="yes", origin="model")
            cast_vote(registry, "fit:h1:0000", vote_id="v3", reviewer_id="c",
                      answer="no", origin="model")
            self.assertEqual(registry["features"]["fit:h1:0000"]["observed_signal_state"],
                             "signal_present")
            self.assertEqual(registry["features"]["fit:h1:0000"]["skyline_risk"]["status"],
                             "no_registered_risk")
            self.assertEqual(registry["features"]["fit:h1:0000"]["vote_summary"]["assurance"],
                             "contested")
            self.assertEqual(registry["features"]["fit:h2:0000"]["observed_signal_state"],
                             "pending")

    def test_fork_at_named_analysis_event_replays_only_prior_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root)
            trace = new_trace(build_feature_registry(manifest, nodes))
            h1 = record_analysis(trace, "main", kind="sh_pre_analysis_import",
                                 analysis_ref="h1", artifact_refs=["sh/h1/node"])
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h2", artifact_refs=["sh/h2/node"])
            before_vote = copy.deepcopy(trace["branches"]["main"])
            with self.assertRaisesRegex(ValueError, "not in the active run"):
                record_fa_vote(trace, "main", "unknown", vote_id="x", reviewer_id="x",
                               answer="yes", origin="model")
            record_fa_vote(trace, "main", "fit:h1:0000", vote_id="a", reviewer_id="a",
                           answer="yes", origin="model")
            fork_branch(trace, parent_branch_id="main", fork_event_id=h1["event_id"],
                        branch_id="child", purpose="recheck h1")
            with self.assertRaisesRegex(ValueError, "no active SH"):
                record_fa_vote(trace, "child", "fit:h2:0000", vote_id="x", reviewer_id="x",
                               answer="yes", origin="model")
            self.assertEqual(trace["branches"]["child"]["state"]["active_pre_analysis"], ["h1"])
            self.assertEqual(trace["branches"]["main"]["state"]["active_pre_analysis"], ["h1", "h2"])
            record_fa_vote(trace, "child", "fit:h1:0000", vote_id="b", reviewer_id="b",
                           answer="no", origin="offline_fixture")
            self.assertEqual(len(trace["branches"]["main"]["state"]["registry"]["features"]
                             ["fit:h1:0000"]["votes"]), 1)
            self.assertEqual(len(trace["branches"]["child"]["state"]["registry"]["features"]
                             ["fit:h1:0000"]["votes"]), 1)
            self.assertEqual(state_at_event(trace, "main", h1["event_id"])["active_pre_analysis"],
                             ["h1"])
            self.assertEqual(before_vote["events"][-1]["event_id"], "main:e0001")
            with self.assertRaisesRegex(ValueError, "does not belong"):
                fork_branch(trace, parent_branch_id="child", fork_event_id=h1["event_id"],
                            branch_id="bad", purpose="invalid parent event")
            with self.assertRaisesRegex(ValueError, "offline fixture"):
                select_branch(trace, "child")
            later = root / "later_result.json"
            _json(later, {"review": "follow-up"})
            register_artifact(trace, "later_result", later, "analysis_result")
            record_analysis(trace, "child", kind="analysis_result", analysis_ref="review-1",
                            artifact_refs=["later_result"])
            self.assertEqual(trace["branches"]["child"]["state"]["analysis_results"], ["review-1"])
            path = write_trace(trace, root / "trace.json")
            exported = json.loads(path.read_text())
            self.assertEqual(set(exported["branches"]), {"main", "child"})
            with self.assertRaises(FileExistsError):
                write_trace(trace, path)

    def test_rejects_incomplete_or_tampered_sh_import(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root)
            with self.assertRaisesRegex(ValueError, "incomplete"):
                build_feature_registry(manifest, nodes[:1])
            nodes[0].parent.joinpath("report.txt").write_text("changed")
            with self.assertRaisesRegex(ValueError, "changed after SH"):
                build_feature_registry(manifest, nodes)


class _FaAgent:
    def __init__(self, tools, fail: bool):
        self.tool = tools[0]
        self.fail = fail

    async def astream(self, state, *, config, stream_mode):
        if self.fail:
            raise RuntimeError("transient test failure")
        prompt = state["messages"][0].content
        assert "cwt:em:0000" not in prompt and "fit:h1:0000" not in prompt
        answer = "yes" if "4242.4" in prompt else "no"
        yield {"model": {"messages": [AIMessage(
            content="", tool_calls=[{"name": "submit_feature_reality",
                                     "args": {"answer": answer}, "id": "call"}],
            response_metadata={"token_usage": {"prompt_tokens": 10,
                                                "completion_tokens": 2,
                                                "total_tokens": 12}},
        )]}}
        result = self.tool.invoke({"answer": answer})
        yield {"tools": {"messages": [ToolMessage(
            content=json.dumps(result), tool_call_id="call",
            name="submit_feature_reality",
        )]}}


class FaReviewTests(unittest.IsolatedAsyncioTestCase):
    async def test_child_review_leaves_parent_feature_pending(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root)
            trace = new_trace(build_feature_registry(manifest, nodes))
            sh = record_analysis(trace, "main", kind="sh_pre_analysis_import",
                                 analysis_ref="h1", artifact_refs=["sh/h1/node"])
            fork_branch(trace, parent_branch_id="main", fork_event_id=sh["event_id"],
                        branch_id="recheck", purpose="independent feature review")
            summary = await review_feature_reality(
                trace=trace, branch_id="recheck", vi_manifest_path=manifest,
                output_root=root / "out", llm=object(),
                feature_ids=["fit:h1:0000"], concurrency=2,
                agent_factory=lambda **kw: _FaAgent(kw["tools"], fail=False),
            )
            self.assertEqual(summary["successful_votes"], 3)
            self.assertEqual(trace["branches"]["main"]["state"]["registry"]["features"]
                             ["fit:h1:0000"]["observed_signal_state"], "pending")
            self.assertEqual(trace["branches"]["recheck"]["state"]["registry"]["features"]
                             ["fit:h1:0000"]["observed_signal_state"], "signal_absent")
            self.assertTrue(all(item["branch_id"] == "recheck"
                                for item in trace["executions"].values()))

    async def test_exhausted_vote_seat_stays_pending_and_keeps_attempts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root)
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            summary = await review_feature_reality(
                trace=trace, branch_id="main", vi_manifest_path=manifest,
                output_root=root / "out", llm=object(),
                feature_ids=["fit:h1:0000"], concurrency=2,
                max_attempts_per_vote=2,
                agent_factory=lambda **kw: _FaAgent(kw["tools"], fail=True),
            )
            self.assertEqual(summary["successful_votes"], 0)
            self.assertEqual(len(summary["failed_seats"]), 3)
            self.assertEqual(len(trace["executions"]), 6)
            entry = trace["branches"]["main"]["state"]["registry"]["features"]["fit:h1:0000"]
            self.assertEqual(entry["votes"], [])
            self.assertEqual(entry["observed_signal_state"], "pending")
            self.assertEqual(summary["pending_features"], ["fit:h1:0000"])

    async def test_full_quorum_retry_shared_cwt_and_scoped_fit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root)
            trace = new_trace(build_feature_registry(manifest, nodes))
            for hyp in ("h1", "h2"):
                record_analysis(trace, "main", kind="sh_pre_analysis_import",
                                analysis_ref=hyp, artifact_refs=[f"sh/{hyp}/node"])
            created = 0

            def factory(*, model, tools, system_prompt):
                nonlocal created
                created += 1
                return _FaAgent(tools, fail=created == 1)

            summary = await review_feature_reality(
                trace=trace, branch_id="main", vi_manifest_path=manifest,
                output_root=root / "out", llm=object(),
                feature_ids=["cwt:em:0000", "fit:h1:0000"], concurrency=2,
                max_attempts_per_vote=2, agent_factory=factory,
            )
            self.assertEqual(summary["scheduled_vote_seats"], 6)
            self.assertEqual(summary["successful_votes"], 6)
            self.assertEqual(summary["failed_seats"], [])
            self.assertEqual(summary["model_call_count"], 6)
            self.assertEqual(summary["input_tokens"], 60)
            self.assertEqual(created, 7)
            self.assertEqual(len(trace["executions"]), 7)
            self.assertEqual(sum(e["kind"] == "fa_attempt_failed" for e in
                                 trace["branches"]["main"]["events"]), 1)
            features = trace["branches"]["main"]["state"]["registry"]["features"]
            self.assertEqual(features["cwt:em:0000"]["observed_signal_state"],
                             "signal_present")
            self.assertEqual(features["fit:h1:0000"]["observed_signal_state"],
                             "signal_absent")
            self.assertEqual(features["fit:h2:0000"]["observed_signal_state"],
                             "pending")
            self.assertEqual(len(features["cwt:em:0000"]["votes"]), 3)
            self.assertTrue((root / "out/reasoning_branches.json").is_file())
            self.assertEqual(summary["pending_features"], [])

    async def test_unusable_window_records_blocker_without_model_call(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root)
            data = json.loads(manifest.read_text())
            data["masked_regions"] = [[4200, 4520]]
            manifest.write_text(json.dumps(data))
            for node_file in nodes:
                node = json.loads(node_file.read_text())
                catalog_file = Path(node["measurement_catalog_path"])
                catalog = json.loads(catalog_file.read_text())
                catalog["masked_regions"] = data["masked_regions"]
                _json(catalog_file, catalog)
                node["measurement_catalog_sha256"] = _digest(catalog_file)
                _json(node_file, node)
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            summary = await review_feature_reality(
                trace=trace, branch_id="main", vi_manifest_path=manifest,
                output_root=root / "out", llm=object(),
                feature_ids=["cwt:em:0000"], concurrency=1,
                agent_factory=lambda **kw: self.fail("model must not be called"),
            )
            self.assertEqual(summary["blocked_features"], ["cwt:em:0000"])
            entry = trace["branches"]["main"]["state"]["registry"]["features"]["cwt:em:0000"]
            self.assertEqual(entry["observed_signal_state"], "unreviewable")
            self.assertEqual(entry["votes"], [])
            with self.assertRaisesRegex(ValueError, "blocked"):
                cast_vote(trace["branches"]["main"]["state"]["registry"],
                          "cwt:em:0000", vote_id="x", reviewer_id="x",
                          answer="yes", origin="model")

    def test_qso_null_route_is_pruned_before_qso_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root)
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            result = run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                                   output_root=root / "out")
            self.assertEqual(result["path_status"], "pruned")
            self.assertEqual([item["node"]["node_type"] for item in result["nodes"]],
                             ["sh2.initial_route"])
            self.assertEqual(result["nodes"][0]["node"]["output"]["reason"],
                             "preliminary_classification_null")
            write_trace(trace, root / "out/tree.json")

    def test_qso_nev_routes_by_branch_local_fa_votes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root, classification="Type 2 QSO",
                                       first_line_id="line:nev-3426")
            trace = new_trace(build_feature_registry(manifest, nodes))
            imported = record_analysis(trace, "main", kind="sh_pre_analysis_import",
                                       analysis_ref="h1", artifact_refs=["sh/h1/node"])
            fork_branch(trace, parent_branch_id="main", fork_event_id=imported["event_id"],
                        branch_id="rejected", purpose="alternate independent FA vote")
            for branch_id, answer in (("main", "yes"), ("rejected", "no")):
                for index in range(3):
                    record_fa_vote(trace, branch_id, "cwt:em:0000",
                                   vote_id=f"{branch_id}-{index}",
                                   reviewer_id=f"{branch_id}-{index}",
                                   answer=answer, origin="model")
            accepted = run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                                     output_root=root / "out")
            rejected = run_qso_entry(trace, branch_id="rejected", hypothesis_ref="h1",
                                     output_root=root / "out")
            self.assertEqual(accepted["path_status"], "survive")
            self.assertEqual(accepted["candidate_type"], "Type 2 QSO")
            self.assertEqual([item["node"]["node_type"] for item in accepted["nodes"]],
                             ["sh2.initial_route", "qso.entry", "qso.evidence_view",
                              "qso.nev_pairing_gate"])
            view = accepted["nodes"][2]["node"]["output"]["cleaned_line_view"]
            nev = next(line for line in view["lines"] if line["line_id"] == "line:nev-3426")
            self.assertEqual(nev["cleaned_pairing"], "adopted")
            self.assertNotIn("skyline_risk", json.dumps(view))
            self.assertEqual(rejected["path_status"], "in_progress")
            self.assertEqual(rejected["nodes"][3]["node"]["output"]["pairing_state"],
                             "rejected_measurement")
            self.assertEqual(rejected["nodes"][4]["node"]["node_type"],
                             "qso.broad_line_inventory")
            write_trace(trace, root / "out/tree.json")

    def test_qso_entry_refuses_unregistered_scientific_classification(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root, classification="ELG")
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            with self.assertRaisesRegex(ValueError, "different initial type graph"):
                run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                              output_root=root / "out")

    def test_qso_entry_preflights_sources_without_partial_route(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root, classification="Type 1 QSO")
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            catalog = Path(trace["artifacts"]["sh/h1/catalog"]["path"])
            catalog.write_text(catalog.read_text(encoding="utf-8") + " ", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "changed source artifact"):
                run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                              output_root=root / "out")
            self.assertEqual(trace["branches"]["main"]["state"]["analysis_results"], [])
            self.assertFalse((root / "out").exists())

    def test_qso_pending_nev_continues_without_type2_support(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root, classification="Type 2 QSO",
                                       first_line_id="line:nev-3426")
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            result = run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                                   output_root=root / "out")
            self.assertEqual(result["path_status"], "in_progress")
            q2 = result["nodes"][3]["node"]["output"]
            self.assertEqual(q2["pairing_state"], "pending_review")
            self.assertIsNone(q2["candidate_type"])
            self.assertEqual(result["nodes"][4]["node"]["node_type"],
                             "qso.broad_line_inventory")
            write_trace(trace, root / "out/tree.json")

    def test_qso_inventory_uses_declared_width_without_type1_survival(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mgii = next(line for line in ONTOLOGY.lines if line.id == "line:mgii-2800")
            redshift = 4242.4 / mgii.rest_wavelength - 1
            manifest, nodes = _fixture(root, classification="Type 1 QSO",
                                       first_line_id="line:mgii-2800",
                                       redshift=redshift, first_fwhm_km_s=2500.0)
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            for index in range(3):
                record_fa_vote(trace, "main", "cwt:em:0000", vote_id=f"v{index}",
                               reviewer_id=f"reviewer{index}", answer="yes", origin="model")
            result = run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                                   output_root=root / "out")
            self.assertEqual(result["path_status"], "in_progress")
            self.assertNotIn("candidate_type", result)
            inventory = result["nodes"][-1]["node"]["output"]
            target = next(row for row in inventory["lines"]
                          if row["line_id"] == "line:mgii-2800")
            self.assertEqual(target["cleaned_pairing"], "adopted")
            self.assertEqual(target["broadness"], "supported")
            self.assertEqual(target["coverage"], "needs_q5")
            write_trace(trace, root / "out/tree.json")


class _Q11Model:
    def __init__(self, *, wrong_status=False, dash_for_null=False):
        self.calls = 0
        self.wrong_status = wrong_status
        self.dash_for_null = dash_for_null

    async def ainvoke(self, messages):
        self.calls += 1
        payload = messages[-1].content.split("```json\n", 1)[1].split("\n```", 1)[0]
        context = json.loads(payload)
        terminal = context["terminal"]
        status = "dead" if self.wrong_status else terminal["path_status"]
        candidate = ("—" if self.dash_for_null and terminal["candidate_type"] is None
                     else terminal["candidate_type"] or "null")
        preliminary = context["preliminary_classification"] or "null"
        report = "\n".join([
            "### 3a. Spectrum Summary", f"Hypothesis redshift: {context['fixed_redshift']}",
            f"Hypothesis {context['hypothesis_ref']} on branch {context['branch_id']}.",
            "### 3b. Recorded Graph Outcome", f"Graph path status: {status}",
            f"Candidate type: {candidate}", f"Source {terminal['source_node_ref']}.",
            "### 3c. Per-Line Results", "[[CANONICAL_PER_LINE_TABLE]]",
            "### 3d. Key Findings and Graph Actions", "Recorded actions only.",
            "### 3e. Recorded Classification",
            f"Preliminary classification: {preliminary}",
            f"Recorded classification: {candidate}",
            "### 3f. Caveats and Open Items", "Skipped checks remain skipped.",
        ])
        return AIMessage(content=report)


class QsoReportTests(unittest.IsolatedAsyncioTestCase):
    async def test_line_only_sh_qso_report_does_not_require_old_sh_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root, classification=None,
                                       first_line_id="line:nev-3426")
            for path in nodes:
                node = json.loads(path.read_text())
                node["schema_version"] = "forma-sh-line-review-v1"
                node.pop("classification")
                path.write_text(json.dumps(node) + "\n", encoding="utf-8")
                path.with_name("report.txt").unlink()
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            for index in range(3):
                record_fa_vote(trace, "main", "cwt:em:0000", vote_id=f"v{index}",
                               reviewer_id=f"reviewer{index}", answer="yes", origin="model")
            route_type_entry(trace, branch_id="main", hypothesis_ref="h1",
                             output_root=root / "out")
            result = await run_qso_entry_through_report(
                trace, branch_id="main", hypothesis_ref="h1",
                output_root=root / "out", llm=_Q11Model())
            self.assertEqual(result["report"]["node"]["output"]["candidate_type"],
                             "Type 2 QSO")
            self.assertNotIn("sh/h1/report", result["report"]["node"]["input_refs"])

    def _q2_trace(self, root):
        manifest, nodes = _fixture(root, classification="Type 2 QSO",
                                   first_line_id="line:nev-3426")
        trace = new_trace(build_feature_registry(manifest, nodes))
        record_analysis(trace, "main", kind="sh_pre_analysis_import",
                        analysis_ref="h1", artifact_refs=["sh/h1/node"])
        for index in range(3):
            record_fa_vote(trace, "main", "cwt:em:0000", vote_id=f"v{index}",
                           reviewer_id=f"reviewer{index}", answer="yes", origin="model")
        entry = run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                              output_root=root / "out")
        self.assertEqual(entry["path_status"], "survive")
        return trace

    async def test_q11_reports_q2_without_new_decision_and_preserves_fork(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = self._q2_trace(root)
            fork_event = trace["branches"]["main"]["events"][-1]["event_id"]
            model = _Q11Model()
            main = await run_qso_report(trace, branch_id="main", hypothesis_ref="h1",
                                        output_root=root / "out", llm=model)
            self.assertEqual(main["node"]["output"]["candidate_type"], "Type 2 QSO")
            self.assertEqual(main["node"]["output"]["path_status"], "survive")
            self.assertIn("Graph path status: survive",
                          Path(main["report_path"]).read_text(encoding="utf-8"))
            self.assertEqual(model.calls, 1)
            with self.assertRaisesRegex(ValueError, "already completed"):
                await run_qso_report(trace, branch_id="main", hypothesis_ref="h1",
                                     output_root=root / "out", llm=model)
            fork_branch(trace, parent_branch_id="main", fork_event_id=fork_event,
                        branch_id="child", purpose="new report branch")
            child = await run_qso_report(trace, branch_id="child", hypothesis_ref="h1",
                                         output_root=root / "out", llm=model)
            self.assertNotEqual(main["report_path"], child["report_path"])
            self.assertEqual(model.calls, 2)
            write_trace(trace, root / "out/reasoning_branches.json")

    async def test_q2_direct_exit_dispatches_q11(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root, classification="Type 2 QSO",
                                       first_line_id="line:nev-3426")
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            for index in range(3):
                record_fa_vote(trace, "main", "cwt:em:0000", vote_id=f"v{index}",
                               reviewer_id=f"reviewer{index}", answer="yes", origin="model")
            result = await run_qso_entry_through_report(
                trace, branch_id="main", hypothesis_ref="h1",
                output_root=root / "out", llm=_Q11Model())
            self.assertEqual(result["entry"]["path_status"], "survive")
            self.assertEqual(result["report"]["node"]["node_type"], "qso.analysis_report")
            write_trace(trace, root / "out/tree.json")

    async def test_q11_rejects_changed_source_before_model_call(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = self._q2_trace(root)
            ref = next(ref for ref, item in trace["artifacts"].items()
                       if item["kind"] == "qso_node" and
                       json.loads(Path(item["path"]).read_text())["node_type"]
                       == "qso.evidence_view")
            path = Path(trace["artifacts"][ref]["path"])
            path.write_text(path.read_text(encoding="utf-8") + " ", encoding="utf-8")
            model = _Q11Model()
            with self.assertRaisesRegex(ValueError, "changed Q11 source"):
                await run_qso_report(trace, branch_id="main", hypothesis_ref="h1",
                                     output_root=root / "out", llm=model)
            self.assertEqual(model.calls, 0)

    async def test_q11_invalid_model_report_keeps_failure_session_out_of_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = self._q2_trace(root)
            model = _Q11Model(wrong_status=True)
            with self.assertRaisesRegex(ValueError, "incorrect canonical lines"):
                await run_qso_report(trace, branch_id="main", hypothesis_ref="h1",
                                     output_root=root / "out", llm=model)
            self.assertEqual(model.calls, 1)
            self.assertFalse(any("qso.analysis_report" in key for key in
                                 trace["branches"]["main"]["state"]["analysis_results"]))
            sessions = list((root / "out").rglob("session.md"))
            self.assertEqual(len(sessions), 1)
            self.assertIn("Status: `failed`", sessions[0].read_text(encoding="utf-8"))

    async def test_q11_archives_recorded_unresolved_q10_without_promoting_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root, classification="Type 1 QSO")
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            entry = run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                                  output_root=root / "out")
            q3_ref = entry["nodes"][-1]["artifact_ref"]
            q9 = _save_node(trace, "main", "h1", "qso.type1_formal_gate",
                            {"gate_status": "type1_unresolved",
                             "effective_line_states": []}, [q3_ref], root / "out")
            _save_node(trace, "main", "h1", "qso.route_result",
                       {"path_status": "unresolved", "candidate_type": None},
                       [q9["artifact_ref"]], root / "out")
            result = await run_qso_report(trace, branch_id="main", hypothesis_ref="h1",
                                          output_root=root / "out", llm=_Q11Model())
            self.assertEqual(result["node"]["output"]["path_status"], "unresolved")
            self.assertIsNone(result["node"]["output"]["candidate_type"])
            self.assertIn("Candidate type: null",
                          Path(result["report_path"]).read_text(encoding="utf-8"))
            write_trace(trace, root / "out/tree.json")

    async def test_q11_normalizes_v8_dash_only_for_authoritative_null_labels(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, nodes = _fixture(root, classification="Type 1 QSO")
            trace = new_trace(build_feature_registry(manifest, nodes))
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h1", artifact_refs=["sh/h1/node"])
            entry = run_qso_entry(trace, branch_id="main", hypothesis_ref="h1",
                                  output_root=root / "out")
            q3_ref = entry["nodes"][-1]["artifact_ref"]
            q9 = _save_node(trace, "main", "h1", "qso.type1_formal_gate",
                            {"gate_status": "type1_failed", "effective_line_states": []},
                            [q3_ref], root / "out")
            _save_node(trace, "main", "h1", "qso.route_result",
                       {"path_status": "dead", "candidate_type": None},
                       [q9["artifact_ref"]], root / "out")
            model = _Q11Model(dash_for_null=True)
            result = await run_qso_report(trace, branch_id="main", hypothesis_ref="h1",
                                          output_root=root / "out", llm=model)
            self.assertEqual(model.calls, 1)
            report = Path(result["report_path"]).read_text(encoding="utf-8")
            session = Path(result["session_path"]).read_text(encoding="utf-8")
            self.assertIn("Candidate type: null", report)
            self.assertIn("Recorded classification: null", report)
            self.assertNotIn("Candidate type: —", report)
            self.assertIn("Candidate type: —", session)
            self.assertIn("canonical_null_render", session)
            self.assertEqual(result["node"]["output"]["path_status"], "dead")


if __name__ == "__main__":
    unittest.main()
