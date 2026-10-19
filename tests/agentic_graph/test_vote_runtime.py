"""Shared vote execution must preserve retry costs and cache observability."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from langchain_core.messages import AIMessage
from langchain_core.tools import tool

from FORMA.agentic_graph.execution_artifacts import allocate_execution
from FORMA.agentic_graph.vote_runtime import (
    VoteSeat, iter_vote_seats, prompt_identity, run_vote_session,
    summarize_usage, vote_tally,
)


class VoteRuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def test_session_failure_keeps_provider_usage_and_markdown(self):
        class FailingAgent:
            async def astream(self, state, *, config, stream_mode):
                yield {"model": {"messages": [AIMessage(
                    content="thinking through the evidence",
                    response_metadata={"token_usage": {
                        "prompt_tokens": 70, "completion_tokens": 9,
                        "prompt_cache_hit_tokens": 12}},
                )]}}
                raise RuntimeError("provider stream stopped")

        @tool("submit_test_vote")
        def submit_test_vote(answer: str) -> dict:
            """Submit a test vote."""
            return {"answer": answer}

        with tempfile.TemporaryDirectory() as directory:
            allocation = allocate_execution(directory, run_id="r", branch_id="main",
                                            node_key="vote/test")
            with self.assertRaisesRegex(RuntimeError, "provider stream stopped") as caught:
                await run_vote_session(
                    llm=object(), allocation=allocation,
                    system="stable system", user="target spectrum",
                    tool=submit_test_vote, tool_name="submit_test_vote",
                    completed=lambda: False,
                    agent_factory=lambda **kwargs: FailingAgent(), recursion_limit=10,
                    stage="test", subject_ref="target", subject_label="Target")
            self.assertEqual(caught.exception.model_calls[0]["cache_hit_tokens"], 12)
            self.assertIn("Status: `failed`", allocation.path("session.md").read_text())

    async def test_failed_call_and_invalid_submission_are_costed_but_not_votes(self):
        with tempfile.TemporaryDirectory() as directory:
            attempts = {}

            async def invoke(seat, allocation):
                number = attempts.get(seat.seat, 0) + 1
                attempts[seat.seat] = number
                call = {"input_tokens": 100, "output_tokens": 4,
                        "cache_hit_tokens": 0 if seat.seat == 0 else None}
                if seat.seat == 0 and number == 1:
                    error = RuntimeError("model returned no valid vote")
                    error.model_calls = [call]
                    raise error
                if seat.seat == 1 and number == 1:
                    return {"answer": "maybe", "model_calls": [call]}
                return {"answer": "yes", "model_calls": [call]}

            results = []
            async for outcome in iter_vote_seats(
                    root=directory, run_id="r", branch_id="main",
                    seats=[VoteSeat("x", 0, "vote/x"), VoteSeat("x", 1, "vote/x")],
                    concurrency=2, max_attempts=2, invoke=invoke):
                results.append(outcome)
            results.sort(key=lambda item: item.seat.seat)
            self.assertEqual([[attempt.status for attempt in result.attempts]
                              for result in results],
                             [["failed", "success"], ["failed", "success"]])
            all_calls = [call for result in results for attempt in result.attempts
                         for call in attempt.model_calls]
            usage = summarize_usage(all_calls)
            self.assertEqual(usage["calls"], 4)
            self.assertEqual(usage["input_tokens"], 400)
            self.assertEqual(usage["cache_hit_reported_calls"], 2)
            self.assertEqual(usage["cache_hit_unreported_calls"], 2)
            for result in results:
                for attempt in result.attempts:
                    stored = json.loads(attempt.allocation.path("model_usage.json").read_text())
                    self.assertEqual(stored["model_calls"], attempt.model_calls)
                    self.assertTrue(attempt.allocation.path("execution.json").exists())
            self.assertEqual(len({attempt.allocation.directory for result in results
                                  for attempt in result.attempts}), 4)

    def test_prompt_fingerprint_and_incomplete_tally(self):
        base = prompt_identity("fixed system", "fixed user", "submit_vote")
        self.assertEqual(base, prompt_identity("fixed system", "fixed user", "submit_vote"))
        self.assertNotEqual(base, prompt_identity("fixed system", "changed", "submit_vote"))
        self.assertEqual(vote_tally([{"answer": "yes"}], 3, True)["status"], "pending")
        self.assertIsNone(vote_tally([], 3, False)["positive"])
        self.assertEqual(vote_tally([], 3, False)["status"], "unreviewable")
        self.assertEqual(vote_tally([{"answer": "yes"}, {"answer": "no"},
                                     {"answer": "yes"}], 3, True)["vote_summary"]["yes"], 2)
        with self.assertRaisesRegex(ValueError, "odd"):
            vote_tally([], 2, True)
