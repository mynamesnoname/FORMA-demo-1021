### 3a. Spectrum Summary

Hypothesis redshift: 0.23805248503053472

Hypothesis reference: H3 (branch `main`, run `graph-853b617a68f04c36bd82f06bdb770ac4`). Reported wavelength coverage is 3600.0–9824.0 Å (approximately), with no masked regions supplied in the spectrum summary. The measurement catalog provenance is `sh/H3/catalog`; SH judgments are registered under `sh/H3/judgments` and `sh/H3/node`.

### 3b. Recorded Graph Outcome

Graph path status: survive
Candidate type: Type 2 QSO

The terminal code node is `sh2/4093cb4c9c084e019e4bc47e17713d92/node`, applying rule `project:qso-nev-type2-exit` (version `forma-qso-entry-v1`). No reason codes were recorded. The recorded graph action at this node is the Q2 `qso.nev_pairing_gate` output for `line:nev-3426` / `cwt:em:0001`: SH status `LIKELY`, FA state `signal_present`, pairing state `adopted`, candidate type `Type 2 QSO`, path status `survive`, next node `qso.analysis_report`. The path therefore survives directly through the Q2 [Ne V] gate; Q3–Q10 were not executed on this path.

### 3c. Per-Line Results

**adopted**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| [Ne V] (`line:nev-3426`) | 4241.567813714612 | `cwt:em:0001` / 4242.400000000146 | CWT / 1917.164597169737 | LIKELY | signal_present (3/3 yes) | q2_type2_support | — |
| [O II] (`line:oii-3727`) | 4614.221611708803 | `cwt:em:0002` / 4616.800000000231 | CWT / 1099.106885263833 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| Hε (`line:heps-3970`) | 4915.192170819726 | `cwt:em:0004` / 4912.8000000002985 | CWT / 1249.668861064443 | MARGINAL | signal_present (3/3 yes) | not_evaluated | — |
| Hδ (`line:hdel-4102`) | 5079.605540831781 | `cwt:em:0005` / 5079.200000000336 | CWT / 999.0464379992876 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| Hβ (`line:hbet-4862`) | 6020.277818957981 | `cwt:em:0008` / 6020.000000000059 | CWT / 630.5250595235257 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| [O III]a (`line:oiii-4960`) | 6141.111741496962 | `cwt:em:0009` / 6140.800000000087 | CWT / 510.89405269143833 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| [O III]b (`line:oiii-5008`) | 6200.414455529924 | `cwt:em:0010` / 6200.0000000001 | CWT / 818.4446238526186 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| Na D2_abs (`line:nad2-5897-abs`) | 7301.538335716083 | `fit:H3:0003` / 7299.47 | fit_doublet / 512.7 | MARGINAL | signal_present (3/3 yes) | not_evaluated | — |
| [N II]a (`line:nii-6549`) | 8108.9961664529965 | `cwt:em:0012` / 8127.200000000138 | CWT / 755.4106187417149 | MARGINAL | signal_present (3/3 yes) | not_evaluated | alignment:TBD |
| Hα (`line:half-6564`) | 8127.319343231449 | `cwt:em:0012` / 8127.200000000138 | CWT / 755.4106187417149 | LIKELY | signal_present (3/3 yes) | not_evaluated | alignment:TBD |
| [N II]b (`line:nii-6585`) | 8152.947029671581 | `cwt:em:0012` / 8127.200000000138 | CWT / 755.4106187417149 | MARGINAL | signal_present (3/3 yes) | not_evaluated | alignment:TBD |
| [S II]a (`line:sii-6718`) | 8317.608010180642 | `cwt:em:0013` / 8318.400000000182 | CWT / 667.9518065731661 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |
| [S II]b (`line:sii-6732`) | 8335.435965965082 | `cwt:em:0014` / 8336.000000000186 | CWT / 284.08683750191113 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |

**rejected_measurement**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| Ca K_abs (`line:cak-3934-abs`) | 4871.488918098148 | `cwt:abs:0006` / 4868.000000000288 | CWT / 4331.473480019335 | MARGINAL | signal_absent (1/3 yes) | not_evaluated | — |
| Hδ_abs (`line:hdel-4102-abs`) | 5079.605540831781 | `cwt:abs:0007` / 5075.200000000335 | CWT / 318.76422245673183 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| G-band_abs (`line:gband-4305-abs`) | 5330.558779547471 | `cwt:abs:0008` / 5333.600000000394 | CWT / 3267.5537798036685 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Hγ (`line:hgam-4341`) | 5375.252474257072 | `cwt:em:0006` / 5387.200000000406 | CWT / 4735.5036222788995 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Hβ_abs (`line:hbet-4862-abs`) | 6020.277818957981 | `cwt:abs:0010` / 6010.400000000057 | CWT / 631.5321539883578 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Na D1_abs (`line:nad1-5891-abs`) | 7294.110020805899 | `fit:H3:0002` / 7326.206 | fit_doublet / 464.3 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| Hα_abs (`line:half-6564-abs`) | 8127.319343231449 | `cwt:abs:0021` / 8120.000000000136 | CWT / 319.34250523490385 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |

**no_pairing**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| Ca H_abs (`line:cah-3969-abs`) | 4914.573144577211 | — | — | NOT_FOUND | — | not_evaluated | — |
| Hε_abs (`line:heps-3970-abs`) | 4915.192170819726 | — | — | NOT_FOUND | — | not_evaluated | — |
| Hγ_abs (`line:hgam-4341-abs`) | 5375.252474257072 | — | — | NOT_FOUND | — | not_evaluated | — |
| Mg I_abs (`line:mgi-5176-abs`) | 6409.026299257569 | — | — | NOT_FOUND | — | not_evaluated | — |
| Na D_abs (`line:nad-5895-abs`) | 7299.062230746022 | — | — | NOT_FOUND | — | not_evaluated | — |

**Hypothesis-local shared-feature alignment (original SH/FA rows retained)**

Source: `alignment/e758789f9f3647478b5ef41bab680576/node`

| Shared measurement | Line ID | Status | Vote | Candidate ID | Representative centre (Å) | Amplitude proxy | FWHM proxy (Å) |
|---|---|---|---|---|---:|---:|---:|
| cwt:em:0012 | line:half-6564 | TBD | — | — | — | — | — |
| cwt:em:0012 | line:nii-6549 | TBD | — | — | — | — | — |
| cwt:em:0012 | line:nii-6585 | TBD | — | — | — | — | — |

### 3d. Key Findings and Graph Actions

The only executed graph gate is the Q2 [Ne V] pairing gate (`sh2/4093cb4c9c084e019e4bc47e17713d92/node`). Its input was the [Ne V] record `line:nev-3426` with measurement `cwt:em:0001` (CWT, measured center 4242.4 Å against predicted 4241.567813714612 Å, FWHM 1917.164597169737 km/s). That record carries SH status `LIKELY`, FA state `signal_present`, a 3-yes/0-no assured vote summary, and cleaned pairing `adopted`; the gate recorded `q2_type2_support` and routed to `survive` with candidate type `Type 2 QSO`.

All other line records carry `graph_gate_state: not_evaluated`; they were not checked by the type graph on this path. Several emission lines have SH `LIKELY` and FA `signal_present` with adopted pairings (e.g., [O II] `cwt:em:0002`, Hε `cwt:em:0004`, Hδ `cwt:em:0005`, Hβ `cwt:em:0008`, [O III]a `cwt:em:0009`, [O III]b `cwt:em:0010`, [S II]a `cwt:em:0013`, [S II]b `cwt:em:0014`), but these are recorded SH/FA layers only and were not used as graph gate inputs. Hγ (`cwt:em:0006`) is SH `MARGINAL` with FA `signal_absent` and a rejected measurement.

Absorption-line records are mixed: Ca K_abs (`cwt:abs:0006`) is SH `MARGINAL`, FA `signal_absent`, contested (1 yes/2 no), rejected; Hδ_abs (`cwt:abs:0007`), G-band_abs (`cwt:abs:0008`), Hβ_abs (`cwt:abs:0010`), and Hα_abs (`cwt:abs:0021`) are SH `MARGINAL`, FA `signal_absent`, assured 0-yes/3-no, rejected. Na D1_abs (`fit:H3:0002`) is SH `MARGINAL`, FA `signal_absent`, rejected, while Na D2_abs (`fit:H3:0003`) is SH `MARGINAL`, FA `signal_present`, adopted. Ca H_abs, Hε_abs, Hγ_abs, Mg I_abs, and Na D_abs have no measurement and SH `NOT_FOUND` with `no_pairing`; these are SH labels only and were not graph-checked.

Line alignment (`alignment/e758789f9f3647478b5ef41bab680576/node`) records one shared-feature collision on `cwt:em:0012`, claimed by `line:half-6564`, `line:nii-6549`, and `line:nii-6585`. It is grouped `unresolved_non_diagnostic`, status `tbd`, eligible `false`, with no slots or ballots and reason `no_diagnostic_vote`. This does not alter the terminal route. No targeted Q8 measurements were supplied (`targeted_measurements` empty).

Skipped nodes on this path: `qso.broad_line_inventory`, `qso.missing_broad_line_queue`, `qso.coverage`, `qso.inspect_line`, `qso.proposed_observation`, `qso.relative_strength`, `qso.type1_formal_gate`, and `qso.route_result`. These were bypassed by the Q2 exit and supply no negative evidence.

### 3e. Recorded Classification

Preliminary classification: Type 2 QSO
Recorded classification: Type 2 QSO

The preliminary classification `Type 2 QSO` was carried through the Q2 [Ne V] gate at `sh2/4093cb4c9c084e019e4bc47e17713d92/node`, which recorded `q2_type2_support` for the adopted [Ne V] measurement `cwt:em:0001` and returned candidate type `Type 2 QSO` with path status `survive` under rule `project:qso-nev-type2-exit` (version `forma-qso-entry-v1`). The final type is the result of this graph rule, not an independent classification. This is one-hypothesis analysis and not the final choice among Redrock hypotheses.

### 3f. Caveats and Open Items

- The path survives solely via the Q2 [Ne V] gate; Q3–Q10 were skipped (`qso.broad_line_inventory`, `qso.missing_broad_line_queue`, `qso.coverage`, `qso.inspect_line`, `qso.proposed_observation`, `qso.relative_strength`, `qso.type1_formal_gate`, `qso.route_result`). Broad-line inventory, coverage, relative-strength, and Type 1 formal checks were therefore not evaluated on this path and provide no negative evidence.
- The shared-feature collision on `cwt:em:0012` (Hα / [N II]a / [N II]b) remains `tbd` and unresolved (`alignment/e758789f9f3647478b5ef41bab680576/node`); no diagnostic vote was recorded, and this does not prove line absence.
- Absorption-line SH `MARGINAL`/`NOT_FOUND` labels and rejected measurements reflect SH/FA layers only; a rejected measurement does not establish that a line is absent, and `NOT_FOUND` is retained strictly as an SH label.
- No masked regions were supplied, and no Q5 full-mask determination is recorded; no Q8 targeted envelope proxies were supplied.
- No conflicts or unresolved items were recorded in the canonical `conflicts` and `unresolved_items` fields.
