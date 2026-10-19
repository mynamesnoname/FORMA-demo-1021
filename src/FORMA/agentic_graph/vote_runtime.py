"""Shared execution mechanics for independent agentic-graph vote sessions.

Scientific preflight and the meaning of a vote belong to each node. This module
owns fresh sessions, bounded seats, retry archives, stable prompt identity and
provider-reported usage. Prompt caching is a measured provider behavior, never
an inferred property of identical text.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, ConfigDict, Field

from .execution_artifacts import ExecutionAllocation, allocate_execution
from .reasoning_trace import register_artifact, register_execution
from .session_markdown import MarkdownSessionRecorder
from .sh_pre_analysis import _run_until


class VoteSessionFailure(RuntimeError):
    """A failed attempt with observed usage and its original error type."""

    def __init__(self, cause: Exception, model_calls: list[dict]):
        super().__init__(str(cause))
        self.original_error_type = type(cause).__name__
        self.model_calls = model_calls


def prompt_identity(system: str, user: str, tool_name: str) -> dict[str, str]:
    """Fingerprint prompt text and tool name, not the full provider request.

    The provider's tool schema, model settings and routing also affect cache
    behavior. Even identical fingerprints do not imply a server cache hit.
    """
    if not system or not user or not tool_name:
        raise ValueError("vote prompts and tool name must be nonempty")

    def digest(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    return {"system_sha256": digest(system), "user_sha256": digest(user),
            "tool_name": tool_name,
            "prompt_text_sha256": digest(json.dumps([system, user, tool_name],
                                                   ensure_ascii=False, separators=(",", ":")))}


def summarize_usage(calls: Iterable[dict]) -> dict[str, int]:
    """Sum observed calls; distinguish an unreported cache field from zero."""
    calls = list(calls)
    reported = [call for call in calls if call.get("cache_hit_tokens") is not None]
    return {"calls": len(calls),
            "input_tokens": sum(call.get("input_tokens") or 0 for call in calls),
            "output_tokens": sum(call.get("output_tokens") or 0 for call in calls),
            "cache_hit_tokens": sum(call["cache_hit_tokens"] for call in reported),
            "cache_hit_reported_calls": len(reported),
            "cache_hit_unreported_calls": len(calls) - len(reported)}


async def run_vote_session(*, llm: Any, allocation: ExecutionAllocation | None,
                           system: str, user: str, tool: Any, tool_name: str,
                           completed: Callable[[], bool],
                           agent_factory: Callable[..., Any], recursion_limit: int,
                           stage: str, subject_ref: str, subject_label: str,
                           session_path: str | Path | None = None,
                           run_id: str | None = None) -> list[dict]:
    """Run one fresh agent and archive all returned events, including failures."""
    prompt_identity(system, user, tool_name)
    if allocation is None and (session_path is None or run_id is None):
        raise ValueError("vote session needs an allocation or explicit path and run ID")
    recorder = MarkdownSessionRecorder(
        allocation.path("session.md") if allocation else session_path,
        run_id=allocation.run_id if allocation else run_id,
        hypothesis_ref=subject_ref, stage=stage, system_prompt=system,
        input_messages=[HumanMessage(content=user)], tools=[tool_name],
        session_kind="FA", subject_label=subject_label)
    try:
        agent = agent_factory(model=llm, tools=[tool], system_prompt=system)
        await _run_until(agent, [HumanMessage(content=user)],
                         config={"recursion_limit": recursion_limit},
                         completed=completed, on_event=recorder.record_event)
        if not completed():
            raise RuntimeError("vote session ended without a valid submission")
        recorder.finish(status="complete")
    except Exception as exc:
        recorder.finish(status="failed", error_type=type(exc).__name__)
        raise VoteSessionFailure(exc, recorder.model_calls) from exc
    return recorder.model_calls


@dataclass(frozen=True)
class VoteSeat:
    target_id: str
    seat: int
    node_key: str


@dataclass(frozen=True)
class VoteAttempt:
    allocation: ExecutionAllocation
    status: str
    result: dict | None
    model_calls: list[dict]
    error_type: str | None = None


@dataclass(frozen=True)
class VoteSeatResult:
    seat: VoteSeat
    attempts: tuple[VoteAttempt, ...]


def _write_json(path: Path, payload: dict) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


class _AdvisoryVoteArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer: Literal["yes", "no"]
    reason: str = Field(min_length=8, max_length=500)


async def run_advisory_vote(*, llm: Any, allocation: ExecutionAllocation,
                            system: str, user: str, tool_name: str,
                            stage: str, subject_ref: str,
                            agent_factory: Callable[..., Any],
                            recursion_limit: int) -> dict:
    """One anonymous advisory yes/no session with a bound submission tool."""
    submitted: dict | None = None

    @tool(tool_name, args_schema=_AdvisoryVoteArgs)
    def submit_vote(answer: Literal["yes", "no"], reason: str) -> dict:
        """Submit one visual observation about the supplied spectrum region."""
        nonlocal submitted
        if submitted is not None:
            return {"ok": False, "error": "vote already submitted"}
        if not reason.strip():
            return {"ok": False, "error": "reason must describe observed pixels"}
        submitted = {"answer": answer, "reason": reason.strip(),
                     "execution": allocation.metadata()}
        return {"ok": True}

    calls = await run_vote_session(
        llm=llm, allocation=allocation, system=system, user=user,
        tool=submit_vote, tool_name=tool_name,
        completed=lambda: submitted is not None,
        agent_factory=agent_factory, recursion_limit=recursion_limit,
        stage=stage, subject_ref=subject_ref,
        subject_label="Advisory claim (internal)")
    if submitted is None:
        raise RuntimeError("advisory vote session returned without a submission")
    try:
        _write_json(allocation.path("vote.json"), submitted)
    except Exception as exc:
        raise VoteSessionFailure(exc, calls) from exc
    return {"answer": submitted["answer"], "reason": submitted["reason"],
            "model_calls": calls}


async def collect_advisory_votes(*, trace: dict, branch_id: str, node_key: str,
                                 output_root: str | Path, llm: Any,
                                 system: str, user: str, tool_name: str,
                                 stage: str, vote_quorum: int, max_attempts: int,
                                 concurrency: int, recursion_limit: int,
                                 agent_factory: Callable[..., Any],
                                 artifact_namespace: str) -> dict:
    """Run all seats and index immutable attempt artifacts in the trace."""
    if vote_quorum < 1 or vote_quorum % 2 != 1:
        raise ValueError("advisory vote quorum must be positive and odd")
    identity = prompt_identity(system, user, tool_name)

    async def invoke(seat: VoteSeat, allocation: ExecutionAllocation) -> dict:
        if prompt_identity(system, user, tool_name) != identity:
            raise ValueError("advisory prompt changed before submission")
        return await run_advisory_vote(
            llm=llm, allocation=allocation, system=system, user=user,
            tool_name=tool_name, stage=stage, subject_ref=node_key,
            agent_factory=agent_factory, recursion_limit=recursion_limit)

    seats = [VoteSeat(node_key, index, node_key) for index in range(vote_quorum)]
    results = []
    async for outcome in iter_vote_seats(
            root=output_root, run_id=trace["run_id"], branch_id=branch_id,
            seats=seats, concurrency=concurrency, max_attempts=max_attempts,
            invoke=invoke):
        results.append(outcome)
    attempt_refs, ballots, calls = [], [], []
    for outcome in sorted(results, key=lambda item: item.seat.seat):
        for attempt in outcome.attempts:
            allocation = attempt.allocation
            register_execution(trace, allocation)
            prefix = f"{artifact_namespace}/{allocation.node_execution_id}"
            files = (["vote.json", "session.md", "model_usage.json"]
                     if attempt.status == "success"
                     else ["failure.json", "model_usage.json"])
            if attempt.status == "failed" and allocation.path("session.md").exists():
                files.append("session.md")
            for filename in files:
                ref = f"{prefix}/{filename}"
                register_artifact(trace, ref, allocation.path(filename),
                                  artifact_namespace + "_" + filename.rsplit(".", 1)[0],
                                  node_execution_id=allocation.node_execution_id)
                attempt_refs.append(ref)
            calls.extend(attempt.model_calls)
            if attempt.status == "success":
                ballots.append({"seat": outcome.seat.seat,
                                "answer": attempt.result["answer"],
                                "reason": attempt.result["reason"],
                                "vote_ref": f"{prefix}/vote.json"})
    return {"ballots": ballots, "attempt_refs": attempt_refs,
            "model_usage": summarize_usage(calls), "prompt_identity": identity}


async def iter_vote_seats(*, root: str | Path, run_id: str, branch_id: str,
                          seats: Iterable[VoteSeat], concurrency: int,
                          max_attempts: int,
                          invoke: Callable[[VoteSeat, ExecutionAllocation], Awaitable[dict]]) \
                          -> AsyncIterator[VoteSeatResult]:
    """Yield completed seats; each attempt receives a new immutable directory.

    `invoke` returns a node-owned result with `answer` and `model_calls`.
    A failed model call may attach `model_calls` to its exception so usage is
    archived and counted even when its vote is invalid.
    """
    if type(concurrency) is not int or concurrency < 1:
        raise ValueError("concurrency must be positive")
    if type(max_attempts) is not int or max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    seats = list(seats)
    if any(type(seat.seat) is not int or seat.seat < 0 or not seat.target_id
           or not seat.node_key for seat in seats):
        raise ValueError("vote seats need stable nonnegative identities")
    if len({(seat.target_id, seat.seat) for seat in seats}) != len(seats):
        raise ValueError("duplicate vote seat")
    semaphore = asyncio.Semaphore(concurrency)

    async def one_seat(seat: VoteSeat) -> VoteSeatResult:
        attempts = []
        for number in range(1, max_attempts + 1):
            allocation = allocate_execution(root, run_id=run_id, branch_id=branch_id,
                                            node_key=seat.node_key)
            result = None
            try:
                async with semaphore:
                    result = await invoke(seat, allocation)
                if result.get("answer") not in {"yes", "no"}:
                    raise ValueError("vote attempt did not produce a binary answer")
                calls = result.get("model_calls")
                if not isinstance(calls, list):
                    raise ValueError("vote attempt has no model-call list")
                _write_json(allocation.path("model_usage.json"), {"model_calls": calls})
                attempts.append(VoteAttempt(allocation, "success", result, calls))
                break
            except Exception as exc:
                calls = getattr(exc, "model_calls", None)
                if calls is None and isinstance(result, dict):
                    calls = result.get("model_calls")
                if not isinstance(calls, list):
                    calls = []
                error_type = getattr(exc, "original_error_type", type(exc).__name__)
                _write_json(allocation.path("failure.json"), {
                    "status": "failed", "target_id": seat.target_id,
                    "seat": seat.seat, "attempt_number": number,
                    "error_type": error_type})
                _write_json(allocation.path("model_usage.json"), {"model_calls": calls})
                attempts.append(VoteAttempt(allocation, "failed", None, calls,
                                            error_type))
        return VoteSeatResult(seat, tuple(attempts))

    tasks = [asyncio.create_task(one_seat(seat)) for seat in seats]
    try:
        for completed in asyncio.as_completed(tasks):
            yield await completed
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)


def vote_tally(ballots: list[dict], required_votes: int, assessable: bool) -> dict:
    """Project only a completed odd quorum to a binary decision."""
    if type(required_votes) is not int or required_votes < 1 or required_votes % 2 != 1:
        raise ValueError("vote quorum must be positive and odd")
    if any(ballot.get("answer") not in {"yes", "no"} for ballot in ballots):
        raise ValueError("vote tally contains an invalid ballot")
    if len(ballots) > required_votes:
        raise ValueError("vote tally exceeds declared quorum")
    complete = len(ballots) == required_votes
    yes = sum(ballot["answer"] == "yes" for ballot in ballots)
    fraction = yes / required_votes if complete else None
    return {"status": "complete" if complete else "pending" if assessable else "unreviewable",
            "positive": yes > required_votes / 2 if complete else None,
            "vote_summary": ({"yes": yes, "no": required_votes - yes,
                              "yes_fraction": fraction,
                              "assurance": "assured" if max(fraction, 1 - fraction) > 0.75
                              else "contested"} if complete else None),
            "successful_votes": len(ballots), "required_votes": required_votes,
            "failed_seats": required_votes - len(ballots) if assessable and not complete else 0}
