"""One independent FA reality vote from a frozen VI measurement and local pixels."""

from __future__ import annotations

import math
import json
from pathlib import Path
from typing import Any, Literal, MutableMapping

import numpy as np
from langchain.agents import create_agent
from langchain_core.tools import tool
from pydantic import BaseModel, ConfigDict

from FORMA.core.config.analysis_method import load_analysis_method

from .execution_artifacts import ExecutionAllocation, validate_execution
from .node_keys import fa_node_key
from .sh_pre_analysis import PROMPT_DIR, _render
from .vi_measurements import _sha256
from .vote_runtime import VoteSessionFailure, prompt_identity, run_vote_session


class _RealityArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answer: Literal["yes", "no"]


def measured_feature_width(measurement: dict) -> tuple[float | None, float | None]:
    """Read the frozen observation's FWHM without exposing a line identity."""
    record = measurement["record"]
    if measurement["source"] == "CWT":
        values = record.get("FWHM_A"), record.get("FWHM_km_s")
    else:
        values = record.get("fwhm"), record.get("fwhm_km_s")
    return tuple(float(value) if isinstance(value, (int, float))
                 and not isinstance(value, bool) and math.isfinite(value) and value > 0
                 else None for value in values)


def build_feature_window(npz_path: str | Path, *, center: float, kind: str,
                         masked_regions: list | None = None,
                         half_width: float | None = None,
                         measured_fwhm_angstrom: float | None = None,
                         measured_fwhm_km_s: float | None = None) -> str:
    """Render local flux and usability; IVAR remains internal to validity/noise."""
    if kind not in ("emission", "absorption") or not math.isfinite(center):
        raise ValueError("candidate needs a finite center and emission/absorption kind")
    if half_width is None:
        half_width = load_analysis_method().audit.feature_read_half_angstrom
    if not math.isfinite(half_width) or half_width <= 0:
        raise ValueError("half_width must be positive and finite")
    with np.load(npz_path) as spectrum:
        wavelength = spectrum["wavelength"]
        flux = spectrum["flux"]
        ivar = spectrum["ivar"] if "ivar" in spectrum else np.full_like(flux, np.nan)
    if wavelength.ndim != 1 or flux.shape != wavelength.shape or ivar.shape != wavelength.shape:
        raise ValueError("invalid spectrum array shapes")
    selected = (wavelength >= center - half_width) & (wavelength <= center + half_width)
    wl, fl, iv = wavelength[selected], flux[selected], ivar[selected]
    if not len(wl):
        raise ValueError("no samples in target window")
    finite = np.isfinite(wl) & np.isfinite(fl) & np.isfinite(iv) & (iv > 0)
    masked = np.zeros(len(wl), dtype=bool)
    for start, end in masked_regions or []:
        masked |= (wl >= start) & (wl <= end)
    valid = finite & ~masked
    if not valid.any():
        raise ValueError("target window has no usable samples")
    errors = np.sqrt(1.0 / iv[valid])
    rows = ["| wavelength (Å) | flux | usable |", "|---:|---:|---|"]
    for wavelength_i, flux_i, good in zip(wl, fl, valid):
        rows.append(f"| {wavelength_i:.8g} | {flux_i:.8g} | "
                    f"{'yes' if good else 'no'} |")
    return _render("fa_real_feature_user.md", {
        "emission_or_absorption": kind,
        "candidate_center_angstrom": f"{center:.8g}",
        "measured_fwhm_angstrom": (
            f"{measured_fwhm_angstrom:.8g}" if measured_fwhm_angstrom is not None
            else "unavailable"),
        "measured_fwhm_km_s": (
            f"{measured_fwhm_km_s:.8g}" if measured_fwhm_km_s is not None
            else "unavailable"),
        "requested_window_angstrom": f"[{center-half_width:.8g}, {center+half_width:.8g}]",
        "actual_window_angstrom": f"[{wl[0]:.8g}, {wl[-1]:.8g}]",
        "validity_summary": f"{int(valid.sum())}/{len(wl)} usable; "
                            f"{int(masked.sum())} in declared masked regions",
        "local_noise_summary": f"median per-pixel 1σ = {float(np.median(errors)):.6g} flux units "
                               "from positive IVAR; this is not a line-significance estimate",
        "all_window_samples_with_wavelength_flux_and_usability": "\n".join(rows),
    }, PROMPT_DIR)


async def run_feature_reality(*, llm: Any, run_id: str, measurement_id: str,
                              vi_catalog_path: str | Path,
                              session_path: str | Path | None = None,
                              execution: ExecutionAllocation | None = None,
                              node_store: MutableMapping[str, dict] | None = None,
                              agent_factory=create_agent,
                              recursion_limit: int = 30,
                              frozen_prompt_identity: dict | None = None) -> dict:
    """Submit one binary judgment; measurement ID stays out of model messages."""
    if not run_id or not measurement_id:
        raise ValueError("run and measurement IDs are required")
    key = fa_node_key(run_id, measurement_id)
    if execution is not None:
        validate_execution(execution)
        if execution.run_id != run_id or execution.node_key != key:
            raise ValueError("FA target differs from allocated execution")
        if session_path is not None:
            raise ValueError("allocated execution chooses FA session path")
        session_path = execution.path("session.md")
    if session_path is None:
        raise ValueError("FA session path or an execution allocation is required")
    catalog_path = Path(vi_catalog_path).resolve(strict=True)
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    if catalog.get("run_id") != run_id:
        raise ValueError("VI catalog belongs to another run")
    matches = [item for item in catalog.get("measurements", [])
               if item.get("id") == measurement_id]
    if len(matches) != 1 or not matches[0].get("adoptable"):
        raise ValueError("measurement ID is absent, duplicate, or not adoptable")
    measurement = matches[0]
    kind = measurement["kind"]
    record = measurement["record"]
    center = record.get("wavelength") if measurement["source"] == "CWT" else record.get("center")
    if not isinstance(center, (int, float)) or not math.isfinite(center):
        raise ValueError("measurement has no finite centre")
    npz_path = Path(catalog["spectrum_npz_path"]).resolve(strict=True)
    if _sha256(npz_path) != catalog["spectrum_npz_sha256"]:
        raise ValueError("spectrum changed since VI catalog was frozen")
    width_a, width_kms = measured_feature_width(measurement)
    user = build_feature_window(
        npz_path, center=center, kind=kind,
        masked_regions=catalog.get("masked_regions"),
        measured_fwhm_angstrom=width_a, measured_fwhm_km_s=width_kms)
    system = (PROMPT_DIR / "fa_real_feature_system.md").read_text(encoding="utf-8")
    identity = prompt_identity(system, user, "submit_feature_reality")
    if frozen_prompt_identity is not None and identity != frozen_prompt_identity:
        raise ValueError("FA prompt differs from the frozen vote-seat input")
    store_key = execution.node_execution_id if execution is not None else key
    store = node_store if node_store is not None else {}
    if store_key in store:
        raise ValueError("FA vote already exists for this target")
    submitted = None

    @tool("submit_feature_reality", args_schema=_RealityArgs)
    def submit_feature_reality(answer: Literal["yes", "no"]) -> dict:
        """Bind a yes/no reality answer to this session's single target."""
        nonlocal submitted
        if submitted is not None:
            return {"ok": False, "error": "answer already submitted"}
        submitted = {"key": key, "measurement_id": measurement_id,
                     "answer": answer, "center": center, "kind": kind,
                     "vi_catalog_path": str(catalog_path),
                     "vi_catalog_sha256": _sha256(catalog_path),
                     "spectrum_npz_sha256": catalog["spectrum_npz_sha256"],
                     "prompt_identity": identity,
                     "session_path": str(Path(session_path).resolve())}
        if execution is not None:
            submitted["execution"] = execution.metadata()
        store[store_key] = submitted
        return {"ok": True}

    calls = None
    try:
        calls = await run_vote_session(
            llm=llm, allocation=execution, system=system, user=user,
            tool=submit_feature_reality, tool_name="submit_feature_reality",
            completed=lambda: submitted is not None,
            agent_factory=agent_factory, recursion_limit=recursion_limit,
            stage="observed feature reality", subject_ref=measurement_id,
            subject_label="Measurement (internal)", session_path=session_path,
            run_id=run_id)
        if submitted is None:
            raise RuntimeError("feature vote session returned without a submission")
        submitted["session_sha256"] = _sha256(Path(session_path))
        if execution is not None:
            with execution.path("node.json").open("x", encoding="utf-8") as stream:
                json.dump(submitted, stream, ensure_ascii=False, indent=2, allow_nan=False)
                stream.write("\n")
    except Exception as exc:
        store.pop(store_key, None)
        if calls is not None and not isinstance(exc, VoteSessionFailure):
            raise VoteSessionFailure(exc, calls) from exc
        raise
    return {"node": submitted, "model_usage": calls,
            "system_prompt": system, "user_prompt": user}
