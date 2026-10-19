"""Structured run/stage telemetry and budget controller (WP-013).

结构化运行/阶段遥测与预算控制器（WP-013）。
"""

from __future__ import annotations

import contextvars
import json
import time
import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field
from langchain_core.callbacks import BaseCallbackHandler

TELEMETRY_SCHEMA_VERSION = "forma-telemetry-v1"


class BudgetConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    max_calls: int = Field(default=200, ge=1)
    max_prompt_tokens: int = Field(default=2_000_000, ge=1)
    max_tool_rounds: int = Field(default=50, ge=1)
    max_wall_time_s: float = Field(default=3600.0, gt=0.0)


class BudgetExceeded(RuntimeError):
    """Raised when a budget boundary is crossed / 超过预算边界时抛出。"""


class BudgetController:
    def __init__(self, config: BudgetConfig | None = None):
        self.config = config or BudgetConfig()

    def check(
        self,
        *,
        calls: int = 0,
        prompt_tokens: int = 0,
        tool_rounds: int = 0,
        elapsed_s: float = 0.0,
    ) -> List[str]:
        exceeded: List[str] = []
        if calls > self.config.max_calls:
            exceeded.append("max_calls")
        if prompt_tokens > self.config.max_prompt_tokens:
            exceeded.append("max_prompt_tokens")
        if tool_rounds > self.config.max_tool_rounds:
            exceeded.append("max_tool_rounds")
        if elapsed_s > self.config.max_wall_time_s:
            exceeded.append("max_wall_time_s")
        return exceeded

    def enforce(self, **counters) -> None:
        exceeded = self.check(**counters)
        if exceeded:
            raise BudgetExceeded("budget exceeded: " + ", ".join(exceeded))


class StageRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    status: LiteralStatus = "running"
    started_at: float
    ended_at: Optional[float] = None
    error: Optional[str] = None

    @property
    def wall_time_s(self) -> Optional[float]:
        if self.ended_at is None:
            return None
        return round(self.ended_at - self.started_at, 6)


_CURRENT_TELEMETRY: contextvars.ContextVar = contextvars.ContextVar(
    "forma_current_telemetry", default=None
)


def set_current_telemetry(telemetry):
    return _CURRENT_TELEMETRY.set(telemetry)


def get_current_telemetry():
    return _CURRENT_TELEMETRY.get()


def record_model_call_from_context(prompt_tokens: int = 0, completion_tokens: int = 0) -> None:
    telemetry = get_current_telemetry()
    if telemetry is not None:
        telemetry.record_model_call(prompt_tokens, completion_tokens)


def reset_current_telemetry(token) -> None:
    _CURRENT_TELEMETRY.reset(token)


def record_tool_rounds_from_context(rounds: int = 1) -> None:
    telemetry = get_current_telemetry()
    if telemetry is not None:
        telemetry.record_tool_rounds(rounds)


class ModelTelemetryHandler(BaseCallbackHandler):
    """Count actual model completions, including calls made inside harness agents."""

    def on_llm_end(self, response, **kwargs) -> None:
        usage = {}
        for generation in getattr(response, "generations", []) or []:
            for item in generation:
                message = getattr(item, "message", None)
                usage = getattr(message, "usage_metadata", None) or {}
                if usage:
                    break
            if usage:
                break
        if not usage:
            usage = (getattr(response, "llm_output", None) or {}).get("token_usage", {})
        record_model_call_from_context(
            prompt_tokens=int(usage.get("input_tokens", usage.get("prompt_tokens", 0)) or 0),
            completion_tokens=int(usage.get("output_tokens", usage.get("completion_tokens", 0)) or 0),
        )

    def on_llm_error(self, error, **kwargs) -> None:
        record_model_call_from_context()


class ToolTelemetryHandler(BaseCallbackHandler):
    """Count agent tool invocations through the LangChain callback path."""

    def on_tool_end(self, output, **kwargs) -> None:
        record_tool_rounds_from_context()

    def on_tool_error(self, error, **kwargs) -> None:
        record_tool_rounds_from_context()


def track_agent_tools(agent):
    """Attach tool callbacks to an agent, including continuation invocations."""
    return agent.with_config(callbacks=[ToolTelemetryHandler()])


class RunTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = TELEMETRY_SCHEMA_VERSION
    run_id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    status: LiteralStatus = "running"
    started_at: float = Field(default_factory=time.time)
    ended_at: Optional[float] = None
    stages: Dict[str, StageRecord] = Field(default_factory=dict)
    #: Digest of the run's frozen declared-parameter set (WP-041); None outside a run.
    #: 该运行冻结的已声明参数集合摘要（WP-041）；运行之外为 None。
    frozen_parameter_digest: Optional[str] = None
    model_calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    tool_rounds: int = 0
    #: When the current budget window started. Retries and escalations reset the
    #: consumption counters and open a fresh window, so a retried attempt does not
    #: start against a cap already spent by the attempt before it.
    #: 当前预算窗口的起点。重试与升级会清零消耗计数器并开新窗口，使重试的尝试不会面对上一尝试
    #: 已花掉的额度。
    budget_started_at: Optional[float] = None
    failures: List[str] = Field(default_factory=list)
    escalations: List[str] = Field(default_factory=list)
    execution_mode: Optional[str] = None
    budget_state: Optional[BudgetConfig] = None
    budget_exceeded: List[str] = Field(default_factory=list)

    def reset_consumption(self) -> None:
        """Zero the consumption counters and open a fresh budget window.

        清零消耗计数器并开启新的预算窗口。

        Escalation and retry call this (decision owner, 2026-10-16): before this, only the
        cap changed while the counters survived, so a run escalated after exhausting the
        standard prompt budget retried straight into the forensic cap and aborted before the
        auditor could run.
        升级与重试会调用它（决策人，2026-10-16）：此前只有上限变化而计数器保留，因此耗尽标准
        提示词预算后升级的运行时，会带着旧计数直接撞进 forensic 上限，在审计阶段之前中止。
        """
        self.model_calls = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.tool_rounds = 0
        self.budget_started_at = time.time()

    def start_stage(self, name: str) -> None:
        if name not in self.stages:
            self.stages[name] = StageRecord(name=name, started_at=time.time())

    def end_stage(self, name: str, status: LiteralStatus = "ok", error: str | None = None) -> None:
        record = self.stages.get(name)
        if record is None:
            record = StageRecord(name=name, started_at=time.time())
            self.stages[name] = record
        record.status = status
        record.ended_at = time.time()
        record.error = error
        if status == "failed":
            self.failures.append(name)

    def record_model_call(self, prompt_tokens: int = 0, completion_tokens: int = 0) -> None:
        self.model_calls += 1
        self.prompt_tokens += int(prompt_tokens)
        self.completion_tokens += int(completion_tokens)

    def record_tool_rounds(self, rounds: int = 1) -> None:
        self.tool_rounds += int(rounds)

    def finish(self, status: LiteralStatus = "ok") -> None:
        self.status = status
        self.ended_at = time.time()

    def to_jsonable(self) -> Dict[str, Any]:
        """Return a secret-safe JSON payload / 返回不含密钥的 JSON 载荷。"""
        payload = self.model_dump()
        payload["wall_time_s"] = (
            round(self.ended_at - self.started_at, 6) if self.ended_at else None
        )
        return payload


LiteralStatus = str

RunTelemetry.model_rebuild()


def sanitize_telemetry_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Drop API keys, authorization, password, and full prompt payloads.

    剔除 API 密钥、授权、密码与完整 prompt 载荷。
    """
    sensitive_suffixes = ("api_key", "apikey", "authorization", "password", "secret")
    sensitive_exact = {"messages", "prompts", "prompt_text"}

    def clean(value):
        if isinstance(value, dict):
            return {
                key: ("[redacted]" if key.lower() in sensitive_exact or any(
                    suffix in key.lower() for suffix in sensitive_suffixes
                ) else clean(item))
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [clean(item) for item in value]
        return value

    return clean(payload)


def to_json(telemetry: RunTelemetry, indent: Optional[int] = 2) -> str:
    return json.dumps(
        sanitize_telemetry_payload(telemetry.to_jsonable()),
        indent=indent,
        ensure_ascii=False,
    )


__all__ = [
    "BudgetConfig",
    "get_current_telemetry",
    "record_model_call_from_context",
    "reset_current_telemetry",
    "record_tool_rounds_from_context",
    "ModelTelemetryHandler",
    "ToolTelemetryHandler",
    "track_agent_tools",
    "set_current_telemetry",
    "BudgetController",
    "BudgetExceeded",
    "RunTelemetry",
    "StageRecord",
    "TELEMETRY_SCHEMA_VERSION",
    "sanitize_telemetry_payload",
    "to_json",
]
