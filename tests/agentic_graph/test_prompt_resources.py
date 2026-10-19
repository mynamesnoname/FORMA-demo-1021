"""Packaged prompt resources are shipped and read from inside the package (demo cut).

打包提示词资源随包分发，并从包内读取（demo 精简）。

The 20 model-facing prompts used to live in ``agenticGraphReasoningDesign/implement/``,
a design directory a demo checkout need not keep.  They now ship with
``FORMA.agentic_graph`` and are read through ``FORMA.agentic_graph.prompts.PROMPT_DIR``.
这些面向模型的提示词原先位于设计目录 ``agenticGraphReasoningDesign/implement/``（demo 检出
不一定会保留），现随 ``FORMA.agentic_graph`` 分发，并经 ``prompts.PROMPT_DIR`` 读取。
"""

from __future__ import annotations

import sys
import tomllib
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from FORMA.agentic_graph.prompts import PROMPT_DIR  # noqa: E402

PACKAGE = (PROJECT_ROOT / "src" / "FORMA" / "agentic_graph").resolve()

#: Every prompt the runtime reads, including the historical two-stage SH path.
#: 运行时读取的全部提示词，含历史两阶段 SH 路径。
EXPECTED = (
    "sh_line_review_system.md", "sh_line_review_user.md",
    "sh_pre_analysis_system.md", "sh_pre_analysis_user_1.md", "sh_pre_analysis_user_2.md",
    "qso_q11_report_system.md", "qso_q11_report_user.md",
    "fa_doublet_system.md", "fa_doublet_user.md",
    "fa_real_feature_system.md", "fa_real_feature_user.md",
    "fa_lya_forest_system.md", "fa_lya_forest_user.md",
    "hs_merge_proposal_system.md", "hs_merge_dossier_user.md", "hs_merge_question_user.md",
    "hs_comparison_system.md", "hs_comparison_user.md",
    "lrg_bgs_cahk_targeted_system.md", "lrg_bgs_cahk_targeted_user.md",
)


class PromptResourceTests(unittest.TestCase):
    def test_the_prompt_directory_is_inside_the_package(self):
        self.assertEqual(PROMPT_DIR.resolve().parent, PACKAGE)
        self.assertEqual(PROMPT_DIR.name, "prompts")

    def test_every_runtime_prompt_is_shipped(self):
        missing = [name for name in EXPECTED if not (PROMPT_DIR / name).is_file()]
        self.assertEqual(missing, [])

    def test_no_prompt_is_empty(self):
        empty = [name for name in EXPECTED if (PROMPT_DIR / name).stat().st_size == 0]
        self.assertEqual(empty, [])

    def test_the_package_ships_the_prompt_files(self):
        metadata = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        patterns = metadata["tool"]["setuptools"]["package-data"]["FORMA.agentic_graph"]
        self.assertIn("prompts/*.md", patterns)

    def test_no_source_reads_the_old_design_directory(self):
        offenders = [
            path.name
            for path in PACKAGE.glob("*.py")
            if "agenticGraphReasoningDesign" in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(offenders, [])
