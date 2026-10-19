"""Demo runner: five-spectrum agentic graph investigation through HS.

Run from the repository root:

    python demo.py --preflight-only                 # FITS labels only; no Redrock, no model
    python demo.py --samples QSO_116                # one sample
    python demo.py                                  # BGS_2, ELG_6, LRG_1, QSO_4, QSO_116

The graph stops after the provisional HS comparison: it reports a type-stage
candidate or an abstention, never a final classification. Full runs use the
configured ``.env`` and write an immutable directory under ``.data/output_``.

从仓库根目录运行。预检只读 FITS 标签，不调用 Redrock 或模型；完整运行使用 `.env`
配置，并在 `.data/output_` 下创建不可变的新目录。图止于 HS 暂定比较：输出类型阶段
候选或弃权，而不是最终分类。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

SAMPLES = ("BGS_2", "ELG_6", "LRG_1", "QSO_4", "QSO_116")
DEFAULT_OUTPUT = ROOT / ".data" / "output_" / "demo"
SCHEMA = "forma-demo-hs-run-v1"


def read_truth(path: Path) -> dict:
    """The FIBERMAP label row used only as a diagnostic reference."""
    from astropy.io import fits

    with fits.open(path, memmap=False) as hdul:
        if "FIBERMAP" not in hdul or hdul["FIBERMAP"].data is None:
            raise ValueError(f"{path.name} lacks FIBERMAP data")
        data = hdul["FIBERMAP"].data
        if len(data) != 1 or not {"VI_Z", "VI_SPECTYPE", "VI_QUALITY"}.issubset(data.names):
            raise ValueError(f"{path.name} needs one fully labeled FIBERMAP row")
        row = data[0]
        return {"vi_z": float(row["VI_Z"]),
                "vi_spectype": str(row["VI_SPECTYPE"]).strip(),
                "vi_quality": float(row["VI_QUALITY"])}


def summarize(name: str, truth: dict, result: dict) -> dict:
    """VI comparison is diagnostic; RA and the final classification are absent."""
    groups = {group["group_id"]: group for group in result["hs_groups"]}
    comparison = result["hs_comparison"]
    winner_id = comparison["winner_group_id"]
    if winner_id is not None and winner_id not in groups:
        raise ValueError("HS winner is absent from the group index")
    winner = groups.get(winner_id)
    redshift = winner["merged_anchor_redshift"] if winner else None
    expected = "LRG/BGS" if truth["vi_spectype"] in {"LRG", "BGS"} else truth["vi_spectype"]
    matches = (None if winner is None else
               winner["candidate_type"] in ({"Type 1 QSO", "Type 2 QSO"}
                                            if expected == "QSO" else {expected}))
    return {"sample": name, "workflow_status": result["status"],
            "final_classification_available": result["final_classification_available"],
            "truth": truth, "surviving_hypotheses": result["surviving_hypotheses"],
            "hs_group_count": len(groups), "hs_comparison_ref": result["hs_comparison_ref"],
            "hs_status": comparison["status"], "winner_group_id": winner_id,
            "winner_type": winner["candidate_type"] if winner else None,
            "winner_member_hypotheses": winner["member_hypotheses"] if winner else [],
            "winner_redshift": redshift,
            "absolute_vi_redshift_error": (
                abs(redshift - truth["vi_z"]) if redshift is not None else None),
            "type_matches_vi": matches, "ra_review_pending": comparison["ra_review_pending"],
            "comparison_reason": comparison["reason"]}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--samples", nargs="+", choices=SAMPLES, default=list(SAMPLES),
                        help="ordered sample subset (default: all five)")
    parser.add_argument("--preflight-only", action="store_true",
                        help="inspect FITS labels and inputs, with no model or Redrock calls")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT,
                        help="parent directory for a new immutable run directory")
    parser.add_argument("--sh-concurrency", type=int, default=4)
    parser.add_argument("--fa-concurrency", type=int, default=4)
    parser.add_argument("--fa-max-attempts", type=int, default=2)
    return parser.parse_args(argv)


async def run(args: argparse.Namespace) -> int:
    samples = list(dict.fromkeys(args.samples))
    inputs = {name: ROOT / "example" / "basic" / f"{name}.fits" for name in samples}
    truth = {name: read_truth(path) for name, path in inputs.items()}
    if args.preflight_only:
        print(json.dumps({"status": "preflight_ok", "sample_count": len(samples),
                          "samples": truth, "redrock_calls": 0, "model_calls": 0},
                         ensure_ascii=False, indent=2))
        return 0
    if min(args.sh_concurrency, args.fa_concurrency, args.fa_max_attempts) < 1:
        raise ValueError("concurrency and attempt limits must be positive")
    from dotenv import load_dotenv
    from FORMA.agentic_graph.graph_workflow import GraphWorkflow
    from FORMA.core.config.model_config import ModelConfig
    from FORMA.core.config.params_config import ParamsConfig

    load_dotenv(ROOT / ".env")
    configs = SimpleNamespace(io=SimpleNamespace(input_format="fits"),
                              model=ModelConfig.from_env(), params=ParamsConfig.from_env())
    runner = GraphWorkflow(configs)
    parent = args.output_root.resolve()
    parent.mkdir(parents=True, exist_ok=True)
    run_dir = parent / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                        + "-" + uuid.uuid4().hex[:8])
    run_dir.mkdir(exist_ok=False)
    index_path = run_dir / "index.json"
    index = {"schema_version": SCHEMA, "status": "running",
             "samples_requested": samples,
             "source_dir": str(ROOT / "example" / "basic"), "results": []}

    def save() -> None:
        index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2,
                                         allow_nan=False) + "\n", encoding="utf-8")

    save()
    for name in samples:
        target = run_dir / name
        try:
            result = await runner.run_fits(
                inputs[name], target, sh_concurrency=args.sh_concurrency,
                fa_concurrency=args.fa_concurrency,
                fa_max_attempts=args.fa_max_attempts)
            if result["status"] != "hs_comparison_complete" or result["final_classification_available"]:
                raise ValueError("graph returned an unexpected HS-stage status")
            row = summarize(name, truth[name], result)
            row["output_root"] = str(target)
        except Exception as exc:
            row = {"sample": name, "workflow_status": "failed",
                   "output_root": str(target), "truth": truth[name],
                   "error_type": type(exc).__name__,
                   "error": str(exc)[:800]}
        index["results"].append(row)
        save()
        print(f"{name}: {row['workflow_status']} | {target}", flush=True)
    failures = [row for row in index["results"] if row["workflow_status"] == "failed"]
    index["status"] = "completed_with_failures" if failures else "completed"
    save()
    print(f"Index: {index_path}")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    return asyncio.run(run(parse_args(argv)))


if __name__ == "__main__":
    raise SystemExit(main())
