"""JSON branch lineage for revisiting an analysis event without erasing history."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from .execution_artifacts import ExecutionAllocation, validate_execution
from .feature_registry import REGISTRY_SCHEMA, _artifact, cast_vote
from .node_keys import fa_node_key, sh_node_key


TRACE_SCHEMA = "forma-agentic-reasoning-tree-v1"


def _state_digest(state: dict) -> str:
    payload = json.dumps(state, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def new_trace(registry: dict) -> dict:
    """Start one run with a root branch and a frozen pre-analysis import state."""
    if registry.get("schema_version") != REGISTRY_SCHEMA:
        raise ValueError("unsupported feature registry")
    base = {"registry": copy.deepcopy(registry),
            "active_pre_analysis": [], "analysis_results": []}
    return {"schema_version": TRACE_SCHEMA, "run_id": registry["run_id"],
            "selected_branch_id": "main", "artifacts": copy.deepcopy(registry["artifacts"]),
            "executions": {},
            "branches": {"main": {
                "branch_id": "main", "parent_branch_id": None,
                "fork_event_id": None, "purpose": "primary",
                "base_state": base, "state": copy.deepcopy(base), "events": [],
            }}}


def _branch(trace: dict, branch_id: str) -> dict:
    if trace.get("schema_version") != TRACE_SCHEMA:
        raise ValueError("unsupported reasoning trace")
    return trace["branches"][branch_id]


def reachable_events(trace: dict, branch_id: str) -> list[dict]:
    """Events visible to a branch, stopping each ancestor at its fork event."""
    branch = _branch(trace, branch_id)
    parent = branch["parent_branch_id"]
    if parent is None:
        return list(branch["events"])
    inherited = reachable_events(trace, parent)
    cutoff = branch["fork_event_id"]
    positions = [index for index, event in enumerate(inherited)
                 if event["event_id"] == cutoff]
    if len(positions) != 1:
        raise ValueError("branch fork event is not reachable from parent")
    return inherited[:positions[0] + 1] + list(branch["events"])


def register_execution(trace: dict, allocation: ExecutionAllocation) -> dict:
    """Index a reserved node attempt before its results become branch events."""
    validate_execution(allocation)
    if allocation.run_id != trace["run_id"] or allocation.branch_id not in trace["branches"]:
        raise ValueError("execution belongs to another run or an unknown branch")
    executions = trace.setdefault("executions", {})
    if allocation.node_execution_id in executions:
        raise ValueError("node execution ID already registered")
    bind_artifact_root(trace, allocation.root)
    item = allocation.metadata()
    executions[allocation.node_execution_id] = item
    register_artifact(trace, f"execution/{allocation.node_execution_id}/manifest",
                      allocation.path("execution.json"), "execution_manifest",
                      node_execution_id=allocation.node_execution_id)
    return item


def register_artifact(trace: dict, artifact_ref: str, path: str | Path,
                      kind: str, *, node_execution_id: str | None = None) -> dict:
    """Add a newly produced result to the global export index before an event cites it."""
    if not artifact_ref or artifact_ref in trace["artifacts"]:
        raise ValueError("artifact reference must be new and nonempty")
    item = _artifact(Path(path), kind)
    if node_execution_id is not None:
        execution = trace.get("executions", {}).get(node_execution_id)
        if execution is None:
            raise ValueError("artifact execution is not registered")
        directory = Path(trace["artifact_root"]) / execution["relative_dir"]
        try:
            relative = Path(item["path"]).relative_to(directory)
        except ValueError as exc:
            raise ValueError("artifact is outside its allocated execution directory") from exc
        if len(relative.parts) != 1:
            raise ValueError("artifact is outside its allocated execution directory")
        item.update({"node_execution_id": node_execution_id,
                     "relative_path": (Path(execution["relative_dir"]) / relative).as_posix()})
    trace["artifacts"][artifact_ref] = item
    return item


def bind_artifact_root(trace: dict, root: str | Path) -> None:
    """Set the single filesystem root used by newly allocated node outputs."""
    resolved = str(Path(root).resolve())
    if trace.get("artifact_root", resolved) != resolved:
        raise ValueError("reasoning trace already uses another artifact root")
    trace["artifact_root"] = resolved


def _execution_event(trace: dict, branch_id: str, node_execution_id: str | None,
                     artifact_refs: list[str],
                     expected_node_key: str | None = None) -> dict | None:
    if node_execution_id is None:
        return None  # Imported historical artifacts have no allocated execution.
    execution = trace.get("executions", {}).get(node_execution_id)
    if execution is None or execution["branch_id"] != branch_id:
        raise ValueError("event execution is not registered on this branch")
    if expected_node_key is not None and execution["node_key"] != expected_node_key:
        raise ValueError("event execution belongs to another logical node")
    if not any(trace["artifacts"][ref].get("node_execution_id") == node_execution_id
               for ref in artifact_refs):
        raise ValueError("event must cite an artifact from its node execution")
    return copy.deepcopy(execution)


def _append(branch: dict, kind: str, payload: dict,
            artifact_refs: list[str], execution: dict | None = None) -> dict:
    event = {"event_id": f"{branch['branch_id']}:e{len(branch['events']):04d}",
             "kind": kind, "payload": payload,
             "artifact_refs": list(artifact_refs),
             "state_sha256_after": _state_digest(branch["state"])}
    if execution is not None:
        event["execution"] = execution
    branch["events"].append(event)
    return event


def record_analysis(trace: dict, branch_id: str, *, kind: str,
                    analysis_ref: str, artifact_refs: list[str],
                    node_execution_id: str | None = None) -> dict:
    """Activate a named analysis result on one branch, preserving its artifact."""
    if kind not in {"sh_pre_analysis_import", "analysis_result"}:
        raise ValueError("unsupported analysis event")
    if not artifact_refs or any(ref not in trace["artifacts"] for ref in artifact_refs):
        raise ValueError("analysis artifacts must already be registered")
    if not analysis_ref:
        raise ValueError("analysis_ref is required")
    expected_key = (sh_node_key(trace["run_id"], analysis_ref)
                    if kind == "sh_pre_analysis_import" else None)
    execution = _execution_event(trace, branch_id, node_execution_id,
                                 artifact_refs, expected_key)
    branch = _branch(trace, branch_id)
    if kind == "sh_pre_analysis_import":
        if (analysis_ref not in branch["state"]["registry"]["hypotheses"]
                or analysis_ref in branch["state"]["active_pre_analysis"]):
            raise ValueError("unknown or already active SH pre-analysis")
        if f"sh/{analysis_ref}/node" not in artifact_refs:
            raise ValueError("SH import must cite its own validated node artifact")
        branch["state"]["active_pre_analysis"].append(analysis_ref)
    else:
        if analysis_ref in branch["state"]["analysis_results"]:
            raise ValueError("analysis result already active on branch")
        branch["state"]["analysis_results"].append(analysis_ref)
    return _append(branch, kind, {"analysis_ref": analysis_ref}, artifact_refs, execution)


def record_entry_route(trace: dict, branch_id: str, *, hypothesis_ref: str,
                       initial_graph: str | None, route_ref: str,
                       node_execution_id: str) -> dict:
    """Set a code-derived initial graph with a replayable, source-bound event."""
    if initial_graph not in {"QSO", "ELG", "LRG/BGS", None}:
        raise ValueError("unknown initial graph")
    branch = _branch(trace, branch_id)
    if hypothesis_ref not in branch["state"]["active_pre_analysis"]:
        raise ValueError("SH review is not active")
    hypothesis = branch["state"]["registry"]["hypotheses"][hypothesis_ref]
    if hypothesis.get("classification") is not None or hypothesis.get("entry_route_ref"):
        raise ValueError("entry route already set or inherited")
    if route_ref not in trace["artifacts"]:
        raise ValueError("route artifact is missing")
    execution = _execution_event(trace, branch_id, node_execution_id, [route_ref])
    route = _checked_entry_route(trace, route_ref)
    if (route.get("hypothesis_ref") != hypothesis_ref
            or route.get("output", {}).get("selected_initial_graph") != initial_graph):
        raise ValueError("entry route outcome differs from requested route")
    hypothesis["classification"] = ("Type 2 QSO" if initial_graph == "QSO" and
                                     route["output"]["selected_reason"] == "adopted_nev"
                                     else "Type 1 QSO" if initial_graph == "QSO"
                                     else initial_graph)
    hypothesis["entry_route_ref"] = route_ref
    return _append(branch, "entry_route", {
        "hypothesis_ref": hypothesis_ref,
        "initial_graph": initial_graph,
        "classification": hypothesis["classification"],
        "route_ref": route_ref,
    }, [route_ref], execution)


def _checked_entry_route(trace: dict, route_ref: str) -> dict:
    """Read the frozen router decision before updating branch state."""
    item = trace["artifacts"][route_ref]
    if item["kind"] != "entry_route_node":
        raise ValueError("entry route artifact has wrong kind")
    path = Path(item["path"]).resolve(strict=True)
    if _artifact(path, item["kind"])["sha256"] != item["sha256"]:
        raise ValueError("entry route artifact changed")
    return json.loads(path.read_text(encoding="utf-8"))


def record_type_handoff(trace: dict, branch_id: str, *, hypothesis_ref: str,
                        from_graph: str, to_graph: str, route_ref: str,
                        evidence_refs: list[str]) -> dict:
    """Archive a graph transfer without changing SH/FA or the initial type."""
    branch = _branch(trace, branch_id)
    if (not hypothesis_ref or from_graph == to_graph
            or hypothesis_ref not in branch["state"]["active_pre_analysis"]):
        raise ValueError("invalid type graph transfer identity")
    refs = [route_ref, *evidence_refs]
    if not evidence_refs or any(ref not in trace["artifacts"] for ref in refs):
        raise ValueError("type graph transfer needs registered evidence")
    from .feature_registry import _digest
    for ref in refs:
        item = trace["artifacts"][ref]
        if _digest(Path(item["path"]).resolve(strict=True)) != item["sha256"]:
            raise ValueError("type graph transfer source changed")
    route = json.loads(Path(trace["artifacts"][route_ref]["path"]).read_text(encoding="utf-8"))
    outcome = route.get("output", {})
    if (route.get("hypothesis_ref") != hypothesis_ref
            or outcome.get("path_status") != "transfer"
            or outcome.get("from_graph") != from_graph
            or outcome.get("to_graph") != to_graph):
        raise ValueError("type graph transfer route does not match its event")
    previous = [event["payload"] for event in reachable_events(trace, branch_id)
                if event["kind"] == "type_graph_handoff"
                and event["payload"]["hypothesis_ref"] == hypothesis_ref]
    history = previous[-1]["route_history"] if previous else [from_graph]
    if history[-1] != from_graph or to_graph in history:
        raise ValueError("type graph transfer would break route history or cycle")
    return _append(branch, "type_graph_handoff", {
        "hypothesis_ref": hypothesis_ref, "from_graph": from_graph,
        "to_graph": to_graph, "route_ref": route_ref,
        "evidence_refs": evidence_refs, "route_history": [*history, to_graph],
    }, refs)


def record_type_fallback(trace: dict, branch_id: str, *, hypothesis_ref: str,
                         from_graph: str, to_graph: str, route_ref: str,
                         entry_route_ref: str) -> dict:
    """Open an already eligible graph after the initial graph ended dead."""
    if from_graph != "LRG/BGS" or to_graph != "ELG":
        raise ValueError("unsupported type-graph fallback")
    branch = _branch(trace, branch_id)
    hypothesis = branch["state"]["registry"]["hypotheses"].get(hypothesis_ref)
    if (hypothesis is None or hypothesis.get("classification") != from_graph
            or hypothesis.get("entry_route_ref") != entry_route_ref):
        raise ValueError("fallback does not match the initial route")
    if any(event["kind"] == "type_graph_fallback"
           and event["payload"]["hypothesis_ref"] == hypothesis_ref
           for event in reachable_events(trace, branch_id)):
        raise ValueError("type-graph fallback already active")
    from .feature_registry import _digest
    for ref in (route_ref, entry_route_ref):
        item = trace["artifacts"].get(ref)
        if item is None or _digest(Path(item["path"]).resolve(strict=True)) != item["sha256"]:
            raise ValueError("fallback source missing or changed")
    route = json.loads(Path(trace["artifacts"][route_ref]["path"]).read_text())
    entry = _checked_entry_route(trace, entry_route_ref)
    active_route_events = [event for event in reachable_events(trace, branch_id)
                           if event["kind"] == "analysis_result"
                           and event["payload"]["analysis_ref"]
                           == f"sh2.lrg_bgs/{hypothesis_ref}/lrg_bgs.route_result"
                           and route_ref in event["artifact_refs"]]
    if (route.get("hypothesis_ref") != hypothesis_ref
            or route.get("node_type") != "lrg_bgs.route_result"
            or route.get("output", {}).get("path_status") != "dead"
            or route["output"].get("from_graph") != from_graph
            or len(active_route_events) != 1
            or entry.get("hypothesis_ref") != hypothesis_ref
            or entry.get("output", {}).get("selected_initial_graph") != from_graph
            or to_graph not in entry["output"].get("eligible_graphs", [])):
        raise ValueError("fallback lacks a dead source and eligible target")
    return _append(branch, "type_graph_fallback", {
        "hypothesis_ref": hypothesis_ref, "from_graph": from_graph,
        "to_graph": to_graph, "route_ref": route_ref,
        "entry_route_ref": entry_route_ref,
    }, [route_ref, entry_route_ref])


def record_fa_vote(trace: dict, branch_id: str, feature_id: str, *,
                   vote_id: str, reviewer_id: str, answer: str, origin: str,
                   artifact_ref: str | None = None,
                   node_execution_id: str | None = None) -> dict:
    """Append a vote to one branch only; state changes at completed quorum."""
    branch = _branch(trace, branch_id)
    payload = {"feature_id": feature_id, "vote_id": vote_id,
               "reviewer_id": reviewer_id, "answer": answer,
               "origin": origin, "artifact_ref": artifact_ref}
    execution = _execution_event(trace, branch_id, node_execution_id,
                                 [artifact_ref] if artifact_ref is not None else [],
                                 fa_node_key(trace["run_id"], feature_id))
    registry = branch["state"]["registry"]
    if feature_id not in registry["features"]:
        raise ValueError("FA target is not in the active run registry")
    entry = registry["features"][feature_id]
    if not any(ref["hypothesis_ref"] in branch["state"]["active_pre_analysis"]
               for ref in entry["references"]):
        raise ValueError("FA target has no active SH pre-analysis on this branch")
    cast_vote(registry, feature_id, vote_id=vote_id,
              reviewer_id=reviewer_id, answer=answer, origin=origin,
              artifact_ref=artifact_ref, artifact_index=trace["artifacts"])
    return _append(branch, "fa_vote", payload,
                   [artifact_ref] if artifact_ref is not None else [], execution)


def record_fa_review_blocked(trace: dict, branch_id: str, feature_id: str, *,
                             reason: str,
                             artifact_refs: list[str] | None = None) -> dict:
    """Record a deterministic data blocker, never a third model answer."""
    if reason != "no_usable_samples":
        raise ValueError("unsupported FA review blocker")
    refs = artifact_refs or []
    if any(ref not in trace["artifacts"] for ref in refs):
        raise ValueError("FA blocker cites an unregistered artifact")
    branch = _branch(trace, branch_id)
    entry = branch["state"]["registry"]["features"][feature_id]
    if (entry["votes"] or entry.get("review_blocker") is not None
            or not any(ref["hypothesis_ref"] in branch["state"]["active_pre_analysis"]
                       for ref in entry["references"])):
        raise ValueError("feature cannot be marked unreviewable in this branch state")
    entry["review_blocker"] = reason
    entry["observed_signal_state"] = "unreviewable"
    return _append(branch, "fa_review_blocked",
                   {"feature_id": feature_id, "reason": reason}, refs)


def record_fa_attempt_failed(trace: dict, branch_id: str, feature_id: str, *,
                             node_execution_id: str, artifact_ref: str,
                             error_type: str) -> dict:
    """Keep failed model/tool attempts in lineage without counting a vote."""
    if not error_type or artifact_ref not in trace["artifacts"]:
        raise ValueError("failed attempt needs a registered failure artifact")
    branch = _branch(trace, branch_id)
    if feature_id not in branch["state"]["registry"]["features"]:
        raise ValueError("unknown FA feature")
    execution = _execution_event(trace, branch_id, node_execution_id, [artifact_ref],
                                 fa_node_key(trace["run_id"], feature_id))
    return _append(branch, "fa_attempt_failed",
                   {"feature_id": feature_id, "error_type": error_type},
                   [artifact_ref], execution)


def state_at_event(trace: dict, branch_id: str, event_id: str) -> dict:
    """Replay from a branch's inherited snapshot to a named local event."""
    branch = _branch(trace, branch_id)
    state = copy.deepcopy(branch["base_state"])
    for event in branch["events"]:
        if event["kind"] == "sh_pre_analysis_import":
            state["active_pre_analysis"].append(event["payload"]["analysis_ref"])
        elif event["kind"] == "analysis_result":
            state["analysis_results"].append(event["payload"]["analysis_ref"])
        elif event["kind"] == "fa_vote":
            payload = event["payload"]
            cast_vote(state["registry"], payload["feature_id"], vote_id=payload["vote_id"],
                      reviewer_id=payload["reviewer_id"], answer=payload["answer"],
                      origin=payload["origin"], artifact_ref=payload["artifact_ref"],
                      artifact_index=trace["artifacts"])
        elif event["kind"] == "fa_review_blocked":
            entry = state["registry"]["features"][event["payload"]["feature_id"]]
            entry["review_blocker"] = event["payload"]["reason"]
            entry["observed_signal_state"] = "unreviewable"
        elif event["kind"] == "entry_route":
            payload = event["payload"]
            hypothesis = state["registry"]["hypotheses"][payload["hypothesis_ref"]]
            hypothesis["classification"] = payload["classification"]
            hypothesis["entry_route_ref"] = payload["route_ref"]
        if _state_digest(state) != event["state_sha256_after"]:
            raise ValueError("branch state and event history diverged")
        if event["event_id"] == event_id:
            return state
    raise ValueError("fork event does not belong to the named parent branch")


def fork_branch(trace: dict, *, parent_branch_id: str, fork_event_id: str,
                branch_id: str, purpose: str) -> dict:
    """Create a child from a historical event; never change the parent."""
    if not branch_id or branch_id in trace["branches"] or not purpose:
        raise ValueError("new branch needs a unique ID and purpose")
    inherited = state_at_event(trace, parent_branch_id, fork_event_id)
    child = {"branch_id": branch_id, "parent_branch_id": parent_branch_id,
             "fork_event_id": fork_event_id, "purpose": purpose,
             "base_state": inherited, "state": copy.deepcopy(inherited),
             "events": []}
    trace["branches"][branch_id] = child
    return child


def select_branch(trace: dict, branch_id: str) -> None:
    """Choose an output path without deleting alternatives or changing data."""
    branch = _branch(trace, branch_id)
    if any(vote["origin"] == "offline_fixture"
           for entry in branch["state"]["registry"]["features"].values()
           for vote in entry["votes"]):
        raise ValueError("offline fixture votes cannot select a scientific output branch")
    trace["selected_branch_id"] = branch_id


def write_trace(trace: dict, path: str | Path) -> Path:
    """Write a complete, new JSON trace; refuse silent overwrite."""
    target = Path(path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    for branch_id, branch in trace["branches"].items():
        for event in branch["events"]:
            execution = event.get("execution")
            if execution is not None:
                if (execution != trace.get("executions", {}).get(execution["node_execution_id"])
                        or execution["branch_id"] != branch_id):
                    raise ValueError("event execution metadata diverged")
                if not any(trace["artifacts"].get(ref, {}).get("node_execution_id")
                           == execution["node_execution_id"]
                           for ref in event["artifact_refs"]):
                    raise ValueError("event lost its node execution artifact")
        if branch["events"]:
            replayed = state_at_event(trace, branch_id, branch["events"][-1]["event_id"])
        else:
            replayed = branch["base_state"]
        if replayed != branch["state"]:
            raise ValueError("branch state differs from replayed history")
    for ref, item in trace["artifacts"].items():
        if "node_execution_id" in item:
            execution = trace.get("executions", {}).get(item["node_execution_id"])
            if execution is None or not trace.get("artifact_root"):
                raise ValueError("allocated artifact lacks its execution root")
            expected = Path(trace["artifact_root"]) / item["relative_path"]
            if (Path(item["path"]).resolve() != expected.resolve()
                    or _artifact(expected, item["kind"])["sha256"] != item["sha256"]):
                raise ValueError(f"allocated artifact changed: {ref}")
    for execution in trace.get("executions", {}).values():
        manifest = Path(trace["artifact_root"]) / execution["relative_dir"] / "execution.json"
        if json.loads(manifest.read_text(encoding="utf-8")) != execution:
            raise ValueError("node execution manifest changed")
    with target.open("x", encoding="utf-8") as stream:
        json.dump(trace, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    return target
