### 3a. Spectrum Summary

Hypothesis redshift: 0.23787248591105023

- Hypothesis reference: H1 (branch `main`, run `graph-853b617a68f04c36bd82f06bdb770ac4`).
- Reported wavelength coverage: 3600.0–9824.000000000524 Å.
- Masked regions: none supplied.
- Measurement catalog: `sh/H1/catalog`; SH judgments from `sh/H1/judgments` and `sh/H1/node`.

### 3b. Recorded Graph Outcome

Graph path status: survive
Candidate type: Type 2 QSO

The terminal code node is `sh2/f38acbe4c26a4b3d874cddbd392aaded/node`, applying rule `project:qso-nev-type2-exit` (version `forma-qso-entry-v1`). No reason codes were recorded. The recorded supporting action is the Q2 `qso.nev_pairing_gate` node (`sh2/f38acbe4c26a4b3d874cddbd392aaded/node`): for `line:nev-3426` / `cwt:em:0001`, SH status `LIKELY`, FA state `signal_present`, pairing `adopted`, yielding candidate type `Type 2 QSO`, path status `survive`, next node `qso.analysis_report`. This is a Q2 [Ne V] gate exit; Q3–Q10 were bypassed (see 3d).

### 3c. Per-Line Results

**adopted**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| [Ne V] (`line:nev-3426`) | 4240.951136731258 | `cwt:em:0001` / 4242.400000000146 | CWT / 1917.164597169737 | LIKELY | signal_present (3/3 yes) | q2_type2_support | — |
| [O II] (`line:oii-3727`) | 4613.550754990484 | `cwt:em:0002` / 4616.800000000231 | CWT / 1099.106885263833 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| Hε (`line:heps-3970`) | 4914.47755631546 | `cwt:em:0004` / 4912.8000000002985 | CWT / 1249.668861064443 | MARGINAL | signal_present (3/3 yes) | not_evaluated | — |
| Hδ (`line:hdel-4102`) | 5078.867022444447 | `cwt:em:0005` / 5079.200000000336 | CWT / 999.0464379992876 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| Hβ (`line:hbet-4862`) | 6019.402537239664 | `cwt:em:0008` / 6020.000000000059 | CWT / 630.5250595235257 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| [O III]a (`line:oiii-4960`) | 6140.2188918645825 | `cwt:em:0009` / 6140.800000000087 | CWT / 510.89405269143833 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| [O III]b (`line:oiii-5008`) | 6199.512983939721 | `cwt:em:0010` / 6200.0000000001 | CWT / 818.4446238526186 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| Na D1_abs (`line:nad1-5891-abs`) | 7293.049537993544 | `fit:H1:0002` / 7298.536 | fit_doublet / 422.6 | MARGINAL | signal_present (3/3 yes) | not_evaluated | — |
| Hα (`line:half-6564`) | 8126.137721011681 | `cwt:em:0012` / 8127.200000000138 | CWT / 755.4106187417149 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| [S II]a (`line:sii-6718`) | 8316.398722096208 | `cwt:em:0013` / 8318.400000000182 | CWT / 667.9518065731661 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| [S II]b (`line:sii-6732`) | 8334.224085893327 | `cwt:em:0014` / 8336.000000000186 | CWT / 284.08683750191113 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |

**rejected_measurement**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| Ca K_abs (`line:cak-3934-abs`) | 4870.7806575628 | `cwt:abs:0006` / 4868.000000000288 | CWT / 4331.473480019335 | MARGINAL | signal_absent (1/3 yes) | not_evaluated | — |
| Hδ_abs (`line:hdel-4102-abs`) | 5078.867022444447 | `cwt:abs:0007` / 5075.200000000335 | CWT / 318.76422245673183 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| G-band_abs (`line:gband-4305-abs`) | 5329.783775338618 | `cwt:abs:0008` / 5333.600000000394 | CWT / 3267.5537798036685 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Hγ (`line:hgam-4341`) | 5374.4709720800065 | `cwt:em:0006` / 5387.200000000406 | CWT / 4735.5036222788995 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Hβ_abs (`line:hbet-4862-abs`) | 6019.402537239664 | `cwt:abs:0010` / 6010.400000000057 | CWT / 631.5321539883578 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Na D2_abs (`line:nad2-5897-abs`) | 7300.47677290901 | `fit:H1:0003` / 7306.344 | fit_doublet / 96.6 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Hα_abs (`line:half-6564-abs`) | 8126.137721011681 | `cwt:abs:0021` / 8120.000000000136 | CWT / 319.34250523490385 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |

**no_pairing**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| Ca H_abs (`line:cah-3969-abs`) | 4913.858620072505 | — | — | NOT_FOUND | — | not_evaluated | — |
| Hε_abs (`line:heps-3970-abs`) | 4914.47755631546 | — | — | NOT_FOUND | — | not_evaluated | — |
| Hγ_abs (`line:hgam-4341-abs`) | 5374.4709720800065 | — | — | NOT_FOUND | — | not_evaluated | — |
| Mg I_abs (`line:mgi-5176-abs`) | 6408.094497815733 | — | — | NOT_FOUND | — | not_evaluated | — |
| Na D_abs (`line:nad-5895-abs`) | 7298.001027937187 | — | — | NOT_FOUND | — | not_evaluated | — |
| [N II]a (`line:nii-6549`) | 8107.817208220196 | — | — | NOT_FOUND | — | not_evaluated | — |
| [N II]b (`line:nii-6585`) | 8151.761681470039 | — | — | NOT_FOUND | — | not_evaluated | — |

### 3d. Key Findings and Graph Actions

- **Q2 gate input (executed):** `line:nev-3426` ([Ne V], predicted 4240.951136731258 Å) has measurement `cwt:em:0001` (CWT, center 4242.400000000146 Å, FWHM 1917.164597169737 km/s), SH `LIKELY`, FA `signal_present`, vote 3 yes / 0 no (`assured`), cleaned pairing `adopted`, gate state `q2_type2_support`. This single gate drove the terminal `survive` / `Type 2 QSO` outcome.
- **Other adopted emission pairings (not evaluated by the type graph):** `[O II]` (`cwt:em:0002`), Hε (`cwt:em:0004`), Hδ (`cwt:em:0005`), Hβ (`cwt:em:0008`), `[O III]a` (`cwt:em:0009`), `[O III]b` (`cwt:em:0010`), Hα (`cwt:em:0012`), `[S II]a` (`cwt:em:0013`), `[S II]b` (`cwt:em:0014`) are all SH `LIKELY` with FA `signal_present` and 3/0 assured votes. Their `graph_gate_state` is `not_evaluated` — they were not checked by the type graph on this path.
- **Rejected measurements (FA signal_absent, cleaned pairing rejected):** Ca K_abs (`cwt:abs:0006`, contested 1/2), Hδ_abs (`cwt:abs:0007`, 0/3), G-band_abs (`cwt:abs:0008`, 0/3), Hγ (`cwt:em:0006`, 0/3), Hβ_abs (`cwt:abs:0010`, 0/3), Na D2_abs (`fit:H1:0003`, 0/3), Hα_abs (`cwt:abs:0021`, 0/3). A rejected measurement does not establish line absence.
- **Adopted absorption:** Na D1_abs (`fit:H1:0002`, fit_doublet, center 7298.536 Å, FWHM 422.6 km/s) is SH `MARGINAL`, FA `signal_present`, 3/0 assured, pairing `adopted`; gate state `not_evaluated`.
- **SH `NOT_FOUND` lines (no measurement):** Ca H_abs, Hε_abs, Hγ_abs, Mg I_abs, Na D_abs, `[N II]a`, `[N II]b` — all `no_pairing`, `not_evaluated`.
- **Line alignment** (`alignment/aae7ecfdafcc422aa438c9cec62207d4/node`): no collisions recorded; all adopted emission/absorption claims retain `original_claim` status; rejected and unmeasured lines are `unassigned`. No shared-feature conflict votes were raised.
- **Skipped nodes:** `qso.broad_line_inventory`, `qso.missing_broad_line_queue`, `qso.coverage`, `qso.inspect_line`, `qso.proposed_observation`, `qso.relative_strength`, `qso.type1_formal_gate`, `qso.route_result` — all bypassed by the Q2 exit. No Q5–Q8 local reads, targeted candidate observations, or Q9/Q10 gate states were executed (`targeted_measurements` empty).

### 3e. Recorded Classification

Preliminary classification: Type 2 QSO
Recorded classification: Type 2 QSO

The preliminary classification `Type 2 QSO` was carried through unchanged. The Q2 `qso.nev_pairing_gate` node (`sh2/f38acbe4c26a4b3d874cddbd392aaded/node`) recorded an adopted, FA-confirmed [Ne V] signal and routed directly to `qso.analysis_report` under rule `project:qso-nev-type2-exit` (v `forma-qso-entry-v1`), producing terminal `survive` / `Type 2 QSO`. The final type is the graph rule's result, not an independent classification; this is one-hypothesis analysis, not the final choice among Redrock hypotheses.

### 3f. Caveats and Open Items

- **Bypassed checks:** Q3–Q10 (broad-line inventory, missing-broad-line queue, coverage, inspect-line, proposed observation, relative strength, Type 1 formal gate, route result) were skipped by the Q2 exit; no broad-line, coverage, or relative-strength properties were evaluated on this path. Skipped nodes supply no negative evidence.
- **No targeted measurements:** `targeted_measurements` is empty; no Q8 envelope proxies or candidate observations exist for this run.
- **Contested/rejected absorption:** Ca K_abs is contested (1 yes / 2 no, `contested`); several absorption and Hγ measurements are FA `signal_absent` and rejected — these do not prove absence.
- **SH `NOT_FOUND` labels** apply only where SH actually supplied them (Ca H_abs, Hε_abs, Hγ_abs, Mg I_abs, Na D_abs, `[N II]a`, `[N II]b`); these were not checked by the type graph.
- **No recorded conflicts or unresolved items** in the canonical context (`conflicts` and `unresolved_items` empty); no classification conflict between preliminary type and terminal type was recorded.
