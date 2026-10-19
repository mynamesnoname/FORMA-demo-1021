"""Code-owned galaxy-to-QSO Type 1 handoff from adopted SH/FA pairings."""

from __future__ import annotations

from .qso_type1_gate import MGII, TYPE1_LINES


MGII_ABS = "line:mgii-2800-abs"


def type1_transfer_evidence(lines: list[dict]) -> dict:
    """A paired diagnostic opens QSO review unless the Mg II pair retains the galaxy.

    This is a routing condition, not a Type 1 classification. QSO Q3–Q10
    still decide whether the transferred hypothesis survives.
    """
    by_id = {row["line_id"]: row for row in lines}
    if len(by_id) != len(lines):
        raise ValueError("duplicate line ID in cleaned view")
    mgii_abs = by_id.get(MGII_ABS)
    if mgii_abs is not None and mgii_abs.get("line_kind") != "absorption":
        raise ValueError("Mg II_abs must be an absorption claim")
    mgii_abs_adopted = bool(mgii_abs and mgii_abs["cleaned_pairing"] == "adopted")
    observed = []
    triggers = []
    for line_id in TYPE1_LINES:
        row = by_id.get(line_id)
        if row is None:
            continue
        if row.get("line_kind") != "emission":
            raise ValueError("QSO diagnostic line must be an emission claim")
        observed.append({"line_id": line_id, "measurement_id": row["measurement_id"],
                         "cleaned_pairing": row["cleaned_pairing"],
                         "fa_vote_artifact_refs": row["fa_vote_artifact_refs"]})
        if row["cleaned_pairing"] == "adopted":
            if row["measurement_id"] is None:
                raise ValueError("adopted QSO line lacks a measurement")
            triggers.append({"line_id": line_id, "measurement_id": row["measurement_id"]})
    mgii_pair = bool(mgii_abs_adopted and by_id.get(MGII)
                     and by_id[MGII]["cleaned_pairing"] == "adopted")
    return {
        "trigger_pairs": [] if mgii_pair else triggers,
        "retained_diagnostic_pairs": triggers if mgii_pair else [],
        "observed_lines": observed,
        "mgii_abs_adopted": mgii_abs_adopted,
        "mgii_abs_measurement_id": mgii_abs["measurement_id"] if mgii_abs_adopted else None,
        "galaxy_retention_by_mgii_pair": mgii_pair,
        "next_graph": "QSO" if triggers and not mgii_pair else None,
    }
