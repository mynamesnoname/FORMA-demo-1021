# SH pre-analysis session: line review

- Run ID: `graph-325ff74c7f444efdb17e3f3b69698eea`
- Hypothesis: `H3`
- Started (UTC): 2026-10-19T11:44:43.367529+00:00
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
Review every predicted line at the fixed Redrock redshift `-0.0005607447321606066`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H3/pre_analysis/branches/main/e6e35209332e4719b84c5fc64b1ca55c/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 4.7 |

Verify the redshift hypothesis z ≈ -0.0005607447321606066.

Verification window: z ∈ [-0.0106, 0.0094]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=47.8731, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=14.3919, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=35.4801, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=34.7805, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=5.99664, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/QSO_116.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H3/pre_analysis/branches/main/e6e35209332e4719b84c5fc64b1ca55c/lines.csv

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


## Predicted Lines at z = -0.0006

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [O II] | 3727.0 | 3724.9 | em | narrow | — |
| Ca K_abs | 3934.8 | 3932.6 | abs | absorption | — |
| Ca H_abs | 3969.6 | 3967.4 | abs | absorption | — |
| Hε | 3970.1 | 3967.9 | em | both | — |
| Hε_abs | 3970.1 | 3967.9 | abs | absorption | — |
| Hδ | 4102.9 | 4100.6 | em | both | — |
| Hδ_abs | 4102.9 | 4100.6 | abs | absorption | — |
| G-band_abs | 4305.6 | 4303.2 | abs | absorption | — |
| Hγ | 4341.7 | 4339.3 | em | both | — |
| Hγ_abs | 4341.7 | 4339.3 | abs | absorption | — |
| Hβ | 4862.7 | 4860.0 | em | both | — |
| Hβ_abs | 4862.7 | 4860.0 | abs | absorption | — |
| [O III]a | 4960.3 | 4957.5 | em | narrow | — |
| [O III]b | 5008.2 | 5005.4 | em | narrow | — |
| Mg I_abs | 5176.7 | 5173.8 | abs | absorption | — |
| Na D1_abs | 5891.6 | 5888.3 | abs | absorption | — |
| Na D_abs | 5895.6 | 5892.3 | abs | absorption | — |
| Na D2_abs | 5897.6 | 5894.3 | abs | absorption | — |
| [N II]a | 6549.8 | 6546.1 | em | narrow | — |
| Hα | 6564.6 | 6560.9 | em | both | — |
| Hα_abs | 6564.6 | 6560.9 | abs | absorption | — |
| [N II]b | 6585.3 | 6581.6 | em | narrow | — |
| [S II]a | 6718.3 | 6714.5 | em | narrow | — |
| [S II]b | 6732.7 | 6728.9 | em | narrow | — |
| CaT1_abs | 8498.0 | 8493.2 | abs | absorption | trough@8468.0±0.8(z=-0.0035) |
| CaT2_abs | 8542.0 | 8537.2 | abs | absorption | trough@8468.0±0.8(z=-0.0087) |
| CaT3_abs | 8662.0 | 8657.1 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 4957.5/5005.4 | fit_doublet | 4907.521±0.0/5035.365±0.0 | 0.0/0.0 | 144.0/140.2 | 0.0 | -0.0 | warning; separation fail; component ratio — |
| [S II]a/[S II]b | 6714.5/6728.9 | fit_doublet | 6664.534±0.0/6678.925±0.0 | 0.0/0.0 | 2107.8/1388.3 | 0.0 | -0.0 | ok; separation pass; component ratio — |
| [N II]a/[N II]b | 6546.1/6581.6 | fit_doublet | 6526.799±5.5106/6579.837±0.0 | 0.098012/0.0 | 2294.3/22763.4 | 0.85 | 0.045 | warning; separation fail; component ratio 0.0 |
| Ca K_abs/Ca H_abs | 3932.6/3967.4 | fit_doublet | 3931.78±2.9232/3977.4±0.9861 | -0.441897/-0.634553 | 1184.2/274.7 | 1.33 | 0.025 | warning; separation fail |
| Na D1_abs/Na D2_abs | 5888.3/5894.3 | fit_doublet | 5852.339±3.0248/5921.026±6.3903 | -0.215965/-0.421247 | 385.2/5511.4 | 1.82 | 0.507 | warning; separation fail; component ratio 1.95 |
| [O II] | 3724.9 | fit_peak | 3759.688±0.0 | 0.0 | 28011.9 | 0.0 | -0.0 | ok |
| Hε | 3967.9 | fit_peak | 4017.874±475.0303 | 0.317698 | 35140.8 | 0.72 | 0.37 | warning: center_at_bound |
| Hδ | 4100.6 | fit_peak | 4057.877±2.5426 | 0.649659 | 3479.7 | 1.74 | 0.269 | ok |
| Hγ | 4339.3 | fit_peak | 4327.332±0.6322 | 0.532864 | 163.1 | 1.61 | 0.011 | ok |
| Hβ | 4860.0 | fit_peak | 4809.973±4.525 | 1.900471 | 8766.7 | 5.79 | 8.886 | warning: center_at_bound |
| Hα | 6560.9 | fit_peak | 6530.296±4.7245 | 0.101724 | 2261.5 | 0.95 | 0.084 | ok |
| Hε_abs | 3967.9 | fit_peak | 3949.957±10.2182 | -0.228709 | 4855.5 | 0.49 | 0.028 | ok |
| Hδ_abs | 4100.6 | fit_peak | 4074.691±0.0 | -0.0 | 173.3 | 0.0 | 0.0 | ok |
| G-band_abs | 4303.2 | fit_peak | 4299.401±1.1352 | -0.328725 | 197.4 | 0.97 | 0.005 | ok |
| Hγ_abs | 4339.3 | fit_peak | 4347.434±2.2271 | -0.362258 | 946.2 | 1.1 | 0.031 | ok |
| Hβ_abs | 4860.0 | fit_peak | 4909.973±16.8638 | -0.319906 | 3866.5 | 0.62 | 0.045 | warning: center_at_bound |
| Mg I_abs | 5173.8 | fit_peak | 5193.639±7.3568 | -0.062967 | 1712.5 | 0.49 | 0.013 | ok |
| Hα_abs | 6560.9 | fit_peak | 6610.795±1.1728 | -0.091715 | 106.8 | 0.84 | 0.003 | ok |
| CaT3_abs | 8657.1 | fit_peak | 8631.968±10.8843 | -0.070615 | 1001.9 | 0.76 | 0.031 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:oii-3727 | [O II] | 3724.9 | emission |
| line:cak-3934-abs | Ca K_abs | 3932.6 | absorption |
| line:cah-3969-abs | Ca H_abs | 3967.4 | absorption |
| line:heps-3970 | Hε | 3967.9 | emission |
| line:heps-3970-abs | Hε_abs | 3967.9 | absorption |
| line:hdel-4102 | Hδ | 4100.6 | emission |
| line:hdel-4102-abs | Hδ_abs | 4100.6 | absorption |
| line:gband-4305-abs | G-band_abs | 4303.2 | absorption |
| line:hgam-4341 | Hγ | 4339.3 | emission |
| line:hgam-4341-abs | Hγ_abs | 4339.3 | absorption |
| line:hbet-4862 | Hβ | 4860.0 | emission |
| line:hbet-4862-abs | Hβ_abs | 4860.0 | absorption |
| line:oiii-4960 | [O III]a | 4957.5 | emission |
| line:oiii-5008 | [O III]b | 5005.4 | emission |
| line:mgi-5176-abs | Mg I_abs | 5173.8 | absorption |
| line:nad1-5891-abs | Na D1_abs | 5888.3 | absorption |
| line:nad-5895-abs | Na D_abs | 5892.3 | absorption |
| line:nad2-5897-abs | Na D2_abs | 5894.3 | absorption |
| line:nii-6549 | [N II]a | 6546.1 | emission |
| line:half-6564 | Hα | 6560.9 | emission |
| line:half-6564-abs | Hα_abs | 6560.9 | absorption |
| line:nii-6585 | [N II]b | 6581.6 | emission |
| line:sii-6718 | [S II]a | 6714.5 | emission |
| line:sii-6732 | [S II]b | 6728.9 | emission |
| line:cat1-8498-abs | CaT1_abs | 8493.2 | absorption |
| line:cat2-8542-abs | CaT2_abs | 8537.2 | absorption |
| line:cat3-8662-abs | CaT3_abs | 8657.1 | absorption |

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
| fit:H3:0000 | fit_doublet | emission | 4907.521 | [O III]a | yes | — |
| fit:H3:0001 | fit_doublet | emission | 5035.365 | [O III]b | yes | — |
| fit:H3:0002 | fit_doublet | emission | 6664.534 | [S II]a | yes | — |
| fit:H3:0003 | fit_doublet | emission | 6678.925 | [S II]b | yes | — |
| fit:H3:0004 | fit_doublet | emission | 6526.799 | [N II]a | yes | — |
| fit:H3:0005 | fit_doublet | emission | 6579.837 | [N II]b | yes | — |
| fit:H3:0006 | fit_doublet | absorption | 3931.780 | Ca K_abs | yes | — |
| fit:H3:0007 | fit_doublet | absorption | 3977.400 | Ca H_abs | yes | — |
| fit:H3:0008 | fit_doublet | absorption | 5852.339 | Na D1_abs | yes | — |
| fit:H3:0009 | fit_doublet | absorption | 5921.026 | Na D2_abs | yes | — |
| fit:H3:0010 | fit_peak | emission | 3759.688 | [O II] | yes | — |
| fit:H3:0011 | fit_peak | emission | 4017.874 | Hε | no | center_at_bound |
| fit:H3:0012 | fit_peak | emission | 4057.877 | Hδ | yes | — |
| fit:H3:0013 | fit_peak | emission | 4327.332 | Hγ | yes | — |
| fit:H3:0014 | fit_peak | emission | 4809.973 | Hβ | no | center_at_bound |
| fit:H3:0015 | fit_peak | emission | 6530.296 | Hα | yes | — |
| fit:H3:0016 | fit_peak | absorption | 3949.957 | Hε_abs | yes | — |
| fit:H3:0017 | fit_peak | absorption | 4074.691 | Hδ_abs | yes | — |
| fit:H3:0018 | fit_peak | absorption | 4299.401 | G-band_abs | yes | — |
| fit:H3:0019 | fit_peak | absorption | 4347.434 | Hγ_abs | yes | — |
| fit:H3:0020 | fit_peak | absorption | 4909.973 | Hβ_abs | no | center_at_bound |
| fit:H3:0021 | fit_peak | absorption | 5193.639 | Mg I_abs | yes | — |
| fit:H3:0022 | fit_peak | absorption | 6610.795 | Hα_abs | yes | — |
| fit:H3:0023 | fit_peak | absorption | 8631.968 | CaT3_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H3/pre_analysis/branches/main/e6e35209332e4719b84c5fc64b1ca55c/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_offset_large",
            "blue_edge"
          ],
          "comment": "No CWT peak near 3724.9; fit_peak centre 3759.7 is 35 A off with zero amplitude and huge width, not credible. Blue edge region."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H3:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "doublet_separation_fail",
            "blend_cah"
          ],
          "comment": "Doublet fit centre 3931.8 close to prediction (offset ~0.8 A) but separation fails and Ca H component lands at 3977.4; low local SNR 1.33. Plausible weak Ca K retained as marginal."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H3:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "doublet_separation_fail",
            "blend_cak_heps"
          ],
          "comment": "Ca H fit centre 3977.4 is ~10 A red of prediction, separation fails, and region blends with Hepsilon/Hepsilon_abs. Weak depth ordering uncertain; retained as marginal."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature",
            "blend_cah"
          ],
          "comment": "Only fit is center_at_bound (4017.9) and unselectable; no CWT peak near 3967.9. Blended with Ca H region."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H3:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "blend_cah"
          ],
          "comment": "Absorption fit centre 3950.0 is ~18 A blue of prediction with low SNR 0.49 and very broad width; weak and blended with Ca H. Marginal."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H3:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit centre 4057.9 is ~43 A blue of prediction, low SNR 1.74, FWHM ~3480 km/s. Weak offset candidate, marginal."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Fit returned zero amplitude at 4074.7; no credible absorption measurement."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H3:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit centre 4299.4 within ~4 A of prediction, but low SNR 0.97 and shallow depth. Marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H3:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "narrow_width"
          ],
          "comment": "Fit centre 4327.3 is ~12 A blue of prediction, SNR 1.61, FWHM 163 km/s (narrower than broad guide). Marginal."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H3:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Absorption fit centre 4347.4 is ~8 A red of prediction, low SNR 1.1, broad width. Marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Only fit is center_at_bound (4810.0) and unselectable; no CWT peak near 4860. No credible measurement."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Fit center_at_bound (4910.0) unselectable; no credible absorption measurement."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit gave zero amplitude at 4907.5 with separation fail; no CWT peak near 4957.5. Not credible."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit zero amplitude at 5035.4, separation fail; no CWT peak near 5005.4. Not credible."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H3:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 5193.6 is ~20 A red of prediction, SNR 0.49, very broad. Weak marginal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H3:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "weak_snr"
          ],
          "comment": "Na D doublet fit centre 5852.3 is ~36 A blue of prediction, separation fails, low SNR 1.82. Marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "doublet_separation_fail"
          ],
          "comment": "No dedicated measurement for the blended Na D central component; doublet fit separation failed. No adopted measurement."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H3:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 5921.0 is ~27 A red of prediction with FWHM ~5500 km/s and separation fail. Weak marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H3:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "weak_snr",
            "blend_halpha"
          ],
          "comment": "Fit centre 6526.8 is ~19 A blue of prediction, separation fails, SNR 0.85; blended with Halpha region. Marginal."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H3:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "blend_nii"
          ],
          "comment": "Fit centre 6530.3 is ~31 A blue of prediction, SNR 0.95, broad width; blended with [N II]. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H3:0022",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "narrow_width"
          ],
          "comment": "Absorption fit centre 6610.8 is ~50 A red of prediction, SNR 0.84, narrow. Weak marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H3:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "blend_halpha"
          ],
          "comment": "Fit centre 6579.8 near prediction but amplitude zero and separation fail; blended with Halpha. Marginal at best."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H3:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width",
            "weak_snr"
          ],
          "comment": "Doublet fit centre 6664.5 is ~50 A blue of prediction with FWHM ~2100 km/s; separation passes but offset weak. Marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "fit:H3:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width",
            "weak_snr"
          ],
          "comment": "Doublet fit centre 6678.9 is ~50 A blue of prediction, broad width; separation passes but offset weak. Marginal."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "offset_large",
            "red_edge"
          ],
          "comment": "No targeted fit; nearest CWT trough 8468.0 implies z=-0.0035, ~25 A off and outside tight tolerance. No adopted measurement."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "offset_large",
            "red_edge"
          ],
          "comment": "No targeted fit; nearest CWT trough 8468.0 implies z=-0.0087, ~69 A off. No adopted measurement."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H3:0023",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "red_edge"
          ],
          "comment": "Fit centre 8632.0 is ~25 A blue of prediction, SNR 0.76, broad; red edge. Weak marginal."
        }
      ]
    },
    "id": "call_00_EpNGRPRxNdBY1hfOeihx8992",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 7333,
  "output_tokens": 2540,
  "total_tokens": 9873,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 6693,
  "provider_usage": {
    "completion_tokens": 2540,
    "prompt_tokens": 7333,
    "total_tokens": 9873,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 6693
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_EpNGRPRxNdBY1hfOeihx8992`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 5, "line_id": "line:hdel-4102", "measurement_id": "fit:H3:0012", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
The Hδ fit centre (4057.9 Å) falls outside the redshift window. I'll repair that row and resubmit the full set.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H3/pre_analysis/branches/main/e6e35209332e4719b84c5fc64b1ca55c/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_offset_large",
            "blue_edge"
          ],
          "comment": "No CWT peak near 3724.9; fit_peak centre 3759.7 is 35 A off with zero amplitude and huge width, not credible. Blue edge region."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H3:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "doublet_separation_fail",
            "blend_cah"
          ],
          "comment": "Doublet fit centre 3931.8 close to prediction (offset ~0.8 A) but separation fails and Ca H component lands at 3977.4; low local SNR 1.33. Plausible weak Ca K retained as marginal."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H3:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "doublet_separation_fail",
            "blend_cak_heps"
          ],
          "comment": "Ca H fit centre 3977.4 is ~10 A red of prediction, separation fails, and region blends with Hepsilon/Hepsilon_abs. Weak depth ordering uncertain; retained as marginal."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature",
            "blend_cah"
          ],
          "comment": "Only fit is center_at_bound (4017.9) and unselectable; no CWT peak near 3967.9. Blended with Ca H region."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H3:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "blend_cah"
          ],
          "comment": "Absorption fit centre 3950.0 is ~18 A blue of prediction with low SNR 0.49 and very broad width; weak and blended with Ca H. Marginal."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_large",
            "weak_snr",
            "broad_width"
          ],
          "comment": "Only fit centre 4057.9 is ~43 A blue of prediction, outside the redshift window and unselectable; low SNR and broad. No adopted measurement."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Fit returned zero amplitude at 4074.7; no credible absorption measurement."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H3:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit centre 4299.4 within ~4 A of prediction, but low SNR 0.97 and shallow depth. Marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H3:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "narrow_width"
          ],
          "comment": "Fit centre 4327.3 is ~12 A blue of prediction, SNR 1.61, FWHM 163 km/s (narrower than broad guide). Marginal."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H3:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Absorption fit centre 4347.4 is ~8 A red of prediction, low SNR 1.1, broad width. Marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Only fit is center_at_bound (4810.0) and unselectable; no CWT peak near 4860. No credible measurement."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Fit center_at_bound (4910.0) unselectable; no credible absorption measurement."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit gave zero amplitude at 4907.5 with separation fail; no CWT peak near 4957.5. Not credible."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit zero amplitude at 5035.4, separation fail; no CWT peak near 5005.4. Not credible."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H3:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 5193.6 is ~20 A red of prediction, SNR 0.49, very broad. Weak marginal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H3:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "weak_snr"
          ],
          "comment": "Na D doublet fit centre 5852.3 is ~36 A blue of prediction, separation fails, low SNR 1.82. Marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "doublet_separation_fail"
          ],
          "comment": "No dedicated measurement for the blended Na D central component; doublet fit separation failed. No adopted measurement."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H3:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 5921.0 is ~27 A red of prediction with FWHM ~5500 km/s and separation fail. Weak marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H3:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "weak_snr",
            "blend_halpha"
          ],
          "comment": "Fit centre 6526.8 is ~19 A blue of prediction, separation fails, SNR 0.85; blended with Halpha region. Marginal."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H3:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "blend_nii"
          ],
          "comment": "Fit centre 6530.3 is ~31 A blue of prediction, SNR 0.95, broad width; blended with [N II]. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H3:0022",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "narrow_width"
          ],
          "comment": "Absorption fit centre 6610.8 is ~50 A red of prediction, SNR 0.84, narrow. Weak marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H3:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "blend_halpha"
          ],
          "comment": "Fit centre 6579.8 near prediction but amplitude zero and separation fail; blended with Halpha. Marginal at best."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H3:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width",
            "weak_snr"
          ],
          "comment": "Doublet fit centre 6664.5 is ~50 A blue of prediction with FWHM ~2100 km/s; separation passes but offset weak. Marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "fit:H3:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width",
            "weak_snr"
          ],
          "comment": "Doublet fit centre 6678.9 is ~50 A blue of prediction, broad width; separation passes but offset weak. Marginal."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "offset_large",
            "red_edge"
          ],
          "comment": "No targeted fit; nearest CWT trough 8468.0 implies z=-0.0035, ~25 A off and outside tight tolerance. No adopted measurement."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "offset_large",
            "red_edge"
          ],
          "comment": "No targeted fit; nearest CWT trough 8468.0 implies z=-0.0087, ~69 A off. No adopted measurement."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H3:0023",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "red_edge"
          ],
          "comment": "Fit centre 8632.0 is ~25 A blue of prediction, SNR 0.76, broad; red edge. Weak marginal."
        }
      ]
    },
    "id": "call_00_PpTAjNtLSP7hVAGqAg9e7343",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 9977,
  "output_tokens": 2542,
  "total_tokens": 12519,
  "cache_hit_tokens": 9728,
  "cache_miss_tokens": 249,
  "provider_usage": {
    "completion_tokens": 2542,
    "prompt_tokens": 9977,
    "total_tokens": 12519,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 9728
    },
    "prompt_cache_hit_tokens": 9728,
    "prompt_cache_miss_tokens": 249
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_PpTAjNtLSP7hVAGqAg9e7343`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H3/pre_analysis/branches/main/e6e35209332e4719b84c5fc64b1ca55c/lines.csv", "n_lines": 27, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H3/pre_analysis/branches/main/e6e35209332e4719b84c5fc64b1ca55c/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:45:01.394050+00:00
