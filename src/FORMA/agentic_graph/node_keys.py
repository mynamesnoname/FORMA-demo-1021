"""Stable logical keys; execution and branch identity are separate."""

from urllib.parse import quote


def sh_node_key(run_id: str, hypothesis_ref: str) -> str:
    if not run_id or not hypothesis_ref:
        raise ValueError("run_id and hypothesis_ref must be non-empty")
    return "sh.pre_analysis/" + quote(run_id, safe="") + "/" + quote(hypothesis_ref, safe="")


def fa_node_key(run_id: str, measurement_id: str) -> str:
    if not run_id or not measurement_id:
        raise ValueError("run_id and measurement_id must be non-empty")
    # Preserve the existing FA logical key; filesystem paths use a separate
    # sanitized, hashed component and never use this string as a path.
    return f"fa.real_feature_or_not/{run_id}/{measurement_id}"


def fa_lya_forest_key(run_id: str, hypothesis_ref: str) -> str:
    if not run_id or not hypothesis_ref:
        raise ValueError("run and hypothesis IDs must be non-empty")
    return f"fa.real_lya_forest_or_not/{quote(run_id, safe='')}/{quote(hypothesis_ref, safe='')}"


def fa_doublet_key(run_id: str, hypothesis_ref: str, doublet_id: str) -> str:
    if not run_id or not hypothesis_ref or not doublet_id:
        raise ValueError("run, hypothesis and doublet IDs must be non-empty")
    return ("fa.real_doublet_or_not/" + quote(run_id, safe="") + "/"
            + quote(hypothesis_ref, safe="") + "/" + quote(doublet_id, safe=""))
