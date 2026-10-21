### 3a. Spectrum Summary

Hypothesis redshift: 0.7079175775287458

Hypothesis reference: H6 (branch `main`, run `graph-325ff74c7f444efdb17e3f3b69698eea`). Reported wavelength coverage: 3600.0–9824.000000000524 Å. No masked regions were supplied in the spectrum summary. Measurement catalog reference: `sh/H6/catalog`.

### 3b. Recorded Graph Outcome

Graph path status: survive
Candidate type: Type 1 QSO

The terminal code node is `sh2/3ee7584874ff49f9862661771dbfaf44/node` (`qso.route_result`), applying rule `project:qso-type1-formal-gate` version `forma-qso-entry-v1`, with no reason codes recorded. The route was driven by the formal Type 1 gate at `sh2/348a2821d578400ebf6fd189a8951e0d/node`, which recorded `gate_status: type1_supported` for the selected line `line:mgii-2800` with effective state `paired`, drawing on the coverage node `sh2/13a17fbf7668439794ad865845ab7903/node` and the broad-line inventory `sh2/5b72c414f0cf456ca43df96d8bed97ad/node`. The broad-line inventory recorded `any_supported_broad_line: true` with Mg II broadness `supported` (FWHM 2497.013289890503 km/s against the strict broad threshold of 2000.0 km/s), and the missing-broad-line queue `sh2/6919df0e16a14a81af29d6323e4ce413/node` selected only `line:mgii-2800` for local read.

### 3c. Per-Line Results

**adopted**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| Mg II (`line:mgii-2800`) | 4782.169217080488 | `cwt:em:0000` / 4768.000000000266 | CWT / 2497.013289890503 | MARGINAL | signal_present (3/3 yes) | paired | — |

**rejected_measurement**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| Ca H_abs (`line:cah-3969-abs`) | 6779.749615758109 | `fit:H6:0003` / 6784.746 | fit_doublet / 2403.0 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Hε (`line:heps-3970`) | 6780.6035745468735 | `fit:H6:0006` / 6798.722 | fit_peak / 1201.4 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Hδ (`line:hdel-4102`) | 7007.415028842691 | `fit:H6:0007` / 7026.638 | fit_peak / 309.0 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Hδ_abs (`line:hdel-4102-abs`) | 7007.415028842691 | `fit:H6:0012` / 7010.401 | fit_peak / 7889.4 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| G-band_abs (`line:gband-4305-abs`) | 7353.609921807769 | `fit:H6:0013` / 7358.995 | fit_peak / 3573.9 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Hβ (`line:hbet-4862`) | 8305.090804249032 | `fit:H6:0009` / 8323.558 | fit_peak / 84.8 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Hβ_abs (`line:hbet-4862-abs`) | 8305.090804249032 | `fit:H6:0015` / 8295.764 | fit_peak / 813.9 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Mg I_abs (`line:mgi-5176-abs`) | 8841.376923593058 | `cwt:abs:0003` / 8831.200000000299 | CWT / 125.14598650991758 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |

**no_pairing**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| Mg II_abs (`line:mgii-2800-abs`) | 4782.169217080488 | — | — | NOT_FOUND | — | not_evaluated | — |
| [Ne V] (`line:nev-3426`) | 5851.325620613483 | — | — | NOT_FOUND | — | not_evaluated | — |
| [O II] (`line:oii-3727`) | 6365.408811449635 | — | — | NOT_FOUND | — | not_evaluated | — |
| Ca K_abs (`line:cak-3934-abs`) | 6720.314084060109 | — | — | NOT_FOUND | — | not_evaluated | — |
| Hε_abs (`line:heps-3970-abs`) | 6780.6035745468735 | — | — | NOT_FOUND | — | not_evaluated | — |
| Hγ (`line:hgam-4341`) | 7415.265746356556 | — | — | NOT_FOUND | — | not_evaluated | — |
| Hγ_abs (`line:hgam-4341-abs`) | 7415.265746356556 | — | — | NOT_FOUND | — | not_evaluated | — |
| [O III]a (`line:oiii-4960`) | 8471.783559815838 | — | — | NOT_FOUND | — | not_evaluated | — |
| [O III]b (`line:oiii-5008`) | 8553.592811779465 | — | — | NOT_FOUND | — | not_evaluated | — |

### 3d. Key Findings and Graph Actions

The only line carried into the Type 1 gate was Mg II (`line:mgii-2800`, measurement `cwt:em:0000`): SH status `MARGINAL`, FA state `signal_present`, vote summary 3 yes / 0 no (`assured`), cleaned pairing `adopted`, graph gate state `paired`. Its coverage node (`sh2/13a17fbf7668439794ad865845ab7903/node`) recorded `usable` coverage over the requested window [4632.169217080488, 4932.169217080488] Å (actual [4632.800000000235, 4932.000000000303] Å), 375/375 usable samples, 0 explicitly masked samples, and `full_window_explicit_mask_proof: false` — so the window is not described as fully masked.

The broad-line inventory (`sh2/5b72c414f0cf456ca43df96d8bed97ad/node`) placed Lyα, C IV, and C III outside the reported wavelength range (`outside_range`, `out_of_scope`), so those lines were not evaluated on this path. The missing-broad-line queue (`sh2/6919df0e16a14a81af29d6323e4ce413/node`) recorded an empty queue and selected only Mg II for local read.

All other supplied line records carry SH `NOT_FOUND` with `no_pairing` and `not_evaluated` gate states (Mg II_abs, [Ne V], [O II], Ca K_abs, Hε_abs, Hγ, Hγ_abs, [O III]a, [O III]b), or carry `MARGINAL` SH status with FA `signal_absent`, 0 yes / 3 no (`assured`) votes, and `rejected_measurement` cleaned pairing (Ca H_abs, Hε, Hδ, Hδ_abs, G-band_abs, Hβ, Hβ_abs, Mg I_abs). These rejected measurements were not promoted to the gate; a rejected measurement does not by itself prove the line absent. No Q8 targeted measurements were supplied (`targeted_measurements` empty), and no Q5–Q8 local reads beyond the Mg II coverage node were executed on this path. No conflicts or unresolved items were recorded, and no nodes were listed as skipped.

The line-alignment record (`alignment/06f7bfce442546da93261a370f8f40bc/node`) shows no collisions; Mg II is the sole `original_claim` (effective feature `cwt:em:0000`), and all other entries are `unassigned` with null effective features. These alignment votes did not modify the original SH/FA rows or the route.

### 3e. Recorded Classification

Preliminary classification: Type 1 QSO
Recorded classification: Type 1 QSO

The preliminary classification (Type 1 QSO) was carried through the formal Type 1 gate at `sh2/348a2821d578400ebf6fd189a8951e0d/node`, which recorded `type1_supported` on the strength of the paired, broad Mg II line, and the route result at `sh2/3ee7584874ff49f9862661771dbfaf44/node` returned `survive` with candidate type Type 1 QSO under rule `project:qso-type1-formal-gate` (v `forma-qso-entry-v1`). This is the graph's rule-based result for hypothesis H6 only, not a final choice among Redrock hypotheses.

### 3f. Caveats and Open Items

- Mg II coverage is `usable` but `full_window_explicit_mask_proof` is `false` (`sh2/13a17fbf7668439794ad865845ab7903/node`); the window is not proven fully masked, and no masked regions were supplied.
- Mg II SH status is `MARGINAL` (not a clean detection label), though FA recorded `signal_present` with an assured 3/0 vote; FA signal presence confirms a signal at the measurement, not independently the line identity.
- Lyα, C IV, and C III fall outside the reported wavelength range and were not evaluated on this path (`sh2/5b72c414f0cf456ca43df96d8bed97ad/node`).
- The many `MARGINAL`/`signal_absent`/`rejected_measurement` lines (Ca H_abs, Hε, Hδ, Hδ_abs, G-band_abs, Hβ, Hβ_abs, Mg I_abs) were not evaluated by the type gate; rejection does not establish absence. For the Ca H-region observations, Hε is not separately resolved.
- No Q8 targeted envelope proxies were supplied, so no model-selected amplitude/width proxies are reported.
- Line-alignment entries other than Mg II are `unassigned` with null effective features; an unassigned slot does not prove line absence.
- No conflicts, unresolved items, or skipped nodes were recorded in the canonical context.
