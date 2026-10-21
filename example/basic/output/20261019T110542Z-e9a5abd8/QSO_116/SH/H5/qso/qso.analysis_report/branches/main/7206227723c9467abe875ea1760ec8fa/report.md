### 3a. Spectrum Summary

Hypothesis redshift: 2.9196962422694117

- Hypothesis reference: H5
- Branch: main
- Reported wavelength coverage: 3600.0–9824.000000000524 Å
- Masked regions: none supplied
- Measurement catalog reference: sh/H5/catalog

### 3b. Recorded Graph Outcome

Graph path status: survive
Candidate type: Type 1 QSO

The terminal code node is `sh2/63a2e13eca9e41bb9a3008c6f87d114a/node` (qso.route_result), applying rule `project:qso-type1-formal-gate` version `forma-qso-entry-v1`. It recorded `path_status: survive` with `candidate_type: Type 1 QSO` and no reason codes. This outcome is supported upstream by the Q10 formal gate node `sh2/25ec1046a7694849b10165a3aec7aab1/node`, which recorded `gate_status: type1_supported` for the selected lines `line:lya-1216` and `line:civ-1549`, both in effective state `paired`, with usable coverage for both.

### 3c. Per-Line Results

**adopted**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| Lyα (`line:lya-1216`) | 4765.057130839656 | `cwt:em:0000` / 4768.000000000266 | CWT / 2497.013289890503 | LIKELY | signal_present (3/3 yes) | paired | — |
| C IV (`line:civ-1549`) | 6071.609479275318 | `cwt:em:0002` / 6072.000000000071 | CWT / 3472.5976450486037 | LIKELY | signal_present (2/3 yes) | paired | — |

**rejected_measurement**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| C III] (`line:ciii-1909`) | 7482.700126492307 | `cwt:em:0003` / 7474.40000000039 | CWT / 3413.130835109371 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |

**no_pairing**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| He II (`line:heii-1640`) | 6429.869715818743 | — | — | NOT_FOUND | — | not_evaluated | — |

### 3d. Key Findings and Graph Actions

- Broad-line inventory (`sh2/7c2f26573577439997525b4056d2b5ed/node`): Lyα (`line:lya-1216`, FWHM 2497.013289890503 km/s) and C IV (`line:civ-1549`, FWHM 3472.5976450486037 km/s) were recorded as broadness `supported` against the strict broad threshold of 2000.0 km/s (`config:rule:formal-width-class-match.width_consistency_score`). C III] (`line:ciii-1909`) was `unresolved` with a rejected measurement, and Mg II (`line:mgii-2800`) was `outside_range`. `any_supported_broad_line: true`.
- Missing broad-line queue (`sh2/4ae027ef899141a39d74ec4d1314c624/node`): selected `line:lya-1216` and `line:civ-1549` for local reads; queue empty; coverage preview usable for Lyα, C IV, and C III], outside range for Mg II.
- Coverage reads: Lyα (`sh2/35c41779be6743279bad3e2776467892/node`) and C IV (`sh2/8f5d69708c29420b809e8089f0bd2127/node`) each returned `usable` coverage with 375/375 usable samples, 0 explicit masked samples, and `full_window_explicit_mask_proof: false`.
- Q10 formal gate (`sh2/25ec1046a7694849b10165a3aec7aab1/node`): effective line states `paired` for both Lyα and C IV; `gate_status: type1_supported`; no reason codes.
- Line alignment (`alignment/819f69b6304740ccbeeb94b46b97eef1/node`): no collisions. Lyα and C IV retained as `original_claim`; C III] and He II recorded as `unassigned`. No model calls were made.
- SH/FA layers: Lyα SH `LIKELY`, FA `signal_present`, vote 3 yes / 0 no (assured). C IV SH `LIKELY`, FA `signal_present`, vote 2 yes / 1 no (contested). C III] SH `MARGINAL`, FA `signal_absent`, vote 0 yes / 3 no (assured), pairing `rejected_measurement`. He II SH `NOT_FOUND`, no FA state, `no_pairing`, gate `not_evaluated`.
- No targeted Q8 measurements were supplied (`targeted_measurements` empty). No skipped nodes were recorded.

### 3e. Recorded Classification

Preliminary classification: Type 1 QSO
Recorded classification: Type 1 QSO

The preliminary classification (Type 1 QSO) was carried through the Q10 formal gate node `sh2/25ec1046a7694849b10165a3aec7aab1/node`, which recorded `type1_supported` on the paired Lyα and C IV lines with usable coverage, and then to the terminal route node `sh2/63a2e13eca9e41bb9a3008c6f87d114a/node`, which recorded `survive` with `candidate_type: Type 1 QSO` under rule `project:qso-type1-formal-gate` (forma-qso-entry-v1). This is the graph's rule result for this single hypothesis, not an independent classification or a final choice among Redrock hypotheses.

### 3f. Caveats and Open Items

- C IV vote is `contested` (2 yes / 1 no); its FA `signal_present` confirms a signal at the measurement, not independently the line identity.
- C III] measurement was rejected (`rejected_measurement`, FA `signal_absent`, 0/3); a rejected measurement does not prove the line is absent, and its gate state is `not_evaluated`.
- He II is SH `NOT_FOUND` with `no_pairing` and gate `not_evaluated`; this is an SH label, not a type-graph negative result.
- Mg II (`line:mgii-2800`) is `outside_range` and was not evaluated on this path.
- Coverage reads show `full_window_explicit_mask_proof: false`; no window is described as fully masked.
- No Q8 targeted measurements were supplied, so no envelope proxies or strength votes are reported.
- No conflicts or unresolved items were recorded in the canonical context.
