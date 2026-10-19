"""Source-bound HS comparison of surviving merged groups."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from .execution_artifacts import allocate_execution
from .fa_doublet import claimed_doublet_ids, read_doublet_information
from .fa_lya_forest import read_lya_forest_information
from .hs_merge import (KEY_LINES, _LINES, SCHEMA as MERGE_SCHEMA, _checked, _resolve,
                       collect_hypothesis)
from .reasoning_trace import (reachable_events, record_analysis, register_artifact,
                              register_execution)
from .session_markdown import MarkdownSessionRecorder

SCHEMA = "forma-hs-group-comparison-v3"
NODE_KEY = "hs.compare_groups"
from .prompts import PROMPT_DIR


def _pair_rows(items: list[dict]) -> list[dict]:
    return [{"line_id": item["line_id"], "feature_id": item["feature_id"],
             "wavelength_angstrom": item["wavelength_angstrom"],
             "measurement_source": item.get("measurement_source"),
             "assignment_status": item.get("final_assignment_status", item.get("best_assignment_status")),
             "provenance": item["provenance"]} for item in items]


def observed_feature_competitions(groups: list[dict]) -> list[dict]:
    """Index exact run-wide CWT identity disagreements across groups."""
    by_feature: dict[str, dict] = {}
    for group in groups:
        for pair in group["selected_pairs"]:
            feature_id = pair["feature_id"]
            if not feature_id.startswith("cwt:"):
                continue  # Local fit and targeted IDs cannot establish shared identity.
            item = by_feature.setdefault(feature_id, {
                "feature_id": feature_id,
                "observed_wavelength_angstrom": pair["wavelength_angstrom"],
                "interpretations": []})
            if item["observed_wavelength_angstrom"] != pair["wavelength_angstrom"]:
                raise ValueError("shared CWT feature has conflicting observed centres")
            item["interpretations"].append({
                "group_id": group["group_id"], "candidate_type": group["candidate_type"],
                "line_id": pair["line_id"]})
    return [item for _, item in sorted(by_feature.items())
            if len({row["group_id"] for row in item["interpretations"]}) > 1
            and len({row["line_id"] for row in item["interpretations"]}) > 1]


def _advisory_rows(trace: dict, branch_id: str, members: list[str],
                   source_refs: set[str]) -> list[dict]:
    """Disclose branch-active FA advice with its exact source, without gating."""
    result = []
    for ref in members:
        row = {"hypothesis_ref": ref, "lya_forest": None, "doublets": []}
        forest = read_lya_forest_information(
            trace, branch_id=branch_id, hypothesis_ref=ref)
        if forest is not None:
            forest_node = json.loads(_checked(trace, forest["node_ref"]).read_text(
                encoding="utf-8"))
            for source_ref in forest_node["source_refs"]:
                _checked(trace, source_ref)
            row["lya_forest"] = {key: forest[key] for key in (
                "node_ref", "status", "visibility", "vote_summary", "coverage")}
            source_refs.add(forest["node_ref"])
        for doublet_id in claimed_doublet_ids(trace, branch_id, ref):
            review = read_doublet_information(
                trace, branch_id=branch_id, hypothesis_ref=ref,
                doublet_id=doublet_id)
            if review is None:
                continue
            row["doublets"].append({
                "node_ref": review["node_ref"], "doublet_id": doublet_id,
                "status": review["status"], "pair_supported": review["pair_supported"],
                "claim_mode": review["claim_mode"],
                "component_line_ids": [item["line_id"] for item in review["components"]],
                "vote_summary": review["vote_summary"],
                "coverage": review["coverage"], "metrics": review["metrics"]})
            source_refs.add(review["node_ref"])
        result.append(row)
    return result


def _compatible_fit_pairs(trace: dict, left: dict, right: dict) -> list[dict]:
    """Find two distinct, FA-confirmed diagnostic fits to the same structure."""
    def fit_snapshot(record: dict) -> dict:
        fields = ("center", "center_err", "amplitude", "amplitude_err", "fwhm")
        snapshot = {}
        for key in fields:
            value = record.get(key)
            snapshot[key] = (value if isinstance(value, (int, float))
                             and math.isfinite(value) else None)
        return snapshot

    if left["candidate_type"] != right["candidate_type"]:
        return []
    diagnostic = KEY_LINES[left["candidate_type"]]
    by_line = lambda group: {row["line_id"]: row for row in group["selected_pairs"]
                             if row["line_id"] in diagnostic
                             and row["feature_id"].startswith("fit:")
                             and row["assignment_status"] == "non_tbd"
                             and any(p.get("fa_state") == "signal_present"
                                     for p in row["provenance"])}
    first, second = by_line(left), by_line(right)
    matches = []
    for line_id in sorted(first.keys() & second.keys()):
        a, b = first[line_id], second[line_id]
        if a["feature_id"] == b["feature_id"]:
            continue
        records = []
        for group, row in ((left, a), (right, b)):
            if len(group["member_hypotheses"]) != 1:
                break  # Cross-merge only two original singletons in this version.
            ref = group["member_hypotheses"][0]
            catalog = json.loads(_checked(trace, f"sh/{ref}/catalog").read_text())
            record = next((m["record"] for m in catalog["measurements"]
                           if m["id"] == row["feature_id"] and m["adoptable"]
                           and m["source"] in {"fit_peak", "fit_doublet"}), None)
            if record is None:
                break
            records.append(record)
        if len(records) != 2:
            continue
        x, y = records
        if x.get("target_line") != y.get("target_line") or x.get("kind") != y.get("kind"):
            continue
        numbers = [record.get(k) for record in (x, y)
                   for k in ("center", "amplitude", "fwhm")]
        if any(not isinstance(v, (int, float)) or not math.isfinite(v) for v in numbers):
            continue
        if (x["fwhm"] <= 0 or y["fwhm"] <= 0
                or x["amplitude"] * y["amplitude"] <= 0):
            continue
        center_gap = abs(x["center"] - y["center"])
        # The fits are local descriptions of the same observed structure, not
        # independent precision redshift estimates. Their FWHM regions must
        # overlap, while reported fit errors and amplitudes remain provenance.
        if center_gap > (x["fwhm"] + y["fwhm"]) / 2:
            continue
        matches.append({"line_id": line_id, "left_feature_id": a["feature_id"],
                        "right_feature_id": b["feature_id"],
                        "center_separation_angstrom": center_gap,
                        "fwhm_overlap_angstrom": (x["fwhm"] + y["fwhm"]) / 2 - center_gap,
                        "left_fit": fit_snapshot(x), "right_fit": fit_snapshot(y)})
    return matches


def _apply_cross_merge(trace: dict, branch_id: str, context: dict,
                       proposal: dict, routes: dict) -> tuple[dict, dict]:
    """Return a new comparison context; never mutate the frozen HS merge node."""
    original = context["groups"]
    ids = proposal.get("group_ids") if isinstance(proposal, dict) else None
    if (not isinstance(ids, list) or len(ids) != 2
            or any(not isinstance(ref, str) for ref in ids) or len(set(ids)) != 2
            or not isinstance(proposal.get("reason"), str) or not proposal["reason"].strip()):
        raise ValueError("cross-merge proposal needs two distinct group IDs and a reason")
    groups = {row["group_id"]: row for row in original}
    if any(ref not in groups for ref in ids):
        raise ValueError("cross-merge cited an unknown group")
    left, right = (groups[ref] for ref in ids)
    if (left["candidate_type"] != right["candidate_type"]
            or any(len(g["member_hypotheses"]) != 1 or g["comparison_status"] != "merged"
                   or g["type_recheck_required"] for g in (left, right))):
        raise ValueError("cross-merge requires two stable same-type singleton groups")
    matches = _compatible_fit_pairs(trace, left, right)
    if len(matches) < 2:
        raise ValueError("cross-merge needs two FA-confirmed compatible diagnostic fits")
    shared_cwt: dict[str, set[str]] = {}
    for group in (left, right):
        for row in group["selected_pairs"]:
            if row["feature_id"].startswith("cwt:"):
                shared_cwt.setdefault(row["feature_id"], set()).add(row["line_id"])
    conflicting_features = {feature_id for feature_id, lines in shared_cwt.items()
                            if len(lines) > 1}
    if any(lines & KEY_LINES[left["candidate_type"]] for feature_id, lines in
           shared_cwt.items() if feature_id in conflicting_features):
        raise ValueError("cross-merge has conflicting diagnostic CWT assignments")
    members = sorted(left["member_hypotheses"] + right["member_hypotheses"])
    records = []
    for ref in members:
        reports = [routes[ref][field] for field in ("report_ref", "qso_report_ref")
                   if routes[ref].get(field)]
        records.append(collect_hypothesis(trace, branch_id, ref,
                                          left["candidate_type"], reports))
    # Set aside every claim on a disputed, non-diagnostic run-wide feature.
    # The resolver must not silently choose one species for that observation.
    unresolved = []
    for feature_id in sorted(conflicting_features):
        claims = [claim for record in records for claim in record["claims"]
                  if claim["feature_id"] == feature_id]
        if any(claim["line_id"] in KEY_LINES[left["candidate_type"]]
               for claim in claims):
            raise ValueError("cross-merge has conflicting diagnostic CWT claims")
        unresolved.append({"feature_id": feature_id,
                           "candidate_line_ids": sorted({claim["line_id"] for claim in claims}),
                           "claims": [{"hypothesis_ref": claim["hypothesis_ref"],
                                       "line_id": claim["line_id"],
                                       "fa_state": claim["fa_state"],
                                       "assignment_status": claim["assignment_status"],
                                       "source_refs": claim["source_refs"]}
                                      for claim in claims]})
    resolution_records = [{**record,
                           "claims": [claim for claim in record["claims"]
                                      if claim["feature_id"] not in conflicting_features]}
                          for record in records]
    resolution = _resolve(resolution_records, [])
    if resolution["merge_status"] != "merged" or resolution["type_recheck_required"]:
        raise ValueError("cross-merge global resolution requires type or anchor review")
    if not {match["line_id"] for match in matches} <= {
            row["line_id"] for row in resolution["selected_pairs"]}:
        raise ValueError("cross-merge lost a matched diagnostic line")
    merged_id = "hs.cross/" + "+".join(members)
    merged = {"group_id": merged_id, "candidate_type": left["candidate_type"],
              "member_hypotheses": members,
              "original_redshifts": {r["hypothesis_ref"]: r["original_redshift"] for r in records},
              "merged_anchor_redshift": resolution["merged_anchor_redshift"],
              "merge_status": "cross_merge", "comparison_status": resolution["merge_status"],
              "type_recheck_required": resolution["type_recheck_required"],
              "selected_pairs": _pair_rows(resolution["selected_pairs"]),
              "excluded_pairs": resolution["excluded_pairs"],
              "lost_shared_key_pairs": resolution["lost_shared_key_pairs"],
              "lost_type_support_line_ids": resolution["lost_type_support_line_ids"],
              "unresolved_identity_competitions": unresolved,
              "advisory_reviews": sorted(
                  left.get("advisory_reviews", []) + right.get("advisory_reviews", []),
                  key=lambda row: row["hypothesis_ref"]),
              "source_reports": left["source_reports"] + right["source_reports"]}
    effective_groups = [g for g in original if g["group_id"] not in ids] + [merged]
    merged_context = {**context, "groups": effective_groups,
                      "observed_feature_competitions": observed_feature_competitions(
                          effective_groups)}
    accepted = {"group_ids": ids, "reason": proposal["reason"],
                "result_group_id": merged_id, "fit_matches": matches,
                "unresolved_identity_competitions": unresolved,
                "resolution": resolution}
    return merged_context, accepted


def build_comparison_context(trace: dict, branch_id: str, hs: dict, routes: dict) -> dict:
    """Construct a uniform dossier for merged groups and singleton groups."""
    state = trace["branches"][branch_id]["state"]
    if NODE_KEY in state["analysis_results"]:
        raise ValueError("HS comparison already active; fork before rerunning")
    if "hs.merge_groups" not in state["analysis_results"]:
        raise ValueError("HS merge is not active on this branch")
    merge_ref = hs["artifact_ref"]
    merge_events = [event for event in reachable_events(trace, branch_id)
                    if event["kind"] == "analysis_result"
                    and event["payload"]["analysis_ref"] == "hs.merge_groups"]
    if (len(merge_events) != 1 or merge_ref not in merge_events[0]["artifact_refs"]
            or trace["artifacts"][merge_ref].get("node_execution_id")
            != merge_events[0]["execution"]["node_execution_id"]):
        raise ValueError("HS comparison merge ref is not the active branch result")
    node = json.loads(_checked(trace, merge_ref).read_text(encoding="utf-8"))
    if (node != hs["node"] or node.get("schema_version") != MERGE_SCHEMA
            or node.get("branch_id") != branch_id or node.get("run_id") != trace["run_id"]
            or node.get("node_key") != "hs.merge_groups"):
        raise ValueError("HS comparison needs the active merge node")
    groups = []
    source_refs = {merge_ref}
    seen = set()
    for group in node["output"]["groups"]:
        members = group["member_hypotheses"]
        if seen.intersection(members) or any(
            ref not in routes or routes[ref]["path_status"] != "survive"
            or routes[ref]["candidate_type"] != group["candidate_type"] for ref in members
        ):
            raise ValueError("HS group membership differs from active routes")
        seen.update(members)
        if len(members) == 1:
            ref = members[0]
            reports = [routes[ref][field] for field in ("report_ref", "qso_report_ref")
                       if routes[ref].get(field)]
            record = collect_hypothesis(trace, branch_id, ref, group["candidate_type"], reports)
            resolution = _resolve([record], [])
            source_refs.update(record["source_refs"])
        else:
            resolution = group["resolution"]
            if resolution is None:
                raise ValueError("merged HS group lacks a resolution")
        reports = []
        for ref in members:
            for field in ("report_ref", "qso_report_ref"):
                report_ref = routes[ref].get(field)
                if report_ref:
                    reports.append({"hypothesis_ref": ref, "source_ref": report_ref,
                                    "text": _checked(trace, report_ref).read_text(encoding="utf-8")})
                    source_refs.add(report_ref)
        groups.append({"group_id": group["group_id"],
                       "candidate_type": group["candidate_type"],
                       "member_hypotheses": members,
                       "original_redshifts": group["original_redshifts"],
                       "merged_anchor_redshift": group["merged_anchor_redshift"],
                       "merge_status": group["merge_status"],
                       "comparison_status": resolution["merge_status"],
                       "type_recheck_required": resolution["type_recheck_required"],
                       "selected_pairs": _pair_rows(resolution["selected_pairs"]),
                       "excluded_pairs": resolution["excluded_pairs"],
                       "lost_shared_key_pairs": resolution["lost_shared_key_pairs"],
                       "lost_type_support_line_ids": resolution["lost_type_support_line_ids"],
                       "advisory_reviews": _advisory_rows(
                           trace, branch_id, members, source_refs),
                       "source_reports": reports})
    if seen != {ref for ref, route in routes.items() if route["path_status"] == "survive"}:
        raise ValueError("HS comparison omits a surviving route")
    for ref in source_refs:
        _checked(trace, ref)
    return {"schema_version": SCHEMA, "run_id": trace["run_id"],
            "branch_id": branch_id, "merge_ref": merge_ref,
            "source_refs": sorted(source_refs), "groups": groups,
            "observed_feature_competitions": observed_feature_competitions(groups)}


def _dossier_value(value: Any) -> str:
    """Render small evidence records without JSON syntax or escaped Markdown."""
    if value is None:
        return "unknown"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, dict):
        return "; ".join(f"{key.replace('_', ' ')}: {_dossier_value(item)}"
                         for key, item in value.items()) or "none"
    if isinstance(value, list):
        return ", ".join(_dossier_value(item) for item in value) or "none"
    return str(value).replace("\n", " ").replace("|", "\\|")


def model_facing_dossier(context: dict) -> str:
    """Render groups for HS; the complete machine-readable context stays archived."""
    lines = ["# Groups to compare", "", "## Shared observations with competing line identities", ""]
    competitions = context.get("observed_feature_competitions")
    if competitions is None:
        competitions = observed_feature_competitions(context["groups"])
    if competitions:
        for item in competitions:
            interpretations = "; ".join(
                f"`{row['group_id']}` ({row['candidate_type']}): `{row['line_id']}`"
                for row in item["interpretations"])
            lines.append(f"- `{item['feature_id']}` at "
                         f"{item['observed_wavelength_angstrom']} Å: {interpretations}.")
    else:
        lines.append("- No exact run-wide CWT identity competition among these groups.")
    lines.extend(["", "Predicted positions below use each member's original Redrock redshift. "
                  "Offsets are descriptive; the redshift and the feature may not be independent.", ""])
    for group in context["groups"]:
        lines.extend([
            f"## Group `{group['group_id']}` — {group['candidate_type']}", "",
            f"This group contains {', '.join(group['member_hypotheses'])}. "
            f"Its merged anchor redshift is {group['merged_anchor_redshift']}. "
            f"Original hypothesis redshifts: {_dossier_value(group['original_redshifts'])}.",
            f"Merge status: {group['merge_status']}; comparison status: "
            f"{group['comparison_status']}; type recheck required: "
            f"{_dossier_value(group['type_recheck_required'])}.", "",
            "### Selected feature–line pairs", "",
        ])
        if group["selected_pairs"]:
            for pair in group["selected_pairs"]:
                provenance = "; ".join(
                    f"{row['hypothesis_ref']}: assignment {row.get('assignment_status', 'unknown')}, "
                    f"FA {_dossier_value(row.get('fa_state'))}"
                    + (f"; this new candidate was not FA-reviewed; earlier "
                       f"`{row.get('prior_measurement_id')}` had FA "
                       f"{_dossier_value(row.get('prior_measurement_fa_state'))}"
                       if row.get('fa_review_status') == 'not_reviewed' else "")
                    for row in pair.get("provenance", [])) or "none recorded"
                rest = _LINES.get(pair["line_id"])
                contributing_refs = {row.get("hypothesis_ref")
                                     for row in pair.get("provenance", [])}
                offsets = "; ".join(
                    f"{ref}: predicted {rest.rest_wavelength * (1 + z):.6g} Å, "
                    f"observed−predicted "
                    f"{pair['wavelength_angstrom'] - rest.rest_wavelength * (1 + z):+.6g} Å"
                    for ref, z in group["original_redshifts"].items()
                    if not contributing_refs or ref in contributing_refs
                ) if rest is not None else "unavailable"
                lines.append(
                    f"- `{pair['line_id']}` ↔ `{pair['feature_id']}` at "
                    f"{pair['wavelength_angstrom']} Å; assignment "
                    f"{pair['assignment_status']}; source "
                    f"{_dossier_value(pair.get('measurement_source'))}; "
                    f"positions: {offsets}; provenance: {provenance}.")
        else:
            lines.append("- None recorded.")
        lines.extend(["", "### Excluded and unresolved pairings", ""])
        if group["excluded_pairs"]:
            for pair in group["excluded_pairs"]:
                lines.append(
                    f"- Excluded `{pair['line_id']}` ↔ `{pair['feature_id']}`; "
                    f"reason: {_dossier_value(pair.get('reason'))}; FA confirmation: "
                    f"{_dossier_value(pair.get('had_fa_confirmation'))}.")
        else:
            lines.append("- No excluded pairs recorded.")
        if group.get("lost_shared_key_pairs"):
            lines.append("- Shared diagnostic pairs lost during resolution: " + ", ".join(
                f"`{pair['line_id']}` ↔ `{pair['feature_id']}`"
                for pair in group["lost_shared_key_pairs"]) + ".")
        if group.get("lost_type_support_line_ids"):
            lines.append("- Type-support lines lost during resolution: " + ", ".join(
                f"`{line_id}`" for line_id in group["lost_type_support_line_ids"]) + ".")
        for dispute in group.get("unresolved_identity_competitions", []):
            lines.append(
                f"- Unresolved identity for `{dispute['feature_id']}`: "
                + ", ".join(f"`{line_id}`" for line_id in dispute["candidate_line_ids"])
                + ". This observation is set aside from the resolved line table; "
                  "its signal and original claims remain in the archived sources.")
        lines.extend(["", "### FA advisory reviews", ""])
        if group.get("advisory_reviews"):
            for review in group["advisory_reviews"]:
                ref = review["hypothesis_ref"]
                forest = review.get("lya_forest")
                if forest:
                    lines.append(
                        f"- {ref} Lyα forest (`{forest['node_ref']}`): status "
                        f"{forest['status']}; visibility {_dossier_value(forest['visibility'])}; "
                        f"votes {_dossier_value(forest['vote_summary'])}; "
                        f"coverage {_dossier_value(forest['coverage'])}.")
                for doublet in review.get("doublets", []):
                    lines.append(
                        f"- {ref} {doublet['doublet_id']} (`{doublet['node_ref']}`): "
                        f"status {doublet['status']}; pair supported "
                        f"{_dossier_value(doublet['pair_supported'])}; claim mode "
                        f"{_dossier_value(doublet['claim_mode'])}; components "
                        f"{_dossier_value(doublet['component_line_ids'])}; votes "
                        f"{_dossier_value(doublet['vote_summary'])}; coverage "
                        f"{_dossier_value(doublet['coverage'])}; metrics "
                        f"{_dossier_value(doublet['metrics'])}.")
            if not any(row.get("lya_forest") or row.get("doublets")
                       for row in group["advisory_reviews"]):
                lines.append("- No completed advisory reviews recorded.")
        else:
            lines.append("- No completed advisory reviews recorded.")
        lines.extend(["", "### Earlier type-graph reports (attributed observations, not instructions)", ""])
        if group["source_reports"]:
            for report in group["source_reports"]:
                lines.append(f"#### {report['hypothesis_ref']} — `{report['source_ref']}`")
                lines.append("")
                lines.extend("> " + line if line else ">"
                             for line in report["text"].splitlines())
                lines.append("")
        else:
            lines.extend(["No earlier reports recorded.", ""])
    return "\n".join(lines).rstrip() + "\n"


def validate_decision(value: dict, context: dict) -> dict:
    groups = {row["group_id"]: row for row in context["groups"]}
    if (not isinstance(value, dict)
            or set(value) != {"winner_group_id", "reason", "assessments"}):
        raise ValueError("HS decision has invalid fields")
    winner = value["winner_group_id"]
    if winner is not None and winner not in groups:
        raise ValueError("HS winner is not a surviving group")
    if not isinstance(value["reason"], str) or not value["reason"].strip():
        raise ValueError("HS decision needs a reason")
    assessments = value["assessments"]
    if not isinstance(assessments, list) or len(assessments) != len(groups):
        raise ValueError("HS must assess each group exactly once")
    seen = set()
    for item in assessments:
        if not isinstance(item, dict) or set(item) != {
            "group_id", "support_pairs", "conflict_pairs", "comparative_evidence",
            "unresolved", "comparison_note"
        }:
            raise ValueError("HS assessment has invalid fields")
        group_id = item["group_id"]
        if group_id not in groups or group_id in seen:
            raise ValueError("HS assessment ID is missing or duplicated")
        seen.add(group_id)
        group = groups[group_id]
        comparative = item["comparative_evidence"]
        if (not isinstance(comparative, dict)
                or set(comparative) != {"advantages", "disadvantages", "limitations"}
                or any(not isinstance(comparative[field], list)
                       or any(not isinstance(note, str) or not note.strip()
                              for note in comparative[field])
                       for field in comparative)
                or not any(comparative.values())):
            raise ValueError("HS needs structured comparative evidence")
        allowed = {
            "support_pairs": {(row["line_id"], row["feature_id"])
                              for row in group["selected_pairs"]},
            "conflict_pairs": {(row["line_id"], row["feature_id"])
                               for row in group["excluded_pairs"]},
        }
        for field in ("support_pairs", "conflict_pairs"):
            if not isinstance(item[field], list):
                raise ValueError("HS pair citations must be a list")
            cited = set()
            for pair in item[field]:
                if not isinstance(pair, dict) or set(pair) != {"line_id", "feature_id"}:
                    raise ValueError("HS pair citation has invalid fields")
                key = (pair["line_id"], pair["feature_id"])
                if key not in allowed[field] or key in cited:
                    raise ValueError("HS cited an absent or duplicate pair")
                cited.add(key)
                if field == "support_pairs":
                    selected = next(row for row in group["selected_pairs"]
                                    if (row["line_id"], row["feature_id"]) == key)
                    if not (any(p.get("fa_state") == "signal_present"
                                for p in selected.get("provenance", []))
                            or selected["assignment_status"] == "llm_selected" and any(
                                p.get("fa_review_status") == "not_reviewed"
                                for p in selected.get("provenance", []))):
                        raise ValueError("HS support citation lacks positive observation")
                    if (selected["assignment_status"] == "llm_selected"
                            and any(p.get("fa_review_status") == "not_reviewed"
                                    for p in selected.get("provenance", []))
                            and not comparative["limitations"]):
                        raise ValueError("HS unreviewed support needs a limitation")
        if (not isinstance(item["unresolved"], list)
                or any(not isinstance(note, str) for note in item["unresolved"])
                or not isinstance(item["comparison_note"], str)
                or not item["comparison_note"].strip()):
            raise ValueError("HS assessment narrative is invalid")
    if winner is not None:
        group = groups[winner]
        if group["comparison_status"] != "merged" or group["type_recheck_required"]:
            raise ValueError("HS cannot select a group requiring review")
        if not next(row for row in assessments if row["group_id"] == winner)["support_pairs"]:
            raise ValueError("HS winner has no cited supporting pair")
    return value


def _sole_group_decision(groups: list[dict]) -> dict:
    if not groups:
        return {"winner_group_id": None, "reason": "No surviving type-graph group.",
                "assessments": []}
    group = groups[0]
    supported = [row for row in group["selected_pairs"]
                 if any(p.get("fa_state") == "signal_present"
                        or row["assignment_status"] == "llm_selected"
                        and p.get("fa_review_status") == "not_reviewed"
                        for p in row.get("provenance", []))]
    unreviewed = any(row["assignment_status"] == "llm_selected"
                     and any(p.get("fa_review_status") == "not_reviewed"
                             for p in row.get("provenance", []))
                     for row in supported)
    admissible = (group["comparison_status"] == "merged"
                  and not group["type_recheck_required"] and bool(supported))
    unresolved = group.get("unresolved_identity_competitions", [])
    return {"winner_group_id": group["group_id"] if admissible else None,
            "reason": ("Only surviving group; provisional pending RA."
                       + (" Non-diagnostic feature identities remain unresolved."
                          if unresolved else "")
                       if admissible else "Sole group requires review or lacks a supported pair."),
            "assessments": [{"group_id": group["group_id"],
                             "support_pairs": [{"line_id": row["line_id"],
                                                "feature_id": row["feature_id"]}
                                               for row in supported],
                             "conflict_pairs": [],
                             "comparative_evidence": {
                                 "advantages": [], "disadvantages": [],
                                 "limitations": [
                                     "Only one group survived; no cross-group comparison was made.",
                                     *(["Non-diagnostic feature identities were set aside during merge."]
                                       if unresolved else []),
                                     *(["A cited targeted observation was not independently FA-reviewed."]
                                       if unreviewed else [])]},
                             "unresolved": [
                                 f"{item['feature_id']}: "
                                 + ", ".join(item["candidate_line_ids"])
                                 for item in unresolved],
                             "comparison_note": "No other surviving group to compare."}]}


def render_report(decision: dict, context: dict) -> str:
    """Keep IDs and redshifts in the human report code-owned."""
    groups = {row["group_id"]: row for row in context["groups"]}
    winner = decision["winner_group_id"]
    lines = ["# HS group comparison", "",
             f"Decision: {'provisional ' + winner if winner else 'abstain'}",
             "RA review: pending", f"Reason: {decision['reason']}", ""]
    for competition in context.get("observed_feature_competitions", []):
        lines.append("Identity competition: " + competition["feature_id"] + " — "
                     + "; ".join(f"{row['group_id']}: {row['line_id']}"
                                 for row in competition["interpretations"]))
    if context.get("observed_feature_competitions"):
        lines.append("")
    for assessment in decision["assessments"]:
        group = groups[assessment["group_id"]]
        lines.extend([f"## {group['group_id']}", "",
                      f"Type: {group['candidate_type']}",
                      f"Members: {', '.join(group['member_hypotheses'])}",
                      f"Merged anchor redshift: {group['merged_anchor_redshift']}",
                      f"Merge status: {group['merge_status']}",
                      f"Comparison status: {group['comparison_status']}",
                      f"Type recheck required: {group['type_recheck_required']}",
                      f"Comparison: {assessment['comparison_note']}",
                      "Supports: " + (", ".join(
                          f"{pair['line_id']} @ {pair['feature_id']}"
                          for pair in assessment["support_pairs"]) or "none"),
                      "Excluded pair citations: " + (", ".join(
                          f"{pair['line_id']} @ {pair['feature_id']}"
                          for pair in assessment["conflict_pairs"]) or "none"),
                      "Comparative advantages: " + ("; ".join(
                          assessment["comparative_evidence"]["advantages"]) or "none"),
                      "Comparative disadvantages: " + ("; ".join(
                          assessment["comparative_evidence"]["disadvantages"]) or "none"),
                      "Evidence limitations: " + ("; ".join(
                          assessment["comparative_evidence"]["limitations"]) or "none"),
                      "Open questions: " + ("; ".join(assessment["unresolved"]) or "none"),
                      ""])
        for dispute in group.get("unresolved_identity_competitions", []):
            lines.append("Unresolved feature identity: " + dispute["feature_id"]
                         + " — " + ", ".join(dispute["candidate_line_ids"])
                         + "; set aside from resolved pairings.\n")
    return "\n".join(lines).rstrip() + "\n"


def validate_merge_answer(value: dict, groups: list[dict]) -> dict:
    if (not isinstance(value, dict) or set(value) != {"proposals", "reason"}
            or not isinstance(value["reason"], str) or not value["reason"].strip()):
        raise ValueError("HS merge answer needs proposals and a reason")
    proposals = value["proposals"]
    if not isinstance(proposals, list):
        raise ValueError("HS merge proposals must be an array")
    known = {group["group_id"] for group in groups}
    seen = set()
    for proposal in proposals:
        if not isinstance(proposal, dict) or set(proposal) != {"group_ids", "reason"}:
            raise ValueError("Each HS merge proposal needs group_ids and a reason")
        ids = proposal["group_ids"]
        if (not isinstance(ids, list) or len(ids) != 2
                or not all(isinstance(item, str) for item in ids)
                or len(set(ids)) != 2 or not set(ids) <= known):
            raise ValueError("HS merge proposal must cite two distinct dossier groups")
        pair = frozenset(ids)
        if pair in seen:
            raise ValueError("HS merge proposal repeats a group pair")
        seen.add(pair)
        if not isinstance(proposal["reason"], str) or not proposal["reason"].strip():
            raise ValueError("HS merge proposal needs a reason")
    return value


async def run_hs_comparison(trace: dict, *, branch_id: str, hs: dict, routes: dict,
                            output_root: str | Path, llm: Any | None) -> dict:
    """Write one comparison node. RA owns any requested fork or reinspection."""
    context = build_comparison_context(trace, branch_id, hs, routes)
    original_context = context
    root = Path(output_root).resolve()
    if trace.get("artifact_root", str(root)) != str(root):
        raise ValueError("HS output root differs from reasoning tree")
    allocation = allocate_execution(root, run_id=trace["run_id"],
                                    branch_id=branch_id, node_key=NODE_KEY)
    allocation.path("context.json").write_text(
        json.dumps(context, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8")
    groups = context["groups"]
    mode = "deterministic"
    recorder = None
    merge_recorder = None
    cross_merges = []
    merge_review = None
    if len(groups) > 1:
        if llm is None:
            raise ValueError("multiple HS groups require a merge model")
        mode = "model"
        merge_system = (PROMPT_DIR / "hs_merge_proposal_system.md").read_text(encoding="utf-8")
        dossier = HumanMessage(content=(PROMPT_DIR / "hs_merge_dossier_user.md").read_text(
            encoding="utf-8").replace("{{HS_GROUP_DOSSIER}}", model_facing_dossier(context)))
        question = HumanMessage(content=(PROMPT_DIR / "hs_merge_question_user.md").read_text(
            encoding="utf-8"))
        merge_messages = [SystemMessage(content=merge_system), dossier, question]
        merge_recorder = MarkdownSessionRecorder(
            allocation.path("merge_session.md"), run_id=trace["run_id"],
            hypothesis_ref="all-groups", stage="HS merge proposal",
            system_prompt=merge_system, input_messages=merge_messages[1:], tools=[],
            session_kind="HS", subject_label="Scope")
        try:
            for attempt in range(2):
                response = await llm.ainvoke(merge_messages)
                if not isinstance(response, AIMessage) or not isinstance(response.content, str):
                    raise ValueError("HS merge model returned no JSON text")
                merge_recorder.record_event({"model": {"messages": [response]}})
                try:
                    merge_answer = validate_merge_answer(json.loads(response.content), groups)
                    break
                except ValueError as invalid:
                    if attempt:
                        raise
                    correction = HumanMessage(content=(
                        "Your merge JSON failed validation: " + str(invalid)
                        + ". Return proposals as an array of distinct group pairs, "
                          "each with group_ids and reason, plus an overall reason."))
                    merge_recorder.record_event({"repair_prompt": {"messages": [correction]}})
                    merge_messages.extend([response, correction])
            merge_recorder.finish(status="complete")
        except Exception as exc:
            merge_recorder.finish(status="failed", error_type=type(exc).__name__)
            raise
        for proposal in merge_answer["proposals"]:
            try:
                merged_context, accepted = _apply_cross_merge(
                    trace, branch_id, context, proposal, routes)
            except ValueError as invalid:
                cross_merges.append({"status": "rejected", "proposal": proposal,
                                     "reason": str(invalid)})
            else:
                cross_merges.append({"status": "accepted", "proposal": proposal, **accepted})
                context = merged_context
                groups = context["groups"]
        if any(item["status"] == "accepted" for item in cross_merges):
            allocation.path("effective_context.json").write_text(
                json.dumps(context, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                encoding="utf-8")
        merge_review = merge_answer
    if len(groups) <= 1:
        decision = _sole_group_decision(groups)
        if any(item["status"] == "accepted" for item in cross_merges):
            decision["reason"] = ("Cross-merge accepted after source-bound checks; "
                                  "sole resolved group pending RA.")
    else:
        if llm is None:
            raise ValueError("multiple HS groups require a comparison model")
        mode = "model"
        system = (PROMPT_DIR / "hs_comparison_system.md").read_text(encoding="utf-8")
        user = ((PROMPT_DIR / "hs_comparison_user.md").read_text(encoding="utf-8")
                .replace("{{HS_GROUP_DOSSIER}}", model_facing_dossier(context)))
        messages = [SystemMessage(content=system), HumanMessage(content=user)]
        recorder = MarkdownSessionRecorder(
            allocation.path("session.md"), run_id=trace["run_id"],
            hypothesis_ref="all-groups", stage="HS cross-comparison",
            system_prompt=system, input_messages=messages[1:], tools=[],
            session_kind="HS", subject_label="Scope")
        try:
            async def ask(active_context: dict, active_messages: list) -> dict:
                for attempt in range(2):
                    response = await llm.ainvoke(active_messages)
                    if not isinstance(response, AIMessage) or not isinstance(response.content, str):
                        raise ValueError("HS model returned no JSON text")
                    recorder.record_event({"model": {"messages": [response]}})
                    try:
                        return validate_decision(json.loads(response.content), active_context)
                    except ValueError as invalid:
                        if attempt:
                            raise
                        correction = HumanMessage(content=(
                            "Your previous JSON failed validation: " + str(invalid)
                            + ". Return the complete corrected JSON object. Preserve only exact "
                            "group and pair IDs from the dossier. Every assessment needs "
                            "comparative_evidence with advantages, disadvantages and limitations "
                            "arrays; unresolved must be an array of strings."
                        ))
                        recorder.record_event({"repair_prompt": {"messages": [correction]}})
                        active_messages.extend([response, correction])
                raise AssertionError("unreachable HS comparison attempt")

            decision = await ask(context, messages)
            recorder.finish(status="complete")
        except Exception as exc:
            recorder.finish(status="failed", error_type=type(exc).__name__)
            raise
    if build_comparison_context(trace, branch_id, hs, routes) != original_context:
        raise ValueError("HS sources changed during comparison")
    decision = validate_decision(decision, context)
    report = render_report(decision, context)
    for cross_merge in cross_merges:
        report += ("\nCross-merge: " + cross_merge["status"] + "; "
                   + (cross_merge.get("reason") or cross_merge["proposal"]["reason"]) + "\n")
    allocation.path("report.md").write_text(report,
                                            encoding="utf-8")
    node = {"schema_version": SCHEMA, "run_id": trace["run_id"],
            "branch_id": branch_id, "node_key": NODE_KEY,
            "node_execution_id": allocation.node_execution_id,
            "attempt_id": allocation.attempt_id, "input_refs": context["source_refs"],
            "mode": mode, "output": {**decision, "merge_review": merge_review,
                                      "cross_merges": cross_merges,
                                      "status": ("provisional_selection"
                                                 if decision["winner_group_id"] else "abstained"),
                                      "ra_review_pending": True}}
    allocation.path("node.json").write_text(
        json.dumps(node, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8")
    register_execution(trace, allocation)
    refs = {}
    artifacts = [("context", "hs_comparison_context"),
                 ("report", "hs_comparison_report"), ("node", "hs_comparison_node")]
    if merge_recorder is not None:
        artifacts.append(("merge_session", "hs_merge_session"))
    if any(item["status"] == "accepted" for item in cross_merges):
        artifacts.append(("effective_context", "hs_comparison_context"))
    if recorder is not None:
        artifacts.append(("session", "hs_comparison_session"))
    for name, kind in artifacts:
        ref = f"hs/{allocation.node_execution_id}/{name}"
        register_artifact(trace, ref,
                          allocation.path(name + (".md" if name in {"report", "session", "merge_session"}
                                                   else ".json")),
                          kind, node_execution_id=allocation.node_execution_id)
        refs[name] = ref
    record_analysis(trace, branch_id, kind="analysis_result", analysis_ref=NODE_KEY,
                    artifact_refs=[*refs.values(), *context["source_refs"]],
                    node_execution_id=allocation.node_execution_id)
    return {"node": node, "artifact_refs": refs, "effective_groups": context["groups"],
            "model_usage": [*(merge_recorder.model_calls if merge_recorder else []),
                            *(recorder.model_calls if recorder else [])]}
