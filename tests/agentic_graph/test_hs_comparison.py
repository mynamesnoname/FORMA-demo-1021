"""HS compares groups rather than counting raw hypotheses."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from langchain_core.messages import AIMessage

from FORMA.agentic_graph.hs_comparison import (_apply_cross_merge, _sole_group_decision,
                                              model_facing_dossier, render_report,
                                              observed_feature_competitions,
                                              run_hs_comparison, validate_decision,
                                              validate_merge_answer)
from FORMA.agentic_graph.feature_registry import _artifact
from FORMA.agentic_graph.hs_merge import _LINES
from FORMA.agentic_graph.reasoning_trace import TRACE_SCHEMA


def _context() -> dict:
    groups = []
    for index in (1, 2):
        groups.append({"group_id": f"g{index}", "candidate_type": "ELG",
                       "member_hypotheses": [f"h{index}"],
                       "original_redshifts": {f"h{index}": index / 10},
                       "merged_anchor_redshift": index / 10,
                       "merge_status": "singleton", "comparison_status": "merged",
                       "type_recheck_required": False,
                       "selected_pairs": [{"line_id": "line:oii-3727",
                                           "feature_id": f"cwt:{index}",
                                           "wavelength_angstrom": 4000 + index,
                                           "assignment_status": "non_tbd",
                                           "provenance": [{"hypothesis_ref": f"h{index}",
                                                           "fa_state": "signal_present",
                                                           "assignment_status": "non_tbd"}]}],
                       "excluded_pairs": [], "lost_shared_key_pairs": [],
                       "lost_type_support_line_ids": [], "source_reports": []})
    return {"schema_version": "forma-hs-group-comparison-v3", "run_id": "r",
            "branch_id": "main", "merge_ref": "hs/merge", "source_refs": [],
            "groups": groups}


def _decision(winner="g1") -> dict:
    return {"winner_group_id": winner, "reason": "One supported interpretation is preferable.",
            "assessments": [{"group_id": f"g{index}",
                             "support_pairs": [{"line_id": "line:oii-3727",
                                                "feature_id": f"cwt:{index}"}],
                             "conflict_pairs": [], "unresolved": [],
                             "comparative_evidence": {"advantages": ["Confirmed feature."],
                                                      "disadvantages": [], "limitations": []},
                             "comparison_note": "Working pairing; independent identity remains to audit."}
                            for index in (1, 2)]}


class _Model:
    def __init__(self, result):
        self.result = result
        self.calls = 0

    async def ainvoke(self, messages):
        self.calls += 1
        assert "g1" in messages[1].content and "g2" in messages[1].content
        if "Considering all groups in the dossier" in messages[-1].content:
            proposal = self.result.get("merge_proposals", [])
            return AIMessage(content=json.dumps({
                "proposals": proposal,
                "reason": "Reviewed all groups."}))
        return AIMessage(content=json.dumps({key: value for key, value in self.result.items()
                                             if key != "merge_proposals"}))


class _RepairModel(_Model):
    async def ainvoke(self, messages):
        self.calls += 1
        if "Considering all groups in the dossier" in messages[-1].content:
            return AIMessage(content=json.dumps({"proposals": [],
                                                 "reason": "No supported duplicate."}))
        result = _decision()
        if self.calls == 2:
            result["assessments"][0]["unresolved"] = "one uncertainty"
        else:
            assert "unresolved must be an array" in messages[-1].content
        return AIMessage(content=json.dumps(result))


class HSComparisonTests(unittest.IsolatedAsyncioTestCase):
    def test_multiple_merge_proposals_validate_without_candidate_list(self):
        groups = [{"group_id": f"g{index}"} for index in range(1, 5)]
        answer = {"proposals": [
            {"group_ids": ["g1", "g2"], "reason": "Shared line structure."},
            {"group_ids": ["g3", "g4"], "reason": "Another shared structure."}],
            "reason": "Two separate pairs."}
        self.assertEqual(validate_merge_answer(answer, groups), answer)
        repeated = json.loads(json.dumps(answer))
        repeated["proposals"][1]["group_ids"] = ["g2", "g1"]
        with self.assertRaisesRegex(ValueError, "repeats"):
            validate_merge_answer(repeated, groups)

    async def test_two_disjoint_merges_are_applied_before_final_comparison(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = {"schema_version": TRACE_SCHEMA, "run_id": "r",
                     "artifact_root": str(root), "artifacts": {}, "executions": {},
                     "branches": {"main": {"branch_id": "main", "parent_branch_id": None,
                                           "fork_event_id": None, "events": [],
                                           "state": {"analysis_results": ["hs.merge_groups"]}}}}
            frozen = _context()
            for index in (3, 4):
                group = json.loads(json.dumps(frozen["groups"][index - 3]))
                group["group_id"] = f"g{index}"
                group["member_hypotheses"] = [f"h{index}"]
                group["selected_pairs"][0]["feature_id"] = f"cwt:{index}"
                frozen["groups"].append(group)

            def apply(_trace, _branch, active, proposal, _routes):
                left_id, right_id = proposal["group_ids"]
                by_id = {group["group_id"]: group for group in active["groups"]}
                left = by_id[left_id]
                combined_id = left_id + "+" + right_id
                combined = {**left, "group_id": combined_id,
                            "member_hypotheses": (left["member_hypotheses"]
                                                  + by_id[right_id]["member_hypotheses"])}
                remaining = [group for group in active["groups"]
                             if group["group_id"] not in (left_id, right_id)]
                return ({**active, "groups": remaining + [combined]},
                        {"result_group_id": combined_id, "fit_matches": [],
                         "unresolved_identity_competitions": []})

            class BatchModel:
                calls = 0

                async def ainvoke(self, messages):
                    self.calls += 1
                    if "Considering all groups in the dossier" in messages[-1].content:
                        return AIMessage(content=json.dumps({
                            "proposals": [{"group_ids": ["g1", "g2"], "reason": "First."},
                                          {"group_ids": ["g3", "g4"], "reason": "Second."}],
                            "reason": "Two duplicate pairs."}))
                    assessments = []
                    for group_id, feature_id in (("g1+g2", "cwt:1"), ("g3+g4", "cwt:3")):
                        assessments.append({
                            "group_id": group_id,
                            "support_pairs": [{"line_id": "line:oii-3727",
                                               "feature_id": feature_id}],
                            "conflict_pairs": [], "unresolved": [],
                            "comparative_evidence": {"advantages": ["Observed signal."],
                                                     "disadvantages": [], "limitations": []},
                            "comparison_note": "Working interpretation."})
                    return AIMessage(content=json.dumps({"winner_group_id": "g1+g2",
                                                         "reason": "First group preferred.",
                                                         "assessments": assessments}))

            model = BatchModel()
            with patch("FORMA.agentic_graph.hs_comparison.build_comparison_context",
                       return_value=frozen), patch(
                           "FORMA.agentic_graph.hs_comparison._apply_cross_merge",
                           side_effect=apply):
                result = await run_hs_comparison(
                    trace, branch_id="main", hs={}, routes={}, output_root=root, llm=model)
            self.assertEqual(model.calls, 2)
            self.assertEqual([item["status"] for item in
                              result["node"]["output"]["cross_merges"]],
                             ["accepted", "accepted"])
            self.assertEqual({group["group_id"] for group in result["effective_groups"]},
                             {"g1+g2", "g3+g4"})

    async def test_cross_merge_of_compatible_local_fits_preserves_both_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lines = ("line:oii-3727", "line:oiii-5008")
            groups, records, artifacts = [], {}, {}
            for index, ref in enumerate(("h1", "h2"), start=1):
                # Redrock starting points may differ beyond fit-centre errors
                # while both local fits describe the same observed structures.
                z = .1068 + (index - 1) * .0132
                selected, claims, measurements = [], [], []
                for seat, line_id in enumerate(lines):
                    fid = f"fit:{ref}:{seat}"
                    center = _LINES[line_id].rest_wavelength * 1.1068
                    fit = {"center": center, "center_err": .001,
                           "amplitude": 2. if index == 1 else 5., "amplitude_err": .001,
                           "fwhm": 10., "target_line": line_id, "kind": "emission"}
                    measurements.append({"id": fid, "adoptable": True,
                                         "source": "fit_doublet", "record": fit})
                    selected.append({"line_id": line_id, "feature_id": fid,
                                     "wavelength_angstrom": center,
                                     "assignment_status": "non_tbd",
                                     "provenance": [{"hypothesis_ref": ref,
                                                     "assignment_status": "non_tbd",
                                                     "fa_state": "signal_present"}]})
                    claims.append({"hypothesis_ref": ref, "line_id": line_id,
                                   "feature_id": fid, "wavelength_angstrom": center,
                                   "rest_wavelength_angstrom": _LINES[line_id].rest_wavelength,
                                   "line_kind": "emission",
                                   "ionization_ev": _LINES[line_id].ionization_ev,
                                   "measurement_source": "fit_doublet",
                                   "fa_state": "signal_present", "assignment_status": "non_tbd",
                                   "source_refs": []})
                catalog = root / f"{ref}.json"
                catalog.write_text(json.dumps({"measurements": measurements}))
                artifacts[f"sh/{ref}/catalog"] = _artifact(catalog, "vi_catalog")
                records[ref] = {"hypothesis_ref": ref, "candidate_type": "ELG",
                                "original_redshift": z, "claims": claims,
                                "source_refs": []}
                groups.append({"group_id": f"g{index}", "candidate_type": "ELG",
                               "member_hypotheses": [ref], "original_redshifts": {ref: z},
                               "merged_anchor_redshift": z, "merge_status": "singleton",
                               "comparison_status": "merged", "type_recheck_required": False,
                               "selected_pairs": selected, "excluded_pairs": [],
                               "lost_shared_key_pairs": [], "lost_type_support_line_ids": [],
                               "advisory_reviews": [], "source_reports": []})
            context = {"groups": groups, "source_refs": [], "run_id": "r", "branch_id": "main"}
            trace = {"artifacts": artifacts}
            routes = {ref: {"report_ref": None} for ref in records}
            with patch("FORMA.agentic_graph.hs_comparison.collect_hypothesis",
                       side_effect=lambda trace, branch, ref, type_, reports: records[ref]):
                effective, accepted = _apply_cross_merge(
                    trace, "main", context,
                    {"group_ids": ["g1", "g2"], "reason": "two diagnostic fit structures agree"},
                    routes)
                self.assertEqual(accepted["result_group_id"], "hs.cross/h1+h2")
                self.assertEqual(len(accepted["fit_matches"]), 2)
                self.assertEqual(accepted["fit_matches"][0]["center_separation_angstrom"], 0)
                self.assertEqual(accepted["fit_matches"][0]["left_fit"]["amplitude"], 2.)
                self.assertEqual(accepted["fit_matches"][0]["right_fit"]["amplitude"], 5.)
                self.assertEqual(effective["groups"][0]["member_hypotheses"], ["h1", "h2"])
                self.assertEqual(len(effective["groups"][0]["excluded_pairs"]), 2)
                # Nearby redshifts alone cannot merge disjoint fitted regions.
                catalog_path = root / "h2.json"
                catalog_data = json.loads(catalog_path.read_text())
                for measurement in catalog_data["measurements"]:
                    measurement["record"]["center"] += 100
                catalog_path.write_text(json.dumps(catalog_data))
                trace["artifacts"]["sh/h2/catalog"] = _artifact(catalog_path, "vi_catalog")
                with self.assertRaisesRegex(ValueError, "two FA-confirmed"):
                    _apply_cross_merge(trace, "main", context,
                                       {"group_ids": ["g1", "g2"], "reason": "close redshifts"},
                                       routes)
                for measurement in catalog_data["measurements"]:
                    measurement["record"]["center"] -= 100
                catalog_path.write_text(json.dumps(catalog_data))
                trace["artifacts"]["sh/h2/catalog"] = _artifact(catalog_path, "vi_catalog")
                catalog_data["measurements"][0]["record"]["amplitude"] *= -1
                catalog_path.write_text(json.dumps(catalog_data))
                trace["artifacts"]["sh/h2/catalog"] = _artifact(catalog_path, "vi_catalog")
                with self.assertRaisesRegex(ValueError, "two FA-confirmed"):
                    _apply_cross_merge(trace, "main", context,
                                       {"group_ids": ["g1", "g2"], "reason": "opposite line sign"},
                                       routes)
                catalog_data["measurements"][0]["record"]["amplitude"] *= -1
                catalog_path.write_text(json.dumps(catalog_data))
                trace["artifacts"]["sh/h2/catalog"] = _artifact(catalog_path, "vi_catalog")
                # Exact run-wide feature identity still forbids conflicting lines.
                conflicting = json.loads(json.dumps(context))
                conflicting["groups"][0]["selected_pairs"].append({
                    "line_id": "line:oii-3727", "feature_id": "cwt:em:0000"})
                conflicting["groups"][1]["selected_pairs"].append({
                    "line_id": "line:oiii-5008", "feature_id": "cwt:em:0000"})
                with self.assertRaisesRegex(ValueError, "conflicting diagnostic CWT"):
                    _apply_cross_merge(trace, "main", conflicting,
                                       {"group_ids": ["g1", "g2"], "reason": "bad identity"},
                                       routes)
                # One shared observation with different non-diagnostic names
                # remains visible as unresolved, without a forced line choice.
                non_diagnostic = json.loads(json.dumps(context))
                for index, line_id in enumerate(("line:nad-5895-abs", "line:nad1-5891-abs")):
                    ref = f"h{index + 1}"
                    non_diagnostic["groups"][index]["selected_pairs"].append({
                        "line_id": line_id, "feature_id": "cwt:abs:0000"})
                    records[ref]["claims"].append({
                        "hypothesis_ref": ref, "line_id": line_id,
                        "feature_id": "cwt:abs:0000", "wavelength_angstrom": 6800.,
                        "rest_wavelength_angstrom": _LINES[line_id].rest_wavelength,
                        "line_kind": "absorption", "ionization_ev": None,
                        "measurement_source": "CWT", "fa_state": "signal_present",
                        "assignment_status": "non_tbd", "source_refs": []})
                effective, accepted = _apply_cross_merge(
                    trace, "main", non_diagnostic,
                    {"group_ids": ["g1", "g2"], "reason": "same ELG structures; Na D unresolved"},
                    routes)
                self.assertEqual(accepted["unresolved_identity_competitions"][0][
                    "feature_id"], "cwt:abs:0000")
                self.assertEqual(len(accepted["unresolved_identity_competitions"][0][
                    "candidate_line_ids"]), 2)
                self.assertNotIn("cwt:abs:0000", {pair["feature_id"] for pair in
                                                 effective["groups"][0]["selected_pairs"]})
                decision = _sole_group_decision(effective["groups"])
                self.assertEqual(decision["winner_group_id"], "hs.cross/h1+h2")
                self.assertIn("cwt:abs:0000", render_report(decision, effective))
                self.assertIn("cwt:abs:0000", model_facing_dossier(effective))
                for ref in ("h1", "h2"):
                    records[ref]["claims"].pop()
                broken = json.loads(json.dumps(context))
                broken["groups"][1]["selected_pairs"].pop()
                with self.assertRaisesRegex(ValueError, "two FA-confirmed"):
                    _apply_cross_merge(trace, "main", broken,
                                       {"group_ids": ["g1", "g2"], "reason": "insufficient"},
                                       routes)
                trace.update({"schema_version": TRACE_SCHEMA, "run_id": "r",
                              "artifact_root": str(root), "executions": {},
                              "branches": {"main": {"branch_id": "main",
                                                     "parent_branch_id": None,
                                                     "fork_event_id": None, "events": [],
                                                     "state": {"analysis_results":
                                                               ["hs.merge_groups"]}}}})
                proposal = {"winner_group_id": None, "reason": "Duplicate diagnostic fits.",
                            "assessments": [{"group_id": group["group_id"],
                                             "support_pairs": [{"line_id": row["line_id"],
                                                                "feature_id": row["feature_id"]}
                                                               for row in group["selected_pairs"]],
                                             "conflict_pairs": [], "unresolved": [],
                                             "comparative_evidence": {
                                                 "advantages": ["Two matched diagnostic structures."],
                                                 "disadvantages": [], "limitations": []},
                                             "comparison_note": "Possible duplicate."}
                                            for group in groups],
                            "merge_proposals": [{"group_ids": ["g1", "g2"],
                                                 "reason": "[O II] and [O III]b local fits agree"}]}
                with patch("FORMA.agentic_graph.hs_comparison.build_comparison_context",
                           return_value=context):
                    result = await run_hs_comparison(
                        trace, branch_id="main", hs={}, routes=routes,
                        output_root=root, llm=_Model(proposal))
                self.assertEqual(result["node"]["output"]["cross_merges"][0]["status"],
                                 "accepted")
                self.assertEqual(result["node"]["output"]["merge_review"]["proposals"][0]["group_ids"],
                                 ["g1", "g2"])
                self.assertEqual(result["node"]["output"]["winner_group_id"],
                                 "hs.cross/h1+h2")
                self.assertIn("effective_context", result["artifact_refs"])
                self.assertNotIn("merge_candidates", result["artifact_refs"])
                self.assertEqual(result["effective_groups"][0]["member_hypotheses"],
                                 ["h1", "h2"])
                session = Path(trace["artifacts"][result["artifact_refs"]["merge_session"]]["path"])
                prompt_record = session.read_text()
                self.assertIn("Considering all groups in the dossier", prompt_record)
                self.assertNotIn("PREVALIDATED_MERGE_CANDIDATES", prompt_record)
                self.assertIn("Input message 2", prompt_record)
                second_trace = {"schema_version": TRACE_SCHEMA, "run_id": "r",
                                "artifact_root": str(root), "artifacts": dict(artifacts),
                                "executions": {},
                                "branches": {"main": {"branch_id": "main",
                                                      "parent_branch_id": None,
                                                      "fork_event_id": None, "events": [],
                                                      "state": {"analysis_results":
                                                                ["hs.merge_groups"]}}}}
                decline_decision = _decision()
                for index, assessment in enumerate(decline_decision["assessments"], start=1):
                    assessment["support_pairs"][0]["feature_id"] = f"fit:h{index}:0"
                decline = _Model(decline_decision)
                with patch("FORMA.agentic_graph.hs_comparison.build_comparison_context",
                           return_value=context):
                    unmerged = await run_hs_comparison(
                        second_trace, branch_id="main", hs={}, routes=routes,
                        output_root=root, llm=decline)
                self.assertEqual(decline.calls, 2)
                self.assertEqual(unmerged["node"]["output"]["cross_merges"], [])
                self.assertEqual(unmerged["node"]["output"]["merge_review"]["proposals"], [])
                self.assertEqual(unmerged["node"]["output"]["winner_group_id"], "g1")
                self.assertIn("merge_session", unmerged["artifact_refs"])
                self.assertIn("session", unmerged["artifact_refs"])

    async def test_one_schema_repair_is_archived(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = {"schema_version": TRACE_SCHEMA, "run_id": "r",
                     "artifact_root": str(root), "artifacts": {}, "executions": {},
                     "branches": {"main": {"branch_id": "main", "parent_branch_id": None,
                                            "fork_event_id": None, "events": [],
                                            "state": {"analysis_results": ["hs.merge_groups"]}}}}
            model = _RepairModel(None)
            with patch("FORMA.agentic_graph.hs_comparison.build_comparison_context",
                       return_value=_context()):
                result = await run_hs_comparison(
                    trace, branch_id="main", hs={}, routes={}, output_root=root, llm=model)
            self.assertEqual(model.calls, 3)
            session = Path(trace["artifacts"][result["artifact_refs"]["session"]]["path"])
            self.assertIn("repair_prompt", session.read_text())
            self.assertEqual(result["node"]["output"]["winner_group_id"], "g1")

    def test_schema_rejects_invented_pair_and_unstable_winner(self):
        context = _context()
        choice = _decision()
        self.assertEqual(validate_decision(choice, context)["winner_group_id"], "g1")
        choice["assessments"][0]["support_pairs"][0]["feature_id"] = "invented"
        with self.assertRaisesRegex(ValueError, "absent"):
            validate_decision(choice, context)
        choice = _decision()
        context["groups"][0]["comparison_status"] = "anchor_assignment_unstable"
        with self.assertRaisesRegex(ValueError, "requiring review"):
            validate_decision(choice, context)
        self.assertIsNone(validate_decision(_decision(None), context)["winner_group_id"])

    async def test_two_group_model_session_is_archived_and_not_final(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = {"schema_version": TRACE_SCHEMA, "run_id": "r",
                     "artifact_root": str(root), "artifacts": {}, "executions": {},
                     "branches": {"main": {"branch_id": "main", "parent_branch_id": None,
                                            "fork_event_id": None, "events": [],
                                            "state": {"analysis_results": ["hs.merge_groups"]}}}}
            model = _Model(_decision())
            with patch("FORMA.agentic_graph.hs_comparison.build_comparison_context",
                       return_value=_context()):
                result = await run_hs_comparison(
                    trace, branch_id="main", hs={}, routes={}, output_root=root, llm=model)
            self.assertEqual(model.calls, 2)
            self.assertEqual(result["node"]["output"]["winner_group_id"], "g1")
            self.assertTrue(result["node"]["output"]["ra_review_pending"])
            for ref in result["artifact_refs"].values():
                self.assertIn(ref, trace["artifacts"])
            session = Path(trace["artifacts"][result["artifact_refs"]["session"]]["path"])
            session_text = session.read_text()
            self.assertIn("HS cross-comparison", session_text)
            model_dossier = session_text.split("<HS_GROUP_DOSSIER>\n", 1)[1].split(
                "\n</HS_GROUP_DOSSIER>", 1)[0]
            self.assertEqual(model_dossier.rstrip(), model_facing_dossier(_context()).rstrip())
            self.assertIn("## Group `g1` — ELG", model_dossier)
            self.assertIn("`line:oii-3727` ↔ `cwt:1`", model_dossier)
            self.assertNotIn("merge_ref", model_dossier)
            self.assertNotIn('"groups":', model_dossier)
            archived = Path(trace["artifacts"][result["artifact_refs"]["context"]]["path"])
            self.assertEqual(json.loads(archived.read_text())["source_refs"], [])
            self.assertIn("merge_ref", json.loads(archived.read_text()))
            report = Path(trace["artifacts"][result["artifact_refs"]["report"]]["path"])
            self.assertIn("provisional g1", report.read_text())
            self.assertIn("hs.compare_groups", trace["branches"]["main"]["state"]["analysis_results"])

    async def test_unrestricted_merge_proposal_rejected_by_code_then_compared(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = {"schema_version": TRACE_SCHEMA, "run_id": "r",
                     "artifact_root": str(root), "artifacts": {}, "executions": {},
                     "branches": {"main": {"branch_id": "main", "parent_branch_id": None,
                                           "fork_event_id": None, "events": [],
                                           "state": {"analysis_results": ["hs.merge_groups"]}}}}
            answer = {**_decision(), "merge_proposals": [{"group_ids": ["g1", "g2"],
                                                           "reason": "Looks duplicated."}]}
            model = _Model(answer)
            with patch("FORMA.agentic_graph.hs_comparison.build_comparison_context",
                       return_value=_context()):
                result = await run_hs_comparison(
                    trace, branch_id="main", hs={}, routes={}, output_root=root, llm=model)
            self.assertEqual(model.calls, 2)
            self.assertEqual(result["node"]["output"]["cross_merges"][0]["status"], "rejected")
            self.assertIn("two FA-confirmed", result["node"]["output"]["cross_merges"][0]["reason"])
            self.assertEqual(result["node"]["output"]["winner_group_id"], "g1")
            self.assertNotIn("effective_context", result["artifact_refs"])
            self.assertIn("session", result["artifact_refs"])

    def test_dossier_renders_advice_and_markdown_reports_as_attributed_text(self):
        context = _context()
        group = context["groups"][0]
        group["selected_pairs"][0]["provenance"] = [{
            "hypothesis_ref": "h1", "assignment_status": "non_tbd",
            "fa_state": "signal_present", "source_refs": ["fa/internal"]}]
        group["advisory_reviews"] = [{
            "hypothesis_ref": "h1", "lya_forest": {
                "node_ref": "fa/forest/node", "status": "complete", "visibility": "visible",
                "vote_summary": {"yes": 2, "no": 1}, "coverage": {"sampled": True}},
            "doublets": []}]
        group["source_reports"] = [{
            "hypothesis_ref": "h1", "source_ref": "sh2/report",
            "text": "# Earlier analysis\n\n| Line | Comment |\n|---|---|\n| O II | seen |"}]
        dossier = model_facing_dossier(context)
        self.assertIn("FA signal_present", dossier)
        self.assertIn("h1 Lyα forest (`fa/forest/node`)", dossier)
        self.assertIn("#### h1 — `sh2/report`", dossier)
        self.assertIn("> # Earlier analysis\n>\n> | Line | Comment |", dossier)
        self.assertNotIn("fa/internal", dossier)
        self.assertNotIn("\\n", dossier)

    def test_shared_cwt_competition_and_targeted_provenance_are_explicit(self):
        context = _context()
        first, second = context["groups"]
        second["candidate_type"] = "Type 1 QSO"
        second["selected_pairs"][0].update({
            "line_id": "line:mgii-2800", "feature_id": "cwt:1",
            "wavelength_angstrom": first["selected_pairs"][0]["wavelength_angstrom"]})
        first["selected_pairs"].append({
            "line_id": "line:civ-1549", "feature_id": "targeted:h1:civ",
            "wavelength_angstrom": 6073.6, "assignment_status": "llm_selected",
            "measurement_source": "LLM_SELECTED", "provenance": [{
                "hypothesis_ref": "h1", "assignment_status": "llm_selected",
                "fa_state": None, "fa_review_status": "not_reviewed",
                "prior_measurement_id": "cwt:em:0002",
                "prior_measurement_fa_state": "signal_absent"}]})
        competition = observed_feature_competitions(context["groups"])
        self.assertEqual(len(competition), 1)
        self.assertEqual(competition[0]["feature_id"], "cwt:1")
        self.assertEqual({row["line_id"] for row in competition[0]["interpretations"]},
                         {"line:oii-3727", "line:mgii-2800"})
        context["observed_feature_competitions"] = competition
        dossier = model_facing_dossier(context)
        self.assertIn("Shared observations with competing line identities", dossier)
        self.assertIn("this new candidate was not FA-reviewed", dossier)
        self.assertIn("earlier `cwt:em:0002` had FA signal_absent", dossier)
        self.assertIn("observed−predicted", dossier)
        choice = _decision()
        choice["assessments"][0]["support_pairs"] = [{
            "line_id": "line:civ-1549", "feature_id": "targeted:h1:civ"}]
        choice["assessments"][1]["support_pairs"] = [{
            "line_id": "line:mgii-2800", "feature_id": "cwt:1"}]
        choice["assessments"][0]["comparative_evidence"]["limitations"] = [
            "Targeted C IV is not independently FA-reviewed."]
        self.assertEqual(validate_decision(choice, context)["winner_group_id"], "g1")
        choice["assessments"][0]["comparative_evidence"]["limitations"] = []
        with self.assertRaisesRegex(ValueError, "unreviewed support needs a limitation"):
            validate_decision(choice, context)
        choice["assessments"][0]["comparative_evidence"]["limitations"] = [
            "Targeted C IV is not independently FA-reviewed."]
        first["selected_pairs"][1]["assignment_status"] = "non_tbd"
        with self.assertRaisesRegex(ValueError, "lacks positive observation"):
            validate_decision(choice, context)

    async def test_invalid_model_citation_does_not_commit_a_comparison_node(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = {"schema_version": TRACE_SCHEMA, "run_id": "r",
                     "artifact_root": str(root), "artifacts": {}, "executions": {},
                     "branches": {"main": {"branch_id": "main", "parent_branch_id": None,
                                            "fork_event_id": None, "events": [],
                                            "state": {"analysis_results": ["hs.merge_groups"]}}}}
            bad = _decision()
            bad["assessments"][0]["support_pairs"][0]["feature_id"] = "fabricated"
            with patch("FORMA.agentic_graph.hs_comparison.build_comparison_context",
                       return_value=_context()):
                with self.assertRaisesRegex(ValueError, "absent"):
                    await run_hs_comparison(trace, branch_id="main", hs={}, routes={},
                                            output_root=root, llm=_Model(bad))
            self.assertEqual(trace["artifacts"], {})
            self.assertEqual(trace["branches"]["main"]["state"]["analysis_results"],
                             ["hs.merge_groups"])
            sessions = list(root.rglob("session.md"))
            self.assertEqual(len(sessions), 1)
            self.assertIn("Status: `failed`", sessions[0].read_text())
