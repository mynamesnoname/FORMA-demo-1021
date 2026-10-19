"""The measured feature-width vocabulary is declared once, with owned boundaries.

实测特征宽度词表只声明一次，且每个边界都有唯一所有者。

`width_class` named two different questions: the class of a *line* (registry) and the
measured band of a *feature* (CWT catalog and contradiction matrix).  The second had
no declaration: `intermediate` lived in two code expressions and one prompt sentence,
both producers read their boundaries from different rule declarations, and the same
feature could therefore be labelled differently depending on which path wrote the row.

`width_class` 曾指两个不同问题：*谱线*的类别（注册表）与*特征*的实测档（CWT 目录与矛盾矩阵）。
后者没有声明：`intermediate` 只存在于两处代码与一句提示词中，两个产出方各自从不同规则声明读取
边界，因此同一特征可能因写入路径不同而得到不同标签。
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from FORMA.core.reasoning.ontology import feature_width as fw  # noqa: E402
from FORMA.core.reasoning.ontology.rule_parameters import (  # noqa: E402
    effective_operand_threshold,
)

CWT_SOURCE = PROJECT_ROOT / "src/FORMA/agents/multi_agents/utils/cwt_feature_finder.py"


class VocabularyTests(unittest.TestCase):
    def test_the_declared_bands(self):
        self.assertEqual(fw.BANDS, ("narrow", "intermediate", "broad"))
        for band in fw.BANDS:
            with self.subTest(band=band):
                self.assertTrue(fw.is_known(band))
                self.assertTrue(fw.MEANING[band])
                self.assertTrue(fw.CONFLICT_NOTE[band])

    def test_each_boundary_has_exactly_one_declared_owner(self):
        limits = fw.boundaries()
        self.assertEqual(
            limits["narrow_intermediate"],
            float(effective_operand_threshold(*fw.NARROW_INTERMEDIATE_OWNER)["value"]),
        )
        self.assertEqual(
            limits["intermediate_broad"],
            float(effective_operand_threshold(*fw.INTERMEDIATE_BROAD_OWNER)["value"]),
        )
        # The upper boundary belongs to the strict-broad rule, not to the
        # width-consistency pivot the CWT finder used to read.
        # 上界属于严格宽线规则，而非 CWT 找特征此前读取的宽度一致性分界。
        self.assertEqual(fw.INTERMEDIATE_BROAD_OWNER[0], "rule:formal-qso-broad-width")

    def test_band_boundaries_are_inclusive_at_the_declared_values(self):
        lower, upper = fw.boundaries().values()
        self.assertEqual(fw.band_of(lower - 0.1), fw.NARROW)
        self.assertEqual(fw.band_of(lower), fw.INTERMEDIATE)
        self.assertEqual(fw.band_of(upper - 0.1), fw.INTERMEDIATE)
        self.assertEqual(fw.band_of(upper), fw.BROAD)

    def test_an_unmeasurable_width_has_no_band(self):
        for value in (None, "", "not-a-number", fw.UNMEASURED):
            with self.subTest(value=value):
                self.assertIsNone(fw.band_of(value))
                self.assertFalse(fw.is_known(value))

    def test_the_middle_band_is_declared_as_a_grey_zone(self):
        note = fw.CONFLICT_NOTE[fw.INTERMEDIATE]
        self.assertIn("neither a clean match", note)
        self.assertIn("rule", note)

    def test_an_undeclared_band_is_refused_by_name(self):
        with self.assertRaises(ValueError) as caught:
            fw.validate(["narrow", "middle", "broad", "middle"])
        message = str(caught.exception)
        self.assertIn("['middle']", message)
        self.assertIn("declared vocabulary", message)

    def test_a_header_only_catalog_passes_validation(self):
        fw.validate([])
        fw.validate([""])

    def test_the_legend_is_rendered_from_the_declaration(self):
        legend = fw.legend()
        lower, upper = fw.boundaries().values()
        self.assertIn(f"narrow < {lower:g} km/s", legend)
        self.assertIn(f"intermediate below {upper:g} km/s", legend)
        self.assertIn("grey zone", legend)


class ProducerTests(unittest.TestCase):
    """Both producers label a feature through the same declaration.

    两个产出方都经同一声明为特征打标签。
    """

    def test_the_cwt_finder_no_longer_borrows_the_width_pivot(self):
        source = CWT_SOURCE.read_text(encoding="utf-8")
        self.assertNotIn("width_consistency_score", source)
        self.assertIn("from FORMA.core.reasoning.ontology.feature_width import band_of",
                      source)

    def test_the_cwt_catalog_write_validates_the_band_column(self):
        source = CWT_SOURCE.read_text(encoding="utf-8")
        self.assertIn("validate_bands(df_out['width_class'].tolist())", source)

