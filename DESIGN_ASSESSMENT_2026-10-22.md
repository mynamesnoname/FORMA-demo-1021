# FORMA Architecture Assessment — Ontology, Early Stopping, and FA/SH Perception

**Date:** 2026-10-22  
**Status:** Discussion-based design assessment; not an implementation specification or experimental result.  
**Scope:** `FORMA-demo-1021`, especially the ontology registry, type routing, SH, FA, and HS.

> This note records architectural assessments from a design discussion. It distinguishes verified code behavior, scientific/engineering judgments, and proposals requiring validation. Nothing below should be interpreted as a measured performance claim.

## 1. Executive summary

FORMA's central engineering objective is **reliable, traceable scientific data verification under practical throughput and inference-cost constraints**, rather than maximising LLM participation or constructing a comprehensive astronomical ontology.

A useful characterization of the current design is:

> **An ontology-inspired, knowledge-constrained, deterministic-first scientific verification workflow with LLM reasoning on demand.**

The ontology registry is substantive: typed concepts, stable IDs, provenance, versioned schemas, diagnostic parameters and formal rules exist. Yet the entire graph should not currently be described as a fully ontology-driven dynamic reasoning system. In particular, some diagnostic priorities and graph transitions remain explicitly encoded in Python.

**Crucial distinction:** Ontology-guided does **not** mean LLM-guided. A deterministic code engine can execute knowledge-derived rules more efficiently and reproducibly than an LLM. The architectural question is whether the scientific semantics and applicability of those rules are explicit, reviewable, versioned, and traceable—not whether a model generates the decision token-by-token.

## 2. Ontology assessment

### Implemented strengths

- `src/FORMA/core/reasoning/ontology/schema.py` defines typed entities such as `LineRecord`, `DoubletRecord`, `FormalRuleRecord`, `OperandRecord`, `ConditionRecord`, and `EmpiricalParameterRecord`.
- `registry/data.py` declares domain quantities and their source citations. Stable identifiers (e.g. `line:nev-3426`) are separate from display names.
- `query.py` exposes typed lookups, including component membership in doublets and spectral reference values.
- The rule layer separates declared operands/thresholds from execution; `prompt_authority.py` supplies per-value source accountability for quantities rendered in prompts.
- Missing or unassessable evidence should not automatically count as negative evidence. This is an important scientific invariant.

### Present limitation

The knowledge model describes many entities and their attributes, and some relations, but broader diagnostic relations (evidence supports/contradicts physical interpretation, interpretation motivates follow-up checks, competing hypotheses predict different features) are not yet uniformly first-class, queryable concepts. Program-specific route priority appears in `agentic_graph/type_entry_router.py`.

This **does not invalidate** the ontology work. It distinguishes a useful *domain knowledge registry with formal rules* from a general-purpose ontology-driven planner.

A particularly useful conceptual separation for future development:

1. **Domain knowledge:** what features, species, doublets, and physical quantities exist.
2. **Diagnostic knowledge:** which observations support or challenge which interpretations, under what assumptions and with what limitations.
3. **Investigation knowledge:** which follow-up checks should be performed to discriminate hypotheses.

A light typed relation layer might eventually link these, without requiring RDF/OWL, a graph database, or unrestricted graph traversal. This is an option, **not a prerequisite** for current VI goals.

## 3. Deterministic hard gates and early stopping

### Design rationale

DESI-scale visual inspection rewards **low wall time, low GPU/token expenditure, reproducibility, and low error**. Local LLM serving may have limited throughput; repeated model calls for tiny, settled decisions add latency and variance.

Therefore, retaining deterministic hard gates is a **deliberate and defensible scientific-computing design**. LLM reasoning should be reserved for ambiguity, conflicts, competing interpretations, and checks that cannot be reduced reliably to known rules.

In `type_entry_router.py`, the code checks evidence in a specified priority order (including adopted [Ne V], QSO diagnostics, old-population diagnostics, and emission-line galaxy diagnostics) and records eligible graph choices. `qso_entry.py` explicitly describes an adopted [Ne V] pair taking a **project-specific Type 2 exit**.

### Important scientific boundary

**Reliable [Ne V] detection → strong evidence for AGN activity** is not strictly identical to **universal physical proof of a Type 2 QSO**. Exact classification can depend on line width, luminosity, alternatives, and the operational class definition. A fast exit can still be valid *within a specified VI protocol* if its assumptions and empirical error rates are explicit.

The project direction discussed was to treat hard gates mainly as:

> **Empirically validated operational stopping rules**, designed for efficient VI while accepting a tightly controlled, nonzero risk of error.

This reflects the practical difficulty of unconditional sufficient conditions for noisy observational data. It does **not** imply scientific sufficient conditions never exist.

Distinguish:

- **Local early exit:** avoid unnecessary nodes within a type investigation.
- **Global early stop:** terminate processing of the spectrum across competing redshift/type hypotheses.

A local accepted result should not automatically imply global termination. The demo presently proceeds to HS merge/comparison after type graphs; the complete pipeline should define global termination separately.

### Recommended rule declaration (illustrative, not current code)

```yaml
rule_id: rule:nev-agn-fast-path
preconditions:
  - feature_id: line:nev-3426
  - state: adopted
conclusion:
  agn_evidence: supported
  project_provisional_class: Type 2 QSO
scope:
  classification_protocol: FORMA_VI
  local_early_exit: qso_investigation
  global_comparison_required: true
audit:
  record_evidence_refs: true
  record_rule_version: true
  record_applicability: true
```

The point is **to move scientific meaning and applicability into reviewable declarations while leaving execution in fast Python**. The example is intentionally not presented as a universal astronomical inference.

## 4. Evaluation of present SH/FA vote design

Relevant code: `agentic_graph/fa_feature_reality.py`, `fa_doublet.py`, `sh_line_review.py`, `vote_runtime.py`, and the associated prompt files.

### What the current code gets right

- FA Reality evaluates the *observed local feature*, independent of astronomical line identity or object type. It consumes frozen measurement/context, valid/masked pixel information and noise summaries.
- FA Doublet evaluates whether a proposed pair is visually corroborated, and uses deterministic computations such as predicted component positions, separation, amplitude ratios, and window assessability.
- SH reviews proposed line-to-measurement assignments under a fixed redshift and writes ID-bound, frozen judgments. It should not be conflated with merely detecting a peak.
- Vote sessions are separated, recorded, and source-linked; runtime captures failures and actual model usage.

### Main concern: correlated votes

Separate LLM sessions using the same model, input, and prompt do **not** guarantee independent prediction errors. A majority can confidently repeat a shared mistake (e.g. an instrumental artifact misread as an emission feature). More votes may reduce random variance without correcting systematic bias, at additional latency/cost.

Evaluate single-vote and quorum accuracy against expert labels, joint failure rates, vote-disagreement informativeness, token usage, and wall time. Do not equate majority fraction with calibrated scientific probability.

### Where dedicated ML is most promising

| Task | Character | Suggested initial approach |
| --- | --- | --- |
| FA feature reality: local peak/trough vs noise/artifact | Predominantly 1D signal recognition | Signal-processing baseline; engineered features + boosted trees; small 1D CNN |
| FA doublet: evidence for two-component interpretation | Signal recognition plus physical/coverage constraints | Preserve deterministic physics checks; evaluate ML for residual ambiguity |
| SH line assignment at fixed redshift | Candidate association with hypothesis-level ambiguity | Keep structured rules and LLM escalation for ambiguous cases; benchmark separately |
| Cross-hypothesis synthesis | Evidence comparison and conflicting interpretations | Rule-constrained LLM reasoning remains plausible; test its actual incremental value |

The present FA reality prompt renders flux samples as a Markdown table. A small numerical model could consume flux, IVAR, mask, wavelength offsets and width/shape features directly. There is no reason to assume an LLM is superior on this closed pattern-recognition task; equally, a dedicated model's advantage must be measured, not presumed.

## 5. Proposal: 2,000-spectrum labeling study

**2,000 spectra are not necessarily 2,000 training examples.** Candidate peaks/troughs create multiple windows per spectrum; the count, quality, class balance, difficulty and dependence of those windows matter. Thousands to tens of thousands of local examples might be available, but this is a hypothesis, not a known dataset statistic.

Suggested labels:
- At window level: convincing peak, convincing trough, noise/artifact, **uncertain/unassessable**.
- At pair level: corroborated doublet, unsupported pair, unassessable.
- Include provenance, masking/coverage, annotation agreement, and the distinction between feature reality and astrophysical identity.

Deliberately sample hard cases: weak true features, single-pixel spikes, skyline residuals, blended profiles, broad/shallow absorption, continuum issues, and partial masks. Hold out entire spectra—and preferably relevant observing groups—to prevent leakage. Keep an independently sampled test set outside active-learning selection.

Compare at least:
1. Existing single LLM vote and multi-vote baselines.
2. Conventional statistical features + gradient boosted trees.
3. A lightweight 1D CNN on local numerical data.
4. A **selective hybrid**: calibrated ML predictions where sufficiently reliable; LLM or human review for uncertain or out-of-distribution cases.

Do **not** use a binary model score directly as a trustworthy probability without calibration. Evaluate on the actual operational candidate distribution, including class-specific false accept/reject costs. The key metric is not only accuracy, but cost and coverage at a preset risk bound.

## 6. Preferred prospective architecture

```text
FITS → deterministic measurements / candidate detection
    → lightweight feature perception (with calibrated selective abstention)
          ├─ sufficiently reliable → accept/reject low-level feature evidence
          └─ ambiguous/OOD       → LLM or human review
    → SH: line association at candidate redshift
    → domain-rule evaluation / cheap type-specific fast paths
          └─ unresolved/conflicting → focused LLM investigation
    → HS: compare competing hypotheses
    → operational stop / continue / abstain
```

This is a **proposal**, not an assertion that the repository currently implements the ML branch. Using ML for perception would not diminish the project's agentic contribution if the latter lies in selecting evidence, managing hypotheses, handling conflicts, and allocating expensive investigations selectively.

## 7. Experiment and decision priorities

1. **Instrument actual costs:** model calls, input/output tokens, provider cache reporting, GPU-seconds if observable, wall time per spectrum, and number of reviewed features.
2. **Ablate voting:** one LLM vote vs independent sessions with majority; compare error correlations and cost.
3. **Establish a human-labeled FA benchmark:** split by spectrum/observation, preserve uncertain examples.
4. **Test ML baselines before engineering a replacement:** simple statistical classifiers first, then small 1D CNN.
5. **Benchmark selective ML→LLM escalation:** evaluate accuracy/risk vs automatically handled fraction and total cost.
6. **Validate hard gates separately:** applicability, empirical error and class-specific scientific consequences; compare enabled vs disabled.
7. **Only then** promote scientific gate declarations to a more generic ontology relation/policy layer where useful.

Suggested outcome metrics: **error rate at stated coverage**, false acceptance on rare critical signals, recall of weak real features, abstention rate, fast-path fraction, latency distribution, GPU cost, and total cost per processed spectrum. All claims about speed or quality require actual measurements.

## 8. Open design questions

- Are hard gates framed as scientific sufficient conditions, or **empirically validated operational stopping policies**? *Current tentative preference: the latter.*
- What exact decision is permitted by a [Ne V] gate: evidence of AGN activity, a project-specific provisional Type 2 QSO label, or final type assignment?
- What level of error is acceptable for local FA rejection, project-level provisional classification, and global early stop? These may differ.
- When should an ambiguous feature be escalated to another LLM vote versus a different model or a human?
- Does SH need LLM reasoning for all candidates, or only when deterministic matching and learned perception leave unresolved alternatives?
- Which real workload metrics should optimize the system: average cost, tail latency, scientific missed discoveries, or a constrained combination?

## 9. Terminology for reports

Prefer:

> **FORMA integrates ontology-inspired domain knowledge and formal diagnostic rules into a deterministic-first, evidence-driven scientific verification workflow, reserving LLM reasoning for cases requiring additional investigation.**

Avoid claiming the current demo is a fully ontology-driven autonomous planner or that operational VI classifications are unconditional physical truths.

## 10. Code references inspected during discussion

- `src/FORMA/core/reasoning/ontology/schema.py`
- `src/FORMA/core/reasoning/ontology/registry/data.py`
- `src/FORMA/core/reasoning/ontology/query.py`
- `src/FORMA/core/reasoning/ontology/prompt_authority.py`
- `src/FORMA/agentic_graph/type_entry_router.py`
- `src/FORMA/agentic_graph/qso_entry.py`
- `src/FORMA/agentic_graph/qso_type1_gate.py`
- `src/FORMA/agentic_graph/graph_workflow.py`
- `src/FORMA/agentic_graph/sh_line_review.py`
- `src/FORMA/agentic_graph/fa_feature_reality.py`
- `src/FORMA/agentic_graph/fa_doublet.py`
- `src/FORMA/agentic_graph/vote_runtime.py`
- `src/FORMA/agentic_graph/prompts/fa_real_feature_system.md`
- `src/FORMA/agentic_graph/prompts/fa_doublet_system.md`

**Review limitations:** This is a targeted architecture/code inspection and design conversation, not a full repository audit or an empirical evaluation. Proposed extensions and expected ML cost/performance benefits remain untested.
