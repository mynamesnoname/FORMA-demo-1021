# SH pre-analysis session: line review

- Run ID: `graph-853b617a68f04c36bd82f06bdb770ac4`
- Hypothesis: `H3`
- Started (UTC): 2026-10-19T11:39:50.064846+00:00
- Available tools: `write_lines_csv`

The record contains model-facing input and returned messages. Provider reasoning appears only if the API returned it; hidden reasoning cannot be archived.

## Model-facing input

### System prompt

```markdown
# Redrock line review

Review one fixed-redshift hypothesis. The supplied line and measurement IDs, predicted positions, CWT features, targeted fits, masks and numeric parameters are the authority for this run. Treat every measured feature as a candidate, not proof of a line identity. Do not classify the object, judge the whole hypothesis, or write a report.

Evaluate every listed predicted line. Prefer a credible CWT measurement; inspect the already computed targeted fit where CWT missed a line. Check sign, redshift window, position, width, quality flags and possible blends. A fit that converged is not automatically a real signal. Failed or center-at-bound fits cannot be selected. A shared feature may be paired with multiple blended lines, but describe that ambiguity in each affected judgment.

Assign exactly one status per line: `LIKELY` or `MARGINAL` with an exact selectable measurement ID, `NOT_FOUND` for a checked position with no credible selected measurement, or `MASKED` only when missing data prevents a fair check. Partially missing windows need an explicit caveat, not an automatic `MASKED`. `NOT_FOUND` means no measurement was adopted in this review; it does not prove the physical line is absent. Preserve plausible weak Ca H/K components despite an uncertain fitted depth ordering. Treat doublet ratios and relative depths as advisory diagnostics, not automatic rejection of component reality. Record suspected blends, noise, edge effects and rejected fits in `reason_codes` and `comment`.

Your only tool is `write_lines_csv(file_path, lines)`. Submit every line in the authoritative ID table exactly once, in the shape `{"line_id":"line:...","measurement_id":"<listed ID>" or null,"status":"LIKELY|MARGINAL|NOT_FOUND|MASKED","reason_codes":["short_code"],"comment":"brief reason"}`. Copy IDs exactly; do not send numeric measurement fields. The tool resolves full precision values from the frozen catalog. If it reports rows to repair, resubmit the full corrected set. Stop after the tool confirms the CSV write. No Markdown report or preliminary classification is produced here.

```

### Input message 1: human

```markdown
Review every predicted line at the fixed Redrock redshift `0.23805248503053472`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H3/pre_analysis/branches/main/a17b8ffe679648b098725b050663ea61/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 46.6 |

Verify the redshift hypothesis z ≈ 0.23805248503053472.

Verification window: z ∈ [0.2281, 0.2481]
A CWT feature supports the hypothesis only if the implied redshift shown beside that predicted line falls within this window.
Lines marked [fully masked] have NO data in the entire z-window — assign status MASKED.
Lines with [λ_pred masked] or [window partially masked] can still be evaluated.

## Relevant ontology parameters (forma-spectral-ontology-v6)

- membership:offset-quality: strong |offset| < 20 Å; 20–80 Å is weaker; > 80 Å rejects the candidate.
- rule:formal-qso-broad-width: strict broad-line guide FWHM ≥ 2000 km/s; width mismatch is a caveat, not sole rejection.
- membership:detection-snr: SNR < 5 weak; ≥ 10 strong. Evaluate CWT ridge persistence as well.
- edge scrutiny: blue λ < 4000 Å; red λ > 7800 Å.
- high-ionization velocity offset reference: -1000 to 0 km/s; diagnostic only.
- Registry fit widths (width_3sigma Å): absorption=20, both=50, broad=90, narrow=25.
- Gaussian tool defaults: single window ±200 Å, doublet window ±300 Å, doublet separation tolerance 5 Å; these are fitting method settings, not line detection significance thresholds.
- Observable doublets:
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=59.3027, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=17.828, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=43.9509, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=43.0842, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=7.42831, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/QSO_4.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H3/pre_analysis/branches/main/a17b8ffe679648b098725b050663ea61/lines.csv

## CWT Detected Features

### Emission (peaks) — 22 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 4143.2 | 0.8 | 1.6 | 22.4 | 1623 | 7 | 8.9 |
| 4242.4 | 0.8 | 4.6 | 27.1 | 1917 | 19 | 21.3 |
| 4616.8 | 0.8 | 11.6 | 16.9 | 1099 | 24 | 76.2 |
| 4791.2 | 0.8 | 6.6 | 22.4 | 1403 | 21 | 17.1 |
| 4912.8 | 0.8 | 1.3 | 20.5 | 1250 | 14 | 10.7 |
| 5079.2 | 0.8 | 2.1 | 16.9 | 999 | 24 | 16.2 |
| 5387.2 | 0.8 | 0.7 | 85.1 | 4736 | 7 | 12.8 |
| 5802.4 | 0.8 | 1.3 | 11.6 | 597 | 8 | 8.6 |
| 6020.0 | 0.8 | 8.6 | 12.7 | 631 | 21 | 36.2 |
| 6140.8 | 0.8 | 20.8 | 10.5 | 511 | 19 | 66.3 |
| 6200.0 | 0.8 | 58.6 | 16.9 | 818 | 24 | 133.7 |
| 7802.4 | 0.8 | 1.9 | 20.5 | 787 | 22 | 25.5 |
| 8127.2 | 0.8 | 22.6 | 20.5 | 755 | 22 | 22.7 |
| 8318.4 | 0.8 | 3.9 | 18.5 | 668 | 23 | 31.8 |
| 8336.0 | 0.8 | 3.4 | 7.9 | 284 | 12 | 27.2 |
| 8837.6 | 0.8 | 0.9 | 12.7 | 430 | 13 | 13.0 |
| 9004.8 | 0.8 | 1.6 | 5.9 | 197 | 13 | 19.1 |
| 9068.8 | 0.8 | 0.1 | 53.1 | 1755 | 4 | 9.6 |
| 9316.8 | 0.8 | 1.3 | 2.5 | 81 | 4 | 14.2 |
| 9327.2 | 0.8 | 2.6 | 3.7 | 118 | 8 | 21.5 |
| 9379.2 | 0.8 | 4.9 | 3.3 | 107 | 7 | 39.8 |
| 9443.2 | 0.8 | 4.0 | 2.8 | 88 | 5 | 22.1 |

### Absorption (troughs) — 32 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 4188.0 | 0.8 | -0.2 | 77.7 | 5563 | 4 | 18.8 |
| 4222.4 | 0.8 | -0.5 | 24.8 | 1759 | 8 | 13.4 |
| 4274.4 | 0.8 | -0.4 | 39.7 | 2785 | 5 | 9.6 |
| 4607.2 | 0.8 | -0.3 | 11.6 | 752 | 20 | 35.4 |
| 4625.6 | 0.8 | -0.5 | 11.6 | 749 | 18 | 35.9 |
| 4748.8 | 0.8 | -0.1 | 53.1 | 3352 | 4 | 17.9 |
| 4868.0 | 0.8 | -0.8 | 70.3 | 4331 | 7 | 24.0 |
| 5075.2 | 0.8 | -0.2 | 5.4 | 319 | 4 | 8.8 |
| 5333.6 | 0.8 | -0.5 | 58.1 | 3268 | 5 | 20.3 |
| 5439.2 | 0.8 | -0.2 | 58.1 | 3204 | 5 | 16.3 |
| 6010.4 | 0.8 | -0.8 | 12.7 | 632 | 19 | 22.2 |
| 6031.2 | 0.8 | -0.1 | 14.0 | 695 | 12 | 17.6 |
| 6084.8 | 0.8 | -0.1 | 103.0 | 5073 | 5 | 132.5 |
| 6132.0 | 0.8 | -2.0 | 9.6 | 467 | 18 | 38.7 |
| 6149.6 | 0.8 | -1.0 | 10.5 | 510 | 9 | 16.7 |
| 6191.2 | 0.8 | -5.4 | 10.5 | 507 | 19 | 35.4 |
| 6216.0 | 0.8 | -0.5 | 20.5 | 988 | 16 | 240.5 |
| 7740.8 | 0.8 | -0.0 | 77.7 | 3010 | 4 | 13.4 |
| 7790.4 | 0.8 | -0.0 | 15.3 | 589 | 7 | 10.0 |
| 7811.2 | 0.8 | -0.1 | 11.6 | 444 | 12 | 10.3 |
| 7850.4 | 0.8 | -0.1 | 64.2 | 2453 | 4 | 10.9 |
| 8120.0 | 0.8 | -3.5 | 8.6 | 319 | 5 | 9.5 |
| 8306.4 | 0.8 | -0.4 | 15.3 | 553 | 17 | 15.4 |
| 8326.4 | 0.8 | -0.4 | 8.6 | 311 | 7 | 25.3 |
| 8350.4 | 0.8 | -0.1 | 20.5 | 735 | 16 | 20.0 |
| 8829.6 | 0.8 | -0.8 | 9.6 | 324 | 4 | 9.2 |
| 9006.4 | 0.8 | -0.1 | 2.5 | 84 | 4 | 10.0 |
| 9315.2 | 0.8 | -1.6 | 2.5 | 81 | 4 | 12.2 |
| 9327.2 | 0.8 | -2.6 | 2.5 | 81 | 4 | 12.0 |
| 9376.8 | 0.8 | -0.3 | 3.0 | 97 | 6 | 29.5 |
| 9441.6 | 0.8 | -2.5 | 2.8 | 88 | 5 | 19.9 |
| 9793.6 | 0.8 | -1.2 | 4.5 | 137 | 6 | 9.0 |


## Predicted Lines at z = 0.2381

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [Ne V] | 3426.0 | 4241.6 | em | narrow | peak@4242.4±0.8(z=0.2383) |
| [O II] | 3727.0 | 4614.2 | em | narrow | peak@4616.8±0.8(z=0.2387) |
| Ca K_abs | 3934.8 | 4871.5 | abs | absorption | trough@4868.0±0.8(z=0.2372) |
| Ca H_abs | 3969.6 | 4914.6 | abs | absorption | — |
| Hε | 3970.1 | 4915.2 | em | both | peak@4912.8±0.8(z=0.2374) |
| Hε_abs | 3970.1 | 4915.2 | abs | absorption | — |
| Hδ | 4102.9 | 5079.6 | em | both | peak@5079.2±0.8(z=0.2380) |
| Hδ_abs | 4102.9 | 5079.6 | abs | absorption | trough@5075.2±0.8(z=0.2370) |
| G-band_abs | 4305.6 | 5330.6 | abs | absorption | trough@5333.6±0.8(z=0.2388) |
| Hγ | 4341.7 | 5375.3 | em | both | peak@5387.2±0.8(z=0.2408) |
| Hγ_abs | 4341.7 | 5375.3 | abs | absorption | trough@5333.6±0.8(z=0.2285) |
| Hβ | 4862.7 | 6020.3 | em | both | peak@6020.0±0.8(z=0.2380) |
| Hβ_abs | 4862.7 | 6020.3 | abs | absorption | trough@6010.4±0.8(z=0.2360), trough@6031.2±0.8(z=0.2403) |
| [O III]a | 4960.3 | 6141.1 | em | narrow | peak@6140.8±0.8(z=0.2380) |
| [O III]b | 5008.2 | 6200.4 | em | narrow | peak@6200.0±0.8(z=0.2380) |
| Mg I_abs | 5176.7 | 6409.0 | abs | absorption | — |
| Na D1_abs | 5891.6 | 7294.1 | abs | absorption | — |
| Na D_abs | 5895.6 | 7299.1 | abs | absorption | — |
| Na D2_abs | 5897.6 | 7301.5 | abs | absorption | — |
| [N II]a | 6549.8 | 8109.0 | em | narrow | peak@8127.2±0.8(z=0.2408) |
| Hα | 6564.6 | 8127.3 | em | both | peak@8127.2±0.8(z=0.2380) |
| Hα_abs | 6564.6 | 8127.3 | abs | absorption | trough@8120.0±0.8(z=0.2369) |
| [N II]b | 6585.3 | 8152.9 | em | narrow | peak@8127.2±0.8(z=0.2341) |
| [S II]a | 6718.3 | 8317.6 | em | narrow | peak@8318.4±0.8(z=0.2382), peak@8336.0±0.8(z=0.2408) |
| [S II]b | 6732.7 | 8335.4 | em | narrow | peak@8336.0±0.8(z=0.2381), peak@8318.4±0.8(z=0.2355) |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| Ca K_abs/Ca H_abs | 4871.5/4914.6 | fit_doublet | 4867.36±6.602/4964.573±29.1272 | -0.825052/-0.229221 | 2606.0/3869.0 | 2.45 | 0.357 | warning; separation fail |
| Na D1_abs/Na D2_abs | 7294.1/7301.5 | fit_doublet | 7326.206±2.9776/7299.47±1.0891 | -0.086797/-0.248897 | 464.3/512.7 | 2.31 | 0.107 | warning; separation fail; component ratio 2.87 |
| Hε_abs | 4915.2 | fit_peak | 4869.036±3.1878 | -0.787451 | 2324.1 | 3.06 | 0.663 | ok |
| Mg I_abs | 6409.0 | fit_peak | 6359.026±18.3764 | -0.819502 | 13132.8 | 4.23 | 9.035 | warning: center_at_bound |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:nev-3426 | [Ne V] | 4241.6 | emission |
| line:oii-3727 | [O II] | 4614.2 | emission |
| line:cak-3934-abs | Ca K_abs | 4871.5 | absorption |
| line:cah-3969-abs | Ca H_abs | 4914.6 | absorption |
| line:heps-3970 | Hε | 4915.2 | emission |
| line:heps-3970-abs | Hε_abs | 4915.2 | absorption |
| line:hdel-4102 | Hδ | 5079.6 | emission |
| line:hdel-4102-abs | Hδ_abs | 5079.6 | absorption |
| line:gband-4305-abs | G-band_abs | 5330.6 | absorption |
| line:hgam-4341 | Hγ | 5375.3 | emission |
| line:hgam-4341-abs | Hγ_abs | 5375.3 | absorption |
| line:hbet-4862 | Hβ | 6020.3 | emission |
| line:hbet-4862-abs | Hβ_abs | 6020.3 | absorption |
| line:oiii-4960 | [O III]a | 6141.1 | emission |
| line:oiii-5008 | [O III]b | 6200.4 | emission |
| line:mgi-5176-abs | Mg I_abs | 6409.0 | absorption |
| line:nad1-5891-abs | Na D1_abs | 7294.1 | absorption |
| line:nad-5895-abs | Na D_abs | 7299.1 | absorption |
| line:nad2-5897-abs | Na D2_abs | 7301.5 | absorption |
| line:nii-6549 | [N II]a | 8109.0 | emission |
| line:half-6564 | Hα | 8127.3 | emission |
| line:half-6564-abs | Hα_abs | 8127.3 | absorption |
| line:nii-6585 | [N II]b | 8152.9 | emission |
| line:sii-6718 | [S II]a | 8317.6 | emission |
| line:sii-6732 | [S II]b | 8335.4 | emission |

| Measurement ID | Source | Kind | Centre (Å) | Target | Selectable | Flags |
|---|---|---|---:|---|---|---|
| cwt:em:0000 | CWT | emission | 4143.200 | — | yes | — |
| cwt:em:0001 | CWT | emission | 4242.400 | — | yes | — |
| cwt:em:0002 | CWT | emission | 4616.800 | — | yes | — |
| cwt:em:0003 | CWT | emission | 4791.200 | — | yes | — |
| cwt:em:0004 | CWT | emission | 4912.800 | — | yes | — |
| cwt:em:0005 | CWT | emission | 5079.200 | — | yes | — |
| cwt:em:0006 | CWT | emission | 5387.200 | — | yes | — |
| cwt:em:0007 | CWT | emission | 5802.400 | — | yes | — |
| cwt:em:0008 | CWT | emission | 6020.000 | — | yes | — |
| cwt:em:0009 | CWT | emission | 6140.800 | — | yes | — |
| cwt:em:0010 | CWT | emission | 6200.000 | — | yes | — |
| cwt:em:0011 | CWT | emission | 7802.400 | — | yes | — |
| cwt:em:0012 | CWT | emission | 8127.200 | — | yes | — |
| cwt:em:0013 | CWT | emission | 8318.400 | — | yes | — |
| cwt:em:0014 | CWT | emission | 8336.000 | — | yes | — |
| cwt:em:0015 | CWT | emission | 8837.600 | — | yes | — |
| cwt:em:0016 | CWT | emission | 9004.800 | — | yes | — |
| cwt:em:0017 | CWT | emission | 9068.800 | — | yes | — |
| cwt:em:0018 | CWT | emission | 9316.800 | — | yes | — |
| cwt:em:0019 | CWT | emission | 9327.200 | — | yes | — |
| cwt:em:0020 | CWT | emission | 9379.200 | — | yes | — |
| cwt:em:0021 | CWT | emission | 9443.200 | — | yes | — |
| cwt:abs:0000 | CWT | absorption | 4188.000 | — | yes | — |
| cwt:abs:0001 | CWT | absorption | 4222.400 | — | yes | — |
| cwt:abs:0002 | CWT | absorption | 4274.400 | — | yes | — |
| cwt:abs:0003 | CWT | absorption | 4607.200 | — | yes | — |
| cwt:abs:0004 | CWT | absorption | 4625.600 | — | yes | — |
| cwt:abs:0005 | CWT | absorption | 4748.800 | — | yes | — |
| cwt:abs:0006 | CWT | absorption | 4868.000 | — | yes | — |
| cwt:abs:0007 | CWT | absorption | 5075.200 | — | yes | — |
| cwt:abs:0008 | CWT | absorption | 5333.600 | — | yes | — |
| cwt:abs:0009 | CWT | absorption | 5439.200 | — | yes | — |
| cwt:abs:0010 | CWT | absorption | 6010.400 | — | yes | — |
| cwt:abs:0011 | CWT | absorption | 6031.200 | — | yes | — |
| cwt:abs:0012 | CWT | absorption | 6084.800 | — | yes | — |
| cwt:abs:0013 | CWT | absorption | 6132.000 | — | yes | — |
| cwt:abs:0014 | CWT | absorption | 6149.600 | — | yes | — |
| cwt:abs:0015 | CWT | absorption | 6191.200 | — | yes | — |
| cwt:abs:0016 | CWT | absorption | 6216.000 | — | yes | — |
| cwt:abs:0017 | CWT | absorption | 7740.800 | — | yes | — |
| cwt:abs:0018 | CWT | absorption | 7790.400 | — | yes | — |
| cwt:abs:0019 | CWT | absorption | 7811.200 | — | yes | — |
| cwt:abs:0020 | CWT | absorption | 7850.400 | — | yes | — |
| cwt:abs:0021 | CWT | absorption | 8120.000 | — | yes | — |
| cwt:abs:0022 | CWT | absorption | 8306.400 | — | yes | — |
| cwt:abs:0023 | CWT | absorption | 8326.400 | — | yes | — |
| cwt:abs:0024 | CWT | absorption | 8350.400 | — | yes | — |
| cwt:abs:0025 | CWT | absorption | 8829.600 | — | yes | — |
| cwt:abs:0026 | CWT | absorption | 9006.400 | — | yes | — |
| cwt:abs:0027 | CWT | absorption | 9315.200 | — | yes | — |
| cwt:abs:0028 | CWT | absorption | 9327.200 | — | yes | — |
| cwt:abs:0029 | CWT | absorption | 9376.800 | — | yes | — |
| cwt:abs:0030 | CWT | absorption | 9441.600 | — | yes | — |
| cwt:abs:0031 | CWT | absorption | 9793.600 | — | yes | — |
| fit:H3:0000 | fit_doublet | absorption | 4867.360 | Ca K_abs | yes | — |
| fit:H3:0001 | fit_doublet | absorption | 4964.573 | Ca H_abs | yes | — |
| fit:H3:0002 | fit_doublet | absorption | 7326.206 | Na D1_abs | yes | — |
| fit:H3:0003 | fit_doublet | absorption | 7299.470 | Na D2_abs | yes | — |
| fit:H3:0004 | fit_peak | absorption | 4869.036 | Hε_abs | yes | — |
| fit:H3:0005 | fit_peak | absorption | 6359.026 | Mg I_abs | no | center_at_bound |


```

## Returned events

### Event 1

#### Graph update: `model`

### Event 1 message: ai

```markdown
I'll evaluate each predicted line against the CWT features and targeted fits, then write the CSV.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H3/pre_analysis/branches/main/a17b8ffe679648b098725b050663ea61/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": "cwt:em:0001",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "comment": "Peak 4242.4 (z=0.2383) within 0.8 A of prediction; SNR 21.3, ridge 19, FWHM 1917 km/s broad for narrow guide but credible detection."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": "cwt:em:0002",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "comment": "Peak 4616.8 (z=0.2387) 2.6 A from prediction; SNR 76.2, ridge 24, strong credible detection."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "cwt:abs:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "doublet_separation_fail",
            "weak_depth"
          ],
          "comment": "Trough 4868.0 (z=0.2372) 3.5 A from prediction; doublet fit separation failed and Ca H landed at 4964.6, so Ca K depth ordering is unreliable. Preserve as plausible weak component."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H3:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "cwt_missed",
            "doublet_separation_fail",
            "blend",
            "weak_depth"
          ],
          "comment": "No CWT trough at 4914.6; targeted doublet fit centre 4964.6 is ~50 A redward with large error and separation fail. Weak plausible Ca H component, depth ordering uncertain."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "cwt:em:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "weak_amplitude",
            "blend"
          ],
          "comment": "Peak 4912.8 (z=0.2374) 2.4 A from prediction but amp 1.3, SNR 10.7; blended with Ca H absorption region, weak."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H3:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "cwt_missed",
            "broad_width",
            "blend"
          ],
          "comment": "Fit centre 4869.0 is ~46 A blueward of prediction with FWHM 2324 km/s; likely the same broad trough as Ca K, not a distinct H-epsilon absorption. Weak/ambiguous."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "cwt:em:0005",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "comment": "Peak 5079.2 (z=0.2380) 0.4 A from prediction; SNR 16.2, ridge 24, credible."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "cwt:abs:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "weak_amplitude",
            "blend"
          ],
          "comment": "Trough 5075.2 (z=0.2370) 4.4 A from prediction, amp -0.2, SNR 8.8; weak and adjacent to H-delta emission."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "cwt:abs:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "broad_width",
            "weak_amplitude"
          ],
          "comment": "Trough 5333.6 (z=0.2388) 3.0 A from prediction but FWHM 3268 km/s and amp -0.5; broad, possibly blended."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "cwt:em:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width",
            "low_ridge"
          ],
          "comment": "Peak 5387.2 (z=0.2408) 11.9 A redward, FWHM 4736 km/s, ridge 7; weak broad feature, offset in weaker band."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_credible_measurement",
            "offset_reject"
          ],
          "comment": "Only nearby trough 5333.6 implies z=0.2285, ~42 A blueward of prediction; no credible H-gamma absorption adopted."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "cwt:em:0008",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "comment": "Peak 6020.0 (z=0.2380) 0.3 A from prediction; SNR 36.2, ridge 21, credible."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "cwt:abs:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "blend",
            "weak_amplitude"
          ],
          "comment": "Trough 6010.4 (z=0.2360) 9.9 A blueward, amp -0.8; adjacent trough 6031.2 also present, blended with H-beta emission."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "cwt:em:0009",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "comment": "Peak 6140.8 (z=0.2380) 0.3 A from prediction; SNR 66.3, ridge 19, credible."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "cwt:em:0010",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent",
            "doublet_ratio_ok"
          ],
          "comment": "Peak 6200.0 (z=0.2380) 0.4 A from prediction; SNR 133.7, ridge 24; separation 59.2 A matches doublet, ratio consistent with 3:1."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_credible_measurement"
          ],
          "comment": "Only targeted fit centre 6359.0 hit the window bound with FWHM 13133 km/s; not selectable, no credible Mg I absorption."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H3:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "cwt_missed",
            "doublet_separation_fail",
            "offset_weak",
            "blend"
          ],
          "comment": "No CWT trough at 7294.1; doublet fit centre 7326.2 is ~32 A redward with separation fail and ratio 2.87. Ambiguous Na D blend."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_credible_measurement",
            "blend"
          ],
          "comment": "No CWT trough near 7299.1 and no targeted fit for this component; unresolved within Na D blend."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H3:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "cwt_missed",
            "doublet_separation_fail",
            "blend"
          ],
          "comment": "Doublet fit centre 7299.5 is 2.0 A from prediction but separation failed against Na D1; weak blended Na D component."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "cwt:em:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "blend",
            "doublet_ratio_caveat"
          ],
          "comment": "Only peak 8127.2 (z=0.2408) available, 18.2 A redward; shared with H-alpha, so [N II]a identity is ambiguous."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "cwt:em:0012",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "comment": "Peak 8127.2 (z=0.2380) 0.1 A from prediction; SNR 22.7, ridge 22, credible; blended with [N II]."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "cwt:abs:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "weak_amplitude",
            "blend"
          ],
          "comment": "Trough 8120.0 (z=0.2369) 7.3 A blueward, amp -3.5 but SNR 9.5 and ridge 5; blended with H-alpha emission."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "cwt:em:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "blend",
            "doublet_ratio_caveat"
          ],
          "comment": "Only peak 8127.2 (z=0.2341) available, 25.9 A blueward; shared with H-alpha, [N II]b identity ambiguous."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "cwt:em:0013",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent",
            "doublet_ratio_ok"
          ],
          "comment": "Peak 8318.4 (z=0.2382) 0.8 A from prediction; SNR 31.8, ridge 23; separation 17.6 A matches doublet."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "cwt:em:0014",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent",
            "doublet_ratio_ok"
          ],
          "comment": "Peak 8336.0 (z=0.2381) 0.6 A from prediction; SNR 27.2, ridge 12; separation consistent with [S II] doublet."
        }
      ]
    },
    "id": "call_00_r4HeXGxFboDX3dS8dEzp6970",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 7396,
  "output_tokens": 2705,
  "total_tokens": 10101,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 6756,
  "provider_usage": {
    "completion_tokens": 2705,
    "prompt_tokens": 7396,
    "total_tokens": 10101,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 6756
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_r4HeXGxFboDX3dS8dEzp6970`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 3, "line_id": "line:cah-3969-abs", "measurement_id": "fit:H3:0001", "reason": "measurement is outside this line's redshift window"}, {"row": 5, "line_id": "line:heps-3970-abs", "measurement_id": "fit:H3:0004", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
Two fits fall outside the redshift window. I'll repair those rows.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H3/pre_analysis/branches/main/a17b8ffe679648b098725b050663ea61/lines.csv",
      "lines": [
        {
          "comment": "Peak 4242.4 (z=0.2383) within 0.8 A of prediction; SNR 21.3, ridge 19, FWHM 1917 km/s broad for narrow guide but credible detection.",
          "line_id": "line:nev-3426",
          "measurement_id": "cwt:em:0001",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "status": "LIKELY"
        },
        {
          "comment": "Peak 4616.8 (z=0.2387) 2.6 A from prediction; SNR 76.2, ridge 24, strong credible detection.",
          "line_id": "line:oii-3727",
          "measurement_id": "cwt:em:0002",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "status": "LIKELY"
        },
        {
          "comment": "Trough 4868.0 (z=0.2372) 3.5 A from prediction; doublet fit separation failed and Ca H landed at 4964.6, so Ca K depth ordering is unreliable. Preserve as plausible weak component.",
          "line_id": "line:cak-3934-abs",
          "measurement_id": "cwt:abs:0006",
          "reason_codes": [
            "blend",
            "doublet_separation_fail",
            "weak_depth"
          ],
          "status": "MARGINAL"
        },
        {
          "comment": "No CWT trough at 4914.6; targeted doublet fit centre 4964.6 is ~50 A redward (outside z-window) with large error and separation fail. No credible Ca H measurement adopted.",
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "reason_codes": [
            "cwt_missed",
            "doublet_separation_fail",
            "offset_reject",
            "no_credible_measurement"
          ],
          "status": "NOT_FOUND"
        },
        {
          "comment": "Peak 4912.8 (z=0.2374) 2.4 A from prediction but amp 1.3, SNR 10.7; blended with Ca H absorption region, weak.",
          "line_id": "line:heps-3970",
          "measurement_id": "cwt:em:0004",
          "reason_codes": [
            "offset_ok",
            "weak_amplitude",
            "blend"
          ],
          "status": "MARGINAL"
        },
        {
          "comment": "Only fit centre 4869.0 implies z=0.2264, outside the verification window; likely the same broad trough as Ca K, not a distinct H-epsilon absorption. No credible measurement.",
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "reason_codes": [
            "cwt_missed",
            "offset_reject",
            "blend",
            "no_credible_measurement"
          ],
          "status": "NOT_FOUND"
        },
        {
          "comment": "Peak 5079.2 (z=0.2380) 0.4 A from prediction; SNR 16.2, ridge 24, credible.",
          "line_id": "line:hdel-4102",
          "measurement_id": "cwt:em:0005",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "status": "LIKELY"
        },
        {
          "comment": "Trough 5075.2 (z=0.2370) 4.4 A from prediction, amp -0.2, SNR 8.8; weak and adjacent to H-delta emission.",
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "cwt:abs:0007",
          "reason_codes": [
            "offset_ok",
            "weak_amplitude",
            "blend"
          ],
          "status": "MARGINAL"
        },
        {
          "comment": "Trough 5333.6 (z=0.2388) 3.0 A from prediction but FWHM 3268 km/s and amp -0.5; broad, possibly blended.",
          "line_id": "line:gband-4305-abs",
          "measurement_id": "cwt:abs:0008",
          "reason_codes": [
            "offset_ok",
            "broad_width",
            "weak_amplitude"
          ],
          "status": "MARGINAL"
        },
        {
          "comment": "Peak 5387.2 (z=0.2408) 11.9 A redward, FWHM 4736 km/s, ridge 7; weak broad feature, offset in weaker band.",
          "line_id": "line:hgam-4341",
          "measurement_id": "cwt:em:0006",
          "reason_codes": [
            "offset_weak",
            "broad_width",
            "low_ridge"
          ],
          "status": "MARGINAL"
        },
        {
          "comment": "Only nearby trough 5333.6 implies z=0.2285, ~42 A blueward of prediction; no credible H-gamma absorption adopted.",
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "reason_codes": [
            "no_credible_measurement",
            "offset_reject"
          ],
          "status": "NOT_FOUND"
        },
        {
          "comment": "Peak 6020.0 (z=0.2380) 0.3 A from prediction; SNR 36.2, ridge 21, credible.",
          "line_id": "line:hbet-4862",
          "measurement_id": "cwt:em:0008",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "status": "LIKELY"
        },
        {
          "comment": "Trough 6010.4 (z=0.2360) 9.9 A blueward, amp -0.8; adjacent trough 6031.2 also present, blended with H-beta emission.",
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "cwt:abs:0010",
          "reason_codes": [
            "offset_ok",
            "blend",
            "weak_amplitude"
          ],
          "status": "MARGINAL"
        },
        {
          "comment": "Peak 6140.8 (z=0.2380) 0.3 A from prediction; SNR 66.3, ridge 19, credible.",
          "line_id": "line:oiii-4960",
          "measurement_id": "cwt:em:0009",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "status": "LIKELY"
        },
        {
          "comment": "Peak 6200.0 (z=0.2380) 0.4 A from prediction; SNR 133.7, ridge 24; separation 59.2 A matches doublet, ratio consistent with 3:1.",
          "line_id": "line:oiii-5008",
          "measurement_id": "cwt:em:0010",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent",
            "doublet_ratio_ok"
          ],
          "status": "LIKELY"
        },
        {
          "comment": "Only targeted fit centre 6359.0 hit the window bound with FWHM 13133 km/s; not selectable, no credible Mg I absorption.",
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "reason_codes": [
            "center_at_bound",
            "no_credible_measurement"
          ],
          "status": "NOT_FOUND"
        },
        {
          "comment": "No CWT trough at 7294.1; doublet fit centre 7326.2 is ~32 A redward with separation fail and ratio 2.87. Ambiguous Na D blend.",
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H3:0002",
          "reason_codes": [
            "cwt_missed",
            "doublet_separation_fail",
            "offset_weak",
            "blend"
          ],
          "status": "MARGINAL"
        },
        {
          "comment": "No CWT trough near 7299.1 and no targeted fit for this component; unresolved within Na D blend.",
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "reason_codes": [
            "no_credible_measurement",
            "blend"
          ],
          "status": "NOT_FOUND"
        },
        {
          "comment": "Doublet fit centre 7299.5 is 2.0 A from prediction but separation failed against Na D1; weak blended Na D component.",
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H3:0003",
          "reason_codes": [
            "cwt_missed",
            "doublet_separation_fail",
            "blend"
          ],
          "status": "MARGINAL"
        },
        {
          "comment": "Only peak 8127.2 (z=0.2408) available, 18.2 A redward; shared with H-alpha, so [N II]a identity is ambiguous.",
          "line_id": "line:nii-6549",
          "measurement_id": "cwt:em:0012",
          "reason_codes": [
            "offset_weak",
            "blend",
            "doublet_ratio_caveat"
          ],
          "status": "MARGINAL"
        },
        {
          "comment": "Peak 8127.2 (z=0.2380) 0.1 A from prediction; SNR 22.7, ridge 22, credible; blended with [N II].",
          "line_id": "line:half-6564",
          "measurement_id": "cwt:em:0012",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent"
          ],
          "status": "LIKELY"
        },
        {
          "comment": "Trough 8120.0 (z=0.2369) 7.3 A blueward, amp -3.5 but SNR 9.5 and ridge 5; blended with H-alpha emission.",
          "line_id": "line:half-6564-abs",
          "measurement_id": "cwt:abs:0021",
          "reason_codes": [
            "offset_ok",
            "weak_amplitude",
            "blend"
          ],
          "status": "MARGINAL"
        },
        {
          "comment": "Only peak 8127.2 (z=0.2341) available, 25.9 A blueward; shared with H-alpha, [N II]b identity ambiguous.",
          "line_id": "line:nii-6585",
          "measurement_id": "cwt:em:0012",
          "reason_codes": [
            "offset_weak",
            "blend",
            "doublet_ratio_caveat"
          ],
          "status": "MARGINAL"
        },
        {
          "comment": "Peak 8318.4 (z=0.2382) 0.8 A from prediction; SNR 31.8, ridge 23; separation 17.6 A matches doublet.",
          "line_id": "line:sii-6718",
          "measurement_id": "cwt:em:0013",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent",
            "doublet_ratio_ok"
          ],
          "status": "LIKELY"
        },
        {
          "comment": "Peak 8336.0 (z=0.2381) 0.6 A from prediction; SNR 27.2, ridge 12; separation consistent with [S II] doublet.",
          "line_id": "line:sii-6732",
          "measurement_id": "cwt:em:0014",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent",
            "doublet_ratio_ok"
          ],
          "status": "LIKELY"
        }
      ]
    },
    "id": "call_00_fv9MVUAQFeltZ9fxQx3x8719",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 10255,
  "output_tokens": 2678,
  "total_tokens": 12933,
  "cache_hit_tokens": 9984,
  "cache_miss_tokens": 271,
  "provider_usage": {
    "completion_tokens": 2678,
    "prompt_tokens": 10255,
    "total_tokens": 12933,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 9984
    },
    "prompt_cache_hit_tokens": 9984,
    "prompt_cache_miss_tokens": 271
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_fv9MVUAQFeltZ9fxQx3x8719`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H3/pre_analysis/branches/main/a17b8ffe679648b098725b050663ea61/lines.csv", "n_lines": 25, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H3/pre_analysis/branches/main/a17b8ffe679648b098725b050663ea61/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:40:09.485828+00:00
