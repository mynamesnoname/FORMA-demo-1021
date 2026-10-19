"""Incremental Markdown archive of model-facing prompts and returned messages."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage


def _fenced(value: Any, language: str = "text") -> str:
    """Preserve arbitrary prompt or tool text without letting it close the fence."""
    body = value if isinstance(value, str) else json.dumps(
        value, ensure_ascii=False, indent=2, default=str)
    longest = max((len(part) for part in re.findall(r"`+", body)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}{language}\n{body}\n{fence}\n"


def _reasoning(message: BaseMessage) -> Any | None:
    """Only provider-returned reasoning is archivable; hidden thinking is absent."""
    for mapping in (getattr(message, "additional_kwargs", None),
                    getattr(message, "response_metadata", None)):
        if isinstance(mapping, dict):
            for key in ("reasoning_content", "reasoning", "thinking"):
                if mapping.get(key) not in (None, ""):
                    return mapping[key]
    return None


class MarkdownSessionRecorder:
    """Write each observed event immediately so failed sessions retain a trace."""

    def __init__(self, path: str | Path, *, run_id: str, hypothesis_ref: str,
                 stage: str, system_prompt: str, input_messages: Iterable[BaseMessage],
                 tools: Iterable[str], session_kind: str = "SH pre-analysis",
                 subject_label: str = "Hypothesis"):
        self.path = Path(path).resolve()
        self.event_count = 0
        self.reasoning_returned = False
        self.model_calls: list[dict[str, Any]] = []
        input_messages = list(input_messages)
        self._seen_call_ids = {
            message.id for message in input_messages
            if isinstance(message, AIMessage) and message.id
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("x", encoding="utf-8") as handle:
            handle.write(
                f"# {session_kind} session: {stage}\n\n"
                f"- Run ID: `{run_id}`\n"
                f"- {subject_label}: `{hypothesis_ref}`\n"
                f"- Started (UTC): {datetime.now(timezone.utc).isoformat()}\n"
                f"- Available tools: {', '.join(f'`{name}`' for name in tools)}\n\n"
                "The record contains model-facing input and returned messages. "
                "Provider reasoning appears only if the API returned it; hidden reasoning cannot be archived.\n\n"
                "## Model-facing input\n\n### System prompt\n\n"
                + _fenced(system_prompt, "markdown")
            )
            for index, message in enumerate(input_messages, start=1):
                self._write_message(handle, message, f"Input message {index}")
            handle.write("\n## Returned events\n")

    def _write_message(self, handle, message: BaseMessage, label: str,
                       *, collect_usage: bool = False) -> None:
        role = getattr(message, "type", type(message).__name__)
        handle.write(f"\n### {label}: {role}\n\n")
        if isinstance(message, ToolMessage):
            handle.write(f"Tool: `{message.name or 'unknown'}`; call ID: `{message.tool_call_id}`\n\n")
        content = getattr(message, "content", "")
        if content not in (None, ""):
            handle.write(_fenced(content, "markdown" if isinstance(content, str) else "json"))
        if isinstance(message, AIMessage) and message.tool_calls:
            handle.write("\nTool calls:\n\n" + _fenced(message.tool_calls, "json"))
        if isinstance(message, AIMessage):
            metadata = message.response_metadata or {}
            raw = metadata.get("token_usage") or {}
            usage = message.usage_metadata or {}
            if raw or usage:
                record = {
                    "input_tokens": raw.get("prompt_tokens", usage.get("input_tokens")),
                    "output_tokens": raw.get("completion_tokens", usage.get("output_tokens")),
                    "total_tokens": raw.get("total_tokens", usage.get("total_tokens")),
                    "cache_hit_tokens": raw.get("prompt_cache_hit_tokens",
                        (usage.get("input_token_details") or {}).get("cache_read")),
                    "cache_miss_tokens": raw.get("prompt_cache_miss_tokens"),
                    "provider_usage": raw,
                }
                visible_chars = len(str(content or "")) + len(json.dumps(
                    message.tool_calls or [], ensure_ascii=False, default=str))
                reported_output = record["output_tokens"]
                if (isinstance(reported_output, (int, float))
                        and reported_output > max(4096, 4 * visible_chars)):
                    # Preserve provider usage verbatim. Hidden reasoning or a
                    # provider counter may explain the gap; it is not billed
                    # cost verified by this client.
                    record["usage_note"] = "reported_output_far_above_visible_response; unverified"
                if collect_usage:
                    call_id = message.id
                    if call_id is None or call_id not in self._seen_call_ids:
                        self.model_calls.append(record)
                        if call_id is not None:
                            self._seen_call_ids.add(call_id)
                handle.write("\nProvider usage:\n\n" + _fenced(record, "json"))
        reasoning = _reasoning(message)
        if reasoning is not None:
            self.reasoning_returned = True
            handle.write("\nProvider-returned reasoning:\n\n" + _fenced(reasoning))

    def record_event(self, event: Any) -> None:
        self.event_count += 1
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(f"\n### Event {self.event_count}\n")
            if not isinstance(event, dict):
                handle.write("\n" + _fenced(event, "json"))
                return
            for node, update in event.items():
                handle.write(f"\n#### Graph update: `{node}`\n")
                if isinstance(update, dict):
                    for message in update.get("messages") or []:
                        self._write_message(handle, message, f"Event {self.event_count} message",
                                            collect_usage=True)
                else:
                    handle.write("\n" + _fenced(update, "json"))

    def finish(self, *, status: str, error_type: str | None = None) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(
                "\n## Session outcome\n\n"
                f"- Status: `{status}`\n"
                f"- Returned events: {self.event_count}\n"
                f"- Provider reasoning field returned: {'yes' if self.reasoning_returned else 'no'}\n"
            )
            if error_type:
                handle.write(f"- Error type: `{error_type}`\n")
            handle.write(f"- Ended (UTC): {datetime.now(timezone.utc).isoformat()}\n")
