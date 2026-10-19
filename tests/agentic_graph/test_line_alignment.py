"""Report-bound alignment does not rewrite frozen SH/FA evidence."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from langchain_core.messages import AIMessage

from FORMA.agentic_graph.line_alignment import (
    active_alignment, alignment_jobs, project_aligned_claims, run_line_alignment, summarize_selections,
    validate_selection,
)
from FORMA.agentic_graph.elg_path import run_elg_path_through_report
from FORMA.agentic_graph.reasoning_trace import bind_artifact_root, write_trace

from test_elg_path import _complete_fa, _elg_fixture


def _row(line_id: str, measurement: str, center: float, kind: str = "emission") -> dict:
    return {"line_id": line_id, "measurement_id": measurement,
            "predicted_obs_angstrom": center, "line_kind": kind,
            "sh_status": "LIKELY", "fa_state": "signal_present"}


class _NullSlotModel:
    async def ainvoke(self, messages):
        payload = json.loads(messages[-1].content)
        return AIMessage(content=json.dumps({
            "slots": {slot["slot"]: None for slot in payload["slots"]},
            "reason": "No separable second peak can be defended."}))


class LineAlignmentTests(unittest.IsolatedAsyncioTestCase):
    def test_only_shared_kept_measurements_trigger_and_cah_expands_to_ca_k(self):
        view = {"lines": [
            _row("line:cak-3934-abs", "a", 3934.8, "absorption"),
            _row("line:cah-3969-abs", "b", 3969.6, "absorption"),
            _row("line:heps-3970-abs", "b", 3970.1, "absorption"),
            {**_row("line:oiii-5008", "c", 5008.2), "sh_status": "MASKED"},
        ]}
        jobs = alignment_jobs(view, "LRG/BGS")
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["tbd_line_ids"],
                         ["line:cah-3969-abs", "line:heps-3970-abs"])
        self.assertEqual([slot["line_id"] for slot in jobs[0]["slots"]],
                         ["line:cak-3934-abs", "line:cah-3969-abs"])
        self.assertTrue(jobs[0]["eligible"])

    def test_oiii_group_keeps_three_fixed_positions(self):
        view = {"lines": [
            _row("line:hbet-4862", "h", 4862.7),
            _row("line:oiii-4960", "o", 4960.3),
            _row("line:oiii-5008", "o", 5008.2),
        ]}
        job = alignment_jobs(view, "ELG")[0]
        self.assertEqual([slot["slot"] for slot in job["slots"]], ["A", "B", "C"])
        self.assertEqual([slot["line_id"] for slot in job["slots"]],
                         ["line:hbet-4862", "line:oiii-4960", "line:oiii-5008"])
        self.assertTrue(job["eligible"])

    def test_ca_two_valleys_resolve_k_and_h_region_without_splitting_h_epsilon(self):
        view = {"lines": [
            _row("line:cak-3934-abs", "k", 3934.8, "absorption"),
            _row("line:cah-3969-abs", "red", 3969.6, "absorption"),
            _row("line:heps-3970-abs", "red", 3970.1, "absorption"),
        ]}
        job = alignment_jobs(view, "LRG/BGS")[0]
        window = {"requested_window_angstrom": [3900., 4000.],
                  "samples": [{"sample_id": i, "wavelength_angstrom": x,
                               "flux": y, "valid": True}
                              for i, (x, y) in enumerate([
                                  (3932., 3.), (3935., 1.), (3938., 3.),
                                  (3967., 3.), (3970., 1.), (3973., 3.)])]}
        answer = {"reason": "Two distinct absorption valleys.",
                  "slots": {"A": {"left_sample_id": 0, "extremum_sample_id": 1,
                                   "right_sample_id": 2},
                            "B": {"left_sample_id": 3, "extremum_sample_id": 4,
                                   "right_sample_id": 5}}}
        selected = validate_selection(answer, job["slots"], window, 3.)
        ballots = [{"seat": seat, "selections": selected,
                    "vote_ref": f"alignment/ca-{seat}/vote.json"} for seat in range(3)]
        results = summarize_selections(job["slots"], ballots, 3)
        conflict = {**job, "line_results": results}
        projected = {item["line_id"]: item for item in
                     project_aligned_claims(view, [conflict])}
        self.assertEqual(projected["line:cak-3934-abs"]["status"], "resolved")
        self.assertEqual(projected["line:cah-3969-abs"]["status"], "resolved")
        self.assertNotEqual(projected["line:cak-3934-abs"]["effective_feature_id"],
                            projected["line:cah-3969-abs"]["effective_feature_id"])
        self.assertEqual(projected["line:heps-3970-abs"]["status"], "tbd")
        self.assertIsNone(projected["line:heps-3970-abs"]["effective_feature_id"])

    def test_qso_oiii_only_collision_is_non_diagnostic(self):
        view = {"lines": [_row("line:oiii-4960", "o", 4960.3),
                          _row("line:oiii-5008", "o", 5008.2)]}
        self.assertFalse(alignment_jobs(view, "QSO")[0]["eligible"])

    def test_slot_choice_and_majority_preserve_wavelength_identity(self):
        slots = [{"slot": "A", "line_id": "line:hbet-4862",
                  "predicted_obs_angstrom": 4862.7, "kind": "emission"},
                 {"slot": "B", "line_id": "line:oiii-4960",
                  "predicted_obs_angstrom": 4960.3, "kind": "emission"},
                 {"slot": "C", "line_id": "line:oiii-5008",
                  "predicted_obs_angstrom": 5008.2, "kind": "emission"}]
        window = {"requested_window_angstrom": [4800., 5050.],
                  "samples": [{"sample_id": i, "wavelength_angstrom": x,
                               "flux": y, "valid": True}
                              for i, (x, y) in enumerate([
                                  (4860., 1.), (4863., 4.), (4866., 1.),
                                  (5005., 1.), (5008., 5.), (5011., 1.)])]}
        answer = {"reason": "Two isolated peaks at A and C.",
                  "slots": {"A": {"left_sample_id": 0, "extremum_sample_id": 1,
                                   "right_sample_id": 2},
                            "B": None,
                            "C": {"left_sample_id": 3, "extremum_sample_id": 4,
                                   "right_sample_id": 5}}}
        selections = validate_selection(answer, slots, window, 3.)
        ballots = [{"seat": seat, "selections": selections,
                    "vote_ref": f"alignment/test-{seat}/vote.json"} for seat in range(3)]
        summary = summarize_selections(slots, ballots, 3)
        self.assertEqual(summary["line:hbet-4862"]["status"], "resolved")
        self.assertEqual(summary["line:oiii-4960"]["status"], "not_separately_supported")
        self.assertEqual(summary["line:oiii-5008"]["status"], "resolved")
        self.assertEqual(summary["line:oiii-5008"]["representative"]["center_angstrom"], 5008.)
        answer["slots"]["B"] = answer["slots"]["C"]
        with self.assertRaises(ValueError):
            validate_selection(answer, slots, window, 3.)

    async def test_live_shape_archives_independent_vote_sessions_and_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _elg_fixture(root, first_line="line:oiii-4960",
                                 reuse_first_measurement=True)
            _complete_fa(trace, "cwt:em:0000")
            output = root / "out"
            bind_artifact_root(trace, output)
            result = await run_line_alignment(
                trace, branch_id="main", hypothesis_ref="h1", graph="ELG",
                output_root=output, llm=_NullSlotModel())
            collision = result["node"]["output"]["collisions"][0]
            self.assertEqual(collision["status"], "tbd")
            self.assertEqual(len(collision["ballots"]), 3)
            self.assertEqual(collision["line_results"]["line:oiii-4960"]["status"],
                             "not_separately_supported")
            projected = {item["line_id"]: item for item in
                         result["node"]["output"]["aligned_claims"]}
            self.assertEqual(projected["line:oiii-4960"]["status"], "tbd")
            self.assertEqual(projected["line:oiii-4960"]["original_measurement_id"],
                             "cwt:em:0000")
            self.assertIsNone(projected["line:oiii-4960"]["effective_feature_id"])
            self.assertEqual(active_alignment(trace, "main", "h1", "ELG")[0],
                             result["artifact_ref"])
            write_trace(trace, output / "reasoning_tree.json")
            self.assertTrue((output / "reasoning_tree.json").is_file())

    async def test_elg_report_is_written_after_alignment_and_cites_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _elg_fixture(root, first_line="line:oiii-4960",
                                 reuse_first_measurement=True)
            _complete_fa(trace, "cwt:em:0000")
            output = root / "out"
            result = await run_elg_path_through_report(
                trace, branch_id="main", hypothesis_ref="h1",
                output_root=output, llm=_NullSlotModel())
            alignment_ref, _ = active_alignment(trace, "main", "h1", "ELG")
            report = result["nodes"][-1]
            self.assertEqual(report["node"]["node_type"], "elg.analysis_report")
            self.assertIn(alignment_ref, report["node"]["input_refs"])
            self.assertIn("Shared-feature alignment",
                          Path(trace["artifacts"][result["report_ref"]]["path"]).read_text())
            events = trace["branches"]["main"]["events"]
            self.assertLess(next(i for i, event in enumerate(events)
                                 if event["payload"].get("analysis_ref", "")
                                 .startswith("sh2.alignment/")),
                            next(i for i, event in enumerate(events)
                                 if event["payload"].get("analysis_ref")
                                 == "sh2.elg/h1/elg.analysis_report"))
