### 3a. Spectrum Summary

Hypothesis redshift: 1.6610183943523609

Hypothesis reference: H5 (branch `main`, run `graph-fe0d30030bcc4939b88103e27753b2c1`). Reported wavelength coverage is 3600.0–9824.0 Å, with no masked regions supplied in the spectrum summary. The measurement catalog provenance is `sh/H5/catalog`.

### 3b. Recorded Graph Outcome

Graph path status: dead
Candidate type: null

The terminal code node is `qso.route_result` (`sh2/8ef3704c2bb2494097189ad9f50dcd84/node`), applying rule `project:qso-type1-formal-gate` version `forma-qso-entry-v1`. Its recorded reason codes are `line:civ-1549:unresolved` and `line:ciii-1909:failed`. These states were produced upstream by the `qso.type1_formal_gate` node (`sh2/dca6088b1b3648059818af6d6365f127/node`), which recorded `gate_status: type1_failed` with effective line states C IV = `unresolved` and C III] = `failed`. The path is recorded as dead with no candidate type; no fallback hypothesis is selected here.

### 3c. Per-Line Results

**adopted**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| C IV (`line:civ-1549`) | 4121.917492851807 | `cwt:em:0000` / 4127.20000000012 | CWT / 1229.4913422868215 | MARGINAL | signal_present (3/3 yes) | unresolved | — |
| Mg II (`line:mgii-2800`) | 7450.85150418661 | `cwt:em:0015` / 7452.000000000385 | CWT / 237.71348835277018 | LIKELY | signal_present (3/3 yes) | not_evaluated | — |

**rejected_measurement**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| Mg II_abs (`line:mgii-2800-abs`) | 7450.85150418661 | `cwt:abs:0019` / 7447.200000000384 | CWT / 237.86670362080292 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |
| [Ne V] (`line:nev-3426`) | 9116.649019051189 | `fit:H5:0002` / 9132.526 | fit_peak / 188.2 | MARGINAL | signal_absent (0/3 yes) | not_evaluated | — |

**no_pairing**

| Line / ID | λ_pred (Å) | Measurement / λ (Å) | Source / FWHM (km/s) | SH | FA | Graph gate | Flags |
|---|---:|---|---|---|---|---|---|
| He II (`line:heii-1640`) | 4365.134574095613 | — | — | NOT_FOUND | — | not_evaluated | — |
| C III] (`line:ciii-1909`) | 5079.884114818657 | — | — | NOT_FOUND | — | failed | — |

### 3d. Key Findings and Graph Actions

- **Q2 [Ne V] pairing gate** (`sh2/2ef3c92dd875484ca52ceedff6f09563/node`): the [Ne V] measurement `fit:H5:0002` was recorded with SH `MARGINAL`, FA `signal_absent`, and pairing `rejected_measurement`; the gate returned `path_status: continue` with no candidate type, routing to the broad-line inventory.
- **Broad-line inventory** (`sh2/69423c8dc1784e59bb896eb1908ae234/node`): Lyα is outside range; C IV (`cwt:em:0000`, FWHM 1229.49 km/s) and Mg II (`cwt:em:0015`, FWHM 237.71 km/s) were both recorded as `not_supported` for broadness against the strict 2000 km/s threshold; C III] had `no_pairing` and `unresolved` broadness. `any_supported_broad_line` is null.
- **Missing broad-line queue** (`sh2/7968105a80124eb3a3e23f3e0fdc59b5/node`): selected C IV (reason `width_not_supported`) and C III] (reason `no_pairing`) for local reads, both with `usable` coverage preview.
- **C IV local read** (`sh2/380964c8d02f4f599dab8e585a84f9ef/node`, `sh2/7a423a8ec7b0428cbbeee232a33b1097/node`): coverage usable (375/375 samples, 0 explicit masked, no full-window mask proof). The inspection recorded `plausible_uncatalogued_signal` with a broad envelope and no absorption fragmentation. A proposed observation (`sh2/b5ae624048c34a8e98729e8b910d32a7/node`) was recorded with `measurement_status: awaiting_q8_point_selection` and `fa_status: not_re_reviewed`; original SH/FA pairing unchanged. This is a proposed observation, not a confirmed line.
- **C IV relative strength** (`sh2/0bca4b6d2d634ff48f8bafd117be3bf2/node`): `reference_unavailable`, no reference line, no votes.
- **C III] local read** (`sh2/5ca1798fdd78492f8847b6879342a135/node`, `sh2/43289539092f4924a71d5441b65e0755/node`): coverage usable (375/375 samples, 0 explicit masked, no full-window mask proof). The inspection recorded `no_coherent_signal_seen`, no broad envelope, no absorption fragmentation.
- **Type 1 formal gate** (`sh2/dca6088b1b3648059818af6d6365f127/node`): recorded `type1_failed` with C IV `unresolved` and C III] `failed`, yielding the terminal dead path.

No Q8 targeted measurements were supplied (`targeted_measurements` empty). No line-alignment collisions were recorded; the alignment node (`alignment/5b8edf0f01b6403691289f16f7df3d01/node`) lists C IV and Mg II as `original_claim`, and C III], He II, Mg II_abs, and [Ne V] as `unassigned`. No skipped nodes were supplied.

### 3e. Recorded Classification

Preliminary classification: Type 1 QSO
Recorded classification: null

The preliminary classification was Type 1 QSO. The `qso.type1_formal_gate` node (`sh2/dca6088b1b3648059818af6d6365f127/node`) evaluated the selected lines C IV and C III] and recorded `type1_failed` (C IV `unresolved`, C III] `failed`), so the `qso.route_result` node (`sh2/8ef3704c2bb2494097189ad9f50dcd84/node`) recorded a dead path with `candidate_type: null` under rule `project:qso-type1-formal-gate` v`forma-qso-entry-v1`. The null type is the result of the graph's rule, not an independent classification. This is one-hypothesis analysis, not the final choice among Redrock hypotheses.

### 3f. Caveats and Open Items

- C IV remains `unresolved`: the local read found a plausible broad uncatalogued signal, but the proposed observation is still `awaiting_q8_point_selection` and `not_re_reviewed` by FA (`sh2/b5ae624048c34a8e98729e8b910d32a7/node`); no Q8 envelope proxy was supplied. The original CWT FWHM (1229.49 km/s) was recorded as `not_supported` for broadness.
- C III] is recorded `failed` from a local read of `no_coherent_signal_seen` (`sh2/43289539092f4924a71d5441b65e0755/node`); this is a checked negative result, distinct from the SH `NOT_FOUND` label on He II and C III] in the line records.
- C IV relative-strength check was not completed (`reference_unavailable`, no votes) (`sh2/0bca4b6d2d634ff48f8bafd117be3bf2/node`).
- Mg II (`cwt:em:0015`) was recorded `not_supported` for broadness and its gate state is `not_evaluated`; Mg II_abs and [Ne V] measurements were `rejected_measurement` with FA `signal_absent`, and their gate states are `not_evaluated`. A rejected measurement does not prove the line is absent.
- Coverage windows for C IV and C III] are usable with no explicit masked samples, but no full-window explicit-mask proof was recorded; `fully_masked` does not apply.
- No line-alignment collisions were recorded; unassigned alignment entries (C III], He II, Mg II_abs, [Ne V]) do not by themselves establish line absence.
