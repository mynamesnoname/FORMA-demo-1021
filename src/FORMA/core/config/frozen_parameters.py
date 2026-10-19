"""One immutable declared-parameter set per run, with a content digest.

每次运行唯一一份不可变的已声明参数集，并带内容摘要。

Consumers used to reload the declared JSON independently — 33 direct loader call sites
(75 including the effective-value readers) — and the loaders do not cache, so every
decision point sampled the files at its own moment. A file edited during a run, or a
stage that read a different path, could therefore give two stages two different value
sets, and `effective_parameters.json` (written once at result-writing time) could not
prove which one any stage had used.

消费方此前各自重载已声明的 JSON——直接加载器调用点 33 处（含生效读取则 75 处）——而加载器不缓存，
因此每个决策点在各自的时刻采样文件。运行期间被编辑的文件、或读了不同路径的阶段，都可能让两个阶段
用到两组不同的值，而 `effective_parameters.json`（写结果时生成一次）无法证明任何阶段当时用的是
哪一组。

This module freezes the three declaration sources once per run. While a set is installed,
the loaders return the frozen snapshot instead of touching the filesystem, so a
mid-run edit cannot change a value; the digest of the frozen set is recorded in the run's
`effective_parameters.json` and in the run telemetry.

本模块在每次运行时把三个声明来源冻结一次。集合安装期间，加载器返回冻结快照而不再访问文件系统，
因此运行中途的编辑无法改变取值；冻结集合的摘要记入该运行的 `effective_parameters.json` 与运行
telemetry。

Scope: the freeze is **per run** (decision, 2026-10-15). Batch mode therefore samples the
files once per input and each input records its own digest, which is what makes a change
between inputs visible rather than silently shared.
范围：冻结是**逐运行**的（2026-10-15 决定）。因此批处理对每个输入采样一次，每个输入记录自己的
摘要，使输入之间的变化可见，而不是被静默共用。
"""

from __future__ import annotations

import hashlib
import json
import os
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class FrozenParameterSet:
    """The run's immutable declarations / 该运行不可变的声明集合。"""

    _analysis_method: Any
    _rule_parameters: Any
    _model_calls: Any
    sources: Mapping[str, Optional[str]] = field(default_factory=dict)
    digests: Mapping[str, str] = field(default_factory=dict)
    digest: str = ""

    def __post_init__(self) -> None:
        for name in ("_analysis_method", "_rule_parameters", "_model_calls"):
            object.__setattr__(self, name, getattr(self, name).model_copy(deep=True))
        object.__setattr__(self, "sources", MappingProxyType(dict(self.sources)))
        object.__setattr__(self, "digests", MappingProxyType(dict(self.digests)))

    @property
    def analysis_method(self) -> Any:
        return self._analysis_method.model_copy(deep=True)

    @property
    def rule_parameters(self) -> Any:
        return self._rule_parameters.model_copy(deep=True)

    @property
    def model_calls(self) -> Any:
        return self._model_calls.model_copy(deep=True)

    def describe(self) -> Dict[str, Any]:
        """The record written into run artifacts / 写入运行产物的记录。"""
        return {
            "schema": "forma-frozen-parameters-v1",
            "digest": self.digest,
            "sources": dict(self.sources),
            "source_digests": dict(self.digests),
            "scope": "per run; loaders return this snapshot while it is installed",
        }


_ACTIVE: ContextVar[Optional[FrozenParameterSet]] = ContextVar(
    "forma_frozen_parameters", default=None
)


def _digest_file(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    target = Path(path)
    if not target.is_file():
        return None
    return hashlib.sha256(target.read_bytes()).hexdigest()


def _digest_payload(payload: Any) -> str:
    if hasattr(payload, "model_dump"):
        payload = payload.model_dump(mode="json")
    blob = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def freeze() -> FrozenParameterSet:
    """Read the three declaration sources once and build the run's frozen set.

    一次性读取三个声明来源并构建该运行的冻结集合。
    """
    from FORMA.core.config.analysis_method import DEFAULT_PATH as AM_PATH
    from FORMA.core.config.analysis_method import ENV_PATH as AM_ENV
    from FORMA.core.config.analysis_method import load_analysis_method
    from FORMA.core.config.model_calls import DEFAULT_PATH as MC_PATH
    from FORMA.core.config.model_calls import ENV_PATH as MC_ENV
    from FORMA.core.config.model_calls import load_model_calls
    from FORMA.core.reasoning.ontology.rule_parameters import load_rule_parameters

    # A new run must sample the files even when called inside a previous scope.
    token = _ACTIVE.set(None)
    try:
        analysis_method = load_analysis_method()
        rule_parameters, rule_path, _ = load_rule_parameters()
        model_calls = load_model_calls()
    finally:
        _ACTIVE.reset(token)

    sources = {
        "analysis_method": os.getenv(AM_ENV) or str(AM_PATH),
        "rule_parameters": rule_path,
        "model_calls": os.getenv(MC_ENV) or str(MC_PATH),
    }
    digests = {}
    for name, path in sources.items():
        digest = _digest_file(path)
        if digest:
            digests[name] = digest
    payload = {
        "analysis_method": _digest_payload(analysis_method),
        "rule_parameters": _digest_payload(rule_parameters),
        "model_calls": _digest_payload(model_calls),
    }
    combined = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return FrozenParameterSet(
        _analysis_method=analysis_method,
        _rule_parameters=rule_parameters,
        _model_calls=model_calls,
        sources=sources,
        digests=digests,
        digest=combined,
    )


def install(frozen: Optional[FrozenParameterSet] = None) -> FrozenParameterSet:
    """Install the run's frozen set (freezing one if none is supplied).

    安装该运行的冻结集合（未提供时先冻结一次）。
    """
    installed = frozen if frozen is not None else freeze()
    _ACTIVE.set(installed)
    return installed


@contextmanager
def run_scope():
    """Freeze one spectrum run and restore the caller's context on every exit."""
    frozen = freeze()
    token = _ACTIVE.set(frozen)
    try:
        yield frozen
    finally:
        _ACTIVE.reset(token)


def current() -> Optional[FrozenParameterSet]:
    """The installed set, or ``None`` outside a frozen run.

    已安装的集合；未冻结的运行返回 ``None``。
    """
    return _ACTIVE.get()


def clear() -> None:
    """Drop the installed set (tests and non-pipeline callers).

    清除已安装的集合（测试与非管线调用方）。
    """
    _ACTIVE.set(None)


def frozen_digest() -> Optional[str]:
    """The digest recorded in run artifacts, or ``None``.

    记入运行产物的摘要；未冻结时为 ``None``。
    """
    frozen = current()
    return frozen.digest if frozen is not None else None


def describe() -> Optional[Dict[str, Any]]:
    """The artifact record, or ``None`` when no set is installed.

    产物记录；未安装集合时为 ``None``。
    """
    frozen = current()
    return frozen.describe() if frozen is not None else None
