"""Allocate immutable, branch-scoped directories for graph node attempts."""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote
EXECUTION_SCHEMA = "forma-agentic-node-execution-v1"
_ID = re.compile(r"^[0-9a-f]{32}$")


def _component(value: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 1024:
        raise ValueError("execution identity must be a nonempty string of at most 1024 characters")
    label = re.sub(r"[^A-Za-z0-9_-]+", "-", value).strip("-")[:48] or "item"
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"{label}-{digest}"


def _readable(value: str) -> str:
    """Keep ordinary refs (H1, main) readable without allowing path escape."""
    if not isinstance(value, str) or not value or len(value) > 1024:
        raise ValueError("execution identity must be a nonempty string of at most 1024 characters")
    if re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", value) and value not in {".", ".."}:
        return value
    return _component(value)


def _location(node_key: str) -> Path:
    """Display layout only; the logical key and execution manifest remain authoritative."""
    if not isinstance(node_key, str) or not node_key or len(node_key) > 1024:
        raise ValueError("node key must be a nonempty string of at most 1024 characters")
    parts = node_key.split("/")
    kind = parts[0]
    if kind == "sh.pre_analysis" and len(parts) == 3:
        return Path("SH") / _readable(unquote(parts[2])) / "pre_analysis"
    if kind.startswith("sh2.") and len(parts) >= 2:
        hypothesis = _readable(unquote(parts[1]))
        graph = kind.removeprefix("sh2.")
        step = _readable(unquote(parts[2])) if len(parts) > 2 else "route"
        location = Path("SH") / hypothesis / _readable(graph) / step
        for detail in parts[3:]:
            location /= _readable(unquote(detail))
        return location
    if kind.startswith("fa."):
        task = _readable(kind.removeprefix("fa."))
        if kind == "fa.real_feature_or_not" and len(parts) >= 3:
            measurement = parts[-1]
            owner = measurement.split(":", 2)[1] if measurement.startswith("fit:") and measurement.count(":") >= 2 else "shared"
            return Path("FA") / _readable(owner) / task / _readable(measurement)
        if len(parts) >= 3:
            hypothesis = _readable(unquote(parts[2]))
            target = _readable(unquote(parts[3])) if len(parts) > 3 else "review"
            return Path("FA") / hypothesis / task / target
        return Path("FA") / task / _component(node_key)
    for prefix, stage in (("hs.", "HS"), ("ra.", "RA")):
        if kind.startswith(prefix):
            return Path(stage) / _readable(kind.removeprefix(prefix)) / (
                _component(node_key) if len(parts) > 1 else "result")
    return Path("OTHER") / _component(node_key)


@dataclass(frozen=True)
class ExecutionAllocation:
    run_id: str
    branch_id: str
    node_key: str
    node_execution_id: str
    attempt_id: str
    root: Path
    relative_dir: str

    @property
    def directory(self) -> Path:
        return self.root / self.relative_dir

    def path(self, filename: str) -> Path:
        if (not filename or filename in {".", ".."}
                or Path(filename).name != filename or "\\" in filename):
            raise ValueError("artifact filename must be one local basename")
        return self.directory / filename

    def metadata(self) -> dict:
        return {"schema_version": EXECUTION_SCHEMA, "run_id": self.run_id,
                "branch_id": self.branch_id, "node_key": self.node_key,
                "node_execution_id": self.node_execution_id,
                "attempt_id": self.attempt_id,
                "relative_dir": self.relative_dir}


def allocate_execution(root: str | Path, *, run_id: str, branch_id: str,
                       node_key: str, node_execution_id: str | None = None,
                       attempt_id: str | None = None) -> ExecutionAllocation:
    """Reserve one new directory atomically; retries must allocate again.

    Stage and hypothesis folders make attempts navigable. A branch folder and
    execution UUID keep forks and retries immutable; the manifest and trace
    retain the original logical key and both full IDs.
    """
    execution_id = node_execution_id or uuid.uuid4().hex
    attempt = attempt_id or uuid.uuid4().hex
    if not _ID.fullmatch(execution_id) or not _ID.fullmatch(attempt):
        raise ValueError("execution and attempt IDs must be 32 lowercase hex characters")
    location = _location(node_key)
    relative = location / "branches" / _readable(branch_id) / execution_id
    root_path = Path(root).resolve()
    directory = root_path / relative
    directory.mkdir(parents=True, exist_ok=False)
    allocation = ExecutionAllocation(run_id, branch_id, node_key, execution_id,
                                     attempt, root_path, relative.as_posix())
    with allocation.path("execution.json").open("x", encoding="utf-8") as stream:
        json.dump(allocation.metadata(), stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return allocation


def validate_execution(allocation: ExecutionAllocation) -> None:
    """Reject a changed allocation manifest before persisting tree references."""
    manifest = json.loads(allocation.path("execution.json").read_text(encoding="utf-8"))
    if manifest != allocation.metadata():
        raise ValueError("node execution manifest changed")
