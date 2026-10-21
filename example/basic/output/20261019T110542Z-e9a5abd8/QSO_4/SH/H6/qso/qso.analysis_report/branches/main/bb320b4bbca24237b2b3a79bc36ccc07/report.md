### 3a. Spectrum Summary

Hypothesis redshift: 1.902738756933621

Hypothesis reference: H6 (branch `main`, run `graph-853b617a68f04c36bd82f06bdb770ac4`). Reported wavelength coverage: 3600.0–9824.0 Å. No masked regions were supplied in the spectrum summary (`masked_regions: []`); the measurement catalog reference is `sh/H6/catalog`.

### 3b. Recorded Graph Outcome

Graph path status: dead
Candidate type: null

The terminal code node is `sh2/e7193dde266d451ca2e04dd1600cd39f/node` (`qso.route_result`), applying rule `project:qso-type1-formal-gate` version `forma-qso-entry-v1`. Its recorded reason codes are `line:civ-1549:failed` and `line:ciii-1909:failed`, carried from the Q10 formal gate node `sh2/f4b31cc7751f4e1aafade840e8eda228/node`, whose `gate_status` is `type1_failed` with both selected lines in effective state `failed`. The path is recorded as dead; no fallback hypothesis is selected here.

### 3c. Per-Line Results

**adopted**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| Mg II (`line:mgii-2800`) | 8127.668519414138 | `cwt:em:0012` / 8127.200000000138 | CWT / 755.4106187417149 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |

**rejected_measurement**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| Mg II_abs (`line:mgii-2800-abs`) | 8127.668519414138 | `cwt:abs:0021` / 8120.000000000136 | CWT / 319.34250523490385 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |

**no_pairing**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| C IV (`line:civ-1549`) | 4496.3423344901785 | — | — | NOT_FOUND | — | failed | — |
| He II (`line:heii-1640`) | 4761.652656873912 | — | — | NOT_FOUND | — | not_evaluated | — |
| C III] (`line:ciii-1909`) | 5541.328286986282 | — | — | NOT_FOUND | — | failed | — |

### 3d. Key Findings and Graph Actions

The broad-line inventory (`sh2/db8e127d68cb483fad7795c395220b0c/node`) found no line meeting the strict broad-width threshold (2000 km/s, `config:rule:formal-width-class-match.width_consistency_score`); Mg II (`line:mgii-2800`) was recorded as `not_supported` for broadness with FWHM 755.41 km/s, and `any_supported_broad_line` is null. Lyα (`line:lya-1216`) is `outside_range`; C IV and C III] were `needs_q5` with `no_pairing`.

The missing-broad-line queue (`sh2/e36be4f9d36d41d08dfef9a635e21964/node`) selected C IV (`line:civ-1549`) and C III] (`line:ciii-1909`) for local reads, both with `usable` coverage preview and a 150 Å half-width window.

Coverage checks confirmed usable windows for both selected lines: C IV (`sh2/57d5b79b10984fe6b0675d2b4d6eea29/node`) 375/375 usable samples, 0 explicitly masked, `full_window_explicit_mask_proof: false`; C III] (`sh2/0537e1c792f14ef8acb95e61d18dad67/node`) likewise 375/375 usable, 0 masked, no full-mask proof.

Local reads found no coherent signal: C IV (`sh2/552f2a1b0e8f460eb7566b866be8fe54/node`) reported `no_coherent_signal_seen`, no broad envelope, no absorption fragmentation, with only a narrow spike near 4613–4619 Å far redward of prediction; C III] (`sh2/b62b8c30d40642a88d9dbc0e1e16a6b3/node`) reported `no_coherent_signal_seen`, no broad envelope, no absorption fragmentation, flat noisy continuum.

Mg II (`line:mgii-2800`) carries a CWT measurement `cwt:em:0012` at 8127.2 Å, SH `LIKELY`, FA `signal_present`, vote summary yes 3 / no 0 (`assured`), cleaned pairing `adopted`; its graph gate state is `not_evaluated`. Mg II_abs (`line:mgii-2800-abs`, `cwt:abs:0021`) is SH `MARGINAL`, FA `signal_absent`, vote yes 0 / no 3 (`assured`), cleaned pairing `rejected_measurement`, gate `not_evaluated`. He II (`line:heii-1640`) is SH `NOT_FOUND`, `no_pairing`, gate `not_evaluated`.

Line alignment (`alignment/f42bee5178d645d58fb31dde5b1cf38b/node`) recorded no collisions; C IV, C III], and He II are `unassigned` with null effective features, Mg II is `original_claim` on `cwt:em:0012`, and Mg II_abs is `unassigned`. No targeted Q8 measurements were supplied (`targeted_measurements: []`). No skipped nodes were recorded (`skipped_nodes: []`).

### 3e. Recorded Classification

Preliminary classification: Type 1 QSO
Recorded classification: null

The preliminary classification was Type 1 QSO. The Q10 formal gate (`sh2/f4b31cc7751f4e1aafade840e8eda228/node`) evaluated the two selected lines C IV and C III] and recorded both as `failed`, yielding `gate_status: type1_failed`. The route result (`sh2/e7193dde266d451ca2e04dd1600cd39f/node`) therefore recorded `path_status: dead` with `candidate_type: null` under rule `project:qso-type1-formal-gate` (`forma-qso-entry-v1`). This is the graph's rule result for this single hypothesis, not an independent classification and not the final choice among Redrock hypotheses.

### 3f. Caveats and Open Items

- The path is dead, not unresolved or transferred; no fallback hypothesis is selected here.
- C IV and C III] local reads found no coherent signal, but coverage records show `full_window_explicit_mask_proof: false`; absence of a full-mask proof is not a `fully_masked` finding, and the reads are visual local assessments, not fitted measurements.
- Mg II is SH `LIKELY` with FA `signal_present` and an assured 3/0 vote, but its graph gate state is `not_evaluated` and its broadness is `not_supported` (FWHM 755.41 km/s below the 2000 km/s strict threshold). FA `signal_present` confirms a signal at the measurement, not independently the line identity.
- Mg II_abs is a rejected measurement (FA `signal_absent`, 0/3 vote); a rejected measurement does not prove the line is absent.
- He II was not evaluated by the type graph (`not_evaluated`); its SH `NOT_FOUND` label is an SH result only.
- Line alignment left C IV, C III], He II, and Mg II_abs `unassigned`; an unassigned or null slot does not prove line absence.
- No Q8 targeted measurements were supplied, so no envelope proxies or Q8 acceptance votes are reported.
- No conflicts or unresolved items were recorded in the canonical context (`conflicts: []`, `unresolved_items: []`).
