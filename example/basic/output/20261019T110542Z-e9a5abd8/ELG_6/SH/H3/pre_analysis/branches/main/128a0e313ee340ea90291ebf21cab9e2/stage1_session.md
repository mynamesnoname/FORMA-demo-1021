# SH pre-analysis session: line review

- Run ID: `graph-fe0d30030bcc4939b88103e27753b2c1`
- Hypothesis: `H3`
- Started (UTC): 2026-10-19T11:18:35.572843+00:00
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
Review every predicted line at the fixed Redrock redshift `0.00016506965303596808`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H3/pre_analysis/branches/main/128a0e313ee340ea90291ebf21cab9e2/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 5.3 |

Verify the redshift hypothesis z ≈ 0.00016506965303596808.

Verification window: z ∈ [-0.0098, 0.0102]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=47.9079, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=14.4024, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=35.5059, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=34.8057, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=6.00099, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/ELG_6.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H3/pre_analysis/branches/main/128a0e313ee340ea90291ebf21cab9e2/lines.csv

## CWT Detected Features

### Emission (peaks) — 20 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 4127.2 | 0.8 | 8.4 | 16.9 | 1229 | 24 | 88.2 |
| 4283.2 | 0.8 | 3.7 | 9.6 | 669 | 18 | 16.5 |
| 4305.6 | 0.8 | 2.3 | 3.7 | 257 | 6 | 10.0 |
| 4540.8 | 0.8 | 2.8 | 5.4 | 356 | 12 | 16.6 |
| 4653.6 | 0.8 | 1.8 | 3.0 | 196 | 4 | 9.1 |
| 4805.6 | 0.8 | 4.6 | 12.7 | 790 | 21 | 30.3 |
| 5381.6 | 0.8 | 10.7 | 14.0 | 779 | 22 | 91.9 |
| 5489.6 | 0.8 | 12.3 | 9.6 | 522 | 18 | 82.7 |
| 5543.2 | 0.8 | 43.4 | 16.9 | 915 | 24 | 267.5 |
| 5545.6 | 0.8 | 0.6 | 103.0 | 5566 | 5 | 77.8 |
| 6504.8 | 0.8 | 1.3 | 9.6 | 440 | 16 | 13.6 |
| 6975.2 | 0.8 | 0.9 | 5.4 | 232 | 10 | 12.5 |
| 7265.6 | 0.8 | 38.3 | 16.9 | 698 | 24 | 327.1 |
| 7288.8 | 0.8 | 1.9 | 5.4 | 222 | 12 | 18.0 |
| 7436.0 | 0.8 | 4.2 | 15.3 | 618 | 23 | 43.4 |
| 7452.0 | 0.8 | 3.1 | 5.9 | 238 | 13 | 31.5 |
| 8830.4 | 0.8 | 1.2 | 2.8 | 94 | 5 | 12.4 |
| 8888.8 | 0.8 | 0.7 | 4.5 | 150 | 10 | 9.9 |
| 9440.8 | 0.8 | 0.8 | 3.3 | 106 | 7 | 12.0 |
| 9477.6 | 0.8 | 0.3 | 2.8 | 87 | 5 | 10.0 |

### Absorption (troughs) — 27 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 4119.2 | 0.8 | -0.2 | 9.6 | 696 | 18 | 44.9 |
| 4139.2 | 0.8 | -0.4 | 15.3 | 1109 | 17 | 41.3 |
| 4801.6 | 0.8 | -0.4 | 4.5 | 278 | 10 | 14.1 |
| 4812.8 | 0.8 | -0.3 | 9.6 | 595 | 6 | 12.0 |
| 5372.8 | 0.8 | -0.0 | 11.6 | 645 | 20 | 43.3 |
| 5393.6 | 0.8 | -0.2 | 15.3 | 851 | 11 | 35.2 |
| 5442.4 | 0.8 | -0.1 | 94.0 | 5179 | 6 | 44.1 |
| 5456.0 | 0.8 | -0.2 | 113.8 | 6251 | 4 | 31.2 |
| 5482.4 | 0.8 | -0.1 | 9.6 | 523 | 18 | 37.4 |
| 5498.4 | 0.8 | -0.1 | 11.6 | 630 | 8 | 37.3 |
| 5535.2 | 0.8 | -0.1 | 10.5 | 567 | 19 | 118.2 |
| 5555.2 | 0.8 | -0.2 | 15.3 | 827 | 11 | 117.7 |
| 5603.2 | 0.8 | -0.0 | 85.1 | 4553 | 7 | 45.6 |
| 7190.4 | 0.8 | -0.0 | 103.0 | 4293 | 5 | 72.8 |
| 7204.0 | 0.8 | -0.1 | 94.0 | 3913 | 6 | 63.0 |
| 7256.8 | 0.8 | -0.0 | 11.6 | 478 | 20 | 141.7 |
| 7285.6 | 0.8 | -0.1 | 3.7 | 152 | 4 | 8.7 |
| 7288.0 | 0.8 | -1.8 | 30.0 | 1233 | 18 | 131.1 |
| 7428.0 | 0.8 | -0.1 | 9.6 | 386 | 18 | 18.3 |
| 7447.2 | 0.8 | -0.0 | 5.9 | 238 | 11 | 30.5 |
| 7463.2 | 0.8 | -0.0 | 15.3 | 615 | 11 | 13.8 |
| 7492.0 | 0.8 | -0.0 | 64.2 | 2570 | 4 | 14.3 |
| 9004.0 | 0.8 | -0.3 | 2.5 | 84 | 4 | 9.0 |
| 9442.4 | 0.8 | -2.9 | 4.5 | 142 | 10 | 21.6 |
| 9452.0 | 0.8 | -0.0 | 113.8 | 3608 | 4 | 9.6 |
| 9462.4 | 0.8 | -1.0 | 3.3 | 106 | 7 | 10.4 |
| 9480.8 | 0.8 | -2.0 | 3.3 | 106 | 7 | 13.5 |


## Predicted Lines at z = 0.0002

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [O II] | 3727.0 | 3727.6 | em | narrow | — |
| Ca K_abs | 3934.8 | 3935.4 | abs | absorption | — |
| Ca H_abs | 3969.6 | 3970.3 | abs | absorption | — |
| Hε | 3970.1 | 3970.8 | em | both | — |
| Hε_abs | 3970.1 | 3970.8 | abs | absorption | — |
| Hδ | 4102.9 | 4103.6 | em | both | peak@4127.2±0.8(z=0.0059) |
| Hδ_abs | 4102.9 | 4103.6 | abs | absorption | trough@4119.2±0.8(z=0.0040), trough@4139.2±0.8(z=0.0088) |
| G-band_abs | 4305.6 | 4306.3 | abs | absorption | — |
| Hγ | 4341.7 | 4342.4 | em | both | peak@4305.6±0.8(z=-0.0083) |
| Hγ_abs | 4341.7 | 4342.4 | abs | absorption | — |
| Hβ | 4862.7 | 4863.5 | em | both | — |
| Hβ_abs | 4862.7 | 4863.5 | abs | absorption | — |
| [O III]a | 4960.3 | 4961.1 | em | narrow | — |
| [O III]b | 5008.2 | 5009.0 | em | narrow | — |
| Mg I_abs | 5176.7 | 5177.6 | abs | absorption | — |
| Na D1_abs | 5891.6 | 5892.6 | abs | absorption | — |
| Na D_abs | 5895.6 | 5896.6 | abs | absorption | — |
| Na D2_abs | 5897.6 | 5898.6 | abs | absorption | — |
| [N II]a | 6549.8 | 6550.9 | em | narrow | peak@6504.8±0.8(z=-0.0069) |
| Hα | 6564.6 | 6565.7 | em | both | peak@6504.8±0.8(z=-0.0091) |
| Hα_abs | 6564.6 | 6565.7 | abs | absorption | — |
| [N II]b | 6585.3 | 6586.4 | em | narrow | — |
| [S II]a | 6718.3 | 6719.4 | em | narrow | — |
| [S II]b | 6732.7 | 6733.8 | em | narrow | — |
| CaT1_abs | 8498.0 | 8499.4 | abs | absorption | — |
| CaT2_abs | 8542.0 | 8543.4 | abs | absorption | — |
| CaT3_abs | 8662.0 | 8663.4 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 4961.1/5009.0 | fit_doublet | 4950.074±0.7062/5013.631±0.0 | 0.384133/0.0 | 142.6/1327.8 | 2.36 | 0.017 | warning; separation fail; component ratio 0.0 |
| [S II]a/[S II]b | 6719.4/6733.8 | fit_doublet | 6718.204±0.0/6737.197±2.3074 | 0.0/0.050901 | 875.7/104.8 | 0.59 | 0.001 | ok; separation pass; component ratio — |
| [N II]a/[N II]b | 6550.9/6586.4 | fit_doublet | 6504.894±0.0775/6604.158±12.5229 | 1.195602/0.019582 | 108.5/749.1 | 12.98 | 0.499 | warning; separation fail; component ratio 0.02 |
| Ca K_abs/Ca H_abs | 3935.4/3970.3 | fit_doublet | 3948.738±3.4848/3985.02±25.4917 | -0.336776/-0.362185 | 178.8/9875.0 | 0.96 | 0.161 | ok; separation pass |
| Na D1_abs/Na D2_abs | 5892.6/5898.6 | fit_doublet | 5843.636±0.0/5900.398±0.8005 | -0.0/-0.185753 | 36241.1/155.2 | 1.52 | 0.009 | warning; separation fail; component ratio — |
| [O II] | 3727.6 | fit_peak | 3716.652±1.0301 | 0.676947 | 328.2 | 1.56 | 0.023 | ok |
| Hε | 3970.8 | fit_peak | 3920.758±0.0 | 0.0 | 180.1 | 0.0 | -0.0 | warning: center_at_bound |
| Hβ | 4863.5 | fit_peak | 4813.503±3.3226 | 0.331163 | 1822.3 | 1.94 | 0.206 | warning: center_at_bound |
| Hε_abs | 3970.8 | fit_peak | 4016.995±18.9827 | -0.693747 | 10196.3 | 1.6 | 0.658 | ok |
| G-band_abs | 4306.3 | fit_peak | 4256.311±46.5592 | -0.978561 | 16486.0 | 2.74 | 3.244 | warning: center_at_bound |
| Hγ_abs | 4342.4 | fit_peak | 4392.415±0.0 | -0.0 | 32143.4 | 0.0 | -0.0 | warning: center_at_bound |
| Hβ_abs | 4863.5 | fit_peak | 4854.395±1.8848 | -0.196898 | 196.8 | 1.18 | 0.008 | ok |
| Mg I_abs | 5177.6 | fit_peak | 5220.682±0.0 | -0.0 | 19603.3 | 0.0 | -0.0 | ok |
| Hα_abs | 6565.7 | fit_peak | 6573.701±2.7033 | -0.090989 | 494.8 | 1.02 | 0.021 | ok |
| CaT1_abs | 8499.4 | fit_peak | 8483.982±3.9544 | -0.069435 | 397.3 | 0.76 | 0.012 | ok |
| CaT2_abs | 8543.4 | fit_peak | 8539.594±1.115 | -0.109007 | 82.7 | 1.26 | 0.007 | ok |
| CaT3_abs | 8663.4 | fit_peak | 8713.43±14.264 | -0.039398 | 1431.2 | 0.48 | 0.018 | warning: center_at_bound |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:oii-3727 | [O II] | 3727.6 | emission |
| line:cak-3934-abs | Ca K_abs | 3935.4 | absorption |
| line:cah-3969-abs | Ca H_abs | 3970.3 | absorption |
| line:heps-3970 | Hε | 3970.8 | emission |
| line:heps-3970-abs | Hε_abs | 3970.8 | absorption |
| line:hdel-4102 | Hδ | 4103.6 | emission |
| line:hdel-4102-abs | Hδ_abs | 4103.6 | absorption |
| line:gband-4305-abs | G-band_abs | 4306.3 | absorption |
| line:hgam-4341 | Hγ | 4342.4 | emission |
| line:hgam-4341-abs | Hγ_abs | 4342.4 | absorption |
| line:hbet-4862 | Hβ | 4863.5 | emission |
| line:hbet-4862-abs | Hβ_abs | 4863.5 | absorption |
| line:oiii-4960 | [O III]a | 4961.1 | emission |
| line:oiii-5008 | [O III]b | 5009.0 | emission |
| line:mgi-5176-abs | Mg I_abs | 5177.6 | absorption |
| line:nad1-5891-abs | Na D1_abs | 5892.6 | absorption |
| line:nad-5895-abs | Na D_abs | 5896.6 | absorption |
| line:nad2-5897-abs | Na D2_abs | 5898.6 | absorption |
| line:nii-6549 | [N II]a | 6550.9 | emission |
| line:half-6564 | Hα | 6565.7 | emission |
| line:half-6564-abs | Hα_abs | 6565.7 | absorption |
| line:nii-6585 | [N II]b | 6586.4 | emission |
| line:sii-6718 | [S II]a | 6719.4 | emission |
| line:sii-6732 | [S II]b | 6733.8 | emission |
| line:cat1-8498-abs | CaT1_abs | 8499.4 | absorption |
| line:cat2-8542-abs | CaT2_abs | 8543.4 | absorption |
| line:cat3-8662-abs | CaT3_abs | 8663.4 | absorption |

| Measurement ID | Source | Kind | Centre (Å) | Target | Selectable | Flags |
|---|---|---|---:|---|---|---|
| cwt:em:0000 | CWT | emission | 4127.200 | — | yes | — |
| cwt:em:0001 | CWT | emission | 4283.200 | — | yes | — |
| cwt:em:0002 | CWT | emission | 4305.600 | — | yes | — |
| cwt:em:0003 | CWT | emission | 4540.800 | — | yes | — |
| cwt:em:0004 | CWT | emission | 4653.600 | — | yes | — |
| cwt:em:0005 | CWT | emission | 4805.600 | — | yes | — |
| cwt:em:0006 | CWT | emission | 5381.600 | — | yes | — |
| cwt:em:0007 | CWT | emission | 5489.600 | — | yes | — |
| cwt:em:0008 | CWT | emission | 5543.200 | — | yes | — |
| cwt:em:0009 | CWT | emission | 5545.600 | — | yes | — |
| cwt:em:0010 | CWT | emission | 6504.800 | — | yes | — |
| cwt:em:0011 | CWT | emission | 6975.200 | — | yes | — |
| cwt:em:0012 | CWT | emission | 7265.600 | — | yes | — |
| cwt:em:0013 | CWT | emission | 7288.800 | — | yes | — |
| cwt:em:0014 | CWT | emission | 7436.000 | — | yes | — |
| cwt:em:0015 | CWT | emission | 7452.000 | — | yes | — |
| cwt:em:0016 | CWT | emission | 8830.400 | — | yes | — |
| cwt:em:0017 | CWT | emission | 8888.800 | — | yes | — |
| cwt:em:0018 | CWT | emission | 9440.800 | — | yes | — |
| cwt:em:0019 | CWT | emission | 9477.600 | — | yes | — |
| cwt:abs:0000 | CWT | absorption | 4119.200 | — | yes | — |
| cwt:abs:0001 | CWT | absorption | 4139.200 | — | yes | — |
| cwt:abs:0002 | CWT | absorption | 4801.600 | — | yes | — |
| cwt:abs:0003 | CWT | absorption | 4812.800 | — | yes | — |
| cwt:abs:0004 | CWT | absorption | 5372.800 | — | yes | — |
| cwt:abs:0005 | CWT | absorption | 5393.600 | — | yes | — |
| cwt:abs:0006 | CWT | absorption | 5442.400 | — | yes | — |
| cwt:abs:0007 | CWT | absorption | 5456.000 | — | yes | — |
| cwt:abs:0008 | CWT | absorption | 5482.400 | — | yes | — |
| cwt:abs:0009 | CWT | absorption | 5498.400 | — | yes | — |
| cwt:abs:0010 | CWT | absorption | 5535.200 | — | yes | — |
| cwt:abs:0011 | CWT | absorption | 5555.200 | — | yes | — |
| cwt:abs:0012 | CWT | absorption | 5603.200 | — | yes | — |
| cwt:abs:0013 | CWT | absorption | 7190.400 | — | yes | — |
| cwt:abs:0014 | CWT | absorption | 7204.000 | — | yes | — |
| cwt:abs:0015 | CWT | absorption | 7256.800 | — | yes | — |
| cwt:abs:0016 | CWT | absorption | 7285.600 | — | yes | — |
| cwt:abs:0017 | CWT | absorption | 7288.000 | — | yes | — |
| cwt:abs:0018 | CWT | absorption | 7428.000 | — | yes | — |
| cwt:abs:0019 | CWT | absorption | 7447.200 | — | yes | — |
| cwt:abs:0020 | CWT | absorption | 7463.200 | — | yes | — |
| cwt:abs:0021 | CWT | absorption | 7492.000 | — | yes | — |
| cwt:abs:0022 | CWT | absorption | 9004.000 | — | yes | — |
| cwt:abs:0023 | CWT | absorption | 9442.400 | — | yes | — |
| cwt:abs:0024 | CWT | absorption | 9452.000 | — | yes | — |
| cwt:abs:0025 | CWT | absorption | 9462.400 | — | yes | — |
| cwt:abs:0026 | CWT | absorption | 9480.800 | — | yes | — |
| fit:H3:0000 | fit_doublet | emission | 4950.074 | [O III]a | yes | — |
| fit:H3:0001 | fit_doublet | emission | 5013.631 | [O III]b | yes | — |
| fit:H3:0002 | fit_doublet | emission | 6718.204 | [S II]a | yes | — |
| fit:H3:0003 | fit_doublet | emission | 6737.197 | [S II]b | yes | — |
| fit:H3:0004 | fit_doublet | emission | 6504.894 | [N II]a | yes | — |
| fit:H3:0005 | fit_doublet | emission | 6604.158 | [N II]b | yes | — |
| fit:H3:0006 | fit_doublet | absorption | 3948.738 | Ca K_abs | yes | — |
| fit:H3:0007 | fit_doublet | absorption | 3985.020 | Ca H_abs | yes | — |
| fit:H3:0008 | fit_doublet | absorption | 5843.636 | Na D1_abs | yes | — |
| fit:H3:0009 | fit_doublet | absorption | 5900.398 | Na D2_abs | yes | — |
| fit:H3:0010 | fit_peak | emission | 3716.652 | [O II] | yes | — |
| fit:H3:0011 | fit_peak | emission | 3920.758 | Hε | no | center_at_bound |
| fit:H3:0012 | fit_peak | emission | 4813.503 | Hβ | no | center_at_bound |
| fit:H3:0013 | fit_peak | absorption | 4016.995 | Hε_abs | yes | — |
| fit:H3:0014 | fit_peak | absorption | 4256.311 | G-band_abs | no | center_at_bound |
| fit:H3:0015 | fit_peak | absorption | 4392.415 | Hγ_abs | no | center_at_bound |
| fit:H3:0016 | fit_peak | absorption | 4854.395 | Hβ_abs | yes | — |
| fit:H3:0017 | fit_peak | absorption | 5220.682 | Mg I_abs | yes | — |
| fit:H3:0018 | fit_peak | absorption | 6573.701 | Hα_abs | yes | — |
| fit:H3:0019 | fit_peak | absorption | 8483.982 | CaT1_abs | yes | — |
| fit:H3:0020 | fit_peak | absorption | 8539.594 | CaT2_abs | yes | — |
| fit:H3:0021 | fit_peak | absorption | 8713.430 | CaT3_abs | no | center_at_bound |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H3/pre_analysis/branches/main/128a0e313ee340ea90291ebf21cab9e2/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H3:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "edge_blue"
          ],
          "comment": "Fit centre 3716.7 vs pred 3727.6, offset ~11 A (weak band), low local SNR 1.6; blue edge, no CWT peak. Weak candidate only."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H3:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "offset_weak",
            "low_snr",
            "doublet_ratio_caveat"
          ],
          "comment": "Doublet fit centre 3948.7 vs 3935.4, offset ~13 A; Ca H partner poorly constrained (huge width). Plausible weak Ca K component retained despite uncertain depth ordering."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H3:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "unconstrained_width",
            "low_snr",
            "doublet_ratio_caveat"
          ],
          "comment": "Ca H fit centre 3985.0 with FWHM ~9900 km/s, essentially unconstrained; blended with H-epsilon region. Weak plausible component, depth ordering uncertain."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit",
            "blend"
          ],
          "comment": "Only fit is center_at_bound with zero amplitude; no credible CWT emission peak near 3970.8. Region blended with Ca H."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H3:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "unconstrained_width",
            "low_snr"
          ],
          "comment": "Fit centre 4017.0 vs 3970.8, offset ~46 A (weak band), FWHM ~10000 km/s unconstrained, local SNR 1.6. Weak marginal absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_fit",
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest CWT peak 4127.2 implies z=0.0059, offset ~24 A and no targeted fit; no credible emission at 4103.6."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_fit",
            "offset_reject",
            "blend"
          ],
          "comment": "Troughs at 4119.2/4139.2 imply z=0.0040/0.0088, offsets ~16-36 A; no targeted fit adopted. No credible H-delta absorption."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit",
            "edge_blue"
          ],
          "comment": "Only fit is center_at_bound at 4256.3 with huge width; CWT peak at 4305.6 is emission-like, not a G-band trough. No credible absorption."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_fit",
            "offset_reject"
          ],
          "comment": "Only nearby CWT peak 4305.6 implies z=-0.0083, offset ~37 A; no targeted fit. No credible H-gamma emission."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Fit center_at_bound at 4392.4 with zero amplitude; no credible absorption at 4342.4."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit",
            "blend"
          ],
          "comment": "Fit center_at_bound at 4813.5 with broad width; CWT peak 4805.6 is offset ~58 A. No credible H-beta emission."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "fit:H3:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blend"
          ],
          "comment": "Fit centre 4854.4 vs 4863.5, offset ~9 A, local SNR 1.2, weak amplitude; blended with nearby troughs. Weak marginal absorption."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "component_ratio_fail",
            "low_snr"
          ],
          "comment": "Doublet fit separation fail, component ratio 0.0, local SNR 2.4; centre 4950.1 offset ~11 A but partner unconstrained. No credible [O III]a."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "low_snr"
          ],
          "comment": "Doublet component amplitude 0.0 with separation fail; no credible [O III]b emission."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "failed_fit"
          ],
          "comment": "Fit centre 5220.7 with zero amplitude and huge width; no credible Mg I absorption."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "unconstrained_width"
          ],
          "comment": "Doublet fit separation fail, D1 amplitude 0.0 with FWHM ~36000 km/s; no credible Na D1 absorption."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_fit",
            "blend"
          ],
          "comment": "No targeted fit for the blended Na D centre; D1/D2 doublet failed. No credible measurement."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H3:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "blend",
            "low_snr"
          ],
          "comment": "D2 fit centre 5900.4 vs 5898.6, offset ~2 A, but doublet separation fail and D1 unconstrained; blended Na D complex. Weak marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H3:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "blend",
            "offset_weak"
          ],
          "comment": "Fit centre 6504.9 vs 6550.9, offset ~46 A (weak band); coincides with CWT peak 6504.8. Doublet separation fail, partner unconstrained. Ambiguous blend."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "cwt:em:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "blend",
            "no_fit"
          ],
          "comment": "CWT peak 6504.8 implies z=-0.0091, offset ~61 A from H-alpha; shared with [N II]a fit. Weak marginal, ambiguous blend."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H3:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blend"
          ],
          "comment": "Fit centre 6573.7 vs 6565.7, offset ~8 A, local SNR 1.0, weak amplitude; blended with H-alpha/[N II] region. Weak marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_reject",
            "low_snr"
          ],
          "comment": "Doublet partner fit centre 6604.2 vs 6586.4, offset ~18 A with tiny amplitude and separation fail; no credible [N II]b."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "low_snr"
          ],
          "comment": "Doublet fit S IIa amplitude 0.0 with FWHM ~876 km/s; local SNR 0.6. No credible [S II]a."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "fit:H3:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "low_snr",
            "doublet_ratio_caveat"
          ],
          "comment": "Fit centre 6737.2 vs 6733.8, offset ~3 A, but S IIa unconstrained (zero amplitude) and local SNR 0.6; separation pass. Weak marginal."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": "fit:H3:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "edge_red"
          ],
          "comment": "Fit centre 8484.0 vs 8499.4, offset ~15 A, local SNR 0.8, weak amplitude; red edge. Weak marginal."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H3:0020",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "edge_red"
          ],
          "comment": "Fit centre 8539.6 vs 8543.4, offset ~4 A, narrow width, local SNR 1.3; red edge. Weak marginal."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit",
            "edge_red"
          ],
          "comment": "Fit center_at_bound at 8713.4 with tiny amplitude and huge width; no credible CaT3 absorption."
        }
      ]
    },
    "id": "call_00_vAQkeSQFR0aZBAY2Tmvu0933",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 8094,
  "output_tokens": 2617,
  "total_tokens": 10711,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 7454,
  "provider_usage": {
    "completion_tokens": 2617,
    "prompt_tokens": 8094,
    "total_tokens": 10711,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 7454
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_vAQkeSQFR0aZBAY2Tmvu0933`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 4, "line_id": "line:heps-3970-abs", "measurement_id": "fit:H3:0013", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
The Hε_abs fit centre (4017.0 Å) falls outside the line's redshift window. I'll set that line to NOT_FOUND and resubmit.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H3/pre_analysis/branches/main/128a0e313ee340ea90291ebf21cab9e2/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H3:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "edge_blue"
          ],
          "comment": "Fit centre 3716.7 vs pred 3727.6, offset ~11 A (weak band), low local SNR 1.6; blue edge, no CWT peak. Weak candidate only."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H3:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "offset_weak",
            "low_snr",
            "doublet_ratio_caveat"
          ],
          "comment": "Doublet fit centre 3948.7 vs 3935.4, offset ~13 A; Ca H partner poorly constrained (huge width). Plausible weak Ca K component retained despite uncertain depth ordering."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H3:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "unconstrained_width",
            "low_snr",
            "doublet_ratio_caveat"
          ],
          "comment": "Ca H fit centre 3985.0 with FWHM ~9900 km/s, essentially unconstrained; blended with H-epsilon region. Weak plausible component, depth ordering uncertain."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit",
            "blend"
          ],
          "comment": "Only fit is center_at_bound with zero amplitude; no credible CWT emission peak near 3970.8. Region blended with Ca H."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "unconstrained_width",
            "low_snr"
          ],
          "comment": "Only fit centre 4017.0 lies outside the line redshift window (offset ~46 A) with unconstrained width and local SNR 1.6; no credible H-epsilon absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_fit",
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest CWT peak 4127.2 implies z=0.0059, offset ~24 A and no targeted fit; no credible emission at 4103.6."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_fit",
            "offset_reject",
            "blend"
          ],
          "comment": "Troughs at 4119.2/4139.2 imply z=0.0040/0.0088, offsets ~16-36 A; no targeted fit adopted. No credible H-delta absorption."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit",
            "edge_blue"
          ],
          "comment": "Only fit is center_at_bound at 4256.3 with huge width; CWT peak at 4305.6 is emission-like, not a G-band trough. No credible absorption."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_fit",
            "offset_reject"
          ],
          "comment": "Only nearby CWT peak 4305.6 implies z=-0.0083, offset ~37 A; no targeted fit. No credible H-gamma emission."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Fit center_at_bound at 4392.4 with zero amplitude; no credible absorption at 4342.4."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit",
            "blend"
          ],
          "comment": "Fit center_at_bound at 4813.5 with broad width; CWT peak 4805.6 is offset ~58 A. No credible H-beta emission."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "fit:H3:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blend"
          ],
          "comment": "Fit centre 4854.4 vs 4863.5, offset ~9 A, local SNR 1.2, weak amplitude; blended with nearby troughs. Weak marginal absorption."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "component_ratio_fail",
            "low_snr"
          ],
          "comment": "Doublet fit separation fail, component ratio 0.0, local SNR 2.4; centre 4950.1 offset ~11 A but partner unconstrained. No credible [O III]a."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "low_snr"
          ],
          "comment": "Doublet component amplitude 0.0 with separation fail; no credible [O III]b emission."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "failed_fit"
          ],
          "comment": "Fit centre 5220.7 with zero amplitude and huge width; no credible Mg I absorption."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "unconstrained_width"
          ],
          "comment": "Doublet fit separation fail, D1 amplitude 0.0 with FWHM ~36000 km/s; no credible Na D1 absorption."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_fit",
            "blend"
          ],
          "comment": "No targeted fit for the blended Na D centre; D1/D2 doublet failed. No credible measurement."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H3:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "blend",
            "low_snr"
          ],
          "comment": "D2 fit centre 5900.4 vs 5898.6, offset ~2 A, but doublet separation fail and D1 unconstrained; blended Na D complex. Weak marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H3:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "blend",
            "offset_weak"
          ],
          "comment": "Fit centre 6504.9 vs 6550.9, offset ~46 A (weak band); coincides with CWT peak 6504.8. Doublet separation fail, partner unconstrained. Ambiguous blend."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "cwt:em:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "blend",
            "no_fit"
          ],
          "comment": "CWT peak 6504.8 implies z=-0.0091, offset ~61 A from H-alpha; shared with [N II]a fit. Weak marginal, ambiguous blend."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H3:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blend"
          ],
          "comment": "Fit centre 6573.7 vs 6565.7, offset ~8 A, local SNR 1.0, weak amplitude; blended with H-alpha/[N II] region. Weak marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_reject",
            "low_snr"
          ],
          "comment": "Doublet partner fit centre 6604.2 vs 6586.4, offset ~18 A with tiny amplitude and separation fail; no credible [N II]b."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "low_snr"
          ],
          "comment": "Doublet fit S IIa amplitude 0.0 with FWHM ~876 km/s; local SNR 0.6. No credible [S II]a."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "fit:H3:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "low_snr",
            "doublet_ratio_caveat"
          ],
          "comment": "Fit centre 6737.2 vs 6733.8, offset ~3 A, but S IIa unconstrained (zero amplitude) and local SNR 0.6; separation pass. Weak marginal."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": "fit:H3:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "edge_red"
          ],
          "comment": "Fit centre 8484.0 vs 8499.4, offset ~15 A, local SNR 0.8, weak amplitude; red edge. Weak marginal."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H3:0020",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "edge_red"
          ],
          "comment": "Fit centre 8539.6 vs 8543.4, offset ~4 A, narrow width, local SNR 1.3; red edge. Weak marginal."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit",
            "edge_red"
          ],
          "comment": "Fit center_at_bound at 8713.4 with tiny amplitude and huge width; no credible CaT3 absorption."
        }
      ]
    },
    "id": "call_00_JeQTte5GxoivBDhtCSr62547",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 10818,
  "output_tokens": 2622,
  "total_tokens": 13440,
  "cache_hit_tokens": 10624,
  "cache_miss_tokens": 194,
  "provider_usage": {
    "completion_tokens": 2622,
    "prompt_tokens": 10818,
    "total_tokens": 13440,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 10624
    },
    "prompt_cache_hit_tokens": 10624,
    "prompt_cache_miss_tokens": 194
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_JeQTte5GxoivBDhtCSr62547`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H3/pre_analysis/branches/main/128a0e313ee340ea90291ebf21cab9e2/lines.csv", "n_lines": 27, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H3/pre_analysis/branches/main/128a0e313ee340ea90291ebf21cab9e2/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:18:53.591309+00:00
