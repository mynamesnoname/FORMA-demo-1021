"""Q11: archive a source-bound QSO hypothesis report without new decisions."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import quote

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from .cleaned_line_view import cleaned_line_view
from .execution_artifacts import allocate_execution
from .feature_registry import _digest
from .line_alignment import active_alignment, run_line_alignment
from .qso_entry import GRAPH_VERSION, NEV, _key, run_qso_entry
from .qso_type1_gate import TYPE1_LINES
from .reasoning_trace import record_analysis, register_artifact, register_execution
from .session_markdown import MarkdownSessionRecorder
from .sh_pre_analysis import PROMPT_DIR, _render


HEADINGS = (
    "### 3a. Spectrum Summary", "### 3b. Recorded Graph Outcome",
    "### 3c. Per-Line Results", "### 3d. Key Findings and Graph Actions",
    "### 3e. Recorded Classification", "### 3f. Caveats and Open Items",
)
_Q2_RULE = "project:qso-nev-type2-exit"
_LINE_TABLE_MARKER = "[[CANONICAL_PER_LINE_TABLE]]"


def _read_artifact(trace: dict, ref: str) -> dict:
    item = trace["artifacts"].get(ref)
    if item is None:
        raise ValueError(f"unregistered Q11 source: {ref}")
    path = Path(item["path"]).resolve(strict=True)
    if _digest(path) != item["sha256"]:
        raise ValueError(f"changed Q11 source: {ref}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Q11 source is not an object: {ref}")
    return value


def _event_at_or_before_fork(trace: dict, branch_id: str, key: str,
                             cutoff: str | None = None) -> dict | None:
    branch = trace["branches"][branch_id]
    events = branch["events"]
    if cutoff is not None:
        positions = [index for index, event in enumerate(events)
                     if event["event_id"] == cutoff]
        if len(positions) != 1:
            raise ValueError("QSO branch fork event is missing from its parent")
        events = events[:positions[0] + 1]
    for event in reversed(events):
        if event["kind"] == "analysis_result" and event["payload"]["analysis_ref"] == key:
            return event
    parent = branch["parent_branch_id"]
    if parent is None:
        return None
    # The child inherits only the parent's events through its fork point.
    return _event_at_or_before_fork(trace, parent, key, branch["fork_event_id"])


def _active_node(trace: dict, branch_id: str, hypothesis_ref: str,
                 node_type: str) -> tuple[str, dict] | None:
    key = _key(hypothesis_ref, node_type)
    if key not in trace["branches"][branch_id]["state"]["analysis_results"]:
        return None
    event = _event_at_or_before_fork(trace, branch_id, key)
    if event is None:
        raise ValueError(f"active QSO node has no reachable event: {key}")
    execution = event.get("execution")
    if execution is None:
        raise ValueError("QSO node has no registered execution")
    refs = [ref for ref in event["artifact_refs"]
            if trace["artifacts"][ref].get("node_execution_id") == execution["node_execution_id"]
            and trace["artifacts"][ref]["kind"] == "qso_node"]
    if len(refs) != 1:
        raise ValueError("QSO event must own exactly one node artifact")
    ref = refs[0]
    node = _read_artifact(trace, ref)
    if (node.get("node_key") != key or node.get("node_type") != node_type
            or node.get("hypothesis_ref") != hypothesis_ref
            or node.get("run_id") != trace["run_id"]
            or node.get("node_execution_id") != execution["node_execution_id"]):
        raise ValueError("QSO node identity differs from active event")
    return ref, node


def build_qso_report_context(trace: dict, branch_id: str,
                             hypothesis_ref: str) -> dict:
    """Preflight the active path and build the only Q11 model-facing facts."""
    branch = trace["branches"][branch_id]
    state = branch["state"]
    if hypothesis_ref not in state["active_pre_analysis"]:
        raise ValueError("Q11 requires active SH pre-analysis")
    if _key(hypothesis_ref, "qso.analysis_report") in state["analysis_results"]:
        raise ValueError("Q11 already completed on this branch; fork before revisiting")
    registry = state["registry"]
    hypothesis = registry["hypotheses"][hypothesis_ref]
    if any(vote["origin"] == "offline_fixture"
           for feature in registry["features"].values() for vote in feature["votes"]):
        raise ValueError("fixture FA ballots cannot enter a QSO report")
    q1 = _active_node(trace, branch_id, hypothesis_ref, "qso.evidence_view")
    entry = _active_node(trace, branch_id, hypothesis_ref, "qso.entry")
    q2 = _active_node(trace, branch_id, hypothesis_ref, "qso.nev_pairing_gate")
    q9 = _active_node(trace, branch_id, hypothesis_ref, "qso.type1_formal_gate")
    q10 = _active_node(trace, branch_id, hypothesis_ref, "qso.route_result")
    if q1 is None or entry is None or entry[0] not in q1[1]["input_refs"]:
        raise ValueError("Q11 requires the cleaned QSO evidence view")
    handoff_ref = entry[1]["output"].get("handoff_ref")
    if entry[1]["output"].get("entry_mode") == "handoff":
        if hypothesis["classification"] not in {"ELG", "LRG/BGS"} or not handoff_ref or handoff_ref not in entry[1]["input_refs"]:
            raise ValueError("Q11 handoff entry has no supported transfer source")
    elif handoff_ref is not None:
        raise ValueError("Q11 initial entry carries an unexpected handoff")
    view = cleaned_line_view(trace, branch_id, hypothesis_ref)
    archived_view = q1[1]["output"].get("cleaned_line_view")
    if (not isinstance(archived_view, dict)
            or {k: v for k, v in archived_view.items() if k != "branch_id"}
            != {k: v for k, v in view.items() if k != "branch_id"}):
        raise ValueError("QSO evidence view is stale relative to active SH/FA state")
    if q10 is not None:
        if q9 is None or q9[0] not in q10[1]["input_refs"]:
            raise ValueError("Q10 lacks its Q9 source")
        terminal_ref, terminal_node = q10
        status = terminal_node["output"].get("path_status")
        candidate = terminal_node["output"].get("candidate_type")
        if status not in {"survive", "dead", "unresolved"} or (
                status == "survive" and candidate != "Type 1 QSO") or (
                status != "survive" and candidate is not None):
            raise ValueError("Q10 has an invalid terminal outcome")
        gate_status = q9[1]["output"].get("gate_status")
        if {"type1_supported": "survive", "type1_failed": "dead",
            "type1_unresolved": "unresolved"}.get(gate_status) != status:
            raise ValueError("Q10 route disagrees with the recorded Q9 gate")
        rule_id = terminal_node["output"].get("rule_id", "project:qso-type1-formal-gate")
    elif q2 is not None:
        terminal_ref, terminal_node = q2
        if (terminal_node["output"].get("path_status") != "survive"
                or terminal_node["output"].get("candidate_type") != "Type 2 QSO"
                or terminal_node["output"].get("pairing_state") != "adopted"
                or q1[0] not in terminal_node["input_refs"]):
            raise ValueError("Q2 has no valid direct Type 2 exit")
        if q9 is not None:
            raise ValueError("Q2 direct exit cannot also have a Type 1 gate")
        status, candidate, rule_id = "survive", "Type 2 QSO", _Q2_RULE
    else:
        raise ValueError("Q11 requires a completed Q2 or Q10 outcome")
    if terminal_node.get("graph_version") != GRAPH_VERSION:
        raise ValueError("Q11 terminal uses an incompatible QSO graph version")

    catalog_ref = f"sh/{hypothesis_ref}/catalog"
    alignment = active_alignment(trace, branch_id, hypothesis_ref, "QSO")
    catalog = _read_artifact(trace, catalog_ref)
    measurements = {item["id"]: item for item in catalog["measurements"]}
    gate_states = {}
    if q9 is not None:
        gate_states = dict(q9[1]["output"].get("effective_line_states", []))
    line_records = []
    vote_refs = set()
    for row in view["lines"]:
        measurement = measurements.get(row["measurement_id"])
        record = measurement["record"] if measurement else None
        center = ((record.get("wavelength") if measurement["source"] == "CWT"
                   else record.get("center")) if record else None)
        vote_refs.update(row["fa_vote_artifact_refs"])
        summary = row["vote_summary"]
        line_records.append({
            "line_id": row["line_id"], "line_name": row["line_name"],
            "predicted_obs_angstrom": row["predicted_obs_angstrom"],
            "measurement_id": row["measurement_id"],
            "measured_center_angstrom": center,
            "measurement_source": row["measurement_source"],
            "fwhm_km_s": row["fwhm_km_s"],
            "measurement_flags": row["measurement_flags"],
            "sh_status": row["sh_status"], "fa_state": row["fa_state"],
            "vote_summary": ({key: summary[key] for key in ("yes", "no", "assurance")}
                             if summary else None),
            "cleaned_pairing": row["cleaned_pairing"],
            "graph_gate_state": ("q2_type2_support" if row["line_id"] == NEV
                                 and candidate == "Type 2 QSO"
                                 else gate_states.get(row["line_id"], "not_evaluated")),
        })
    conflicts = []
    if candidate == "Type 2 QSO" and hypothesis["classification"] == "Type 1 QSO":
        conflicts.append({"code": "preliminary_type1_vs_q2_type2",
                          "source_refs": [f"sh/{hypothesis_ref}/node", terminal_ref]})
    if candidate == "Type 2 QSO" and hypothesis["classification"] in {"ELG", "LRG/BGS"}:
        conflicts.append({"code": ("preliminary_elg_vs_q2_type2"
                                    if hypothesis["classification"] == "ELG"
                                    else "preliminary_lrg_bgs_vs_q2_type2"),
                          "source_refs": [f"sh/{hypothesis_ref}/node", terminal_ref]})
    if candidate == "Type 2 QSO":
        adopted = [row["line_id"] for row in line_records
                   if row["line_id"] in TYPE1_LINES and row["cleaned_pairing"] == "adopted"]
        if adopted:
            conflicts.append({"code": "type1_diagnostic_pairings_on_q2_exit",
                              "line_ids": adopted, "source_refs": [q1[0], terminal_ref],
                              "note": "These pairings were not assessed by the skipped Type 1 gate."})
    unresolved = [{"line_id": row["line_id"], "state": row["cleaned_pairing"]}
                  for row in line_records
                  if row["cleaned_pairing"] in {"pending_review", "unreviewable_data"}]
    action_prefix = f"sh2.qso/{quote(hypothesis_ref, safe='')}/qso."
    graph_actions = []
    action_refs = set()
    targeted_measurements = []
    for analysis_ref in state["analysis_results"]:
        if not analysis_ref.startswith(action_prefix):
            continue
        node_type = analysis_ref.removeprefix(
            f"sh2.qso/{quote(hypothesis_ref, safe='')}/")
        if node_type in {"qso.entry", "qso.evidence_view", "qso.analysis_report"}:
            continue
        active = _active_node(trace, branch_id, hypothesis_ref, node_type)
        if active is None:
            raise ValueError(f"active QSO action has no source: {node_type}")
        action_refs.add(active[0])
        graph_actions.append({"node_type": node_type, "source_node_ref": active[0],
                              "output": active[1]["output"]})
        if node_type.startswith("qso.relative_strength/"):
            outcome = active[1]["output"]
            representative = outcome.get("representative_target_measurement")
            if outcome.get("status") == "accepted" and representative is not None:
                targeted_measurements.append({
                    "line_id": outcome["target_line_id"],
                    "candidate_id": outcome["candidate_id"],
                    "peak_wavelength_angstrom": representative["peak_wavelength_angstrom"],
                    "amplitude_proxy": representative["amplitude_proxy"],
                    "fwhm_proxy_angstrom": representative["fwhm_proxy_angstrom"],
                    "fwhm_proxy_km_s": representative["fwhm_proxy_km_s"],
                    "measurement_source": representative["measurement_source"],
                    "representative_target_seat": representative["target_seat"],
                    "representative_broadness": outcome["representative_broadness"],
                    "q8_ref": active[0], "q7_ref": outcome["q7_ref"],
                })
    sh_node_ref = f"sh/{hypothesis_ref}/node"
    sh_node = _read_artifact(trace, sh_node_ref)
    sh_report_refs = ([f"sh/{hypothesis_ref}/report"]
                      if sh_node.get("schema_version") != "forma-sh-line-review-v1" else [])
    source_refs = sorted({q1[0], entry[0], terminal_ref, catalog_ref,
                          sh_node_ref, *sh_report_refs,
                          f"sh/{hypothesis_ref}/judgments", *vote_refs, *action_refs,
                          *([q9[0]] if q9 else []),
                          *([alignment[0]] if alignment else []),
                          *([handoff_ref] if handoff_ref else [])})
    for ref in source_refs:
        item = trace["artifacts"].get(ref)
        if item is None or _digest(Path(item["path"])) != item["sha256"]:
            raise ValueError(f"Q11 source missing or changed: {ref}")
    return {
        "run_id": trace["run_id"], "branch_id": branch_id,
        "hypothesis_ref": hypothesis_ref,
        "fixed_redshift": repr(float(hypothesis["redshift"])),
        "preliminary_classification": hypothesis["classification"],
        "graph_handoff": ({"from_graph": hypothesis["classification"], "to_graph": "QSO",
                           "route_ref": handoff_ref,
                           "route_history": entry[1]["output"].get("route_history")}
                          if handoff_ref else None),
        "spectrum_summary": {
            "wavelength_min_angstrom": catalog.get("wavelength_min"),
            "wavelength_max_angstrom": catalog.get("wavelength_max"),
            "masked_regions": catalog.get("masked_regions", []),
            "measurement_catalog_ref": catalog_ref,
        },
        "terminal": {"source_node_ref": terminal_ref, "path_status": status,
                     "candidate_type": candidate, "rule_id": rule_id,
                     "rule_version": terminal_node["graph_version"],
                     "reason_codes": terminal_node["output"].get("reason_codes", [])},
        "line_records": line_records,
        "targeted_measurements": targeted_measurements,
        "line_alignment": alignment[1]["output"] if alignment else None,
        "line_alignment_ref": alignment[0] if alignment else None,
        "graph_actions": graph_actions,
        "conflicts": conflicts, "unresolved_items": unresolved,
        "skipped_nodes": (["qso.broad_line_inventory", "qso.missing_broad_line_queue",
                           "qso.coverage", "qso.inspect_line", "qso.proposed_observation",
                           "qso.relative_strength", "qso.type1_formal_gate",
                           "qso.route_result"] if candidate == "Type 2 QSO" else []),
        "source_refs": source_refs,
    }


def render_qso_line_table(context: dict) -> str:
    """Code owns all line IDs, numbers and projected states in the final table."""
    def cell(value: Any) -> str:
        if value is None:
            return "—"
        return str(value).replace("|", "\\|").replace("\n", " ")

    groups = ("adopted", "rejected_measurement", "pending_review",
              "unreviewable_data", "no_pairing")
    output = []
    for group in groups:
        records = [row for row in context["line_records"]
                   if row["cleaned_pairing"] == group]
        if not records:
            continue
        output.extend([f"**{group}**", "",
                       "| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |",
                       "|---|---:|---|---|---|---|---|---|"])
        for row in records:
            vote = row["vote_summary"]
            fa = row["fa_state"] or "—"
            if vote:
                fa += f" ({vote['yes']}/{vote['yes'] + vote['no']} yes)"
            measurement = (f"`{row['measurement_id']}` / {cell(row['measured_center_angstrom'])}"
                           if row["measurement_id"] else "—")
            source_width = (f"{cell(row['measurement_source'])} / {cell(row['fwhm_km_s'])}"
                            if row["measurement_source"] else "—")
            flags = list(map(str, row["measurement_flags"]))
            for conflict in (context.get("line_alignment") or {}).get("collisions", []):
                if row["line_id"] in conflict["tbd_line_ids"]:
                    resolved = conflict["line_results"].get(row["line_id"], {})
                    flags.append("alignment:" + ("advisory_resolved" if resolved.get("status") == "resolved"
                                                 else "TBD"))
            flags = ", ".join(flags) or "—"
            output.append(
                f"| {cell(row['line_name'])} (`{row['line_id']}`) | "
                f"{cell(row['predicted_obs_angstrom'])} | {measurement} | "
                f"{source_width} | {cell(row['sh_status'])} | {cell(fa)} | "
                f"{cell(row['graph_gate_state'])} | {cell(flags)} |")
        output.append("")
    if sum(row["cleaned_pairing"] in groups for row in context["line_records"]) != len(
            context["line_records"]):
        raise ValueError("Q11 line table has an unknown cleaned pairing state")
    targeted = context.get("targeted_measurements", [])
    if targeted:
        output.extend(["**Targeted candidates (Q8 envelope proxies; original SH/FA rows unchanged)**", "",
                       "| Line ID | Candidate ID | Peak λ (Å) | Amplitude proxy | FWHM proxy (Å) | FWHM proxy (km/s) | Broadness | Source |",
                       "|---|---|---:|---:|---:|---:|---|---|"])
        for item in targeted:
            output.append(
                f"| {cell(item['line_id'])} | {cell(item['candidate_id'])} | "
                f"{cell(item['peak_wavelength_angstrom'])} | {cell(item['amplitude_proxy'])} | "
                f"{cell(item['fwhm_proxy_angstrom'])} | "
                f"{cell(item['fwhm_proxy_km_s'])} | {cell(item['representative_broadness'])} | "
                f"{cell(item['q8_ref'])} |")
        output.append("")
    alignment = context.get("line_alignment")
    if alignment and alignment["collisions"]:
        output.extend(["**Hypothesis-local shared-feature alignment (original SH/FA rows retained)**", "",
                       f"Source: `{cell(context.get('line_alignment_ref'))}`", "",
                       "| Shared measurement | Line ID | Status | Vote | Candidate ID | Representative centre (Å) | Amplitude proxy | FWHM proxy (Å) |",
                       "|---|---|---|---|---|---:|---:|---:|"])
        for conflict in alignment["collisions"]:
            results = conflict["line_results"]
            for line_id in conflict["tbd_line_ids"]:
                result = results.get(line_id)
                representative = result["representative"] if result else None
                vote_label = (f"{result['positive_votes']}/{result['total_votes']}"
                              if result else None)
                output.append(
                    f"| {cell(conflict['measurement_id'])} | {cell(line_id)} | "
                    f"{cell(result['status'] if result else 'TBD')} | "
                    f"{cell(vote_label)} | "
                    f"{cell(representative['candidate_id'] if representative else None)} | "
                    f"{cell(representative['center_angstrom'] if representative else None)} | "
                    f"{cell(representative['amplitude_proxy'] if representative else None)} | "
                    f"{cell(representative['fwhm_proxy_angstrom'] if representative else None)} |")
        output.append("")
    return "\n".join(output).rstrip()


def validate_qso_report(report: str, context: dict) -> None:
    """Reject copied or invented routing fields before committing Q11."""
    if not isinstance(report, str) or report.startswith("Q11_INPUT_INCOMPLETE:"):
        raise ValueError("Q11 model did not produce a complete report")
    lines = report.splitlines()
    positions = []
    for heading in HEADINGS:
        hits = [i for i, line in enumerate(lines) if line == heading]
        if len(hits) != 1:
            raise ValueError(f"Q11 report needs exactly one {heading}")
        positions.append(hits[0])
    if positions != sorted(positions):
        raise ValueError("Q11 report headings are out of order")
    ends = positions[1:] + [len(lines)]
    sections = [lines[start + 1:end] for start, end in zip(positions, ends)]
    if any(not any(line.strip() for line in section) for section in sections):
        raise ValueError("Q11 report has an empty required section")
    required = (
        (0, [f"Hypothesis redshift: {context['fixed_redshift']}"]),
        (1, [f"Graph path status: {context['terminal']['path_status']}",
             f"Candidate type: {context['terminal']['candidate_type'] or 'null'}"]),
        (4, [f"Preliminary classification: {context['preliminary_classification'] or 'null'}",
             f"Recorded classification: {context['terminal']['candidate_type'] or 'null'}"]),
    )
    for index, expected in required:
        nonempty = [line for line in sections[index] if line.strip()]
        if nonempty[:len(expected)] != expected:
            raise ValueError(f"Q11 report has incorrect canonical lines in section {index}")
    if context["terminal"]["source_node_ref"] not in report:
        raise ValueError("Q11 report omits terminal source reference")
    if [line for line in sections[2] if line.strip()] != [_LINE_TABLE_MARKER]:
        raise ValueError("Q11 per-line section must contain only the canonical table marker")


def _normalize_q11_null_labels(report: str, context: dict) -> tuple[str, list[str]]:
    """Resolve the v8 dash/null display collision only for code-owned null labels."""
    replacements = {
        label: f"{label} null"
        for label, value in (("Candidate type:", context["terminal"]["candidate_type"]),
                             ("Recorded classification:",
                              context["terminal"]["candidate_type"]))
        if value is None
    }
    changed = []
    lines = []
    for line in report.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        label = next((name for name in replacements if body == f"{name} —"), None)
        if label is not None:
            line = replacements[label] + line[len(body):]
            changed.append(label)
        lines.append(line)
    return "".join(lines), changed


async def run_qso_report(trace: dict, *, branch_id: str, hypothesis_ref: str,
                         output_root: str | Path, llm: Any,
                         prompt_dir: Path = PROMPT_DIR) -> dict:
    """Run one tool-free report session and commit a validated Q11 artifact."""
    context = build_qso_report_context(trace, branch_id, hypothesis_ref)
    key = _key(hypothesis_ref, "qso.analysis_report")
    root = Path(output_root).resolve()
    if trace.get("artifact_root", str(root)) != str(root):
        raise ValueError("Q11 output root differs from the existing reasoning tree")
    system = (prompt_dir / "qso_q11_report_system.md").read_text(encoding="utf-8")
    user = _render("qso_q11_report_user.md", {
        "Q11_CANONICAL_CONTEXT_JSON": json.dumps(context, ensure_ascii=False,
                                                  indent=2, allow_nan=False),
    }, prompt_dir)
    allocation = allocate_execution(root, run_id=trace["run_id"],
                                    branch_id=branch_id, node_key=key)
    with allocation.path("context.json").open("x", encoding="utf-8") as stream:
        json.dump(context, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    messages = [SystemMessage(content=system), HumanMessage(content=user)]
    recorder = MarkdownSessionRecorder(
        allocation.path("session.md"), run_id=trace["run_id"],
        hypothesis_ref=hypothesis_ref, stage="Q11 report",
        system_prompt=system, input_messages=messages[1:], tools=[],
        session_kind="QSO", subject_label="Hypothesis",
    )
    try:
        response = await llm.ainvoke(messages)
        if not isinstance(response, AIMessage) or not isinstance(response.content, str):
            raise ValueError("Q11 model returned no text report")
        recorder.record_event({"model": {"messages": [response]}})
        report_draft = response.content.strip()
        report_draft, normalized_labels = _normalize_q11_null_labels(report_draft, context)
        if normalized_labels:
            recorder.record_event({"canonical_null_render": json.dumps(
                {"labels": normalized_labels, "from": "—", "to": "null"},
                ensure_ascii=False)})
        validate_qso_report(report_draft, context)
        if build_qso_report_context(trace, branch_id, hypothesis_ref) != context:
            raise ValueError("Q11 source state changed while the report was being written")
        report = report_draft.replace(_LINE_TABLE_MARKER,
                                      render_qso_line_table(context))
        with allocation.path("report.md").open("x", encoding="utf-8") as stream:
            stream.write(report + "\n")
        recorder.finish(status="complete")
    except Exception as exc:
        recorder.finish(status="failed", error_type=type(exc).__name__)
        raise
    node = {
        "schema_version": "forma-qso-node-v1", "graph_version": GRAPH_VERSION,
        "run_id": trace["run_id"], "branch_id": branch_id,
        "hypothesis_ref": hypothesis_ref, "node_key": key,
        "node_type": "qso.analysis_report", "status": "completed",
        "input_refs": context["source_refs"],
        "output": {"path_status": context["terminal"]["path_status"],
                   "candidate_type": context["terminal"]["candidate_type"],
                   "terminal_node_ref": context["terminal"]["source_node_ref"],
                   "unresolved_items": context["unresolved_items"],
                   "report_sha256": _digest(allocation.path("report.md")),
                   "context_sha256": _digest(allocation.path("context.json")),
                   "session_sha256": _digest(allocation.path("session.md")),
                   "system_prompt_sha256": hashlib.sha256(system.encode()).hexdigest(),
                   "user_prompt_sha256": hashlib.sha256(user.encode()).hexdigest()},
        "evidence_refs": context["source_refs"],
        "unresolved_reasons": [f"{item['line_id']}:{item['state']}"
                               for item in context["unresolved_items"]],
        "created_by": "mixed", "node_execution_id": allocation.node_execution_id,
        "attempt_id": allocation.attempt_id,
    }
    with allocation.path("node.json").open("x", encoding="utf-8") as stream:
        json.dump(node, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    register_execution(trace, allocation)
    refs = {}
    for name, kind in (("context", "qso_report_context"), ("report", "qso_report"),
                       ("session", "qso_session"), ("node", "qso_node")):
        ref = f"sh2/{allocation.node_execution_id}/{name}"
        register_artifact(trace, ref, allocation.path(name + (".md" if name in
                          {"report", "session"} else ".json")), kind,
                          node_execution_id=allocation.node_execution_id)
        refs[name] = ref
    record_analysis(trace, branch_id, kind="analysis_result", analysis_ref=key,
                    artifact_refs=[*refs.values(), *context["source_refs"]],
                    node_execution_id=allocation.node_execution_id)
    return {"node": node, "artifact_refs": refs,
            "report_path": str(allocation.path("report.md")),
            "session_path": str(allocation.path("session.md")),
            "model_usage": recorder.model_calls}


async def run_qso_entry_through_report(trace: dict, *, branch_id: str,
                                       hypothesis_ref: str, output_root: str | Path,
                                       llm: Any) -> dict:
    """Run Q0–Q11 for a routed QSO, including the Type 1 investigation path."""
    entry = run_qso_entry(trace, branch_id=branch_id,
                          hypothesis_ref=hypothesis_ref, output_root=output_root)
    type1 = None
    if entry["path_status"] == "in_progress":
        from .qso_type1_path import run_qso_type1_path
        type1 = await run_qso_type1_path(
            trace, branch_id=branch_id, hypothesis_ref=hypothesis_ref,
            output_root=output_root, llm=llm)
    if entry["path_status"] != "pruned":
        await run_line_alignment(trace, branch_id=branch_id,
                                 hypothesis_ref=hypothesis_ref, graph="QSO",
                                 output_root=output_root, llm=llm)
    report = (await run_qso_report(trace, branch_id=branch_id,
                                   hypothesis_ref=hypothesis_ref,
                                   output_root=output_root, llm=llm)
              if entry["path_status"] != "pruned" else None)
    return {"entry": entry, "type1": type1, "report": report}
