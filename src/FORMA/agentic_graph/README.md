# Agentic graph reasoning implementation boundary

This package is the independent implementation path for the investigation graph.
`graph_workflow.py` now controls a pilot run through VI, concurrent SH, FA
feature-reality voting, the three implemented type graphs, deterministic HS
hypothesis consolidation and provisional HS cross-group comparison. It stops before RA and final reporting. `demo.py` at the repository root
runs the five example FITS inputs (or a selected subset). The graph runner
writes `type_graph_summary.json` and `reasoning_tree.json` under a fresh
per-spectrum directory. `final_classification_available` is false and no
legacy `final_report.md` or `in_brief.csv` is produced. The controller can
also resume at a complete frozen SH boundary through `run_from_sh`.

New node attempts are stored under readable stage directories in each
per-spectrum output root. For example, `SH/H1/pre_analysis/branches/main/<execution-id>/`
contains the first SH node's `execution.json`, session and result files;
`SH/H1/qso/...` contains its type-graph nodes. FA uses `FA/shared/...` for
run-wide CWT features and `FA/H3/...` for hypothesis-scoped fits or reviews.
HS uses `HS/...`; future RA nodes use `RA/...`. A branch folder separates
reasoning forks, and each retry gets a new execution directory. The manifest
retains the full logical node key, execution ID and attempt ID. Run-level
indexes such as `reasoning_tree.json`, `sh_batch_summary.json` and
`type_graph_summary.json` remain at the output root for quick access. Existing
archives retain their old `runs/.../nodes/...` paths; trace replay resolves
the recorded `relative_dir` and does not require moving them.

`vi_fits_adapter.py` reuses the FITS reader, CWT detector and Redrock runner
as measurement services, then freezes run-scoped CWT IDs and hypothesis-scoped
fits. It assigns neutral H labels from unique Redrock `znum` values and records
the seed and referents. This adapter does not build the old Evidence Graph.
The shared FITS reader has already filtered masked pixels, so the current new
catalog records no explicit mask intervals; coverage checks still inspect
available pixels and IVAR. Preserving the original pixel-mask provenance is a
remaining input-boundary task.

New graph runs write `spectrum.png` at the sample root (full spectrum plus
configured camera bands). The `VI/` directory holds the CWT CSVs,
`measurements/` catalogs, `features.png` and `continuum_display.npz`.
The Chebyshev continuum is a display-only fit and never changes CWT, prefits,
FA or HS decisions. Every completed `SH/<hypothesis>/pre_analysis/...` attempt
also writes `adopted_lines.png` from the frozen `lines.csv`, showing only
`LIKELY` and `MARGINAL` rows. Existing archives retain their recorded VI paths;
to add PNGs without relocating evidence, run
`python evaluation/agentic_graph/render_demo_plots.py <basic-five-run-directory>`.
Completed FITS graph runs also write `visualization_data.json` and
`visualization_data.js` at the sample root. These contain the full-resolution
spectrum, valid-pixel mask, display continuum, frozen VI CWT/Gaussian
measurements and each SH hypothesis's exact CSV cells, with relative source
names and SHA-256 digests. They contain no absolute machine paths. A local HTML
file beside the JS can use `<script src="./visualization_data.js"></script>`
and read `window.FORMA_VISUALIZATION_DATA` without `fetch`, a server, Python,
FITS or NPZ decoding. The JSON and JS are display projections; the original
NPZ, catalogs and CSVs remain authoritative. `run_from_sh` resumption and old
archives can create the bundle with the same `render_demo_plots.py` command.

The automatic FA phase runs single-feature
reality votes, then eligible Lyα forest and doublet advisory reviews. Their
results enter only the HS group-comparison dossier. The LRG/BGS graph opens
its own targeted Ca H/K review when needed; it does not reuse an FA doublet
vote as a type-gate result. Its
current route admits strong Dn4000 or an adopted Ca component for further
inspection. A single adopted Ca component with non-strong Dn4000 requires a
completed doublet vote and branch-local pixel-ID sampling of the missing
absorption component before the type path can survive. Those selections save
an explicitly assumed `±kσ` FWHM proxy in Å and km/s; the Ca value has its own
`audit.doublet_review.cahk_outer_reference_sigma` method setting. QSO Q8's
existing FWHM proxy is also shown in both units in Q11.

`PYTHONPATH=src python -m FORMA.agentic_graph --status` remains a status-only entry point from a source checkout.

The fixed workflow remains available on the research branch. Start the new graph
from SH questions and primary scientific inputs; do not import `FORMA.core.evidence`
nodes/edges or ingest its projected graph as a runtime foundation. Reuse only
individually reviewed readers, measurement tools, reference knowledge, LLM
client, configuration and output contracts through explicit adapters. Do not
move the old implementation into this package or silently fall back to it.

Design source: `agenticGraphReasoningDesign/agentGraphicReasoningDesign.md` and
its Canvas diagrams. The research branch retains WP-044 and WP-045 as the
SH→FA and downstream plan records. The
SH→FA feature registry and JSON branch tree implement historical forks; the
graph-wide action contracts and downstream invalidation remain open. See
`agenticGraphReasoningDesign/implement/README.md` for the prompt draft and
adapter contract.

The new VI measurement boundary (`vi_measurements.py`) assigns run-local CWT
IDs once and shares them across Redrock hypotheses. After Redrock, it runs
targeted Gaussian prefits for each hypothesis, assigns hypothesis-scoped fit
IDs, and freezes a catalog per hypothesis before any SH model call. The new SH
adapter requires a frozen VI catalog and never refits or renumbers observations.

New FITS graph runs use `sh_line_review.py`: one model session writes only the
ID-bound per-line CSV and judgment record. It does not write a hypothesis
verdict, preliminary type, or SH report. Historical SH nodes with the earlier
report and second-stage classification remain importable for replay.
After FA, `type_entry_router.py` records all four ordered checks ([Ne V], QSO
diagnostic lines, Dn4000/Ca H/K, [O II]/[O III]) and their measurement and vote
sources. The first eligible graph is a starting investigation path, not a final
type; all eligible graphs remain visible in the route artifact. No positive
check leaves the hypothesis unresolved rather than pruning it because SH chose
`null`. Type graph reports are produced after graph analysis.

`qso_type1_gate.py` is the pure Q9 policy component. It selects Lyα+C IV,
C IV+C III], C III], or Mg II according to the
four predicted-line coverage states. A proven fully masked line is neutral;
if every line in the chosen group is fully masked, the next in-range line is
tried. Neutral masks alone cannot support Type 1. Partial masks and no usable
data from other causes stay unresolved. `qso_type1_path.py` now connects this
component to Q4–Q8 and persists Q9/Q10 on the active branch. Q5 verifies full
window masks against explicit mask intervals; invalid IVAR alone is unresolved.
Q6 reads frozen NPZ samples; Q7 registers a branch-local candidate without
requiring a new Gaussian fit. Q8 runs isolated anonymous peak-plus-two-baseline
selection sessions, computes local amplitude and envelope-width proxies, and
then opens fresh ratio-acceptance sessions. On an accepted vote it records the
complete target pick at the median proxy width. Q9 requires that proxy to meet
the declared broad-line width threshold before marking a recovered line as
`vote_explained`. These proxies do not overwrite VI/FA measurements and are
not fitted Gaussian FWHM values. QSO-specific read width, edge-sigma
convention, odd vote quorum and retry limit are declared in
`config/analysis_method.example.json`; a run can override them in its local
`config/analysis_method.json`.
`cleaned_line_view.py` now joins SH line judgments to the current branch's FA
feature states by exact measurement ID. `qso_entry.py` persists the global
initial route and the QSO Q0–Q3 entry segment as branch-scoped code nodes.
Historical null preliminary types are pruned before QSO entry; new line-only
nodes are routed from SH×FA evidence instead. An adopted [Ne V] pairing
takes the project's Type 2 exit, while unresolved pairings continue to the
Type 1 inventory. `GraphWorkflow` dispatches this segment after FA reality.
`qso_report.py` implements Q11 for a completed Q2 Type 2 exit or a validated
Q9→Q10 Type 1 outcome. It verifies the active branch, terminal rule mapping,
source digests and unchanged SH×FA view before asking the model to summarize.
The model writes only the explanatory sections; code inserts the exact per-line
table and rejects changed redshift, path or type lines. Report, context, session
and node have separate branch-scoped artifacts and digests. A fresh QSO entry
can call `run_qso_entry_through_report` for either Q2 or Type 1 Q4–Q10; an already archived path can use
`evaluation/agentic_graph/run_qso_reports.py <input-trace> <new-output-trace> <hypothesis-ref>`.
The CLI graph workflow calls this path. `hs_merge.py` then groups surviving
hypotheses by terminal type and exact shared diagnostic CWT pair, records
nearest-redshift merge steps, solves a global monotone one-to-one line table,
and publishes a separate `merged_anchor_redshift`. Its source-bound
`hs.merge_groups` node preserves all candidates, exclusions and original
redshifts. `type_recheck_required` and `anchor_assignment_unstable` remain
open outcomes. The summary exposes group IDs and the HS artifact reference;
RA, final classification and final report remain open. The detailed contract
is `agenticGraphReasoningDesign/implement/hs_merge_contract.md`.
`line_alignment.py` runs between a type graph's recorded route and its report
in the live graph workflow. It detects one frozen feature claimed by multiple
kept lines within a hypothesis. Diagnostic collisions open anonymous,
independent pixel-selection votes over the frozen NPZ; non-diagnostic cases
remain TBD. Ca K/H uses two slots, with Hε left unresolved in the red Ca H
region. Hβ/[O III] uses fixed wavelength-ordered slots, so two observed peaks
are never shifted into the first two names. The node archives all selections,
retries, source digests and branch references. It adds advisory measurements
and report annotations without changing SH/FA rows or an already decided type
route. A null slot means no separately defensible feature, not line absence.
`elg_path.py` now implements the branch-local ELG E0–E5 path. Adopted [Ne V]
creates a source-bound handoff event and enters QSO Q2 under the same
hypothesis and redshift; an optional async wrapper completes Q11. The
ELG and LRG/BGS graphs also check adopted Lyα, C IV, C III] and Mg II after
the [Ne V] guard. Any such pairing hands the hypothesis to the QSO Type 1
investigation, where Q3–Q10 decide the outcome. An adopted Mg II emission
plus Mg II absorption pair keeps the hypothesis in its galaxy graph, even if
another diagnostic line is adopted. The guard records those retained lines;
pending or rejected FA measurements never trigger a handoff. Both wrappers
complete the transferred Type 1 path before Q11, and the workflow reports
the QSO terminal status rather than the intermediate Q3 status. The
Ca K/H and mask-aware Dn4000 findings are consultative, and an unpaired
[O II]/[O III] claim stays unknown rather than proving absence. ELG-only
survivors receive a deterministic source-bound report. The offline
`evaluation/agentic_graph/run_elg_paths.py` appends these nodes to an existing
SH+FA trace without calling an LLM. Its outputs are graph-path candidates,
not independently calibrated spectral classifications.
`lrg_bgs_path.py` implements the LRG/BGS G0–G7 path on the same frozen
SH+FA boundary. An adopted [Ne V] pair transfers to QSO Q2 with a checked
route source. The user-approved, graph-specific Canvas rule routes a measurable
strong Dn4000 to LRG/BGS survival and a measurable weaker index to failure;
unmeasurable Dn4000 remains unresolved. Ca H/K counts and independent
window votes are advisory, and neither changes FA feature state. The async
runner may complete Q11 after a QSO handoff. The offline
`evaluation/agentic_graph/run_lrg_bgs_paths.py` archives the deterministic
path without LLM calls and leaves assessable Ca H/K advice pending. This new
route is not yet scientifically validated on real LRG/BGS spectra; the older
pipeline's Dn4000 rule remains descriptive.
The model writes line IDs, measurement IDs, statuses and short judgments;
`sh_measurement_refs.py` resolves measurements into the existing CSV schema.
The provisional node records digests for the catalog, judgments, CSV and
report. The legacy batch SH interface is unchanged, and `GraphWorkflow` now
submits the new SH sessions. This ID-boundary pilot does not
certify line identities or report prose.

An allocated SH execution writes `stage1_session.md` and `stage2_session.md`
beside its report; callers using the earlier direct-path API get
`<report-stem>_stage1_session.md` and `<report-stem>_stage2_session.md`.
The files contain the model input and returned messages, including tool calls
and results, and any reasoning field that the provider actually returns. They
are appended during execution, so failed stages retain their partial record.
Completed node values carry both archive paths and SHA-256 digests. The current
DeepSeek tool-calling setup disables thinking, so no separate reasoning field
is expected in its archives.

`fa_feature_reality.py` now provides a one-feature FA boundary. It binds an
internal measurement ID to a frozen VI catalog and checks the spectrum digest
before rendering the complete local pixel window. The model sees neither
measurement source nor proposed line identity and submits exactly one `yes` or
`no` observation judgment. `fa_review.py` now collects independent sessions
up to the declared odd vote quorum, with bounded concurrency and retries. It
records failed attempts and unusable windows without counting them as votes.
The graph workflow imports the finished SH nodes before FA voting. SH and FA session archives include provider token/cache usage;
carried history is excluded from new-call totals.

`fa_lya_forest.py` adds a separate, hypothesis-scoped advisory node for a kept
Lyα claim. It reads a configured blueward region and redward reference from the
frozen spectrum, records coverage and masks, and collects an odd number of
independent yes/no visibility votes. Insufficient blueward samples produce
`unreviewable` without a model call; exhausted vote seats leave `pending`.
`read_lya_forest_information` resolves the active branch result for HS
comparison; a future RA may also read it. `not_seen` means only that the submitted pixels did not show
a forest; it is not a missing-line verdict, feature reality vote, or QSO gate.
The offline runner is `evaluation/agentic_graph/run_fa_lya_forest.py`.

`fa_doublet.py` reviews the five legacy FA doublets ([O III], [S II],
[N II], Ca K/H, Na D) per hypothesis when SH keeps at least one component.
It handles complete pairs and orphan claims, joins branch-local cleaned
SH×FA pairings to frozen VI measurements, and renders the joint spectrum
around both predicted positions. Code records usable pixel coverage,
predicted/measured separations and the registry-backed amplitude-ratio hint;
the configured independent model sessions vote on the joint interpretation.
An out-of-range or unusable component is `unreviewable`, and exhausted
sessions are `pending`. The result is advisory, does not change feature
reality or any type gate, and can be read through `read_doublet_information`.
Its windows, valid-pixel minimum, odd quorum and retry limit live in
`config/analysis_method.example.json` under `audit.doublet_review`.
The offline runner is `evaluation/agentic_graph/run_fa_doublet.py`; it needs
an existing SH+FA branch trace and writes a new trace under the same artifact
root. The current default windows are engineering starting values, not a
calibrated scientific detection threshold.

The three FA vote paths share `vote_runtime.py` for independent session
submission, bounded concurrency/retries, immutable attempt directories,
binary quorum and model-usage accounting. Scientific preflight and state
writeback remain node-owned: only feature-reality ballots update the registry.
The runtime freezes the rendered system/user prompt text for a vote batch;
each feature-reality seat rechecks its prompt fingerprint before submission.
The fingerprint covers prompt text and tool name, not the provider's full
request or tool schema. It is provenance, not proof of a KV cache hit.
`cache_hit_reported_calls` and `cache_hit_unreported_calls` distinguish an
explicit provider-reported zero from an absent field. Calls made during failed
attempts are archived and included in usage when the provider returned them.
The existing `session.md` contains the exact prompts and provider usage for
each attempt. Concurrent identical requests may benefit from a provider's
prefix cache, but this is observed from actual usage rather than assumed.

The offline SH→FA handoff is implemented in `feature_registry.py` and
`reasoning_trace.py`. SH only contributes pre-analysis artifacts. Selected
CWT IDs become one run-scoped feature entry; Gaussian fit IDs stay local to
their hypothesis. FA ballots are appended to the relevant entry and project
an observed-signal state only at the declared odd quorum. A revisit forks the
JSON reasoning tree at a named analysis event, preserving the parent branch.
Each entry also freezes `skyline_risk` from the 274 vacuum, Earth-frame
wavelengths in `data/desi_sky_lines.json` (DESI `desispec.sky.get_sky_lines()`,
v0.70.0). The existing configurable skyline-proximity rule supplies the match
tolerance; registry OH bands supply separate region warnings. The matched line,
offset, threshold provenance and catalog digest are recorded. This is a risk
annotation, not a mask, atmospheric-origin verdict or change to FA ballots.
DESI's list gives positions without species labels, so a nearby entry must not
be reported as a confirmed OH identification. The QSO type graph and its Q9
gate do not consume this property; it is reserved for a later HS or RA review
contract.
The bundle exporter in `evaluation/agentic_graph/replay_sh_fa_branch.py`
demonstrates this contract against archived QSO_4 artifacts without further
model calls. Its fixture-vote branch is excluded from scientific selection.

For new branch-aware runs, `execution_artifacts.py` reserves one directory
per stage, hypothesis or feature, logical node, branch and execution. Its
`execution.json` records the full run, execution and attempt IDs. The runners
write readable artifact filenames there and
include the execution identity in `node.json`. `reasoning_trace.py` indexes
executions and output artifacts by relative path and SHA-256, and events cite
the producing execution. Retries and child branches allocate new directories;
older archives remain importable. `GraphWorkflow` uses this allocation API for
SH and type-graph attempts.

For a complete FA reality run from validated VI/SH archives, use
`evaluation/agentic_graph/run_fa_reality.py <source> <new-output-dir>`.
The entry point loads the configured model, imports all SH nodes, reviews every
selected feature, and saves the registry, per-event branch snapshots, final
branch JSON and vote summary. The QSO_4 live record is in
the research branch's WP-045 evaluation archive.

After type-graph routing, `GraphWorkflow` archives deterministic `hs.merge_groups`
and runs `hs.compare_groups`. The comparator presents surviving groups, not raw
Redrock hypotheses, and writes a branch-bound JSON decision and readable report.
Multiple groups use one archived, tool-free model session; zero or one group is
resolved by code. A selection remains provisional until RA review. See
`agenticGraphReasoningDesign/implement/hs_comparison_contract.md`.
