# Spectral Line Reference

## Related Knowledge

- Classification diagnostics (ELG, LRG, QSO, Star rules, fatal problems): see `kb/classification.md`
- Ionization physics (redshift anchoring priorities, consistency rules, outflow): see `kb/ionization.md`
- Emission-absorption composite profiles (Mg II, Hα, Hβ): see `kb/composite_profile.md`

## Rest-Frame Line Table

The versioned table of line IDs, rest wavelengths, types, and width classes is
generated from the ontology registry in `kb/ontology_lines.generated.md`.
Use `ontology_lookup` for exact values. Wavelengths mentioned in the diagnostic
prose below are approximate labels or rule parameters, not a second line catalog.

## Doublet Rules

**Owned rule parameters**: executable doublet spacing/ratio checks live in the
registry — `rule:formal-oiii-doublet`, `rule:formal-cahk-doublet` (see
`kb/ontology_rules.generated.md` via `grep_kb`). The prose below explains how
to apply them; it is not a second numeric table.

**General principle — spacing alone does NOT confirm a doublet.** The targeted search harness pre-selects features whose observed wavelengths are near the predicted line positions. Matching spacing is therefore *expected* for any candidate hypothesis — it is not an independent verification. The real diagnostic question is whether **both components are physically real features**. Specifically:
- Is the weaker component a genuine peak/trough, or just noise at roughly the right position?
- In the OH airglow scrutiny zone (boundary supplied in the run message), if the weaker line is unusually bright, suspect OH skyline contamination masquerading as the doublet partner. Flag explicitly.

### [O III] (4960.3 / 5008.2 Å)
- Rest separation: 47.9 Å. Observed separation: 47.9 × (1+z) Å.
- Spacing check: compare |λ_obs(b) − λ_obs(a) − 47.9×(1+z)| with the configured [O III] tolerance. Wrong spacing weakens the identification.
- Amplitude ratio: b : a ≈ 3:1. Reversed ratio (a > b) disqualifies.

### [S II] (6718.3 / 6732.7 Å)
- Rest separation: 14.4 Å. Observed: 14.4 × (1+z) Å.
- Amplitude ratio: a ≈ b (both similar strength).

### [N II] (6549.8 / 6585.3 Å)
- Rest separation: 35.5 Å. Observed: 35.5 × (1+z) Å.
- Amplitude ratio: a : b ≈ 1:3 (b brighter).

### Ca K/H absorption (3934.8 / 3969.6 Å)
- Rest separation: 34.8 Å. Observed: 34.8 × (1+z) Å.
- Ca K MUST be deeper than Ca H. A single absorption without its partner is likely a misidentification.

### [O II] Unresolved Doublet (3726.0 / 3729.0 Å)

The [O II] 3727 line is a close doublet (rest separation 2.8–3.0 Å). At DESI resolution, the doublet is **unresolved** — it appears as a single blended emission peak. The key diagnostic is a **rising-edge slope-change** signature that a true single line ([O III]b, Hβ) cannot produce.

**Primary diagnostic — rising-edge derivative dip**: On the rising edge of the blended profile, [O II]a contributes flux before [O II]b takes over. The discrete derivative (flux[i] − flux[i−1]) shows a characteristic pattern: large positive → small positive → large positive. This "derivative valley" is the imprint of two unresolved components. A single line shows a smoothly decreasing derivative with no dip. Use the `detect_oii_slope_change` tool for an automated check.

**Corroborating**: A blended profile is broader than a single narrow line. FWHM > 500 km/s supports the [O II] identification, but is not required — a slope-change without broadened FWHM still warrants a FLAG.

**Discriminating from [O III]b**: When the same observed emission feature is claimed as [O II] by one hypothesis and [O III]b by another, the slope-change test is decisive. Rely on the morphological test and your visual assessment of the feature's prominence, width, and overall context within the spectrum. Use your perceptual judgment as an astronomer — there is no rigid amplitude-based rule.

**False negatives**: In a noisy spectrum or at very low redshift (z < 0.15, where observed separation is < 4 pixels), the morphological signatures may be undetectable. Report "morphology inconclusive at this SNR" rather than claiming [O II] is absent. The execution-mode routing threshold is not a line-detectability threshold.

### Lyα Forest and DLA

Lyα at z ≳ 1.5 is accompanied by the **Lyα forest** — a dense series of narrow H I absorption lines blueward of the Lyα emission peak. A **DLA** (Damped Lyman-α Absorber) produces a broad, saturated absorption trough immediately blueward of Lyα.

**Asymmetric rule — confirmatory only** (executable form owned by
`rule:formal-lya-forest-visibility`):
- **Forest visible**: A series of narrow absorption lines blueward of Lyα, with flux systematically depressed blueward compared to redward. This is **strong positive confirmation** of the Lyα identification and redshift.
- **Forest NOT visible but observable** (the probe lies above the configured blue-edge boundary): Flag as "Lyα identification uncertain." Downgrade confidence but do NOT exclude the hypothesis.
- **Forest beyond blue edge** (the probe lies below the configured blue-edge boundary): **Zero information.** Do NOT use as evidence against the hypothesis.
- **DLA check**: If Lyα appears narrower/weaker than expected, a DLA trough may be absorbing the blue wing — this explains the width anomaly and should NOT be held against the hypothesis.

## Line Blend Disentanglement

### Hβ + [O III] complex (rest 4820–5050 Å)
Hβ 4862.7, [O III]a 4960.3, [O III]b 5008.2.
```
wavelength_1 → Hβ        (shortest)
wavelength_2 → [O III]a  (middle)
wavelength_3 → [O III]b  (longest)
```
If only 2 peaks detected: Hβ+[O III]b (a too weak), or [O III]a+[O III]b (Hβ blended).

### Hα + [N II] complex (rest 6520–6620 Å)
[N II]a 6549.8, Hα 6564.6, [N II]b 6585.3. Separated ~15–20 Å each.
May blend into single asymmetric profile. Always check [N II]a/b presence alongside Hα.

### Ca K/H + Hε absorption (rest 3930–3975 Å)
Ca K_abs 3934.8, Ca H_abs 3969.6, Hε_abs 3970.1. Ca H+Hε separated by 0.5 Å → always blended.
```
wavelength_1 → Ca K_abs  (shortest, ~3935 Å)
wavelength_2 → Ca H_abs  (middle, ~3970 Å)
wavelength_3 → Hε_abs    (longest, ~3970 Å — blended with Ca H)
```

### Mg II Emission vs Absorption Coexistence (2800 Å rest)

Mg II 2800 Å can appear as both broad emission (QSO BLR; strict width boundary supplied in the run message) and narrow absorption (ISM). When both are claimed near the same observed wavelength, they may form a single emission–absorption composite profile. **For the full diagnostic criteria (morphological "M" test, center consistency, wing broadness, symmetry, spike–valley–spike detection), see `kb/composite_profile.md`.** Key principle: a genuine composite profile (broad, symmetric, smooth "M" shape) supports both claims as a single physical system; spike–valley–spike patterns do not.

## Blue Edge Noise Zone (configured observed-wavelength boundary)

Executable threshold owned by `rule:formal-blue-edge-risk`.

The blue end of DESI coverage has reduced throughput and elevated noise. Spectral features there require additional scrutiny; the run message gives the operational boundary:

- **Throughput drop**: Sensitivity falls toward the blue edge. The noise can have outliers that CWT interprets as peaks.
- **Evaluation**: A line below the configured blue-edge boundary should be flagged for scrutiny. Features barely distinguishable from the elevated noise envelope should be capped at MARGINAL. Features invisible against that envelope should be assigned NOT_FOUND. Read the configured read window supplied in the run message before accepting a blue-zone line as evidence.
- Lines that naturally fall here at higher redshift: Lyα (1216), C IV (1549), He II (1640), C III] (1909). These are high-ionization AGN indicators routinely claimed in low-SNR blue data — treat them as **presumptively unreliable until visually confirmed**.

## OH Airglow Zone and Skyline Contamination

Executable thresholds owned by `rule:formal-oh-zone-risk` and
`rule:formal-skyline-contamination`; the fixed-wavelength skyline table lives
in the registry `skyline:*` records (see `kb/ontology_lines.generated.md` and
`kb/ontology_rules.generated.md` via `grep_kb`).

### OH Airglow (Red edge: > 7000 Å, strongest > 9000 Å)

Hydroxyl (OH) molecular bands produce dense, bright narrow emission lines. Even after sky subtraction, residual OH lines appear at fixed observed wavelengths.

- **Evaluation**: Beyond the configured OH scrutiny boundary, flag the candidate for closer inspection. This boundary is an analysis convention; the OH forest itself is a physical source of contamination. Features indistinguishable from OH residuals should be capped at MARGINAL. A visually dominant peak may be real but should carry a contamination caveat. Read the configured read window supplied in the run message before accepting an OH-zone line.
- Proximity to a registered discrete airglow emission line within the configured tolerance is evidence of possible contamination. Inspect its profile and local residuals before assigning the astrophysical line a status. Membership in a broad OH band alone is a separate risk warning, not a zero-distance match to a discrete line.

### OI Airglow (Visible: 5577, 6300, 6364 Å)

Atomic oxygen forbidden transitions at fixed observed wavelengths:

| λ_obs (Å) | Transition | Notes |
|-----------|-----------|-------|
| 5577.3 | [OI] green line | Strong, isolated. Often the brightest skyline in the visible band |
| 6300.3 | [OI] red line | Weaker, but narrow and persistent |
| 6363.8 | [OI] red line | Companion to 6300.3, ratio 6300/6364 ≈ 3:1 |

Unlike OH which is a red-edge problem, OI lines can contaminate features ANYWHERE in the visible spectrum (4000–7000 Å). Any narrow emission feature near these wavelengths should be checked against OI contamination regardless of the claimed redshift.

### Comprehensive Skyline / Atmospheric Feature Table

| Type | Name | Wavelength (Å) | Notes |
|------|------|----------------|-------|
| Airglow Emission | [O I] | 5577.3 | Most famous skyline; easily produces spurious narrow emission peaks |
| Airglow Emission | Na D | 5890, 5896 | Upper-atmosphere sodium layer emission doublet |
| Airglow Emission | [O I] | 6300.3 | Often confused with astrophysical [O I] 6300 in AGN |
| Airglow Emission | [O I] | 6363.8 | 3:1 doublet companion to 6300.3 |
| Atmospheric Absorption | O₂ B-band | 6867 | Strong absorption band; affects continuum and weak-line identification |
| OH Airglow Forest | OH Meinel Bands | 7000–7400 | Dense OH emission lines begin |
| Atmospheric Absorption | O₂ A-band | 7605 | One of the strongest atmospheric absorption bands |
| OH Airglow Forest | OH Meinel Bands | 7800–9800 | Extremely dense OH forest |

When evaluating a narrow emission feature, cross-reference λ_obs against the discrete airglow emission entries. Apply the run-message proximity tolerance to those entries only; treat OH bands as risk regions and atmospheric absorption separately.

Lines that may fall in the OH zone at higher redshift include: [O II] (3727), Ca K/H (3935/3970), Hδ (4103) — rest-frame optical features that are key diagnostics for galaxy classification. When these fall beyond the configured scrutiny boundary, their reliability should be examined and noted in the synthesis verdict.
