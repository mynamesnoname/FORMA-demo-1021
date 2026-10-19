"""Session archives preserve complete prompts and only returned reasoning."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage

from FORMA.agentic_graph.session_markdown import MarkdownSessionRecorder


class MarkdownSessionTests(unittest.TestCase):
    def test_provider_reasoning_and_embedded_fence_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.md"
            recorder = MarkdownSessionRecorder(
                path, run_id="run-1", hypothesis_ref="fit-1", stage="review",
                system_prompt="System ``` inside prompt", input_messages=[HumanMessage("User prompt")],
                tools=["write_lines_csv"],
            )
            recorder.record_event({"agent": {"messages": [AIMessage(
                content="Visible answer", additional_kwargs={"reasoning_content": "Returned reasoning"},
            )]}})
            recorder.finish(status="complete")
            content = path.read_text()
            self.assertIn("System ``` inside prompt", content)
            self.assertIn("User prompt", content)
            self.assertIn("Visible answer", content)
            self.assertIn("Returned reasoning", content)
            self.assertIn("Provider reasoning field returned: yes", content)
            self.assertIn("````markdown", content)

    def test_provider_cache_usage_is_recorded(self):
        with tempfile.TemporaryDirectory() as directory:
            recorder = MarkdownSessionRecorder(
                Path(directory) / "session.md", run_id="r", hypothesis_ref="h",
                stage="test", system_prompt="s", input_messages=[HumanMessage("u")],
                tools=["submit"],
            )
            recorder.record_event({"model": {"messages": [AIMessage(
                content="yes", response_metadata={"token_usage": {
                    "prompt_tokens": 100, "completion_tokens": 5,
                    "total_tokens": 105, "prompt_cache_hit_tokens": 80,
                    "prompt_cache_miss_tokens": 20}},
            )]}})
            self.assertEqual(recorder.model_calls[0]["cache_hit_tokens"], 80)
            self.assertIn("prompt_cache_hit_tokens", recorder.path.read_text())

    def test_carried_history_and_repeated_event_do_not_double_count(self):
        with tempfile.TemporaryDirectory() as directory:
            prior = AIMessage(content="previous", id="call-1",
                              response_metadata={"token_usage": {"prompt_tokens": 10}})
            new = AIMessage(content="new", id="call-2",
                            response_metadata={"token_usage": {"prompt_tokens": 20}})
            recorder = MarkdownSessionRecorder(
                Path(directory) / "session.md", run_id="r", hypothesis_ref="h",
                stage="second", system_prompt="s",
                input_messages=[HumanMessage("u"), prior], tools=["submit"],
            )
            recorder.record_event({"model": {"messages": [prior, new]}})
            recorder.record_event({"model": {"messages": [new]}})
            self.assertEqual([row["input_tokens"] for row in recorder.model_calls], [20])


if __name__ == "__main__":
    unittest.main()
