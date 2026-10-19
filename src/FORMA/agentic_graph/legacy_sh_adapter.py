"""Explicit adapter for the existing SH spectrum context and measurement tools.

The new node owns its prompts, state and validation. This module reads the VI
catalog and borrows the reviewed prompt context and measurement write tool.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, MutableMapping

from FORMA.agents.multi_agents.harness import single_hypothesis as legacy_sh

from .sh_line_review import run_sh_line_review
from .execution_artifacts import ExecutionAllocation
from .sh_measurement_refs import build_id_writer, render_catalog
from .vi_measurements import _sha256


async def run_with_existing_sh_inputs(
    *,
    llm: Any,
    run_id: str,
    hypothesis_ref: str,
    hypothesis_redshift: float,
    fits_path: str,
    npz_path: str,
    csv_path: str | Path | None = None,
    report_path: str | Path | None = None,
    vi_catalog_path: str | Path,
    execution: ExecutionAllocation | None = None,
    snr_median: float | None = None,
    node_store: MutableMapping[str, dict[str, Any]] | None = None,
    recursion_limit: int = 100,
    agent_factory: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    """Run SH from a frozen VI catalog; no fitting or ID allocation occurs here."""
    import numpy as np

    if execution is not None:
        if csv_path is not None or report_path is not None:
            raise ValueError("allocated execution chooses SH output paths")
        csv_path, report_path = execution.path("lines.csv"), execution.path("report.md")
    if csv_path is None or report_path is None:
        raise ValueError("SH output paths or an execution allocation are required")

    catalog_path = Path(vi_catalog_path).resolve(strict=True)
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    if (catalog.get("run_id") != run_id
            or catalog.get("hypothesis_ref") != hypothesis_ref
            or catalog.get("redshift") != hypothesis_redshift):
        raise ValueError("VI measurement catalog does not match this SH hypothesis")
    if Path(catalog.get("spectrum_npz_path", "")).resolve() != Path(npz_path).resolve():
        raise ValueError("VI measurement catalog belongs to another spectrum")
    if catalog.get("spectrum_npz_sha256") != _sha256(Path(npz_path)):
        raise ValueError("spectrum changed since the VI measurement catalog was frozen")
    with np.load(npz_path) as spectrum:
        wl = spectrum["wavelength"]
        actual_min, actual_max = float(np.min(wl)), float(np.max(wl))
    if (catalog["wavelength_min"] != actual_min
            or catalog["wavelength_max"] != actual_max):
        raise ValueError("VI measurement catalog wavelength coverage has changed")
    vi_peaks = [item["record"] for item in catalog["measurements"] if item["source"] == "CWT" and item["kind"] == "emission"]
    vi_troughs = [item["record"] for item in catalog["measurements"] if item["source"] == "CWT" and item["kind"] == "absorption"]
    csv_target = Path(csv_path).resolve()
    judgment_path = csv_target.with_name(csv_target.stem + "_judgments.json")
    if judgment_path.exists():
        raise FileExistsError("SH judgments already exist for this node")
    context = legacy_sh._build_user_message(
        hypothesis_redshift, fits_path, npz_path,
        wavelength_min=actual_min, wavelength_max=actual_max,
        snr_median=snr_median, peaks=vi_peaks, troughs=vi_troughs,
        z_min=catalog["z_min"], z_max=catalog["z_max"],
        masked_regions=catalog["masked_regions"],
        csv_path=str(Path(csv_path).resolve()),
        report_path=None,
        fit_attempts=catalog["fit_attempts"], pre_analysis=True,
    )
    former_phase = "Phases: evaluate all lines → write CSV → write report → wait for the second user message."
    if context.count(former_phase) != 1:
        raise ValueError("legacy SH context no longer has its expected phase marker")
    context = context.replace(
        former_phase,
        "Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.")
    context += "\n" + render_catalog(catalog)
    agent_kwargs = {"agent_factory": agent_factory} if agent_factory is not None else {}
    return await run_sh_line_review(
        llm=llm, run_id=run_id, hypothesis_ref=hypothesis_ref,
        hypothesis_redshift=hypothesis_redshift, sh_context=context,
        csv_path=csv_path,
        csv_writer=build_id_writer(catalog, masked_regions=catalog["masked_regions"],
                                   judgment_path=judgment_path),
        measurement_catalog_path=catalog_path,
        judgment_path=judgment_path,
        node_store=node_store, recursion_limit=recursion_limit, execution=execution,
        **agent_kwargs,
    )
