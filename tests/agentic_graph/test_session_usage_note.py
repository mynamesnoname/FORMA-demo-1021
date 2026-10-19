"""Preserve suspicious provider counters without silently rewriting them."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from langchain_core.messages import AIMessage

from FORMA.agentic_graph.session_markdown import MarkdownSessionRecorder


class SessionUsageNoteTests(unittest.TestCase):
    def test_huge_reported_output_with_short_visible_answer_is_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            recorder = MarkdownSessionRecorder(
                Path(directory) / "session.md", run_id="r", hypothesis_ref="h",
                stage="stage", system_prompt="system", input_messages=[], tools=[])
            response = AIMessage(content="Now the report.",
                                 response_metadata={"token_usage": {
                                     "completion_tokens": 384000,
                                     "prompt_tokens": 100, "total_tokens": 384100}})
            recorder.record_event({"model": {"messages": [response]}})
            self.assertEqual(recorder.model_calls[0]["output_tokens"], 384000)
            self.assertIn("unverified", recorder.model_calls[0]["usage_note"])
            self.assertIn("384000", recorder.path.read_text())
