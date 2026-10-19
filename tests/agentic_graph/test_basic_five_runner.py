"""The fixed basic spectra can drive a reproducible HS smoke check.

固定示例光谱可驱动可复现的 HS 冒烟检查。入口是仓库根目录的 ``demo.py``。

``demo.py`` lives at the repository root (the tracked demo entry); the historical
``evaluation/agentic_graph/run_basic_five.py`` is local-only and untracked, so the
test must not depend on it.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from demo import ROOT, SAMPLES, read_truth, summarize  # noqa: E402


class BasicFiveRunnerTests(unittest.TestCase):
    def test_all_basic_spectra_have_vi_truth(self):
        self.assertEqual(len(SAMPLES), 5)
        for name in SAMPLES:
            with self.subTest(name=name):
                truth = read_truth(ROOT / "example/basic" / f"{name}.fits")
                self.assertGreater(truth["vi_quality"], 0)
                self.assertEqual(truth["vi_spectype"], name.split("_")[0])

    def test_summarize_keeps_provisional_hs_separate_from_vi(self):
        result = {"status": "hs_comparison_complete", "final_classification_available": False,
                  "surviving_hypotheses": ["H1", "H2"],
                  "hs_groups": [{"group_id": "g", "candidate_type": "Type 2 QSO",
                                 "member_hypotheses": ["H1", "H2"],
                                 "merged_anchor_redshift": 0.238}],
                  "hs_comparison_ref": "hs/node", "hs_comparison": {
                      "status": "provisional_selection", "winner_group_id": "g",
                      "reason": "a specific line identity", "ra_review_pending": True}}
        row = summarize("QSO_4", {"vi_z": 0.2381, "vi_spectype": "QSO",
                                  "vi_quality": 4.0}, result)
        self.assertTrue(row["type_matches_vi"])
        self.assertAlmostEqual(row["absolute_vi_redshift_error"], 0.0001)
        self.assertFalse(row["final_classification_available"])
        result["hs_comparison"]["winner_group_id"] = None
        row = summarize("QSO_4", {"vi_z": 0.2381, "vi_spectype": "QSO",
                                  "vi_quality": 4.0}, result)
        self.assertIsNone(row["type_matches_vi"])
        self.assertIsNone(row["absolute_vi_redshift_error"])
