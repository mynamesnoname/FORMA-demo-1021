"""Deterministic HS consolidation and immutable type-stage integration."""

from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path

from FORMA.agentic_graph.hs_merge import (_LINES, _claim, _pool, _resolve, _score_better,
                                          collect_hypothesis, merge_hypotheses)
from FORMA.agentic_graph.lrg_bgs_path import run_lrg_bgs_path
from FORMA.agentic_graph.reasoning_trace import record_analysis, record_fa_vote

from test_lrg_bgs_path import _fixture_lrg


def claim(ref: str, line_id: str, feature_id: str, wavelength: float,
          *, status: str = "non_tbd", source: str = "CWT",
          fa_state: str = "signal_present") -> dict:
    line = _LINES[line_id]
    return {"hypothesis_ref": ref, "line_id": line_id,
            "feature_id": feature_id, "wavelength_angstrom": wavelength,
            "rest_wavelength_angstrom": line.rest_wavelength,
            "line_kind": line.line_type, "ionization_ev": line.ionization_ev,
            "measurement_source": source, "fa_state": fa_state,
            "assignment_status": status, "source_refs": []}


def record(ref: str, type_: str, z: float, *claims: dict) -> dict:
    return {"hypothesis_ref": ref, "candidate_type": type_,
            "original_redshift": z, "claims": list(claims), "source_refs": []}


class HSMergeTests(unittest.TestCase):
    def test_new_targeted_candidate_does_not_inherit_original_fa_verdict(self):
        row = {"line_id": "line:civ-1549", "measurement_id": "cwt:em:0002",
               "fa_state": "signal_absent"}
        targeted = _claim("H2", row, {"feature_id": "targeted:H2:civ",
                                       "center_angstrom": 6073.6,
                                       "source": "LLM_SELECTED"},
                          status="llm_selected", source_ref="qso/q8")
        self.assertIsNone(targeted["fa_state"])
        self.assertEqual(targeted["fa_review_status"], "not_reviewed")
        self.assertEqual(targeted["prior_measurement_id"], "cwt:em:0002")
        self.assertEqual(targeted["prior_measurement_fa_state"], "signal_absent")
        pooled = _pool([record("H2", "Type 1 QSO", 2.92, targeted)])[0]
        self.assertEqual(pooled["provenance"][0]["fa_review_status"], "not_reviewed")
        self.assertIsNone(pooled["provenance"][0]["fa_state"])
        original = _claim("H2", row, {"feature_id": "cwt:em:0002",
                                       "center_angstrom": 6072., "source": "CWT"},
                          status="non_tbd", source_ref="sh/H2/judgments")
        self.assertEqual(original["fa_state"], "signal_absent")
        self.assertEqual(original["fa_review_status"], "original_measurement")

    def test_transitive_group_and_closest_redshift_first(self):
        oii = "line:oii-3727"
        oiii = "line:oiii-4960"
        rows = [record("h1", "ELG", .010,
                       claim("h1", oii, "cwt:1", 3764.27)),
                record("h2", "ELG", .011,
                       claim("h2", oii, "cwt:1", 3764.27),
                       claim("h2", oiii, "cwt:2", 5009.903)),
                record("h3", "ELG", .015,
                       claim("h3", oiii, "cwt:2", 5009.903)),
                record("h4", "Type 2 QSO", .011,
                       claim("h4", "line:nev-3426", "cwt:1", 3764.27))]
        output = merge_hypotheses(rows)
        self.assertEqual(len(output["groups"]), 2)
        group = next(item for item in output["groups"] if item["candidate_type"] == "ELG")
        self.assertEqual(group["member_hypotheses"], ["h1", "h2", "h3"])
        self.assertEqual(group["merge_steps"][0]["left_members"], ["h1"])
        self.assertEqual(group["merge_steps"][0]["right_members"], ["h2"])
        self.assertEqual(len(group["shared_key_edges"]), 2)
        self.assertEqual(group["merge_status"], "merged")
        self.assertEqual(group["resolution"]["retained_line_count"], 2)

    def test_hypothesis_scoped_fit_is_not_a_cross_hypothesis_key(self):
        line = "line:oii-3727"
        rows = [record("h1", "ELG", 0., claim("h1", line, "fit:h1:0", 3727.,
                                              source="Gaussian")),
                record("h2", "ELG", 0., claim("h2", line, "fit:h2:0", 3727.,
                                              source="Gaussian"))]
        self.assertEqual(len(merge_hypotheses(rows)["groups"]), 2)

    def test_inversion_discards_confirmed_pair_with_recorded_reason(self):
        a, b = "line:oii-3727", "line:oiii-4960"
        shared = claim("h1", a, "cwt:key", 4000.)
        rows = [record("h1", "ELG", .073, shared,
                       claim("h1", a, "cwt:inverted", 4300.)),
                record("h2", "ELG", .074,
                       claim("h2", a, "cwt:key", 4000.),
                       claim("h2", b, "cwt:b", 4200.))]
        group = merge_hypotheses(rows)["groups"][0]
        selected = {(item["line_id"], item["feature_id"])
                    for item in group["resolution"]["selected_pairs"]}
        self.assertIn((a, "cwt:key"), selected)
        self.assertIn((b, "cwt:b"), selected)
        self.assertNotIn((a, "cwt:inverted"), selected)
        excluded = group["resolution"]["excluded_pairs"]
        self.assertTrue(next(item for item in excluded if item["feature_id"] == "cwt:inverted")
                        ["had_fa_confirmation"])

    def test_l1_tie_uses_squared_error_then_stable_id(self):
        concentrated = (2, .2, .04, (("a", "f1"), ("b", "f2")))
        balanced = (2, .1 + .1, .01 + .01, (("a", "f2"), ("b", "f1")))
        self.assertTrue(_score_better(balanced, concentrated))
        self.assertFalse(_score_better(concentrated, balanced))
        self.assertTrue(_score_better((2, .2, .02, (("a", "f0"),)), balanced))

    def test_anchor_lowest_ionization_and_absorption_order(self):
        lya, mgii = "line:lya-1216", "line:mgii-2800"
        rows = [record("h1", "Type 1 QSO", 1.,
                       claim("h1", lya, "cwt:lya", _LINES[lya].rest_wavelength * 2),
                       claim("h1", mgii, "cwt:mgii", _LINES[mgii].rest_wavelength * 2)),
                record("h2", "Type 1 QSO", 1.01,
                       claim("h2", lya, "cwt:lya", _LINES[lya].rest_wavelength * 2))]
        group = merge_hypotheses(rows)["groups"][0]
        self.assertEqual(group["resolution"]["anchor_source"]["line_id"], lya)
        self.assertEqual(group["merged_anchor_redshift"], 1.)
        k, h = "line:cak-3934-abs", "line:cah-3969-abs"
        lrg = [record("h1", "LRG/BGS", .1,
                      claim("h1", k, "cwt:k", _LINES[k].rest_wavelength * 1.1),
                      claim("h1", h, "cwt:h", _LINES[h].rest_wavelength * 1.1)),
               record("h2", "LRG/BGS", .11,
                      claim("h2", k, "cwt:k", _LINES[k].rest_wavelength * 1.1))]
        ca = merge_hypotheses(lrg)["groups"][0]
        self.assertEqual(ca["resolution"]["anchor_source"]["line_id"], k)

    def test_all_tbd_uses_original_redshift_fallback(self):
        line = "line:oii-3727"
        rows = [record("h1", "ELG", .01,
                       claim("h1", line, "cwt:1", 3764.27, status="tbd")),
                record("h2", "ELG", .02,
                       claim("h2", line, "cwt:1", 3764.27, status="tbd"))]
        group = merge_hypotheses(rows)["groups"][0]
        self.assertEqual(group["member_hypotheses"], ["h1", "h2"])
        result = group["resolution"]
        self.assertEqual(result["anchor_source"]["kind"], "original_redshift_fallback")
        self.assertEqual(result["merged_anchor_redshift"], .01)

    def test_exact_pair_provenance_sets_final_status(self):
        line = "line:oii-3727"
        original = claim("h1", line, "cwt:1", 3727., status="non_tbd")
        other = claim("h2", line, "cwt:1", 3727., status="tbd")
        pool = _pool([record("h1", "ELG", 0., original),
                      record("h2", "ELG", 0., other)])
        self.assertEqual(pool[0]["best_assignment_status"], "non_tbd")
        self.assertEqual(len(pool[0]["provenance"]), 2)

    def test_fa_confirmed_feature_wins_line_conflict_before_global_fit(self):
        line = "line:oii-3727"
        rest = _LINES[line].rest_wavelength
        rows = [record("h1", "ELG", 0.,
                       claim("h1", line, "cwt:confirmed", rest * 1.03)),
                record("h2", "ELG", 0.,
                       claim("h2", line, "fit:h2:pending", rest,
                             status="tbd", source="Gaussian", fa_state="pending"))]
        result = _resolve(rows, [])
        self.assertEqual(result["selected_pairs"][0]["feature_id"], "cwt:confirmed")
        self.assertEqual(result["merge_tbd_line_ids"], [])
        self.assertEqual(result["fa_resolved_line_ids"], [line])
        self.assertEqual(result["excluded_pairs"][0]["reason"],
                         "fa_confirmed_alternative_for_line")

    def test_lost_type2_key_requires_type_recheck(self):
        nev, oii = "line:nev-3426", "line:oii-3727"
        observed = _LINES[oii].rest_wavelength * 1.2
        rows = [record(ref, "Type 2 QSO", .2,
                       claim(ref, nev, "cwt:shared", observed, status="tbd"),
                       claim(ref, oii, "cwt:shared", observed, status="tbd"))
                for ref in ("h1", "h2")]
        group = merge_hypotheses(rows)["groups"][0]
        self.assertEqual(group["merge_status"], "type_recheck_required")
        self.assertEqual(group["resolution"]["lost_shared_key_pairs"],
                         [{"line_id": nev, "feature_id": "cwt:shared"}])
        self.assertEqual(group["resolution"]["lost_type_support_line_ids"], [nev])

    def test_real_trace_collection_keeps_original_redshifts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            trace = _fixture_lrg(root, mode="two")
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref="h2", artifact_refs=["sh/h2/node"])
            for feature in trace["branches"]["main"]["state"]["registry"]["features"]:
                for seat in range(3):
                    record_fa_vote(trace, "main", feature,
                                   vote_id=f"{feature}:{seat}", reviewer_id=f"r{seat}",
                                   answer="yes", origin="model")
            outcome = asyncio.run(run_lrg_bgs_path(
                trace, branch_id="main", hypothesis_ref="h1",
                output_root=root / "out"))
            self.assertEqual(outcome["path_status"], "survive")
            imported = collect_hypothesis(trace, "main", "h1", "LRG/BGS", [])
            self.assertEqual(imported["original_redshift"], 0.)
            self.assertTrue(any(item["line_id"] == "line:cak-3934-abs"
                                for item in imported["claims"]))
            self.assertEqual(trace["branches"]["main"]["state"]["registry"]
                             ["hypotheses"]["h1"]["redshift"], 0.)
            with self.assertRaises(ValueError):
                collect_hypothesis(trace, "main", "h1", "ELG", [])


if __name__ == "__main__":
    unittest.main()
