"""Record the external Redrock authority used for one spectrum.

Only explicitly selected process inputs are recorded. The inherited environment may
contain API keys, so it is never copied into an artifact.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import shutil
from pathlib import Path
from typing import Any, Mapping, Sequence


def _file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _identity(path: str | None, *, source_only: bool = False) -> dict[str, Any]:
    if not path:
        return {"path": None, "status": "not_supplied", "sha256": None}
    target = Path(path).expanduser().resolve()
    if target.is_file():
        return {"path": str(target), "status": "file", "sha256": _file_digest(target)}
    if not target.is_dir():
        return {"path": str(target), "status": "missing", "sha256": None}
    digest = hashlib.sha256()
    count = 0
    for child in sorted(target.rglob("*")):
        if not child.is_file():
            continue
        if source_only and child.suffix not in {".py", ".so", ".pyd"}:
            continue
        relative = child.relative_to(target).as_posix()
        digest.update(f"{relative}\0{_file_digest(child)}\n".encode("utf-8"))
        count += 1
    return {"path": str(target), "status": "directory", "sha256": digest.hexdigest(),
            "file_count": count}


def redrock_authority(command: Sequence[str], environment: Mapping[str, str],
                      *, archetype_dir: str | None = None) -> dict[str, Any]:
    """Describe exactly the command and external inputs selected for rrdesi."""
    binary = shutil.which(command[0])
    try:
        version = importlib.metadata.version("redrock")
    except importlib.metadata.PackageNotFoundError:
        version = None
    try:
        spec = importlib.util.find_spec("redrock")
    except (ImportError, ValueError):
        spec = None
    package_dir = next(iter(spec.submodule_search_locations), None) if spec and spec.submodule_search_locations else None
    return {
        "schema": "forma-redrock-external-authority-v1",
        "argv": list(command),
        "binary": _identity(binary),
        "package_probe": {
            "scope": "FORMA Python interpreter; rrdesi may use another interpreter",
            "version": version,
            "source": _identity(package_dir, source_only=True),
        },
        "templates": _identity(environment.get("RR_TEMPLATE_DIR")),
        "archetypes": _identity(archetype_dir),
        "selected_environment": {
            "OMP_NUM_THREADS": environment.get("OMP_NUM_THREADS"),
            "RR_TEMPLATE_DIR": environment.get("RR_TEMPLATE_DIR"),
        },
        "other_environment": "inherited; values not recorded",
        "omitted_options": "Redrock defaults; interpretation requires the recorded binary identity",
    }


def write_redrock_authority(path: str | Path, document: Mapping[str, Any]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
