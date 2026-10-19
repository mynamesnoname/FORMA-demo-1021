"""Coverage boundary and unknown-state checks for the Type 1 QSO gate."""

import unittest

from FORMA.agentic_graph.qso_type1_gate import (
    CIII, CIV, LYA, MGII, infer_type1_gate, select_type1_gate_lines,
)


def coverage(*in_range: str, masked: tuple[str, ...] = ()) -> dict[str, str]:
    states = {line: "outside_range" for line in (LYA, CIV, CIII, MGII)}
    states.update({line: "usable" for line in in_range})
    states.update({line: "fully_masked" for line in masked})
    return states


class Type1GateTests(unittest.TestCase):
    def test_coverage_fallback_selects_only_the_declared_lines(self):
        self.assertEqual(select_type1_gate_lines(coverage(LYA, CIV, CIII, MGII)),
                         (LYA, CIV))
        self.assertEqual(select_type1_gate_lines(coverage(CIV, CIII, MGII)),
                         (CIV, CIII))
        self.assertEqual(select_type1_gate_lines(coverage(CIII, MGII)), (CIII,))
        self.assertEqual(select_type1_gate_lines(coverage(MGII)), (MGII,))
        self.assertEqual(select_type1_gate_lines(coverage()), ())

    def test_one_fully_masked_gate_is_neutral_when_other_gate_passes(self):
        cov = coverage(CIV, CIII, MGII, masked=(LYA,))
        self.assertEqual(select_type1_gate_lines(cov), (LYA, CIV))
        result = infer_type1_gate(cov, {CIV: "paired"})
        self.assertEqual(result.status, "type1_supported")
        self.assertEqual(result.effective_line_states[0],
                         (LYA, "neutral_masked"))
        self.assertEqual(infer_type1_gate(cov, {CIV: "failed"}).status,
                         "type1_failed")

    def test_masked_single_gate_falls_through_to_next_line(self):
        cov = coverage(MGII, masked=(CIII,))
        self.assertEqual(select_type1_gate_lines(cov), (CIII, MGII))
        result = infer_type1_gate(cov, {MGII: "vote_explained"})
        self.assertEqual(result.status, "type1_supported")
        self.assertEqual(result.effective_line_states,
                         ((CIII, "neutral_masked"), (MGII, "vote_explained")))

    def test_all_masked_falls_through_but_cannot_pass_without_evidence(self):
        cov = coverage(masked=(LYA, CIV, CIII, MGII))
        self.assertEqual(select_type1_gate_lines(cov), (LYA, CIV, CIII, MGII))
        self.assertEqual(infer_type1_gate(cov, {}).status, "type1_unresolved")

    def test_partial_or_unusable_data_does_not_count_as_full_mask(self):
        partial = coverage(LYA, CIV, CIII) | {LYA: "partial"}
        self.assertEqual(select_type1_gate_lines(partial), (LYA, CIV))
        self.assertEqual(infer_type1_gate(
            partial, {LYA: "paired", CIV: "paired"}).status,
            "type1_supported")
        no_ivar = coverage(CIII, MGII) | {CIII: "no_usable_data"}
        self.assertEqual(select_type1_gate_lines(no_ivar), (CIII,))
        self.assertEqual(infer_type1_gate(no_ivar, {}).status,
                         "type1_unresolved")

    def test_vote_explanation_supports_selected_line_and_ignores_unselected(self):
        result = infer_type1_gate(coverage(CIV, CIII, MGII),
                                  {CIV: "paired", CIII: "vote_explained",
                                   MGII: "failed"})
        self.assertEqual(result.status, "type1_supported")
        self.assertEqual(result.selected_line_ids, (CIV, CIII))

    def test_failure_precedes_unknown_but_no_gate_never_passes(self):
        result = infer_type1_gate(coverage(LYA, CIV),
                                  {LYA: "failed", CIV: "unresolved"})
        self.assertEqual(result.status, "type1_failed")
        self.assertEqual(infer_type1_gate(coverage(), {}).status,
                         "type1_unresolved")

    def test_missing_or_invalid_coverage_rejected(self):
        with self.assertRaises(ValueError):
            select_type1_gate_lines({LYA: "usable"})
        with self.assertRaises(ValueError):
            select_type1_gate_lines(coverage(LYA, CIV) | {CIV: "unknown"})


if __name__ == "__main__":
    unittest.main()
