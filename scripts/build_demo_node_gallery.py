"""Build a portable, read-only node gallery for a completed basic demo run.

The generated page uses local JavaScript data, so it also works via file://.
It projects selected node outputs into cards and never embeds raw trace dumps.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


STAGES = ["VI", "SH", "FA", "ROUTE", "GRAPH", "HS"]
IGNORED = {
    "schema_version", "graph_version", "run_id", "branch_id", "node_key",
    "node_execution_id", "attempt_id", "input_refs", "source_refs",
    "evidence_refs", "attempt_refs", "vote_refs", "method_snapshot",
    "method_snapshot_sha256", "prompt_identity", "model_usage", "execution",
    "session_sha256", "context_sha256", "report_sha256", "system_prompt_sha256",
    "user_prompt_sha256", "strict_broad_threshold_payload_sha256",
    "fa_vote_artifact_refs", "state_source_refs", "vi_catalog_sha256",
    "spectrum_npz_sha256", "session_path", "vi_catalog_path",
    "measurement_catalog_path", "measurement_catalog_sha256", "csv_path",
    "csv_sha256", "judgment_path", "judgment_sha256", "session_stage1_path",
    "session_stage1_sha256", "adopted_lines_plot_path", "adopted_lines_plot_sha256",
}
LABELS = {
    "pre_analysis": "谱线预分析", "entry_router": "类型入口路由",
    "initial_route": "初始类型入口", "alignment": "谱线对齐",
    "real_doublet_or_not": "双线审查", "real_lya_forest_or_not": "Lyα forest 审查",
    "merge_groups": "假设合并", "compare_groups": "跨组比较",
    "evidence_view": "清洗后的谱线", "broad_line_inventory": "宽线清单",
    "missing_broad_line_queue": "缺线复核队列", "type1_formal_gate": "Type 1 形式门",
    "route_result": "类型图出口", "analysis_report": "类型分析报告",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def clean(value, depth=0):
    """Keep scientific decisions; elide provenance internals and very large payloads."""
    if depth > 4:
        return "…"
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            if key in IGNORED or key.endswith("_sha256") or key.endswith("_path"):
                continue
            if key in {"source_reports", "report_markdown", "session", "trace"}:
                continue
            out[key] = clean(item, depth + 1)
        return out
    if isinstance(value, list):
        limit = 36 if depth < 2 else 15
        out = [clean(item, depth + 1) for item in value[:limit]]
        if len(value) > limit:
            out.append(f"另有 {len(value) - limit} 项，见原始产物")
        return out
    if isinstance(value, str):
        return value[:700] + ("…" if len(value) > 700 else "")
    return value


def brief(output):
    if not isinstance(output, dict):
        return "查看节点产物"
    for key in ("reason", "gate_status", "path_status", "candidate_type", "route_status",
                "visibility", "reference_strength", "pair_supported", "selected_initial_graph",
                "status", "next_node"):
        value = output.get(key)
        if value is not None and not isinstance(value, (dict, list)):
            return str(value)[:145]
    for key in ("lines", "groups", "checks", "queue", "collisions", "aligned_claims"):
        if isinstance(output.get(key), list):
            return f"{len(output[key])} 项 {key.replace('_', ' ')}"
    return "展开查看该节点的观测与判断"


def rel_link(path: Path, ui_dir: Path):
    return "../" + str(path.relative_to(ui_dir.parent)).replace("\\", "/")


def add_node(nodes, *, stage, title, subtitle, status, output, path=None, hyp=None,
             graph=None, order=0, links=None, ui_dir=None):
    links = list(links or [])
    if path:
        links.insert(0, {"label": "节点产物", "href": rel_link(path, ui_dir)})
    nodes.append({
        "id": len(nodes), "stage": stage, "title": title, "subtitle": subtitle,
        "status": str(status or "recorded"), "brief": brief(output),
        "hyp": hyp, "graph": graph, "order": order,
        "output": clean(output), "links": links,
    })


def build_sample(run: Path, result: dict, ui_dir: Path):
    sample = result["sample"]
    root = run / sample
    summary = read_json(root / "type_graph_summary.json")
    tree = read_json(root / "reasoning_tree.json")
    event_order = {
        event.get("execution", {}).get("node_execution_id"): i
        for i, event in enumerate(tree.get("branches", {}).get("main", {}).get("events", []))
        if event.get("execution", {}).get("node_execution_id")
    }
    nodes = []
    visual = read_json(root / "visualization_data.json")
    cwt = visual.get("vi", {}).get("cwt_features", [])
    gaussian = visual.get("vi", {}).get("gaussian_measurements", [])
    cwt_count = sum(len(features) for features in cwt.values()) if isinstance(cwt, dict) else len(cwt)
    feature_positions = {}
    cwt_groups = cwt.values() if isinstance(cwt, dict) else [cwt]
    for group in cwt_groups:
        for feature in group:
            if feature.get("feature_id") and feature.get("wavelength") is not None:
                feature_positions[feature["feature_id"]] = feature["wavelength"]
    for feature in gaussian:
        center = feature.get("record", {}).get("center")
        if feature.get("id") and center is not None:
            feature_positions[feature["id"]] = center
    add_node(nodes, stage="VI", title="冻结光谱测量", subtitle="FITS · CWT · Gaussian · Redrock",
             status="complete", output={"CWT features": cwt_count, "Gaussian measurements": len(gaussian),
             "Hypotheses": len(visual.get("sh", {})), "Continuum": visual.get("continuum", {}).get("method")},
             order=0, ui_dir=ui_dir, links=[
                 {"label": "全谱图", "href": rel_link(root / "spectrum.png", ui_dir)},
                 {"label": "特征图", "href": rel_link(root / "VI/features.png", ui_dir)},
             ])

    for hdir in sorted((root / "SH").glob("H*")):
        hyp = hdir.name
        for path in hdir.glob("pre_analysis/branches/*/*/node.json"):
            data = read_json(path)
            judgments_file = path.parent / "lines_judgments.json"
            judgments = read_json(judgments_file) if judgments_file.exists() else []
            counts = Counter(j.get("status", "unknown") for j in judgments)
            matched = [j for j in judgments if j.get("measurement_id") and j.get("status") not in {"NOT_FOUND", "MASKED"}]
            output = {"假设红移": data.get("hypothesis_redshift"), "审查谱线": len(judgments),
                      "状态分布": dict(counts), "采纳或待定的线对": [
                          {"line": j.get("line_id", "").removeprefix("line:"),
                           "feature": j.get("measurement_id"), "status": j.get("status"),
                           "comment": j.get("comment")} for j in matched[:16]]}
            links = [{"label": "谱线表", "href": rel_link(path.parent / "lines.csv", ui_dir)}]
            if judgments_file.exists():
                links.append({"label": "线审判读", "href": rel_link(judgments_file, ui_dir)})
            plot = path.parent / "adopted_lines.png"
            if plot.exists():
                links.append({"label": "采纳谱线图", "href": rel_link(plot, ui_dir)})
            add_node(nodes, stage="SH", title=f"{hyp} · 谱线审查", subtitle="固定红移下的 ID 绑定线表",
                     status=data.get("status"), output=output, path=path, hyp=hyp, order=0,
                     links=links, ui_dir=ui_dir)

    # Each independent vote remains linked, while the UI presents one card per feature.
    votes = defaultdict(list)
    for path in (root / "FA").rglob("node.json"):
        if "real_feature_or_not" not in path.parts:
            continue
        data = read_json(path)
        if "answer" in data:
            votes[data.get("measurement_id", "unknown")].append((path, data))
    for mid, ballots in sorted(votes.items()):
        answers = Counter(item.get("answer", "unknown") for _, item in ballots)
        sample_vote = ballots[0][1]
        hyp = mid.split(":")[1] if mid.startswith("fit:") else None
        output = {"feature ID": mid, "中心波长 Å": sample_vote.get("center"),
                  "信号类型": sample_vote.get("kind"), "独立票数": len(ballots),
                  "赞成": answers.get("yes", 0), "反对": answers.get("no", 0),
                  "票决": "signal_present" if answers.get("yes", 0) > answers.get("no", 0) else "signal_absent",
                  "单票": [{"vote": i + 1, "answer": d.get("answer")} for i, (_, d) in enumerate(ballots)]}
        links = [{"label": f"第 {i} 票", "href": rel_link(p, ui_dir)} for i, (p, _) in enumerate(ballots, 1)]
        add_node(nodes, stage="FA", title=f"特征真实性 · {mid}", subtitle="独立投票 · 同一测量合并展示",
                 status=output["票决"], output=output, hyp=hyp, order=0, links=links, ui_dir=ui_dir)
    for path in sorted((root / "FA").rglob("node.json")):
        if not any(p in path.parts for p in ("real_doublet_or_not", "real_lya_forest_or_not")):
            continue
        data = read_json(path)
        hyp = data.get("hypothesis_ref")
        label = "双线审查" if data.get("doublet_id") else "Lyα forest 审查"
        name = data.get("doublet_id") or data.get("line_id") or "review"
        output = {k: v for k, v in data.items() if k in {
            "doublet_id", "claim_mode", "components", "metrics", "coverage", "status",
            "pair_supported", "forest_visible", "visibility", "consultative_only",
            "vote_summary", "successful_votes", "required_votes", "failed_seats"}}
        add_node(nodes, stage="FA", title=f"{hyp} · {label}", subtitle=name,
                 status=data.get("status"), output=output, path=path, hyp=hyp, order=1, ui_dir=ui_dir)

    for hdir in sorted((root / "SH").glob("H*")):
        hyp = hdir.name
        for path in hdir.glob("entry_router/route/branches/*/*/node.json"):
            data = read_json(path)
            out = data.get("output", {})
            add_node(nodes, stage="ROUTE", title=f"{hyp} · 类型入口", subtitle="代码依次检查诊断证据",
                     status=out.get("selected_initial_graph") or "undecided", output=out,
                     path=path, hyp=hyp, order=0, ui_dir=ui_dir)
        for path in hdir.glob("initial_route/route/branches/*/*/node.json"):
            data = read_json(path)
            out = data.get("output", {})
            add_node(nodes, stage="ROUTE", title=f"{hyp} · 类型图起点", subtitle="初始入口及固定假设红移",
                     status=out.get("route_status") or data.get("status"), output=out,
                     path=path, hyp=hyp, order=1, ui_dir=ui_dir)
        for path in hdir.glob("alignment/*/branches/*/*/node.json"):
            data = read_json(path)
            add_node(nodes, stage="GRAPH", title=f"{hyp} · 谱线对齐", subtitle="同一假设内部处理线对冲突",
                     status="complete", output=data.get("output", {}), path=path, hyp=hyp,
                     graph=data.get("graph"),
                     order=event_order.get(data.get("node_execution_id"), 10000), ui_dir=ui_dir)
        for graph in ("qso", "elg", "lrg_bgs"):
            for path in sorted((hdir / graph).glob("*/branches/*/*/node.json")):
                data = read_json(path)
                node_type = data.get("node_type", path.parent.parent.parent.parent.name)
                short = node_type.split(".")[-1]
                add_node(nodes, stage="GRAPH", title=f"{hyp} · {LABELS.get(short, short.replace('_', ' '))}",
                         subtitle=f"{graph.upper().replace('_', '/')} · {node_type}",
                         status=data.get("status"), output=data.get("output", {}), path=path,
                         hyp=hyp, graph=graph.upper(),
                         order=event_order.get(data.get("node_execution_id"), 10000), ui_dir=ui_dir,
                         links=[{"label": "报告", "href": rel_link(path.parent / "report.md", ui_dir)}]
                         if (path.parent / "report.md").exists() else [])
    for kind, order in (("merge_groups", 0), ("compare_groups", 1)):
        for path in (root / "HS" / kind).glob("result/branches/*/*/node.json"):
            data = read_json(path)
            output = data.get("output", {})
            if kind == "compare_groups":
                output = summary.get("hs_comparison", output)
            add_node(nodes, stage="HS", title=LABELS[kind], subtitle="同类型组合并" if order == 0 else "候选组间证据横评",
                     status=output.get("status") or ("provisional" if order else "complete"),
                     output=output, path=path, order=order, ui_dir=ui_dir,
                     links=[{"label": "分析报告", "href": rel_link(path.parent / "report.md", ui_dir)}]
                     if (path.parent / "report.md").exists() else [])

    spectrum = visual.get("spectrum", {})
    return {"name": sample, "result": {k: v for k, v in result.items() if k not in {"output_root", "comparison_reason"}},
            "comparison_reason": result.get("comparison_reason"),
            "counts": dict(Counter(n["stage"] for n in nodes)), "nodes": nodes,
            "spectrum_data": {
                "wavelength": spectrum.get("wavelength_angstrom", []),
                "flux": spectrum.get("flux", []),
                "valid": spectrum.get("valid_pixel", []),
                "continuum": visual.get("continuum", {}).get("flux", []),
                "feature_positions": feature_positions,
            },
            "spectrum": rel_link(root / "spectrum.png", ui_dir),
            "feature_plot": rel_link(root / "VI/features.png", ui_dir)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path, help="completed demo run directory")
    args = parser.parse_args()
    run = args.run.resolve()
    ui_dir = run / "ui"
    ui_dir.mkdir(exist_ok=True)
    index = read_json(run / "index.json")
    payload = {"run": run.name, "status": index["status"], "stages": STAGES,
               "samples": [build_sample(run, result, ui_dir) for result in index["results"]]}
    safe = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    (ui_dir / "data.js").write_text("window.FORMA_GALLERY_DATA=" + safe + ";\n", encoding="utf-8")
    template = Path(__file__).with_name("node_gallery.html")
    (ui_dir / "index.html").write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
    graph_script = Path(__file__).with_name("node_graph.js")
    (ui_dir / "node_graph.js").write_text(graph_script.read_text(encoding="utf-8"), encoding="utf-8")
    spectrum_script = Path(__file__).with_name("spectrum_panel.js")
    (ui_dir / "spectrum_panel.js").write_text(spectrum_script.read_text(encoding="utf-8"), encoding="utf-8")
    i18n_script = Path(__file__).with_name("gallery_i18n.js")
    (ui_dir / "gallery_i18n.js").write_text(i18n_script.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Wrote {ui_dir / 'index.html'} with {sum(len(x['nodes']) for x in payload['samples'])} cards")


if __name__ == "__main__":
    main()
