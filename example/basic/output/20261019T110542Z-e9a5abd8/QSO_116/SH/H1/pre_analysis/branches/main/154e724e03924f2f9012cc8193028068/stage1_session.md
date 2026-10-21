# SH pre-analysis session: line review

- Run ID: `graph-325ff74c7f444efdb17e3f3b69698eea`
- Hypothesis: `H1`
- Started (UTC): 2026-10-19T11:44:43.193978+00:00
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
Review every predicted line at the fixed Redrock redshift `-0.0010220268078304992`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H1/pre_analysis/branches/main/154e724e03924f2f9012cc8193028068/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 4.7 |

Verify the redshift hypothesis z ≈ -0.0010220268078304992.

Verification window: z ∈ [-0.011, 0.009]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=47.851, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=14.3853, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=35.4637, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=34.7644, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=5.99387, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/QSO_116.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H1/pre_analysis/branches/main/154e724e03924f2f9012cc8193028068/lines.csv

## CWT Detected Features

### Emission (peaks) — 18 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 4768.0 | 0.8 | 4.9 | 39.7 | 2497 | 15 | 13.0 |
| 5488.0 | 0.8 | 0.3 | 113.8 | 6214 | 4 | 11.6 |
| 6072.0 | 0.8 | 1.7 | 70.3 | 3473 | 9 | 23.3 |
| 7474.4 | 0.8 | 0.3 | 85.1 | 3413 | 7 | 20.0 |
| 8769.6 | 0.8 | 0.6 | 3.0 | 104 | 6 | 12.3 |
| 8828.8 | 0.8 | 0.5 | 3.7 | 125 | 8 | 20.4 |
| 9317.6 | 0.8 | 0.9 | 2.5 | 81 | 4 | 11.2 |
| 9328.0 | 0.8 | 2.1 | 2.8 | 89 | 5 | 11.2 |
| 9381.6 | 0.8 | 1.0 | 5.9 | 189 | 13 | 42.9 |
| 9424.8 | 0.8 | -0.1 | 2.8 | 88 | 5 | 13.6 |
| 9444.8 | 0.8 | 0.6 | 6.5 | 207 | 14 | 53.9 |
| 9463.2 | 0.8 | 2.3 | 4.5 | 141 | 10 | 28.3 |
| 9481.6 | 0.8 | 1.9 | 4.0 | 128 | 9 | 32.3 |
| 9507.2 | 0.8 | 0.4 | 3.0 | 96 | 6 | 18.2 |
| 9524.0 | 0.8 | 1.5 | 3.3 | 105 | 7 | 26.5 |
| 9557.6 | 0.8 | 0.5 | 2.8 | 86 | 5 | 10.5 |
| 9572.8 | 0.8 | 0.1 | 3.7 | 115 | 8 | 22.8 |
| 9794.4 | 0.8 | 0.4 | 4.0 | 124 | 9 | 16.6 |

### Absorption (troughs) — 15 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 4926.4 | 0.8 | -0.4 | 103.0 | 6265 | 5 | 28.9 |
| 8468.0 | 0.8 | -1.4 | 3.0 | 108 | 6 | 11.6 |
| 8772.0 | 0.8 | -0.8 | 2.8 | 94 | 5 | 12.0 |
| 8831.2 | 0.8 | -1.5 | 3.7 | 125 | 8 | 27.0 |
| 8923.2 | 0.8 | -2.3 | 2.8 | 93 | 5 | 16.8 |
| 9326.4 | 0.8 | -1.8 | 2.8 | 89 | 5 | 9.6 |
| 9377.6 | 0.8 | -0.1 | 4.9 | 156 | 11 | 39.1 |
| 9422.4 | 0.8 | -1.7 | 2.8 | 88 | 5 | 14.8 |
| 9440.8 | 0.8 | -0.5 | 4.9 | 155 | 11 | 45.4 |
| 9460.8 | 0.8 | -0.7 | 3.7 | 117 | 8 | 22.6 |
| 9478.4 | 0.8 | -0.3 | 4.5 | 141 | 10 | 32.9 |
| 9504.8 | 0.8 | -0.9 | 3.0 | 96 | 6 | 22.0 |
| 9521.6 | 0.8 | -1.1 | 3.3 | 105 | 7 | 25.6 |
| 9569.6 | 0.8 | -1.3 | 4.9 | 153 | 11 | 25.0 |
| 9623.2 | 0.8 | -0.6 | 3.0 | 95 | 6 | 10.3 |


## Predicted Lines at z = -0.0010

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [O II] | 3727.0 | 3723.2 | em | narrow | — |
| Ca K_abs | 3934.8 | 3930.8 | abs | absorption | — |
| Ca H_abs | 3969.6 | 3965.5 | abs | absorption | — |
| Hε | 3970.1 | 3966.0 | em | both | — |
| Hε_abs | 3970.1 | 3966.0 | abs | absorption | — |
| Hδ | 4102.9 | 4098.7 | em | both | — |
| Hδ_abs | 4102.9 | 4098.7 | abs | absorption | — |
| G-band_abs | 4305.6 | 4301.2 | abs | absorption | — |
| Hγ | 4341.7 | 4337.3 | em | both | — |
| Hγ_abs | 4341.7 | 4337.3 | abs | absorption | — |
| Hβ | 4862.7 | 4857.7 | em | both | — |
| Hβ_abs | 4862.7 | 4857.7 | abs | absorption | — |
| [O III]a | 4960.3 | 4955.2 | em | narrow | — |
| [O III]b | 5008.2 | 5003.1 | em | narrow | — |
| Mg I_abs | 5176.7 | 5171.4 | abs | absorption | — |
| Na D1_abs | 5891.6 | 5885.6 | abs | absorption | — |
| Na D_abs | 5895.6 | 5889.6 | abs | absorption | — |
| Na D2_abs | 5897.6 | 5891.6 | abs | absorption | — |
| [N II]a | 6549.8 | 6543.1 | em | narrow | — |
| Hα | 6564.6 | 6557.9 | em | both | — |
| Hα_abs | 6564.6 | 6557.9 | abs | absorption | — |
| [N II]b | 6585.3 | 6578.6 | em | narrow | — |
| [S II]a | 6718.3 | 6711.4 | em | narrow | — |
| [S II]b | 6732.7 | 6725.8 | em | narrow | — |
| CaT1_abs | 8498.0 | 8489.3 | abs | absorption | trough@8468.0±0.8(z=-0.0035) |
| CaT2_abs | 8542.0 | 8533.3 | abs | absorption | trough@8468.0±0.8(z=-0.0087) |
| CaT3_abs | 8662.0 | 8653.1 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 4955.2/5003.1 | fit_doublet | 4905.268±0.0/5053.064±0.0 | 0.0/0.0 | 143.9/139.7 | 0.0 | -0.0 | warning; separation fail; component ratio — |
| [S II]a/[S II]b | 6711.4/6725.8 | fit_doublet | 6761.434±2.2029/6736.027±0.0 | 0.052035/0.0 | 104.4/31439.6 | 0.48 | 0.001 | warning: center_1_deviation_large; separation fail; component ratio 0.0 |
| [N II]a/[N II]b | 6543.1/6578.6 | fit_doublet | 6525.576±5.2188/6564.712±1.1557 | 0.101951/0.127321 | 2139.5/170.2 | 1.1 | 0.052 | ok; separation pass; component ratio 1.25 |
| Ca K_abs/Ca H_abs | 3930.8/3965.5 | fit_doublet | 3931.745±2.9373/3977.4±0.9978 | -0.442645/-0.634655 | 1171.7/274.8 | 1.33 | 0.025 | warning; separation fail |
| Na D1_abs/Na D2_abs | 5885.6/5891.6 | fit_doublet | 5870.095±1.4989/5918.54±6.1771 | -0.242123/-0.428304 | 120.3/5763.7 | 1.84 | 0.529 | warning; separation fail; component ratio 1.77 |
| [O II] | 3723.2 | fit_peak | 3673.415±0.0 | 0.0 | 27852.2 | 0.0 | -0.0 | ok |
| Hε | 3966.0 | fit_peak | 4015.037±0.8039 | 0.558233 | 175.8 | 1.22 | 0.007 | ok |
| Hδ | 4098.7 | fit_peak | 4057.803±2.5194 | 0.650436 | 3438.9 | 1.76 | 0.271 | ok |
| Hγ | 4337.3 | fit_peak | 4327.332±0.6282 | 0.535737 | 163.1 | 1.62 | 0.012 | ok |
| Hβ | 4857.7 | fit_peak | 4807.73±4.2477 | 1.955827 | 8602.7 | 6.18 | 9.915 | warning: center_at_bound |
| Hα | 6557.9 | fit_peak | 6530.398±4.737 | 0.101474 | 2251.6 | 0.95 | 0.083 | ok |
| Hε_abs | 3966.0 | fit_peak | 3949.566±10.0565 | -0.234471 | 4880.2 | 0.5 | 0.031 | ok |
| Hδ_abs | 4098.7 | fit_peak | 4102.807±0.0 | -0.0 | 343.3 | 0.0 | 0.0 | ok |
| G-band_abs | 4301.2 | fit_peak | 4299.399±1.136 | -0.328567 | 198.2 | 0.97 | 0.005 | ok |
| Hγ_abs | 4337.3 | fit_peak | 4347.34±2.196 | -0.36295 | 924.7 | 1.1 | 0.031 | ok |
| Hβ_abs | 4857.7 | fit_peak | 4907.73±17.0015 | -0.298764 | 3429.9 | 0.57 | 0.035 | warning: center_at_bound |
| Mg I_abs | 5171.4 | fit_peak | 5193.575±7.4029 | -0.062679 | 1710.5 | 0.5 | 0.014 | ok |
| Hα_abs | 6557.9 | fit_peak | 6574.235±2.0427 | -0.09001 | 314.0 | 0.82 | 0.009 | ok |
| CaT3_abs | 8653.1 | fit_peak | 8632.257±10.936 | -0.069613 | 979.2 | 0.76 | 0.03 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:oii-3727 | [O II] | 3723.2 | emission |
| line:cak-3934-abs | Ca K_abs | 3930.8 | absorption |
| line:cah-3969-abs | Ca H_abs | 3965.5 | absorption |
| line:heps-3970 | Hε | 3966.0 | emission |
| line:heps-3970-abs | Hε_abs | 3966.0 | absorption |
| line:hdel-4102 | Hδ | 4098.7 | emission |
| line:hdel-4102-abs | Hδ_abs | 4098.7 | absorption |
| line:gband-4305-abs | G-band_abs | 4301.2 | absorption |
| line:hgam-4341 | Hγ | 4337.3 | emission |
| line:hgam-4341-abs | Hγ_abs | 4337.3 | absorption |
| line:hbet-4862 | Hβ | 4857.7 | emission |
| line:hbet-4862-abs | Hβ_abs | 4857.7 | absorption |
| line:oiii-4960 | [O III]a | 4955.2 | emission |
| line:oiii-5008 | [O III]b | 5003.1 | emission |
| line:mgi-5176-abs | Mg I_abs | 5171.4 | absorption |
| line:nad1-5891-abs | Na D1_abs | 5885.6 | absorption |
| line:nad-5895-abs | Na D_abs | 5889.6 | absorption |
| line:nad2-5897-abs | Na D2_abs | 5891.6 | absorption |
| line:nii-6549 | [N II]a | 6543.1 | emission |
| line:half-6564 | Hα | 6557.9 | emission |
| line:half-6564-abs | Hα_abs | 6557.9 | absorption |
| line:nii-6585 | [N II]b | 6578.6 | emission |
| line:sii-6718 | [S II]a | 6711.4 | emission |
| line:sii-6732 | [S II]b | 6725.8 | emission |
| line:cat1-8498-abs | CaT1_abs | 8489.3 | absorption |
| line:cat2-8542-abs | CaT2_abs | 8533.3 | absorption |
| line:cat3-8662-abs | CaT3_abs | 8653.1 | absorption |

| Measurement ID | Source | Kind | Centre (Å) | Target | Selectable | Flags |
|---|---|---|---:|---|---|---|
| cwt:em:0000 | CWT | emission | 4768.000 | — | yes | — |
| cwt:em:0001 | CWT | emission | 5488.000 | — | yes | — |
| cwt:em:0002 | CWT | emission | 6072.000 | — | yes | — |
| cwt:em:0003 | CWT | emission | 7474.400 | — | yes | — |
| cwt:em:0004 | CWT | emission | 8769.600 | — | yes | — |
| cwt:em:0005 | CWT | emission | 8828.800 | — | yes | — |
| cwt:em:0006 | CWT | emission | 9317.600 | — | yes | — |
| cwt:em:0007 | CWT | emission | 9328.000 | — | yes | — |
| cwt:em:0008 | CWT | emission | 9381.600 | — | yes | — |
| cwt:em:0009 | CWT | emission | 9424.800 | — | yes | — |
| cwt:em:0010 | CWT | emission | 9444.800 | — | yes | — |
| cwt:em:0011 | CWT | emission | 9463.200 | — | yes | — |
| cwt:em:0012 | CWT | emission | 9481.600 | — | yes | — |
| cwt:em:0013 | CWT | emission | 9507.200 | — | yes | — |
| cwt:em:0014 | CWT | emission | 9524.000 | — | yes | — |
| cwt:em:0015 | CWT | emission | 9557.600 | — | yes | — |
| cwt:em:0016 | CWT | emission | 9572.800 | — | yes | — |
| cwt:em:0017 | CWT | emission | 9794.400 | — | yes | — |
| cwt:abs:0000 | CWT | absorption | 4926.400 | — | yes | — |
| cwt:abs:0001 | CWT | absorption | 8468.000 | — | yes | — |
| cwt:abs:0002 | CWT | absorption | 8772.000 | — | yes | — |
| cwt:abs:0003 | CWT | absorption | 8831.200 | — | yes | — |
| cwt:abs:0004 | CWT | absorption | 8923.200 | — | yes | — |
| cwt:abs:0005 | CWT | absorption | 9326.400 | — | yes | — |
| cwt:abs:0006 | CWT | absorption | 9377.600 | — | yes | — |
| cwt:abs:0007 | CWT | absorption | 9422.400 | — | yes | — |
| cwt:abs:0008 | CWT | absorption | 9440.800 | — | yes | — |
| cwt:abs:0009 | CWT | absorption | 9460.800 | — | yes | — |
| cwt:abs:0010 | CWT | absorption | 9478.400 | — | yes | — |
| cwt:abs:0011 | CWT | absorption | 9504.800 | — | yes | — |
| cwt:abs:0012 | CWT | absorption | 9521.600 | — | yes | — |
| cwt:abs:0013 | CWT | absorption | 9569.600 | — | yes | — |
| cwt:abs:0014 | CWT | absorption | 9623.200 | — | yes | — |
| fit:H1:0000 | fit_doublet | emission | 4905.268 | [O III]a | yes | — |
| fit:H1:0001 | fit_doublet | emission | 5053.064 | [O III]b | yes | — |
| fit:H1:0002 | fit_doublet | emission | 6761.434 | [S II]a | yes | — |
| fit:H1:0003 | fit_doublet | emission | 6736.027 | [S II]b | yes | — |
| fit:H1:0004 | fit_doublet | emission | 6525.576 | [N II]a | yes | — |
| fit:H1:0005 | fit_doublet | emission | 6564.712 | [N II]b | yes | — |
| fit:H1:0006 | fit_doublet | absorption | 3931.745 | Ca K_abs | yes | — |
| fit:H1:0007 | fit_doublet | absorption | 3977.400 | Ca H_abs | yes | — |
| fit:H1:0008 | fit_doublet | absorption | 5870.095 | Na D1_abs | yes | — |
| fit:H1:0009 | fit_doublet | absorption | 5918.540 | Na D2_abs | yes | — |
| fit:H1:0010 | fit_peak | emission | 3673.415 | [O II] | yes | — |
| fit:H1:0011 | fit_peak | emission | 4015.037 | Hε | yes | — |
| fit:H1:0012 | fit_peak | emission | 4057.803 | Hδ | yes | — |
| fit:H1:0013 | fit_peak | emission | 4327.332 | Hγ | yes | — |
| fit:H1:0014 | fit_peak | emission | 4807.730 | Hβ | no | center_at_bound |
| fit:H1:0015 | fit_peak | emission | 6530.398 | Hα | yes | — |
| fit:H1:0016 | fit_peak | absorption | 3949.566 | Hε_abs | yes | — |
| fit:H1:0017 | fit_peak | absorption | 4102.807 | Hδ_abs | yes | — |
| fit:H1:0018 | fit_peak | absorption | 4299.399 | G-band_abs | yes | — |
| fit:H1:0019 | fit_peak | absorption | 4347.340 | Hγ_abs | yes | — |
| fit:H1:0020 | fit_peak | absorption | 4907.730 | Hβ_abs | no | center_at_bound |
| fit:H1:0021 | fit_peak | absorption | 5193.575 | Mg I_abs | yes | — |
| fit:H1:0022 | fit_peak | absorption | 6574.235 | Hα_abs | yes | — |
| fit:H1:0023 | fit_peak | absorption | 8632.257 | CaT3_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H1/pre_analysis/branches/main/154e724e03924f2f9012cc8193028068/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_zero_amp",
            "blue_edge"
          ],
          "comment": "No CWT peak near 3723 A; fit_peak returned zero amplitude at 3673 A (50 A off, blue edge). No credible measurement."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H1:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "blend_cah"
          ],
          "comment": "Doublet fit centre 3931.7 A within ~1 A of prediction, negative amplitude -0.44; separation failed and Ca H component landed at 3977 A, so depth ordering unreliable. Weak but plausible Ca K trough."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H1:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "blend_cak"
          ],
          "comment": "Ca H fit centre 3977.4 A, ~12 A red of prediction, amplitude -0.63; separation from Ca K failed (45.7 A vs 34.8 expected). Plausible weak component but blended/uncertain."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H1:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "blend_cah"
          ],
          "comment": "Fit centre 4015 A, ~49 A red of prediction (weak offset band), amplitude 0.56, local SNR 1.2. Marginal; region blended with Ca H absorption."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H1:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "large_offset",
            "broad_width"
          ],
          "comment": "Fit centre 3949.6 A, ~16 A blue of prediction, amplitude -0.23, SNR 0.5, FWHM ~4880 km/s. Very weak, broad; marginal at best."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H1:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 4057.8 A, ~41 A blue of prediction, amplitude 0.65, SNR 1.8, FWHM ~3400 km/s. Weak offset emission; marginal."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H1:0017",
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_signal"
          ],
          "comment": "Fit returned zero amplitude at 4102.8 A; no credible absorption trough detected."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H1:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "shallow"
          ],
          "comment": "Fit centre 4299.4 A, ~2 A from prediction, amplitude -0.33, SNR 0.97. Shallow but positionally consistent; marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H1:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit centre 4327.3 A, ~10 A blue of prediction, amplitude 0.54, SNR 1.6. Weak emission; marginal."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H1:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 4347.3 A, ~10 A red of prediction, amplitude -0.36, SNR 1.1, FWHM ~925 km/s. Weak; marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "fit_rejected",
            "blend_cwt_4768"
          ],
          "comment": "Only fit (fit:H1:0014) hit center_at_bound and is not selectable. Nearest CWT peak 4768 A is ~90 A blue, beyond offset tolerance. No adoptable measurement."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "fit_rejected"
          ],
          "comment": "Fit (fit:H1:0020) hit center_at_bound at 4907.7 A and is not selectable. No credible absorption measurement."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_fail",
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Doublet fit gave zero amplitudes at 4905/5053 A with separation failure; no credible [O III]a signal."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_fail",
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Doublet fit zero amplitude at 5053 A, separation failed; no credible [O III]b signal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H1:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 5193.6 A, ~22 A red of prediction, amplitude -0.06, SNR 0.5, FWHM ~1710 km/s. Very shallow; marginal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H1:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend_nad"
          ],
          "comment": "Na D doublet fit centre 5870.1 A, ~15 A blue of prediction, amplitude -0.24; separation failed (48 A vs 6 expected). Blended Na D complex; marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_dedicated_fit",
            "blend_nad"
          ],
          "comment": "No dedicated measurement for the intermediate Na D line; only the D1/D2 doublet fit exists and it failed separation. No adoptable measurement."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H1:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "broad_width",
            "blend_nad"
          ],
          "comment": "Fit centre 5918.5 A, ~27 A red of prediction, amplitude -0.43, FWHM ~5760 km/s; separation failed. Blended Na D complex; marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H1:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width",
            "blend_ha"
          ],
          "comment": "Doublet fit centre 6525.6 A, ~17 A blue of prediction, amplitude 0.10, SNR 1.1, FWHM ~2140 km/s. Separation passed but very weak; blended with Halpha region; marginal."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H1:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "blend_nii"
          ],
          "comment": "Fit centre 6530.4 A, ~27 A blue of prediction, amplitude 0.10, SNR 0.95, FWHM ~2250 km/s. Weak; blended with [N II]; marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H1:0022",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit centre 6574.2 A, ~16 A red of prediction, amplitude -0.09, SNR 0.8. Very shallow; marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H1:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blend_ha",
            "ratio_advisory"
          ],
          "comment": "Doublet fit centre 6564.7 A, ~14 A blue of prediction, amplitude 0.13, SNR 1.1. Separation passed; blended with Halpha; marginal."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H1:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "weak_snr"
          ],
          "comment": "Fit centre 6761.4 A, ~50 A red of prediction, amplitude 0.05, SNR 0.48; separation failed. Weak, marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_fail",
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Second [S II] component fit zero amplitude at 6736 A with separation failure; no credible measurement."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_dedicated_fit"
          ],
          "comment": "Nearest CWT trough 8468 A implies z=-0.0035, ~21 A blue of prediction; no dedicated fit. No adoptable measurement."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_dedicated_fit"
          ],
          "comment": "Nearest CWT trough 8468 A implies z=-0.0087, ~65 A blue of prediction; no dedicated fit. No adoptable measurement."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H1:0023",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 8632.3 A, ~21 A blue of prediction, amplitude -0.07, SNR 0.76, FWHM ~980 km/s. Very shallow; marginal."
        }
      ]
    },
    "id": "call_00_FSRq306serFfWYI8EZEO8371",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 7326,
  "output_tokens": 2712,
  "total_tokens": 10038,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 6686,
  "provider_usage": {
    "completion_tokens": 2712,
    "prompt_tokens": 7326,
    "total_tokens": 10038,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 6686
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_FSRq306serFfWYI8EZEO8371`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 3, "line_id": "line:heps-3970", "measurement_id": "fit:H1:0011", "reason": "measurement is outside this line's redshift window"}, {"row": 6, "line_id": "line:hdel-4102-abs", "reason": "unadopted line needs null measurement_id"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
Two repairs needed: Hε fit is outside the redshift window, and Hδ_abs must be null.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H1/pre_analysis/branches/main/154e724e03924f2f9012cc8193028068/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_zero_amp",
            "blue_edge"
          ],
          "comment": "No CWT peak near 3723 A; fit_peak returned zero amplitude at 3673 A (50 A off, blue edge). No credible measurement."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H1:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "blend_cah"
          ],
          "comment": "Doublet fit centre 3931.7 A within ~1 A of prediction, negative amplitude -0.44; separation failed and Ca H component landed at 3977 A, so depth ordering unreliable. Weak but plausible Ca K trough."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H1:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "blend_cak"
          ],
          "comment": "Ca H fit centre 3977.4 A, ~12 A red of prediction, amplitude -0.63; separation from Ca K failed (45.7 A vs 34.8 expected). Plausible weak component but blended/uncertain."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_outside_window",
            "no_cwt_feature"
          ],
          "comment": "Only fit centre 4015 A implies z outside the verification window; no CWT peak near 3966 A. No adoptable measurement."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H1:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "large_offset",
            "broad_width"
          ],
          "comment": "Fit centre 3949.6 A, ~16 A blue of prediction, amplitude -0.23, SNR 0.5, FWHM ~4880 km/s. Very weak, broad; marginal at best."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H1:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 4057.8 A, ~41 A blue of prediction, amplitude 0.65, SNR 1.8, FWHM ~3400 km/s. Weak offset emission; marginal."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_signal"
          ],
          "comment": "Fit returned zero amplitude at 4102.8 A; no credible absorption trough detected."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H1:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "shallow"
          ],
          "comment": "Fit centre 4299.4 A, ~2 A from prediction, amplitude -0.33, SNR 0.97. Shallow but positionally consistent; marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H1:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit centre 4327.3 A, ~10 A blue of prediction, amplitude 0.54, SNR 1.6. Weak emission; marginal."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H1:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 4347.3 A, ~10 A red of prediction, amplitude -0.36, SNR 1.1, FWHM ~925 km/s. Weak; marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "fit_rejected",
            "blend_cwt_4768"
          ],
          "comment": "Only fit (fit:H1:0014) hit center_at_bound and is not selectable. Nearest CWT peak 4768 A is ~90 A blue, beyond offset tolerance. No adoptable measurement."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "fit_rejected"
          ],
          "comment": "Fit (fit:H1:0020) hit center_at_bound at 4907.7 A and is not selectable. No credible absorption measurement."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_fail",
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Doublet fit gave zero amplitudes at 4905/5053 A with separation failure; no credible [O III]a signal."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_fail",
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Doublet fit zero amplitude at 5053 A, separation failed; no credible [O III]b signal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H1:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 5193.6 A, ~22 A red of prediction, amplitude -0.06, SNR 0.5, FWHM ~1710 km/s. Very shallow; marginal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H1:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend_nad"
          ],
          "comment": "Na D doublet fit centre 5870.1 A, ~15 A blue of prediction, amplitude -0.24; separation failed (48 A vs 6 expected). Blended Na D complex; marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_dedicated_fit",
            "blend_nad"
          ],
          "comment": "No dedicated measurement for the intermediate Na D line; only the D1/D2 doublet fit exists and it failed separation. No adoptable measurement."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H1:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "broad_width",
            "blend_nad"
          ],
          "comment": "Fit centre 5918.5 A, ~27 A red of prediction, amplitude -0.43, FWHM ~5760 km/s; separation failed. Blended Na D complex; marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H1:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width",
            "blend_ha"
          ],
          "comment": "Doublet fit centre 6525.6 A, ~17 A blue of prediction, amplitude 0.10, SNR 1.1, FWHM ~2140 km/s. Separation passed but very weak; blended with Halpha region; marginal."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H1:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "blend_nii"
          ],
          "comment": "Fit centre 6530.4 A, ~27 A blue of prediction, amplitude 0.10, SNR 0.95, FWHM ~2250 km/s. Weak; blended with [N II]; marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H1:0022",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit centre 6574.2 A, ~16 A red of prediction, amplitude -0.09, SNR 0.8. Very shallow; marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H1:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blend_ha",
            "ratio_advisory"
          ],
          "comment": "Doublet fit centre 6564.7 A, ~14 A blue of prediction, amplitude 0.13, SNR 1.1. Separation passed; blended with Halpha; marginal."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H1:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "weak_snr"
          ],
          "comment": "Fit centre 6761.4 A, ~50 A red of prediction, amplitude 0.05, SNR 0.48; separation failed. Weak, marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_fail",
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Second [S II] component fit zero amplitude at 6736 A with separation failure; no credible measurement."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_dedicated_fit"
          ],
          "comment": "Nearest CWT trough 8468 A implies z=-0.0035, ~21 A blue of prediction; no dedicated fit. No adoptable measurement."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_dedicated_fit"
          ],
          "comment": "Nearest CWT trough 8468 A implies z=-0.0087, ~65 A blue of prediction; no dedicated fit. No adoptable measurement."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H1:0023",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 8632.3 A, ~21 A blue of prediction, amplitude -0.07, SNR 0.76, FWHM ~980 km/s. Very shallow; marginal."
        }
      ]
    },
    "id": "call_00_TSgz6IGcNfTmqrCHnocq1876",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 10176,
  "output_tokens": 2688,
  "total_tokens": 12864,
  "cache_hit_tokens": 9984,
  "cache_miss_tokens": 192,
  "provider_usage": {
    "completion_tokens": 2688,
    "prompt_tokens": 10176,
    "total_tokens": 12864,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 9984
    },
    "prompt_cache_hit_tokens": 9984,
    "prompt_cache_miss_tokens": 192
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_TSgz6IGcNfTmqrCHnocq1876`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H1/pre_analysis/branches/main/154e724e03924f2f9012cc8193028068/lines.csv", "n_lines": 27, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H1/pre_analysis/branches/main/154e724e03924f2f9012cc8193028068/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:45:02.031367+00:00
