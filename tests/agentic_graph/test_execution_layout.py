"""Readable new paths and compatibility with old trace-owned paths."""

import json
import tempfile
import unittest
from pathlib import Path

from FORMA.agentic_graph.execution_artifacts import (
    ExecutionAllocation, allocate_execution, validate_execution,
)
from FORMA.agentic_graph.feature_registry import REGISTRY_SCHEMA
from FORMA.agentic_graph.reasoning_trace import new_trace, register_execution, write_trace


class ExecutionLayoutTests(unittest.TestCase):
    def test_stage_and_hypothesis_folders_keep_retries_and_forks_separate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cases = {
                "sh.pre_analysis/run-1/H1": "SH/H1/pre_analysis/branches/main/",
                "sh2.qso/H1/qso.analysis_report": "SH/H1/qso/qso.analysis_report/branches/main/",
                "sh2.alignment/H2/lrg_bgs/fit:H2:0001/seat-0": "SH/H2/alignment/",
                "fa.real_feature_or_not/run-1/cwt:em:0001": "FA/shared/real_feature_or_not/",
                "fa.real_feature_or_not/run-1/fit:H3:0002": "FA/H3/real_feature_or_not/",
                "fa.real_doublet_or_not/run-1/H4/cahk": "FA/H4/real_doublet_or_not/cahk/",
                "hs.merge_groups": "HS/merge_groups/result/branches/main/",
                "ra.review": "RA/review/result/branches/main/",
            }
            for key, prefix in cases.items():
                with self.subTest(key=key):
                    allocation = allocate_execution(root, run_id="run-1", branch_id="main",
                                                    node_key=key)
                    self.assertTrue(allocation.relative_dir.startswith(prefix))
                    validate_execution(allocation)
            key = "sh.pre_analysis/run-1/H1"
            retry = allocate_execution(root, run_id="run-1", branch_id="main", node_key=key)
            fork = allocate_execution(root, run_id="run-1", branch_id="review-2", node_key=key)
            self.assertNotEqual(retry.directory, fork.directory)
            self.assertIn("/branches/review-2/", f"/{fork.relative_dir}/")
            self.assertEqual(retry.metadata()["node_key"], key)
            self.assertEqual(len(retry.node_execution_id), 32)

    def test_old_manifest_path_remains_valid_and_unsafe_ids_stay_contained(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            legacy = ExecutionAllocation("r", "main", "sh.pre_analysis/r/H1",
                                         "a" * 32, "b" * 32, root,
                                         "runs/r-123/branches/main-123/nodes/sh-old/a-b")
            legacy.directory.mkdir(parents=True)
            legacy.path("execution.json").write_text(json.dumps(legacy.metadata()))
            validate_execution(legacy)
            trace = new_trace({"schema_version": REGISTRY_SCHEMA, "run_id": "r",
                               "artifacts": {}})
            register_execution(trace, legacy)
            exported = json.loads(write_trace(trace, root / "historical-tree.json").read_text())
            self.assertEqual(exported["executions"][legacy.node_execution_id]
                             ["relative_dir"], legacy.relative_dir)
            allocation = allocate_execution(root, run_id="r", branch_id="../fork",
                                            node_key="sh.pre_analysis/r/%2E%2E%2Fsecret")
            self.assertTrue(allocation.directory.is_relative_to(root))
            self.assertNotIn("..", allocation.directory.relative_to(root).parts)
            validate_execution(allocation)


if __name__ == "__main__":
    unittest.main()
