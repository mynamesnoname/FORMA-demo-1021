"""Run VI → SH → FA → type graphs → HS merge and comparison.

The controller owns scheduling and route validation. Agents run inside nodes;
their submissions do not invoke graph transitions directly. This pilot ends
after a provisional HS comparison, before RA and final reporting.
"""

from __future__ import annotations

import asyncio
import json
import re
import uuid
from pathlib import Path
from typing import Any, Callable

from FORMA.agents.multi_agents.harness import single_hypothesis as legacy_sh
from FORMA.core.config.model_calls import temperature_for
from FORMA.core.llm import (_build_thinking_extra_body, _create_chat_openai,
                            _detect_vendor)

from .elg_path import run_elg_path_through_report
from .execution_artifacts import allocate_execution
from .fa_advisory import review_fa_advisories
from .fa_review import review_feature_reality
from .feature_registry import build_feature_registry
from .hs_comparison import run_hs_comparison
from .hs_merge import run_hs_merge
from .legacy_sh_adapter import run_with_existing_sh_inputs
from .lrg_bgs_path import run_lrg_bgs_path_through_report
from .node_keys import sh_node_key
from .qso_entry import run_qso_entry
from .qso_report import run_qso_entry_through_report
from .type_entry_router import route_type_entry
from .reasoning_trace import (bind_artifact_root, new_trace, record_analysis,
                              record_type_fallback,
                              write_trace)
from .vi_fits_adapter import prepare_fits_inputs
from .browser_visualization import write_browser_bundle


_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


class SHBatchIncompleteError(RuntimeError):
    """One or more SH attempts failed; successful sibling artifacts are retained."""


class GraphWorkflow:
    """One spectrum per instance call; all results belong to its output root."""

    def __init__(self, configs, *, model_factory: Callable[[str], Any] | None = None,
                 sh_runner: Callable[..., Any] = run_with_existing_sh_inputs,
                 fa_reviewer: Callable[..., Any] = review_feature_reality,
                 fa_advisory_reviewer: Callable[..., Any] = review_fa_advisories,
                 vi_preparer: Callable[..., dict] = prepare_fits_inputs):
        self.configs = configs
        self.model_factory = model_factory or self._model_for
        self.sh_runner = sh_runner
        self.fa_reviewer = fa_reviewer
        self.fa_advisory_reviewer = fa_advisory_reviewer
        self.vi_preparer = vi_preparer

    def _model_for(self, stage: str):
        config = self.configs.model.llm
        vendor = _detect_vendor(config["base_url"])
        return _create_chat_openai(
            model=config["model"], api_key=config["api_key"],
            base_url=config["base_url"], temperature=temperature_for(stage),
            max_tokens=legacy_sh._resolve_max_tokens(),
            extra_body=(_build_thinking_extra_body("disabled", vendor)
                        if vendor != "unknown" else None))

    async def run_fits(self, fits_path: str | Path, output_root: str | Path,
                       *, sh_concurrency: int = 4, fa_concurrency: int = 4,
                       fa_max_attempts: int = 2) -> dict:
        """Start a new graph run from FITS; never reuse an old output tree."""
        fits = Path(fits_path).resolve(strict=True)
        root = Path(output_root).resolve()
        if root.exists():
            raise FileExistsError("graph output directory must be new")
        if self.configs.io.input_format != "fits":
            raise ValueError("graph workflow currently accepts FITS inputs only")
        if sh_concurrency < 1 or fa_concurrency < 1 or fa_max_attempts < 1:
            raise ValueError("concurrency and retry limits must be positive")
        root.mkdir(parents=True)
        run_id = f"graph-{uuid.uuid4().hex}"
        try:
            prepared = await asyncio.to_thread(
                self.vi_preparer, fits_path=fits, run_id=run_id,
                output_root=root, params=self.configs.params)
            manifest = json.loads(Path(prepared["manifest_path"]).read_text(encoding="utf-8"))
            if manifest.get("run_id") != run_id:
                raise ValueError("VI manifest run ID differs from the graph run")
            result = await self.run_prepared(
                manifest_path=prepared["manifest_path"],
                fits_path=prepared["fits_path"], output_root=root,
                snr_median=prepared["snr_median"],
                sh_concurrency=sh_concurrency, fa_concurrency=fa_concurrency,
                fa_max_attempts=fa_max_attempts)
            await asyncio.to_thread(write_browser_bundle, root,
                                    manifest_path=prepared["manifest_path"])
            return result
        except BaseException as exc:
            outcome = {"schema_version": "forma-agentic-run-outcome-v1",
                       "run_id": run_id, "status": "failed",
                       "error_type": type(exc).__name__,
                       "final_classification_available": False}
            (root / "run_outcome.json").write_text(
                json.dumps(outcome, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")
            raise

    async def run_prepared(self, *, manifest_path: str | Path,
                           fits_path: str | Path, output_root: str | Path,
                           snr_median: float | None = None,
                           sh_concurrency: int = 4, fa_concurrency: int = 4,
                           fa_max_attempts: int = 2) -> dict:
        """Run all SH sessions, then the branch-aware FA/type graph stages."""
        if sh_concurrency < 1:
            raise ValueError("SH concurrency must be positive")
        manifest_file = Path(manifest_path).resolve(strict=True)
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        root = Path(output_root).resolve()
        root.mkdir(parents=True, exist_ok=True)
        fits = Path(fits_path).resolve(strict=True)
        sem = asyncio.Semaphore(sh_concurrency)
        sh_model = self.model_factory("single_hypothesis")
        node_paths = {}
        sh_failures = {}

        async def one(ref: str, info: dict) -> None:
            if not _SAFE_NAME.fullmatch(ref):
                raise ValueError("unsafe hypothesis reference")
            allocation = allocate_execution(
                root, run_id=manifest["run_id"], branch_id="main",
                node_key=sh_node_key(manifest["run_id"], ref))
            try:
                async with sem:
                    await self.sh_runner(
                        llm=sh_model, run_id=manifest["run_id"], hypothesis_ref=ref,
                        hypothesis_redshift=info["redshift"], fits_path=str(fits),
                        npz_path=manifest["spectrum_npz_path"],
                        vi_catalog_path=info["catalog_path"], execution=allocation,
                        snr_median=snr_median)
                if not allocation.path("node.json").is_file():
                    raise FileNotFoundError("SH runner did not write node.json")
                node_paths[ref] = allocation.path("node.json")
            except Exception as exc:
                sh_failures[ref] = type(exc).__name__

        async with asyncio.TaskGroup() as group:
            for ref, info in manifest["hypotheses"].items():
                group.create_task(one(ref, info))
        (root / "sh_batch_summary.json").write_text(
            json.dumps({"schema_version": "forma-sh-batch-summary-v1",
                        "run_id": manifest["run_id"],
                        "completed": {ref: str(node_paths[ref]) for ref in sorted(node_paths)},
                        "failed": {ref: sh_failures[ref] for ref in sorted(sh_failures)}},
                       ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if sh_failures:
            raise SHBatchIncompleteError(
                "SH incomplete for " + ", ".join(sorted(sh_failures))
                + "; successful sibling nodes and sh_batch_summary.json are preserved")
        if set(node_paths) != set(manifest["hypotheses"]):
            raise RuntimeError("SH did not complete every Redrock hypothesis")
        return await self.run_from_sh(
            manifest_path=manifest_file, sh_node_paths=list(node_paths.values()),
            output_root=root, fa_concurrency=fa_concurrency,
            fa_max_attempts=fa_max_attempts)

    async def run_from_sh(self, *, manifest_path: str | Path,
                          sh_node_paths: list[str | Path], output_root: str | Path,
                          fa_concurrency: int = 4, fa_max_attempts: int = 2) -> dict:
        """Resume at the complete frozen SH boundary; then dispatch type graphs."""
        root = Path(output_root).resolve()
        root.mkdir(parents=True, exist_ok=True)
        registry = build_feature_registry(manifest_path, sh_node_paths)
        if any(not _SAFE_NAME.fullmatch(ref) for ref in registry["hypotheses"]):
            raise ValueError("unsafe hypothesis reference in SH archive")
        trace = new_trace(registry)
        bind_artifact_root(trace, root)
        for ref in registry["hypotheses"]:
            record_analysis(trace, "main", kind="sh_pre_analysis_import",
                            analysis_ref=ref, artifact_refs=[f"sh/{ref}/node"])
        write_trace(trace, root / "trace_after_sh.json")
        fa_model = self.model_factory("feature_audit")
        fa_summary = await self.fa_reviewer(
            trace=trace, branch_id="main", vi_manifest_path=manifest_path,
            output_root=root, llm=fa_model, concurrency=fa_concurrency,
            max_attempts_per_vote=fa_max_attempts)
        await self.fa_advisory_reviewer(
            trace=trace, branch_id="main", output_root=root, llm=fa_model,
            concurrency=fa_concurrency)
        write_trace(trace, root / "trace_after_fa_advisory.json")
        graph_model = self.model_factory("single_hypothesis")
        routes = {}
        for ref, hypothesis in registry["hypotheses"].items():
            sh_node = json.loads(Path(trace["artifacts"][f"sh/{ref}/node"]["path"]).read_text(encoding="utf-8"))
            code_route = None
            if sh_node.get("schema_version") == "forma-sh-line-review-v1":
                code_route = route_type_entry(trace, branch_id="main",
                                              hypothesis_ref=ref, output_root=root)
                hypothesis = trace["branches"]["main"]["state"]["registry"]["hypotheses"][ref]
            classification = hypothesis["classification"]
            if classification is None:
                if code_route is None:
                    result = run_qso_entry(trace, branch_id="main",
                                           hypothesis_ref=ref, output_root=root)
                    path_status = result["path_status"]
                else:
                    path_status = "unresolved"
                routes[ref] = {"preliminary_classification": None,
                               "entry_route_ref": code_route["artifact_ref"] if code_route else None,
                               "path_status": path_status,
                               "candidate_type": None, "report_ref": None}
            elif classification in {"Type 1 QSO", "Type 2 QSO"}:
                result = await run_qso_entry_through_report(
                    trace, branch_id="main", hypothesis_ref=ref,
                    output_root=root, llm=graph_model)
                qso_report = result["report"]
                terminal = (result["type1"]["path_status"] if result["type1"]
                            else result["entry"]["path_status"])
                candidate = (result["type1"].get("candidate_type") if result["type1"]
                             else result["entry"].get("candidate_type"))
                routes[ref] = {"preliminary_classification": classification,
                               "path_status": terminal, "candidate_type": candidate,
                               "report_ref": (qso_report["artifact_refs"]["report"]
                                              if qso_report else None)}
            elif classification == "ELG":
                result = await run_elg_path_through_report(
                    trace, branch_id="main", hypothesis_ref=ref,
                    output_root=root, llm=graph_model)
                qso_terminal = result.get("qso_type1") or result["qso_entry"]
                effective_status = (qso_terminal["path_status"]
                                    if qso_terminal else result["path_status"])
                routes[ref] = {"preliminary_classification": classification,
                               "path_status": effective_status,
                               "source_path_status": result["path_status"],
                               "candidate_type": (qso_terminal.get("candidate_type")
                                                  if qso_terminal else result["candidate_type"]),
                               "report_ref": result["report_ref"],
                               "qso_report_ref": (result["qso_report"]["artifact_refs"]["report"]
                                                  if result["qso_report"] else None)}
            elif classification == "LRG/BGS":
                result = await run_lrg_bgs_path_through_report(
                    trace, branch_id="main", hypothesis_ref=ref,
                    output_root=root, llm=graph_model)
                initial_result = result
                fallback = None
                if (code_route is not None and result["path_status"] == "dead"
                        and "ELG" in code_route["node"]["output"]["eligible_graphs"]):
                    initial_route = next(item for item in result["nodes"]
                                         if item["node"]["node_type"] == "lrg_bgs.route_result")
                    fallback = record_type_fallback(
                        trace, "main", hypothesis_ref=ref, from_graph="LRG/BGS",
                        to_graph="ELG", route_ref=initial_route["artifact_ref"],
                        entry_route_ref=code_route["artifact_ref"])
                    result = await run_elg_path_through_report(
                        trace, branch_id="main", hypothesis_ref=ref,
                        output_root=root, llm=graph_model)
                qso_terminal = result.get("qso_type1") or result["qso_entry"]
                effective_status = (qso_terminal["path_status"]
                                    if qso_terminal else result["path_status"])
                routes[ref] = {"preliminary_classification": classification,
                               "path_status": effective_status,
                               "source_path_status": result["path_status"],
                               "candidate_type": (qso_terminal.get("candidate_type")
                                                  if qso_terminal else result["candidate_type"]),
                               "report_ref": result["report_ref"],
                               "qso_report_ref": (result["qso_report"]["artifact_refs"]["report"]
                                                  if result["qso_report"] else None)}
                if fallback is not None:
                    routes[ref].update({
                        "initial_graph_status": initial_result["path_status"],
                        "initial_graph_report_ref": initial_result["report_ref"],
                        "fallback_from_graph": "LRG/BGS",
                        "fallback_to_graph": "ELG",
                        "fallback_source_route_ref": fallback["payload"]["route_ref"],
                    })
            else:
                raise ValueError(f"unsupported preliminary class: {classification!r}")
            if code_route is not None:
                routes[ref]["entry_route_ref"] = code_route["artifact_ref"]
                routes[ref]["eligible_graphs"] = code_route["node"]["output"]["eligible_graphs"]
            # Every finished hypothesis has a replayable checkpoint; a later
            # failure does not erase successful sibling routes.
            write_trace(trace, root / f"trace_after_{ref}.json")
        hs = run_hs_merge(trace, branch_id="main", routes=routes, output_root=root)
        hs_model = (self.model_factory("hypothesis_synthesis")
                    if len(hs["node"]["output"]["groups"]) > 1 else None)
        comparison = await run_hs_comparison(
            trace, branch_id="main", hs=hs, routes=routes,
            output_root=root, llm=hs_model)
        write_trace(trace, root / "reasoning_tree.json")
        summary = {"schema_version": "forma-agentic-graph-summary-v2",
                   "run_id": registry["run_id"], "status": "hs_comparison_complete",
                   "final_classification_available": False,
                   "active_branch_id": "main", "hypotheses": routes,
                   "surviving_hypotheses": [ref for ref, row in routes.items()
                                            if row["path_status"] == "survive"],
                   "hs_merge_ref": hs["artifact_ref"],
                   "hs_comparison_ref": comparison["artifact_refs"]["node"],
                   "hs_comparison": comparison["node"]["output"],
                   "hs_groups": [{"group_id": group["group_id"],
                                  "candidate_type": group["candidate_type"],
                                  "member_hypotheses": group["member_hypotheses"],
                                  "merge_status": group["merge_status"],
                                  "merged_anchor_redshift": group["merged_anchor_redshift"]}
                                 for group in comparison["effective_groups"]],
                   "hs_initial_groups": [{"group_id": group["group_id"],
                                          "member_hypotheses": group["member_hypotheses"]}
                                         for group in hs["node"]["output"]["groups"]],
                   "fa_summary": fa_summary,
                   "reasoning_tree_path": str(root / "reasoning_tree.json")}
        (root / "type_graph_summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
            encoding="utf-8")
        return summary
