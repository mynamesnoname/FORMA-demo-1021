"""Initial spectral ontology registry (WP-009).

初始谱线本体注册表（WP-009）。

Wavelengths and diagnostics are transcribed from the repository's Markdown
knowledge base and ``utils/VI.py``; every record carries a repo-relative
citation so a consumer can audit where a fact came from.
波长与诊断转写自仓库 Markdown 知识库与 ``utils/VI.py``；每条记录都带仓库相对引用，
便于消费方审计事实来源。
"""

from __future__ import annotations

from FORMA.core.reasoning.ontology.schema import (
    EmpiricalParameterRecord,
    ParameterSource,
    ONTOLOGY_SCHEMA_VERSION,
    ClassRecord,
    ConditionRecord,
    DoubletRecord,
    FormalRuleRecord,
    IndexBandRecord,
    LineRecord,
    OntologyRegistry,
    OperandRecord,
    OutcomeSpec,
    RuleRecord,
    SkylineRecord,
    Width3SigmaRecord,
)

_KB = "src/FORMA/agents/multi_agents/harness/kb"


def _cite(path: str, note: str = ""):
    citation = {"source": path}
    if note:
        citation["note"] = note
    return citation


_LINES = [
    LineRecord(
        id="line:lya-1216", name="Lyα", rest_wavelength=1215.67,
        transition="Lyα", species="H I", ionization_ev=13.6,
        line_type="emission", width_class="broad", anchor_priority=12,
        citations=[_cite(f"{_KB}/lines.md", "KB rest-frame table uses 1216.0 Å display"),
                   _cite(f"{_KB}/ionization.md", "last-resort anchor priority 12")],
    ),
    LineRecord(
        id="line:civ-1549", name="C IV", rest_wavelength=1549.0,
        transition="C IV", species="C IV", ionization_ev=64.5,
        line_type="emission", width_class="broad", anchor_priority=10,
        citations=[_cite(f"{_KB}/lines.md"),
                   _cite(f"{_KB}/ionization.md", "fallback anchor priority 10")],
    ),
    LineRecord(
        id="line:heii-1640", name="He II", rest_wavelength=1640.4,
        transition="He II", species="He II", ionization_ev=54.4,
        line_type="emission", width_class="both", anchor_priority=9,
        citations=[_cite(f"{_KB}/lines.md"),
                   _cite(f"{_KB}/ionization.md", "fallback anchor priority 9")],
    ),
    LineRecord(
        id="line:ciii-1909", name="C III]", rest_wavelength=1909.0,
        transition="C III]", species="C III", ionization_ev=47.9,
        line_type="emission", width_class="broad", anchor_priority=8,
        citations=[_cite(f"{_KB}/lines.md"),
                   _cite(f"{_KB}/ionization.md", "fallback anchor priority 8")],
    ),
    LineRecord(
        id="line:mgii-2800", name="Mg II", rest_wavelength=2800.0,
        transition="Mg II", species="Mg II", ionization_ev=15.0,
        line_type="emission", width_class="broad", anchor_priority=6,
        citations=[_cite(f"{_KB}/ionization.md", "anchor priority 6")],
    ),
    LineRecord(
        id="line:mgii-2800-abs", name="Mg II_abs", rest_wavelength=2800.0,
        transition="Mg II", species="Mg II", ionization_ev=15.0,
        line_type="absorption",
        # Decision owner, 2026-10-15: the absorption side of Mg II is the
        # ISM/circumgalactic feature, so its width class is `absorption` like every
        # other absorption line.  The KB associates the BLR with the *emission*
        # side ("broad emission (QSO BLR) and narrow absorption (ISM)"); the earlier
        # citation inverted that.  `broad` was consumed as "claims a broad emission
        # line", which mis-scored this row and polluted the broad-width operands.
        # 决策人 2026-10-15：Mg II 的吸收侧是 ISM/环星系介质特征，因此宽度类别与其它吸收线
        # 一样是 `absorption`。KB 把 BLR 归于*发射*侧（"broad emission (QSO BLR) and narrow
        # absorption (ISM)"），此前的引用把意思写反了。`broad` 被当作"主张一条宽发射线"消费，
        # 因而错算了这一行并污染了宽线宽度操作数。
        width_class="absorption",
        citations=[_cite(f"{_KB}/lines.md"),
                   _cite(f"{_KB}/composite_profile.md",
                         "Mg II + Mg II_abs: broad emission = QSO BLR, narrow absorption = ISM")],
    ),
    LineRecord(
        id="line:nev-3426", name="[Ne V]", rest_wavelength=3426.0,
        transition="[Ne V]", species="Ne V", ionization_ev=97.1,
        line_type="emission", width_class="narrow", anchor_priority=11,
        citations=[_cite(f"{_KB}/lines.md"), _cite(f"{_KB}/classification.md"),
                   _cite(f"{_KB}/ionization.md", "fallback anchor priority 11")],
    ),
    LineRecord(
        id="line:oii-3727", name="[O II]", rest_wavelength=3727.0,
        transition="[O II]", species="O II", ionization_ev=13.6,
        line_type="emission", width_class="narrow", anchor_priority=2,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:cak-3934-abs", name="Ca K_abs", rest_wavelength=3934.8,
        transition="Ca II K", species="Ca II",
        line_type="absorption", width_class="absorption", anchor_priority=1,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:cah-3969-abs", name="Ca H_abs", rest_wavelength=3969.6,
        transition="Ca II H", species="Ca II",
        line_type="absorption", width_class="absorption", anchor_priority=1,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:heps-3970", name="Hε", rest_wavelength=3970.1,
        transition="Hε", species="H I", ionization_ev=13.6,
        line_type="emission", width_class="both", anchor_priority=5,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:heps-3970-abs", name="Hε_abs", rest_wavelength=3970.1,
        transition="Hε", species="H I",
        line_type="absorption", width_class="absorption",
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:hdel-4102", name="Hδ", rest_wavelength=4102.9,
        transition="Hδ", species="H I", ionization_ev=13.6,
        line_type="emission", width_class="both", anchor_priority=5,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:hdel-4102-abs", name="Hδ_abs", rest_wavelength=4102.9,
        transition="Hδ", species="H I",
        line_type="absorption", width_class="absorption",
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:gband-4305-abs", name="G-band_abs", rest_wavelength=4305.6,
        transition="CH G-band", species="CH",
        line_type="absorption", width_class="absorption", anchor_priority=1,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:hgam-4341", name="Hγ", rest_wavelength=4341.7,
        transition="Hγ", species="H I", ionization_ev=13.6,
        line_type="emission", width_class="both", anchor_priority=5,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:hgam-4341-abs", name="Hγ_abs", rest_wavelength=4341.7,
        transition="Hγ", species="H I",
        line_type="absorption", width_class="absorption",
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:hbet-4862", name="Hβ", rest_wavelength=4862.7,
        transition="Hβ", species="H I", ionization_ev=13.6,
        line_type="emission", width_class="both", anchor_priority=5,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:hbet-4862-abs", name="Hβ_abs", rest_wavelength=4862.7,
        transition="Hβ", species="H I",
        line_type="absorption", width_class="absorption",
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:oiii-4960", name="[O III]a", rest_wavelength=4960.3,
        transition="[O III]a", species="O III", ionization_ev=35.1,
        line_type="emission", width_class="narrow", anchor_priority=7,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:oiii-5008", name="[O III]b", rest_wavelength=5008.2,
        transition="[O III]b", species="O III", ionization_ev=35.1,
        line_type="emission", width_class="narrow", anchor_priority=7,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:mgi-5176-abs", name="Mg I_abs", rest_wavelength=5176.7,
        transition="Mg I", species="Mg I",
        line_type="absorption", width_class="absorption", anchor_priority=1,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:nad-5895-abs", name="Na D_abs", rest_wavelength=5895.6,
        transition="Na D", species="Na I",
        line_type="absorption", width_class="absorption", anchor_priority=1,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:nad1-5891-abs", name="Na D1_abs", rest_wavelength=5891.6,
        transition="Na I D1", species="Na I",
        line_type="absorption", width_class="absorption", anchor_priority=1,
        citations=[_cite(f"{_KB}/lines.md", "Na D doublet components; blended label is Na D_abs"),
                   _cite(f"{_KB}/ionization.md", "resolved component anchor priority 1")],
    ),
    LineRecord(
        id="line:nad2-5897-abs", name="Na D2_abs", rest_wavelength=5897.6,
        transition="Na I D2", species="Na I",
        line_type="absorption", width_class="absorption", anchor_priority=1,
        citations=[_cite(f"{_KB}/lines.md", "Na D doublet components; blended label is Na D_abs"),
                   _cite(f"{_KB}/ionization.md", "resolved component anchor priority 1")],
    ),
    LineRecord(
        id="line:nii-6549", name="[N II]a", rest_wavelength=6549.8,
        transition="[N II]a", species="N II",
        # ionization energy of the observed ion (NIST), the ordinal marker the
        # outflow contrast compares; decision owner 2026-10-15
        ionization_ev=29.6,
        line_type="emission", width_class="narrow", anchor_priority=4,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:half-6564", name="Hα", rest_wavelength=6564.6,
        transition="Hα", species="H I", ionization_ev=13.6,
        line_type="emission", width_class="both", anchor_priority=5,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:half-6564-abs", name="Hα_abs", rest_wavelength=6564.6,
        transition="Hα", species="H I",
        line_type="absorption", width_class="absorption",
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:nii-6585", name="[N II]b", rest_wavelength=6585.3,
        transition="[N II]b", species="N II",
        # ionization energy of the observed ion (NIST), the ordinal marker the
        # outflow contrast compares; decision owner 2026-10-15
        ionization_ev=29.6,
        line_type="emission", width_class="narrow", anchor_priority=4,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:sii-6718", name="[S II]a", rest_wavelength=6718.3,
        transition="[S II]a", species="S II",
        # ionization energy of the observed ion (NIST), the ordinal marker the
        # outflow contrast compares; decision owner 2026-10-15
        ionization_ev=23.34,
        line_type="emission", width_class="narrow", anchor_priority=3,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:sii-6732", name="[S II]b", rest_wavelength=6732.7,
        transition="[S II]b", species="S II",
        # ionization energy of the observed ion (NIST), the ordinal marker the
        # outflow contrast compares; decision owner 2026-10-15
        ionization_ev=23.34,
        line_type="emission", width_class="narrow", anchor_priority=3,
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:cat1-8498-abs", name="CaT1_abs", rest_wavelength=8498.0,
        transition="Ca II triplet", species="Ca II",
        line_type="absorption", width_class="absorption",
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:cat2-8542-abs", name="CaT2_abs", rest_wavelength=8542.0,
        transition="Ca II triplet", species="Ca II",
        line_type="absorption", width_class="absorption",
        citations=[_cite(f"{_KB}/lines.md")],
    ),
    LineRecord(
        id="line:cat3-8662-abs", name="CaT3_abs", rest_wavelength=8662.0,
        transition="Ca II triplet", species="Ca II",
        line_type="absorption", width_class="absorption",
        citations=[_cite(f"{_KB}/lines.md")],
    ),
]

_DOUBLETS = [
    DoubletRecord(
        id="doublet:oiii", name="[O III] 4960/5008",
        component_ids=["line:oiii-4960", "line:oiii-5008"],
        rest_separation=47.9,
        amplitude_ratio_note="b:a ≈ 3:1",
        amplitude_ratio=3.0,
        ratio_window=[0.25, 0.5],
        citations=[_cite(f"{_KB}/lines.md", "Doublet Rules"),
                   _cite("src/FORMA/agentic_graph/fa_doublet.py",
                         "Doublet ratio window consumed by the FA doublet advisory")],
    ),
    DoubletRecord(
        id="doublet:sii", name="[S II] 6718/6732",
        component_ids=["line:sii-6718", "line:sii-6732"],
        rest_separation=14.4,
        amplitude_ratio_note="a ≈ b",
        amplitude_ratio=1.0,
        ratio_window=[0.7, 1.4],
        citations=[_cite(f"{_KB}/lines.md", "Doublet Rules"),
                   _cite("src/FORMA/agentic_graph/fa_doublet.py",
                         "Doublet ratio window consumed by the FA doublet advisory")],
    ),
    DoubletRecord(
        id="doublet:nii", name="[N II] 6549/6585",
        component_ids=["line:nii-6549", "line:nii-6585"],
        rest_separation=35.5,
        amplitude_ratio_note="a:b ≈ 1:3",
        amplitude_ratio=3.0,
        ratio_window=[0.20, 0.45],
        citations=[_cite(f"{_KB}/lines.md", "Doublet Rules"),
                   _cite("src/FORMA/agentic_graph/fa_doublet.py",
                         "Doublet ratio window consumed by the FA doublet advisory")],
    ),
    DoubletRecord(
        id="doublet:cahk", name="Ca K/H 3934/3969",
        component_ids=["line:cak-3934-abs", "line:cah-3969-abs"],
        rest_separation=34.8,
        amplitude_ratio_note="Ca K must be deeper than Ca H",
        # Decision owner, 2026-10-15: the doublet's fit width follows its own
        # component lines' declared class instead of a harness constant.  The
        # initial sigma therefore starts at the `absorption` window (20 Å 3σ →
        # σ0 ≈ 6.7 Å) rather than the former hard-coded `broad` (90 Å → 30 Å).
        # 决策人 2026-10-15：该双线的拟合宽度跟随其分量线本身声明的类别，而不是 harness
        # 常量。初始 sigma 因而从 `absorption` 窗口起步（20 Å 3σ → σ0 ≈ 6.7 Å），而非此前
        # 硬编码的 `broad`（90 Å → 30 Å）。
        fit_width_class="absorption",
        citations=[_cite(f"{_KB}/lines.md", "Doublet Rules")],
    ),
    DoubletRecord(
        id="doublet:na-d", name="Na I D 5891.6/5897.6",
        component_ids=["line:nad1-5891-abs", "line:nad2-5897-abs"],
        rest_separation=6.0,
        amplitude_ratio_note="a:b ≈ 2:1 (fitting hint)",
        amplitude_ratio=2.0,
        ratio_window=[1.4, 2.8],
        citations=[_cite(f"{_KB}/lines.md", "Skyline/atmospheric table"),
                   _cite("src/FORMA/agentic_graph/fa_doublet.py",
                         "Doublet ratio window consumed by the FA doublet advisory")],
    ),
]

_CLASSES = [
    ClassRecord(
        id="class:elg", name="ELG",
        description="Strong narrow emission lines; weak or absent absorption",
        citations=[_cite(f"{_KB}/classification.md")],
    ),
    ClassRecord(
        id="class:lrg-bgs", name="LRG/BGS",
        description="Strong stellar absorption; weak or no emission lines",
        citations=[_cite(f"{_KB}/classification.md")],
    ),
    ClassRecord(
        id="class:qso-type1", name="QSO Type 1",
        description="Broad emission lines with FWHM > 2000 km/s",
        citations=[_cite(f"{_KB}/classification.md")],
    ),
    ClassRecord(
        id="class:qso-type2", name="QSO Type 2 / Host Galaxy dominated AGN",
        description="Narrow emission lines with [Ne V] as AGN indicator",
        citations=[_cite(f"{_KB}/classification.md")],
    ),
    ClassRecord(
        id="class:star", name="Star",
        description="Broad stellar absorption, no emission lines",
        citations=[_cite(f"{_KB}/classification.md")],
    ),
    ClassRecord(
        id="class:unknown", name="Unknown",
        description="Insufficient or contradictory evidence for a class",
        citations=[_cite(f"{_KB}/classification.md")],
    ),
]

_RULES = [
    RuleRecord(
        id="rule:blue-edge", kind="coverage",
        description="DESI blue arm below 4000 Å has elevated non-Gaussian noise; blue-zone detections require visual confirmation",
        citations=[_cite(f"{_KB}/lines.md", "Blue Edge Noise Zone")],
    ),
    RuleRecord(
        id="rule:oh-zone", kind="coverage",
        description="OH airglow beyond 7800 Å can masquerade as astrophysical emission; flag OH-zone detections",
        citations=[_cite(f"{_KB}/lines.md", "OH Airglow Zone")],
    ),
    RuleRecord(
        id="rule:ionization-consistency", kind="ionization",
        description="Higher-ionization lines of an element imply lower-ionization lines unless masked or off-spectrum",
        citations=[_cite(f"{_KB}/ionization.md")],
    ),
    RuleRecord(
        id="rule:anchor-priority", kind="ionization",
        description="Prefer the lowest-ionization likely line to anchor systemic redshift",
        citations=[_cite(f"{_KB}/ionization.md")],
    ),
    RuleRecord(
        id="rule:doublet-physics", kind="classification",
        description="Doublet spacing and amplitude ratios must match the registered doublet record",
        citations=[_cite(f"{_KB}/lines.md", "Doublet Rules")],
    ),
    RuleRecord(
        id="rule:composite-profile", kind="quality",
        description="Emission-absorption pairs at the same transition require the composite-profile morphological test",
        citations=[_cite(f"{_KB}/composite_profile.md")],
    ),
]

_FORMAL_RULES = [
    FormalRuleRecord(
        id="rule:formal-ionization-consistency",
        name="Higher ionization implies lower ionization",
        runtime_scope="harness",
        kind="hard_constraint",
        premise_ids=["line:oiii-4960", "line:oiii-5008", "line:oii-3727"],
        applies_to_ids=["line:oiii-4960", "line:oiii-5008"],
        units={"oiii_claimed": "count", "oii_claimed": "count", "oii_excused": "count"},
        conclusion="[O III] detection requires [O II] unless masked or off-spectrum",
        conclusion_polarity="positive",
        satisfied_when="any",
        operands=[
            OperandRecord(
                id="oiii_claimed",
                description="an [O III] component is claimed in the analysis",
                unit="count",
            ),
            OperandRecord(
                id="oii_claimed",
                description="[O II] is claimed in the analysis",
                unit="count",
            ),
            OperandRecord(
                id="oii_excused",
                description="[O II] is masked or off-spectrum at this redshift",
                unit="count",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="oiii_claimed", operator="eq", rhs=0.0,
                            note="no [O III] claim, nothing to require"),
            ConditionRecord(lhs="oii_claimed", operator="ge", rhs=1.0),
            ConditionRecord(lhs="oii_excused", operator="ge", rhs=1.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="ionization consistency holds or is excused",
            fail_verdict="[O III] claimed without [O II] and no mask/edge excuse",
            fail_polarity="negative",
        ),
        provenance=[_cite(f"{_KB}/ionization.md")],
    ),
    FormalRuleRecord(
        id="rule:formal-oiii-doublet",
        name="[O III] doublet spacing and ratio",
        runtime_scope="harness",
        kind="hard_constraint",
        premise_ids=["doublet:oiii"],
        applies_to_ids=["doublet:oiii"],
        units={"sep_deviation": "Angstrom", "ratio_b_over_a": "dimensionless"},
        conclusion="Observed separation and b:a amplitude ratio must satisfy their configured acceptance windows",
        conclusion_polarity="neutral",
        operands=[
            OperandRecord(
                id="sep_deviation",
                description="|observed separation − 47.9*(1+z)|",
                unit="Angstrom",
                threshold=5.0,
                threshold_unit="Angstrom",
                threshold_basis="empirical acceptance tolerance around the physical [O III] separation",
            ),
            OperandRecord(
                id="ratio_b_over_a",
                description="observed amplitude ratio [O III]b / [O III]a",
                unit="dimensionless",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="sep_deviation", operator="le", rhs=5.0),
            ConditionRecord(lhs="ratio_b_over_a", operator="between", rhs=2.0, rhs_high=4.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="doublet spacing and amplitude ratio consistent with [O III]",
            fail_verdict="spacing or ratio outside the [O III] tolerance",
            fail_polarity="negative",
        ),
        provenance=[_cite(f"{_KB}/lines.md", "Doublet Rules")],
    ),
    FormalRuleRecord(
        id="rule:formal-cahk-doublet",
        name="Ca K/H absorption pairing",
        runtime_scope="harness",
        kind="hard_constraint",
        premise_ids=["doublet:cahk"],
        applies_to_ids=["doublet:cahk"],
        units={"amp_cak": "amplitude", "amp_cah": "amplitude"},
        conclusion="Ca K must be deeper than Ca H; a lone component is likely misidentified",
        conclusion_polarity="positive",
        operands=[
            OperandRecord(
                id="amp_cak",
                description="fitted Ca K amplitude (negative for absorption)",
                unit="amplitude",
            ),
            OperandRecord(
                id="amp_cah",
                description="fitted Ca H amplitude (negative for absorption)",
                unit="amplitude",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="amp_cak", operator="le", rhs="amp_cah",
                            note="both amplitudes negative; deeper = more negative"),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="Ca K is deeper than Ca H",
            fail_verdict="Ca K is not deeper than Ca H — likely misidentification",
            fail_polarity="negative",
        ),
        provenance=[_cite(f"{_KB}/lines.md", "Doublet Rules")],
    ),
    FormalRuleRecord(
        id="rule:formal-qso-broad-width",
        name="Type 1 QSO broad-line width",
        runtime_scope="harness",
        kind="graded_diagnostic",
        premise_ids=["class:qso-type1"],
        applies_to_ids=["class:qso-type1"],
        units={"fwhm_kms": "km/s"},
        conclusion="Claimed strict broad lines require FWHM at or above the configured strict boundary",
        conclusion_polarity="positive",
        unknown_handling="if width is unknown, report unknown and do not count the line as broad",
        operands=[
            OperandRecord(
                id="fwhm_kms",
                description="claimed broad-line FWHM",
                unit="km/s",
                threshold=2000.0,
                threshold_unit="km/s",
                threshold_basis="derived strict broad-line boundary shared with width-class match",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="fwhm_kms", operator="ge", rhs=2000.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="broad-line width requirement met",
            fail_verdict="claimed broad line is too narrow for Type 1 QSO",
            fail_polarity="negative",
        ),
        provenance=[_cite(f"{_KB}/classification.md")],
    ),
    FormalRuleRecord(
        id="rule:formal-line-inventory",
        name="Low LIKELY-line inventory confidence cap",
        kind="graded_diagnostic",
        premise_ids=[],
        units={"n_likely_lines": "count"},
        conclusion="Too few LIKELY lines limit evidence strength",
        conclusion_polarity="negative",
        unknown_handling="missing line rows are not absence; only evaluated rows count",
        runtime_scope="synthesis",
        operands=[
            OperandRecord(
                id="n_likely_lines",
                description="number of evaluated lines with status LIKELY",
                unit="count",
                threshold=2.0,
                threshold_unit="count",
                threshold_basis=(
                    "empirical sufficiency floor: two or fewer credible lines "
                    "cannot support strong evidence; the fuzzy membership ramp "
                    "derives its lower endpoint from this bound"
                ),
            ),
        ],
        conditions=[
            ConditionRecord(lhs="n_likely_lines", operator="le", rhs=2.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="line inventory at or below the configured sufficiency bound",
            pass_polarity="negative",
            fail_verdict="line inventory sufficient; no cap from this rule",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/../skills/HypothesisAnalyst/hypothesis_synthesis_skill.md")],
    ),
    FormalRuleRecord(
        id="rule:formal-blue-edge-risk",
        name="DESI blue-edge scrutiny",
        kind="graded_diagnostic",
        premise_ids=[],
        units={"wavelength_obs": "Angstrom"},
        conclusion="Observed wavelengths below the configured blue-edge scrutiny boundary require visual confirmation; invisible features are NOT_FOUND",
        conclusion_polarity="neutral",
        unknown_handling="ambiguous blue-edge morphology remains MARGINAL",
        runtime_scope="synthesis",
        operands=[
            OperandRecord(
                id="wavelength_obs",
                description="observed wavelength of the evaluated line",
                unit="Angstrom",
                threshold=4000.0,
                threshold_unit="Angstrom",
                threshold_basis="empirical start of enhanced scrutiny at the blue end of the DESI spectrum",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="wavelength_obs", operator="lt", rhs=4000.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="blue-edge scrutiny required",
            pass_polarity="neutral",
            fail_verdict="outside the blue-edge zone",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/lines.md", "Blue Edge Noise Zone")],
    ),
    FormalRuleRecord(
        id="rule:formal-oh-zone-risk",
        name="OH airglow contamination scrutiny",
        kind="graded_diagnostic",
        premise_ids=[],
        units={"wavelength_obs": "Angstrom"},
        conclusion="Observed wavelengths above the configured OH scrutiny boundary require a skyline cross-check",
        conclusion_polarity="neutral",
        unknown_handling="ambiguous OH-zone morphology remains MARGINAL",
        runtime_scope="synthesis",
        operands=[
            OperandRecord(
                id="wavelength_obs",
                description="observed wavelength of the evaluated line",
                unit="Angstrom",
                threshold=7800.0,
                threshold_unit="Angstrom",
                threshold_basis="empirical start of the enhanced OH scrutiny zone; OH emission itself is physical, but this boundary is an analysis convention",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="wavelength_obs", operator="gt", rhs=7800.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="OH-zone scrutiny required",
            pass_polarity="neutral",
            fail_verdict="outside the OH-zone",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/lines.md", "OH Airglow Zone")],
    ),
]

_SKYLINES = [
    SkylineRecord(
        id="skyline:oi-5577", name="[O I] 5577 green line",
        kind="emission", wavelength_obs=5577.3,
        note="strong, isolated; often the brightest visible-band skyline",
        citations=[_cite(f"{_KB}/lines.md", "Comprehensive Skyline Table")],
    ),
    SkylineRecord(
        id="skyline:nad1-airglow-5890", name="Na D airglow 5890",
        kind="emission", wavelength_obs=5890.0,
        note="upper-atmosphere sodium layer emission doublet",
        citations=[_cite(f"{_KB}/lines.md", "Comprehensive Skyline Table")],
    ),
    SkylineRecord(
        id="skyline:nad2-airglow-5896", name="Na D airglow 5896",
        kind="emission", wavelength_obs=5896.0,
        note="upper-atmosphere sodium layer emission doublet",
        citations=[_cite(f"{_KB}/lines.md", "Comprehensive Skyline Table")],
    ),
    SkylineRecord(
        id="skyline:oi-6300", name="[O I] 6300 red line",
        kind="emission", wavelength_obs=6300.3,
        note="weaker but narrow and persistent; confused with AGN [O I] 6300",
        citations=[_cite(f"{_KB}/lines.md", "Comprehensive Skyline Table")],
    ),
    SkylineRecord(
        id="skyline:oi-6364", name="[O I] 6364 red line",
        kind="emission", wavelength_obs=6363.8,
        note="3:1 doublet companion to 6300.3",
        citations=[_cite(f"{_KB}/lines.md", "Comprehensive Skyline Table")],
    ),
    SkylineRecord(
        id="skyline:o2-b-6867", name="O₂ B-band",
        kind="absorption", wavelength_obs=6867.0,
        note="strong absorption band; affects continuum and weak-line identification",
        citations=[_cite(f"{_KB}/lines.md", "Comprehensive Skyline Table")],
    ),
    SkylineRecord(
        id="skyline:o2-a-7605", name="O₂ A-band",
        kind="absorption", wavelength_obs=7605.0,
        note="one of the strongest atmospheric absorption bands",
        citations=[_cite(f"{_KB}/lines.md", "Comprehensive Skyline Table")],
    ),
    SkylineRecord(
        id="skyline:oh-band-7000", name="OH Meinel bands 7000–7400",
        kind="band", wavelength_obs=7000.0, wavelength_max=7400.0,
        note="dense OH emission lines begin",
        citations=[_cite(f"{_KB}/lines.md", "Comprehensive Skyline Table")],
    ),
    SkylineRecord(
        id="skyline:oh-band-7800", name="OH Meinel bands 7800–9800",
        kind="band", wavelength_obs=7800.0, wavelength_max=9800.0,
        note="extremely dense OH forest",
        citations=[_cite(f"{_KB}/lines.md", "Comprehensive Skyline Table")],
    ),
]

_WIDTH3SIGMA = [
    Width3SigmaRecord(
        id="fitwin:broad", width_class="broad", width_3sigma_A=90.0,
        citations=[_cite("config/analysis_method.json",
                             "gaussian_fit.width_3sigma_angstrom_by_class")],
    ),
    Width3SigmaRecord(
        id="fitwin:narrow", width_class="narrow", width_3sigma_A=25.0,
        citations=[_cite("config/analysis_method.json",
                             "gaussian_fit.width_3sigma_angstrom_by_class")],
    ),
    Width3SigmaRecord(
        id="fitwin:both", width_class="both", width_3sigma_A=50.0,
        citations=[_cite("config/analysis_method.json",
                             "gaussian_fit.width_3sigma_angstrom_by_class")],
    ),
    Width3SigmaRecord(
        id="fitwin:absorption", width_class="absorption", width_3sigma_A=20.0,
        citations=[_cite("config/analysis_method.json",
                             "gaussian_fit.width_3sigma_angstrom_by_class")],
    ),
]

_INDICES = [
    IndexBandRecord(
        id="index:dn4000", name="Dn4000 (Balogh+ 1999)",
        blue_low=3850.0, blue_high=3950.0,
        red_low=4000.0, red_high=4100.0,
        citations=[_cite("src/FORMA/agentic_graph/elg_path.py", "Dn4000 band computation")],
    ),
]

#: v2 formal rules absorbing the remaining inventory gaps (2026-10-11).
#: v2 正式规则，吸收清单中剩余 gap（2026-10-11）。
_FORMAL_RULES_V2 = [
    FormalRuleRecord(
        id="rule:formal-oiii-orphan",
        name="[O III] doublet orphan in a clean region",
        runtime_scope="harness",
        kind="graded_diagnostic",
        premise_ids=["doublet:oiii"],
        applies_to_ids=["doublet:oiii"],
        units={"n_oiii_components": "count", "clean_unmasked_region": "boolean"},
        conclusion="One [O III] component KEEP while the partner is NOT_FOUND in a clean, unmasked region means the feature is likely not [O III]",
        conclusion_polarity="negative",
        unknown_handling="if the partner status is unknown (masked region, low SNR), report unknown rather than treating absence as negative evidence",
        operands=[
            OperandRecord(
                id="n_oiii_components",
                description="number of [O III] components kept (0, 1 or 2)",
                unit="count",
            ),
            OperandRecord(
                id="clean_unmasked_region",
                description="the partner position lies in a clean, unmasked region (1) or not (0)",
                unit="boolean",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="n_oiii_components", operator="eq", rhs=1.0),
            ConditionRecord(lhs="clean_unmasked_region", operator="eq", rhs=1.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="[O III] doublet orphan in a clean region — fatal for the identification",
            pass_polarity="negative",
            fail_verdict="no clean-region [O III] orphan",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/classification.md", "ELG fatal problems")],
    ),
    FormalRuleRecord(
        id="rule:formal-galaxy-cahk-fatal",
        name="LRG/BGS Ca K/H pairing fatal",
        kind="graded_diagnostic",
        premise_ids=["doublet:cahk", "index:dn4000"],
        applies_to_ids=["class:lrg-bgs"],
        units={"n_cahk_components": "count", "dn4000_break_observed": "boolean"},
        conclusion="One Ca K/H component present without the other AND no 4000 Å break observed is a hard exclusion",
        conclusion_polarity="negative",
        unknown_handling="unknown component or break status yields unknown, never negative evidence",
        operands=[
            OperandRecord(
                id="n_cahk_components",
                description="number of Ca K/H components detected (0, 1 or 2)",
                unit="count",
            ),
            OperandRecord(
                id="dn4000_break_observed",
                description="a 4000 Å break is observed (1) or not (0)",
                unit="boolean",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="n_cahk_components", operator="eq", rhs=1.0),
            ConditionRecord(lhs="dn4000_break_observed", operator="eq", rhs=0.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="Ca K/H pairing violated without a 4000 Å break — hard exclusion",
            pass_polarity="negative",
            fail_verdict="Ca K/H pairing satisfied or excused by a 4000 Å break",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/classification.md", "LRG/BGS fatal problems")],
    ),
    FormalRuleRecord(
        id="rule:formal-galaxy-broad-emission-fatal",
        name="Broad emission in an LRG/BGS classification",
        kind="graded_diagnostic",
        premise_ids=["class:lrg-bgs"],
        applies_to_ids=["class:lrg-bgs"],
        units={"broad_emission_fwhm_kms": "km/s"},
        conclusion="Broad emission at or above the strict width boundary is fatal for LRG/BGS",
        conclusion_polarity="negative",
        unknown_handling="unknown widths are unknown, never fatal",
        operands=[
            OperandRecord(
                id="broad_emission_fwhm_kms",
                description="FWHM of the broadest claimed emission feature",
                unit="km/s",
                threshold=2000.0,
                threshold_unit="km/s",
                threshold_basis="derived strict broad-line boundary shared with width-class match",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="broad_emission_fwhm_kms", operator="ge", rhs=2000.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="strict broad emission in an LRG/BGS classification — fatal",
            pass_polarity="negative",
            fail_verdict="no emission meeting the strict broad width boundary",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/classification.md", "LRG/BGS fatal problems")],
    ),
    FormalRuleRecord(
        id="rule:formal-elg-cahk-zero-weight",
        name="ELG Ca K/H zero exclusion weight",
        kind="graded_diagnostic",
        premise_ids=["doublet:cahk", "class:elg"],
        applies_to_ids=["class:elg"],
        units={"cahk_violation": "boolean"},
        conclusion="Ca K/H failures carry zero exclusion weight for ELG; the emission lines drive the classification",
        conclusion_polarity="neutral",
        unknown_handling="no Ca K/H assessment is not a violation",
        operands=[
            OperandRecord(
                id="cahk_violation",
                description="a Ca K/H violation was recorded (1) or not (0)",
                unit="boolean",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="cahk_violation", operator="eq", rhs=1.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="Ca K/H violation recorded but carries zero exclusion weight for ELG",
            pass_polarity="neutral",
            fail_verdict="no Ca K/H violation to neutralise",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/classification.md", "ELG Ca K/H absorption")],
    ),
    FormalRuleRecord(
        id="rule:formal-qso1-no-broad-line",
        name="Type 1 QSO: no broad line meets the width bound",
        kind="graded_diagnostic",
        premise_ids=["class:qso-type1"],
        applies_to_ids=["class:qso-type1"],
        units={"n_claimed_broad_lines": "count", "n_broad_lines_at_or_above_fwhm_limit": "count"},
        conclusion="If all claimed broad lines fall below the configured general broad-line floor, Type 1 QSO is unsupported",
        conclusion_polarity="negative",
        unknown_handling="unknown widths are unknown, never counted as narrow",
        operands=[
            OperandRecord(
                id="n_claimed_broad_lines",
                description="number of claimed broad emission lines",
                unit="count",
            ),
            OperandRecord(
                id="n_broad_lines_at_or_above_fwhm_limit",
                description="number of claimed broad lines with FWHM at or above the configured limit",
                unit="count",
                threshold=1500.0,
                threshold_unit="km/s",
                threshold_basis="empirical Type 1 broad-line width convention (configurable via rule parameters)",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="n_claimed_broad_lines", operator="ge", rhs=1.0),
            ConditionRecord(lhs="n_broad_lines_at_or_above_fwhm_limit", operator="le", rhs=0.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="all claimed broad lines are below the configured general width floor — Type 1 classification unsupported",
            pass_polarity="negative",
            fail_verdict="at least one claimed broad line meets the width bound",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/classification.md", "Type 1 QSO fatal problems")],
    ),
    FormalRuleRecord(
        id="rule:formal-qso1-missing-broad-line",
        name="Type 1 QSO: a required broad line missing",
        kind="graded_diagnostic",
        premise_ids=["class:qso-type1", "line:lya-1216", "line:civ-1549", "line:ciii-1909", "line:mgii-2800"],
        applies_to_ids=["class:qso-type1"],
        units={"missing_broad_line_in_coverage": "boolean", "missing_broad_line_masked": "boolean"},
        conclusion="Any of Lyα/C IV/C III]/Mg II missing at its predicted, unmasked, in-range position is fatal for Type 1 QSO",
        conclusion_polarity="negative",
        unknown_handling="unknown coverage or mask status is unknown, never fatal",
        operands=[
            OperandRecord(
                id="missing_broad_line_in_coverage",
                description="a required broad line is missing at a predicted position inside the observed range (1) or not (0)",
                unit="boolean",
            ),
            OperandRecord(
                id="missing_broad_line_masked",
                description="the predicted position is masked (1) or unmasked (0)",
                unit="boolean",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="missing_broad_line_in_coverage", operator="eq", rhs=1.0),
            ConditionRecord(lhs="missing_broad_line_masked", operator="eq", rhs=0.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="a required broad line is missing, unmasked, in range — fatal for Type 1 QSO",
            pass_polarity="negative",
            fail_verdict="no unmasked in-range missing broad line",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/classification.md", "Type 1 QSO fatal problems")],
    ),
    FormalRuleRecord(
        id="rule:formal-qso2-nev-requirement",
        name="Type 2 QSO requires a convincing [Ne V]",
        kind="graded_diagnostic",
        premise_ids=["class:qso-type2", "line:nev-3426"],
        applies_to_ids=["class:qso-type2"],
        units={"nev_convincing": "boolean", "has_broad_lines": "boolean"},
        conclusion="A Type 2 QSO without a convincing [Ne V] and without broad lines must not be classified QSO",
        conclusion_polarity="negative",
        unknown_handling="unknown [Ne V] or broad-line status is unknown, never fatal",
        operands=[
            OperandRecord(
                id="nev_convincing",
                description="[Ne V] 3426 is visually convincing (1) or not (0)",
                unit="boolean",
            ),
            OperandRecord(
                id="has_broad_lines",
                description="broad emission lines are present (1) or not (0)",
                unit="boolean",
                threshold=1500.0,
                threshold_unit="km/s",
                threshold_basis="empirical broad-emission width floor (configurable via rule parameters)",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="nev_convincing", operator="eq", rhs=0.0),
            ConditionRecord(lhs="has_broad_lines", operator="eq", rhs=0.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="Type 2 QSO lacks both a convincing [Ne V] and broad lines — do not classify QSO",
            pass_polarity="negative",
            fail_verdict="a convincing [Ne V] or broad lines support the QSO classification",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/classification.md", "Type 2 QSO fatal problems")],
    ),
    FormalRuleRecord(
        id="rule:formal-qso-broad-ordering",
        name="Typical QSO broad-line amplitude ordering",
        kind="graded_diagnostic",
        premise_ids=["class:qso-type1", "line:lya-1216", "line:civ-1549", "line:ciii-1909", "line:mgii-2800"],
        applies_to_ids=["class:qso-type1"],
        units={"amp_lya": "amplitude", "amp_civ": "amplitude", "amp_ciii": "amplitude", "amp_mgii": "amplitude"},
        conclusion="Typical ordering is Lyα > C IV > C III] > Mg II; significant deviations suggest re-examining the identifications",
        conclusion_polarity="negative",
        unknown_handling="missing amplitudes are unknown and do not count as ordering violations",
        operands=[
            OperandRecord(id="amp_lya", description="Lyα amplitude", unit="amplitude"),
            OperandRecord(id="amp_civ", description="C IV amplitude", unit="amplitude"),
            OperandRecord(id="amp_ciii", description="C III] amplitude", unit="amplitude"),
            OperandRecord(id="amp_mgii", description="Mg II amplitude", unit="amplitude"),
        ],
        conditions=[
            ConditionRecord(lhs="amp_lya", operator="ge", rhs="amp_civ"),
            ConditionRecord(lhs="amp_civ", operator="ge", rhs="amp_ciii"),
            ConditionRecord(lhs="amp_ciii", operator="ge", rhs="amp_mgii"),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="broad-line amplitude ordering is typical",
            pass_polarity="neutral",
            fail_verdict="broad-line amplitude ordering deviates — re-examine the line identifications",
            fail_polarity="negative",
        ),
        provenance=[_cite(f"{_KB}/classification.md", "QSO amplitude ordering")],
    ),
    FormalRuleRecord(
        id="rule:formal-outflow-blueshift",
        name="Normal outflow blueshift window",
        runtime_scope="harness",
        kind="graded_diagnostic",
        premise_ids=[],
        units={"delta_v_kms": "km/s"},
        conclusion="High-ionization blueshifts within the configured reference interval are common; offsets outside it warrant scrutiny",
        conclusion_polarity="neutral",
        unknown_handling="unknown velocity offsets are unknown, never a violation",
        operands=[
            OperandRecord(
                id="delta_v_kms",
                description=(
                    "Δv = (z_high − z_low)/(1+z_low)·c; negative = blueshift. "
                    "Requires two kept emission lines with declared rest "
                    "wavelengths and ionization potentials; with fewer there is no "
                    "high-versus-low ionization contrast, so the operand is not "
                    "applicable rather than unknown."
                ),
                unit="km/s",
                # Fewer than two pairable lines is not a missing measurement but an
                # inapplicable rule, and the trace says so per hypothesis:
                # "operand 'delta_v_kms' unknown or missing; missing_meaning=not_applicable".
                # 少于两条可配对谱线不是"测量缺失"，而是规则不适用；trace 会逐假设写明：
                # "operand 'delta_v_kms' unknown or missing; missing_meaning=not_applicable"。
                missing_meaning="not_applicable",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="delta_v_kms", operator="between", rhs=-1000.0, rhs_high=0.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="high-ionization offset within the configured blueshift reference window",
            pass_polarity="neutral",
            fail_verdict="offset outside the normal window — suspect misidentification",
            fail_polarity="negative",
        ),
        provenance=[_cite(f"{_KB}/ionization.md", "Outflow Blueshift Rule")],
    ),
    FormalRuleRecord(
        id="rule:formal-width-class-match",
        name="Feature width consistent with the line width class",
        runtime_scope="harness",
        kind="graded_diagnostic",
        premise_ids=[],
        units={"width_consistency_score": "km/s"},
        conclusion="A narrow feature matching a broad line (or a broad feature matching a narrow line) is flagged, never a sole veto",
        conclusion_polarity="negative",
        unknown_handling="unknown widths are unknown, never flagged",
        operands=[
            OperandRecord(
                id="width_consistency_score",
                description="caller-derived: broad class → fwhm−limit; narrow class → positive below limit, negative at or above; 'both' class → +1 (check skipped)",
                unit="km/s",
                threshold=2000.0,
                threshold_unit="km/s",
                threshold_basis="broad/narrow width-class pivot (configurable via rule parameters)",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="width_consistency_score", operator="ge", rhs=0.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="feature width consistent with the registered width class",
            pass_polarity="neutral",
            fail_verdict="width contradicts the width class — flag, do not veto on this alone",
            fail_polarity="negative",
        ),
        provenance=[_cite(f"{_KB}/ionization.md", "Width Mismatch Policy")],
    ),
    FormalRuleRecord(
        id="rule:formal-width-class-contradiction",
        name="Broad-class claim below the narrow-width boundary",
        runtime_scope="harness",
        kind="graded_diagnostic",
        premise_ids=[],
        units={"claimed_broad_fwhm_kms": "km/s"},
        conclusion="A 'broad'-class line narrower than the configured narrow-width boundary is misidentification or noise",
        conclusion_polarity="negative",
        unknown_handling="unknown widths are unknown, never a contradiction",
        operands=[
            OperandRecord(
                id="claimed_broad_fwhm_kms",
                description="FWHM of a claimed broad-class line; caller supplies it only for broad-class claims",
                unit="km/s",
                threshold=1000.0,
                threshold_unit="km/s",
                threshold_basis="narrow/intermediate classification boundary shared with CWT",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="claimed_broad_fwhm_kms", operator="lt", rhs=1000.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="broad-class claim below the configured narrow-width boundary — misidentification or noise",
            pass_polarity="negative",
            fail_verdict="no broad-class claim below the configured narrow-width boundary",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/../skills/AnalysisAuditor/result_auditor_skill.md")],
    ),
    FormalRuleRecord(
        id="rule:formal-detection-snr",
        name="Detection SNR confidence threshold",
        runtime_scope="harness",
        kind="graded_diagnostic",
        premise_ids=[],
        units={"detection_snr": "dimensionless"},
        conclusion="Detection SNR at the full-confidence bound supports the feature",
        conclusion_polarity="positive",
        unknown_handling="unknown SNR is unknown, never negative evidence",
        operands=[
            OperandRecord(
                id="detection_snr",
                description="detection SNR of the evaluated feature",
                unit="dimensionless",
                threshold=10.0,
                threshold_unit="dimensionless",
                threshold_basis=(
                    "empirical full-confidence detection floor; the fuzzy "
                    "membership ramp derives its upper endpoint from this bound"
                ),
            ),
        ],
        conditions=[
            ConditionRecord(lhs="detection_snr", operator="ge", rhs=10.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="detection SNR meets the full-confidence bound",
            pass_polarity="positive",
            fail_verdict="detection SNR is below the full-confidence bound",
            fail_polarity="negative",
        ),
        provenance=[_cite("src/FORMA/core/reasoning/fuzzy.py", "snr_confidence threshold 5→10")],
    ),
    FormalRuleRecord(
        id="rule:formal-auditor-confidence-cap",
        name="Evidence-sufficiency notice (thin inventory or major revisions)",
        kind="graded_diagnostic",
        premise_ids=[],
        units={"n_credible_lines": "count", "has_major_revisions": "boolean"},
        conclusion="≤2 credible lines or major revisions mean the inventory is insufficient for strong support; this is an evidence-strength notice and does not cap the defect rating by itself",
        conclusion_polarity="negative",
        unknown_handling="unknown line counts or revision status are unknown, never a cap",
        satisfied_when="any",
        operands=[
            OperandRecord(
                id="n_credible_lines",
                description="number of credible (visually confirmed) lines",
                unit="count",
            ),
            OperandRecord(
                id="has_major_revisions",
                description="major revisions were needed (1) or not (0)",
                unit="boolean",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="n_credible_lines", operator="le", rhs=2.0),
            ConditionRecord(lhs="has_major_revisions", operator="ge", rhs=1.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="insufficient inventory for strong support: ≤2 credible lines or major revisions (evidence-strength notice; the defect rating is not capped by this rule alone)",
            pass_polarity="negative",
            fail_verdict="no cap from this rule",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/../skills/AnalysisAuditor/result_auditor_skill.md")],
    ),
    FormalRuleRecord(
        id="rule:formal-lya-forest-visibility",
        name="Lyα forest visibility window",
        kind="graded_diagnostic",
        premise_ids=["line:lya-1216"],
        units={"forest_probe_obs": "Angstrom", "forest_not_visible": "boolean"},
        conclusion="A forest that is observable above the configured blue-edge boundary but not visible downgrades the Lyα identification; beyond the blue edge it is zero information",
        conclusion_polarity="negative",
        unknown_handling="unknown probe or unverified forest visibility is unknown, never negative evidence",
        runtime_scope="synthesis",
        operands=[
            OperandRecord(
                id="forest_probe_obs",
                description="observed wavelength of the forest probe window (λ_pred(Lyα) − configured offset)",
                unit="Angstrom",
                threshold=200.0,
                threshold_unit="Angstrom",
                threshold_basis="blueward forest-probe offset (configurable via rule parameters)",
            ),
            OperandRecord(
                id="forest_not_visible",
                description="FeatureAuditor explicitly found no forest in an observable region (1), or found it (0)",
                unit="boolean",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="forest_probe_obs", operator="ge", rhs=4000.0),
            ConditionRecord(lhs="forest_not_visible", operator="eq", rhs=1.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="forest observable but not visible — downgrade confidence, do not exclude",
            pass_polarity="negative",
            fail_verdict="forest window beyond the blue edge — zero information",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/lines.md", "Lyα Forest and DLA")],
    ),
    FormalRuleRecord(
        id="rule:formal-skyline-contamination",
        name="Skyline proximity contamination",
        kind="graded_diagnostic",
        premise_ids=["skyline:oi-5577", "skyline:oi-6300", "skyline:o2-a-7605"],
        units={"nearest_skyline_offset": "Angstrom"},
        conclusion="Proximity to a registered discrete airglow emission line is evidence of possible atmospheric contamination; inspect the observed feature before assigning its status",
        conclusion_polarity="negative",
        unknown_handling="unknown skyline proximity is unknown, never contamination evidence",
        runtime_scope="synthesis",
        operands=[
            OperandRecord(
                id="nearest_skyline_offset",
                description="|λ_obs − nearest registered discrete airglow emission wavelength|; OH bands are assessed separately",
                unit="Angstrom",
                threshold=10.0,
                threshold_unit="Angstrom",
                threshold_basis="empirical proximity tolerance for discrete airglow lines, not a width of an OH band",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="nearest_skyline_offset", operator="le", rhs=10.0),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="near a registered discrete airglow line — atmospheric contamination possible",
            pass_polarity="negative",
            fail_verdict="not near a registered skyline",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/lines.md", "Comprehensive Skyline Table")],
    ),
    FormalRuleRecord(
        id="rule:formal-dn4000-interpretation",
        name="Dn4000 interpretation bands",
        kind="graded_diagnostic",
        premise_ids=["index:dn4000"],
        applies_to_ids=[],
        units={"dn4000": "ratio"},
        conclusion="Dn4000 is a continuum reference indicator interpreted using the configured moderate and strong bands; it is not a hard class veto",
        conclusion_polarity="neutral",
        unknown_handling="a missing Dn4000 value is unknown and never an exclusion",
        runtime_scope="synthesis",
        operands=[
            OperandRecord(
                id="dn4000",
                description="continuum break ratio computed from the index:dn4000 bands",
                unit="ratio",
                missing_meaning="unknown",
            ),
        ],
        conditions=[
            ConditionRecord(lhs="dn4000", operator="gt", rhs=1.6,
                            note="strong 4000 Å break band"),
            ConditionRecord(lhs="dn4000", operator="between", rhs=1.3, rhs_high=1.6,
                            note="moderate 4000 Å break band"),
        ],
        outcomes=OutcomeSpec(
            pass_verdict="Dn4000 is characteristic of an old stellar population",
            pass_polarity="neutral",
            fail_verdict="Dn4000 does not by itself support or exclude a galaxy classification",
            fail_polarity="neutral",
        ),
        provenance=[_cite(f"{_KB}/classification.md", "Dn4000 as a continuum reference metric")],
    ),
]


#: Empirical judgement numbers (v5).  Declared here, values supplied by a
#: validated payload (``FORMA_RULE_PARAMETERS`` / ``config/rule_parameters.json``).
#: 经验判断数值（v5）。在此声明，取值由受校验载荷提供
#: （``FORMA_RULE_PARAMETERS`` / ``config/rule_parameters.json``）。
_EMPIRICAL_PARAMETERS = [
    EmpiricalParameterRecord(
        id="membership:offset-quality",
        name="Wavelength-offset quality",
        kind="trapezoid",
        unit="Angstrom",
        parameters={
            "left": -80.0,
            "center_left": -20.0,
            "center_right": 20.0,
            "right": 80.0,
        },
        basis=(
            "the single-hypothesis skill treats |offset| < 20 A as a strong "
            "match and > 80 A as a rejection; the trapezoid is that convention "
            "made continuous"
        ),
        citations=[_cite(
            "src/FORMA/agents/multi_agents/harness/skills/HypothesisAnalyst/"
            "single_hypothesis_redrock_skill.md",
            "LIKELY threshold |offset| < 20 A",
        )],
        consumers=[
            "src/FORMA/core/reasoning/fuzzy.py",
            "harness/single_hypothesis.py (run message)",
            "evaluation/calibration (offset weighting)",
        ],
    ),
    EmpiricalParameterRecord(
        id="membership:broad-qso",
        name="Broad-line QSO width membership",
        kind="threshold",
        unit="km/s",
        parameters={"low": 1500.0, "high": 2000.0},
        sources={
            "low": ParameterSource(
                kind="operand_threshold",
                rule_id="rule:formal-qso1-no-broad-line",
                operand_id="n_broad_lines_at_or_above_fwhm_limit",
            ),
            "high": ParameterSource(
                kind="operand_threshold",
                rule_id="rule:formal-width-class-match",
                operand_id="width_consistency_score",
            ),
        },
        basis=(
            "the broad-emission width floor and the width-consistency pivot are "
            "rule bounds, so both endpoints derive from them instead of "
            "restating the numbers"
        ),
        citations=[_cite(
            "src/FORMA/agents/multi_agents/harness/kb/classification.md",
            "Type 1 QSO requires broad lines",
        )],
        consumers=[
            "src/FORMA/core/reasoning/fuzzy.py",
            "harness/single_hypothesis.py (run message)",
        ],
    ),
    EmpiricalParameterRecord(
        id="membership:detection-snr",
        name="Detection SNR confidence",
        kind="threshold",
        unit="dimensionless",
        parameters={"low": 5.0, "high": 10.0},
        sources={
            "high": ParameterSource(
                kind="operand_threshold",
                rule_id="rule:formal-detection-snr",
                operand_id="detection_snr",
            ),
        },
        basis=(
            "full confidence at or above the declared detection floor, fading to "
            "zero at the weak-detection floor of 5"
        ),
        citations=[_cite(
            "src/FORMA/core/reasoning/fuzzy.py", "snr_confidence threshold 5->10"
        )],
        consumers=[
            "src/FORMA/core/reasoning/fuzzy.py",
            "harness/single_hypothesis.py (run message)",
        ],
    ),
    EmpiricalParameterRecord(
        id="membership:line-inventory",
        name="Line-inventory sufficiency",
        kind="threshold",
        unit="count",
        parameters={"low": 2.0, "high": 4.0},
        sources={
            "low": ParameterSource(
                kind="operand_threshold",
                rule_id="rule:formal-line-inventory",
                operand_id="n_likely_lines",
            ),
        },
        basis=(
            "the sufficiency floor is the rule bound (at most two credible lines "
            "caps evidence strength); four lines is the membership's own "
            "saturation point"
        ),
        citations=[_cite(
            "src/FORMA/agents/multi_agents/harness/skills/HypothesisAnalyst/"
            "hypothesis_synthesis_skill.md",
            "<=2 LIKELY lines limits confidence to MEDIUM",
        )],
        consumers=[
            "src/FORMA/core/reasoning/fuzzy.py",
            "src/FORMA/core/reasoning/ontology/harness_rules.py",
        ],
    ),
    EmpiricalParameterRecord(
        id="parameter:oiii-ratio-b-over-a",
        name="[O III] b:a acceptance interval",
        kind="interval",
        unit="dimensionless",
        parameters={"low": 2.0, "high": 4.0},
        basis="empirical ratio acceptance around the physical [O III] doublet strength relation",
        citations=[_cite(f"{_KB}/lines.md", "[O III] doublet")],
        consumers=["src/FORMA/core/reasoning/ontology/evaluator.py",
                   "src/FORMA/agentic_graph/fa_doublet.py"],
    ),
    EmpiricalParameterRecord(
        id="parameter:outflow-blueshift-window",
        name="High-ionization blueshift reference interval",
        kind="interval",
        unit="km/s",
        parameters={"low": -1000.0, "high": 0.0},
        basis="empirical common blueshift interval, not a physical impossibility bound",
        citations=[_cite(f"{_KB}/ionization.md", "Outflow Blueshift Rule")],
        consumers=["src/FORMA/core/reasoning/ontology/evaluator.py"],
    ),
    EmpiricalParameterRecord(
        id="parameter:dn4000-reference-bands",
        name="Dn4000 reference interpretation boundaries",
        kind="interval",
        unit="dimensionless",
        parameters={"low": 1.3, "high": 1.6},
        basis="interpretation bands for a continuum reference indicator, never a hard classification veto",
        citations=[_cite(f"{_KB}/classification.md", "Dn4000 as a continuum reference metric")],
        consumers=["src/FORMA/core/reasoning/ontology/evaluator.py"],
    ),
]


ONTOLOGY = OntologyRegistry(
    schema_version=ONTOLOGY_SCHEMA_VERSION,
    updated="2026-10-14",
    lines=_LINES,
    doublets=_DOUBLETS,
    classes=_CLASSES,
    rules=_RULES,
    formal_rules=_FORMAL_RULES + _FORMAL_RULES_V2,
    skylines=_SKYLINES,
    width3sigma=_WIDTH3SIGMA,
    indices=_INDICES,
    empirical_parameters=_EMPIRICAL_PARAMETERS,
)


__all__ = ["ONTOLOGY"]
