# FORMA demo

[中文说明](README_Chinese.md)

FORMA investigates one-dimensional DESI spectra with a bounded agentic graph. This repository is the **demo version**: it runs from FITS through VI measurements, SH line review, FA feature votes, type-specific graphs, and HS synthesis. It stops **before RA**. Its output is a provisional `Type 1 QSO`, `Type 2 QSO`, `ELG`, or `LRG/BGS` candidate with an anchor redshift, or an explicit abstention. It is not a final classification or defect grade.

```text
FITS → VI (CWT + Redrock + fits) → SH (line review) → FA (independent votes)
     → code-owned type entry → QSO / ELG / LRG-BGS graph → HS merge → HS comparison
     → provisional result or abstention; RA not implemented
```

## Run the demo

Use Python 3.12 from the repository root. The five labeled example FITS files are already in `example/basic/`.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

Install DESI Redrock **in the same environment** so `rrdesi` is on `PATH`. For an existing Redrock checkout, use `python -m pip install -e /path/to/redrock`, then check `rrdesi --help`. Redrock's templates and, when enabled, archetypes are external inputs; they are not included in this repository.

Copy the local configuration templates:

```bash
cp .env.example .env
cp config/analysis_method.example.json config/analysis_method.json
cp config/model_calls.example.json config/model_calls.json
cp config/rule_parameters.example.json config/rule_parameters.json
```

In `.env`, set `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`, and `RR_TEMPLATE_DIR`. Set `ARCHETYPE_DIR` when `USE_ARCHETYPES=true` (the example default). Check that `rrdesi` and these directories resolve in the shell used for the run. The three JSON files are validated method, model-call, and ontology rule-parameter profiles; their example values match the local demo profile. `analysis_method.json` must retain `instrument.arms`. The remaining legacy entries in `.env.example` are not required for `demo.py`.

```bash
python demo.py --preflight-only       # FITS labels only; no Redrock or LLM calls
python demo.py --samples QSO_116     # one sample
python demo.py                       # all five: BGS_2, ELG_6, LRG_1, QSO_4, QSO_116
```

`--samples` accepts any subset of these five names. `--output-root DIR` changes the parent output directory; `--sh-concurrency`, `--fa-concurrency`, and `--fa-max-attempts` control execution. A full run calls Redrock and the configured LLM endpoint, and can be slow or costly. Preflight needs only the FITS reading dependencies. Each full invocation creates a **new** timestamped run directory; it does not resume or overwrite an earlier run.

## Read the outputs

By default, outputs go to `.data/output_/demo/<UTC timestamp>-<id>/`. Start at `index.json`:

```text
<run>/
├── index.json                         Run status and one result/error row per sample
└── QSO_116/                         One directory per requested spectrum
    ├── spectrum.png / spectrum.npz    Full observed spectrum / numerical array
    ├── VI/
    │   ├── features.png               CWT and Gaussian feature overview
    │   └── measurements/manifest.json Frozen measurements and hypothesis references
    ├── SH/H1/.../lines.csv            One ID-bound line table per Redrock hypothesis
    ├── FA/shared/ and FA/H*/           Feature votes and advisory checks
    ├── HS/merge_groups/               Merged candidate groups
    ├── HS/compare_groups/.../report.md Cross-group comparison narrative
    ├── type_graph_summary.json        Routes, surviving hypotheses, HS groups and winner
    ├── reasoning_tree.json            Branch and node lineage, artifact references
    └── visualization_data.json        Read-only browser projection of VI/SH data
```

`index.json` uses `status: completed` when all requested samples finish and `completed_with_failures` when some fail. Each result has `workflow_status`; failed rows include `error_type` and `error`. A completed row's `winner_type`, `winner_redshift`, and `winner_group_id` describe the **provisional HS selection**. `winner_group_id: null` means abstention. `truth`, `type_matches_vi`, and `absolute_vi_redshift_error` are comparisons with the FITS `FIBERMAP` VI label, not inputs to the HS decision or an independent accuracy measurement.

For a sample, read `type_graph_summary.json` for `hypotheses`, `surviving_hypotheses`, `hs_groups`, and `hs_comparison`. `hs_comparison.reason` explains the selected group or abstention; `ra_review_pending: true` and `final_classification_available: false` mark the boundary. Then follow `reasoning_tree.json` and the referenced `node.json` files to inspect individual decisions. SH's `lines.csv` records line-to-feature assignments; FA's separate vote artifacts record the feature-reality votes. `stage1_session.md` and other session Markdown files preserve model prompts and responses. `visualization_data.json` and plots are reading aids; the original node artifacts remain the evidence source.

After a **successful** run, generate the optional offline HTML node gallery:

```bash
python scripts/build_demo_node_gallery.py .data/output_/demo/<run-directory>
# Open <run-directory>/ui/index.html in a browser; file:// works.
```

The gallery shows investigation paths, node decisions, votes, and spectrum positions with a Chinese/English switch. It is generated from that run's artifacts; it is not automatically created by `demo.py`. Local runs and generated galleries are ignored by Git, so a fresh clone must run the demo to create them.

## Configuration and scope

`config/analysis_method.example.json` holds instrument ranges and measurement/review methods; `config/model_calls.example.json` holds stage sampling temperatures; `config/rule_parameters.example.json` holds declared ontology operand overrides. The code records frozen parameter sources and digests in its run artifacts. `.env` and local `config/*.json` are ignored by Git; never commit credentials. Model-facing prompts are packaged under `src/FORMA/agentic_graph/prompts/`.

The five spectra are developer examples, not a held-out evaluation set. Model outputs can vary between runs. The graph ends at HS: no RA review, final report, or final classification is claimed. A failed sample may retain partial stage artifacts and a `run_outcome.json` for diagnosis.

## Tests

```bash
python -m unittest discover -s tests/agentic_graph -p 'test_*.py'
python -m unittest discover -s tests/reasoning -p 'test_*.py'
```

License: MIT.
