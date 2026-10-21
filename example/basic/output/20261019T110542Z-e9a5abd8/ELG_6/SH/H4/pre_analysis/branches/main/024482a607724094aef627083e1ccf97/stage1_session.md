# SH pre-analysis session: line review

- Run ID: `graph-fe0d30030bcc4939b88103e27753b2c1`
- Hypothesis: `H4`
- Started (UTC): 2026-10-19T11:18:35.855680+00:00
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
Review every predicted line at the fixed Redrock redshift `0.00021988006120168826`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H4/pre_analysis/branches/main/024482a607724094aef627083e1ccf97/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 5.3 |

Verify the redshift hypothesis z ≈ 0.00021988006120168826.

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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=47.9105, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=14.4032, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=35.5078, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=34.8077, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=6.00132, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/ELG_6.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H4/pre_analysis/branches/main/024482a607724094aef627083e1ccf97/lines.csv

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
| [O II] | 3727.0 | 3727.8 | em | narrow | — |
| Ca K_abs | 3934.8 | 3935.7 | abs | absorption | — |
| Ca H_abs | 3969.6 | 3970.5 | abs | absorption | — |
| Hε | 3970.1 | 3971.0 | em | both | — |
| Hε_abs | 3970.1 | 3971.0 | abs | absorption | — |
| Hδ | 4102.9 | 4103.8 | em | both | peak@4127.2±0.8(z=0.0059) |
| Hδ_abs | 4102.9 | 4103.8 | abs | absorption | trough@4119.2±0.8(z=0.0040), trough@4139.2±0.8(z=0.0088) |
| G-band_abs | 4305.6 | 4306.5 | abs | absorption | — |
| Hγ | 4341.7 | 4342.7 | em | both | peak@4305.6±0.8(z=-0.0083) |
| Hγ_abs | 4341.7 | 4342.7 | abs | absorption | — |
| Hβ | 4862.7 | 4863.8 | em | both | — |
| Hβ_abs | 4862.7 | 4863.8 | abs | absorption | — |
| [O III]a | 4960.3 | 4961.4 | em | narrow | — |
| [O III]b | 5008.2 | 5009.3 | em | narrow | — |
| Mg I_abs | 5176.7 | 5177.8 | abs | absorption | — |
| Na D1_abs | 5891.6 | 5892.9 | abs | absorption | — |
| Na D_abs | 5895.6 | 5896.9 | abs | absorption | — |
| Na D2_abs | 5897.6 | 5898.9 | abs | absorption | — |
| [N II]a | 6549.8 | 6551.2 | em | narrow | peak@6504.8±0.8(z=-0.0069) |
| Hα | 6564.6 | 6566.0 | em | both | peak@6504.8±0.8(z=-0.0091) |
| Hα_abs | 6564.6 | 6566.0 | abs | absorption | — |
| [N II]b | 6585.3 | 6586.7 | em | narrow | — |
| [S II]a | 6718.3 | 6719.8 | em | narrow | — |
| [S II]b | 6732.7 | 6734.2 | em | narrow | — |
| CaT1_abs | 8498.0 | 8499.9 | abs | absorption | — |
| CaT2_abs | 8542.0 | 8543.9 | abs | absorption | — |
| CaT3_abs | 8662.0 | 8663.9 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 4961.4/5009.3 | fit_doublet | 4985.746±1.0429/5024.961±1.9128 | 0.260377/0.154285 | 141.6/166.0 | 1.6 | 0.011 | warning; separation fail; component ratio 0.59 |
| [S II]a/[S II]b | 6719.8/6734.2 | fit_doublet | 6718.803±0.0/6735.083±7.6078 | 0.0/0.02551 | 875.6/282.4 | 0.29 | 0.001 | ok; separation pass; component ratio — |
| [N II]a/[N II]b | 6551.2/6586.7 | fit_doublet | 6598.157±1.9359/6634.073±1.3209 | 0.070319/0.118208 | 160.8/210.3 | 1.29 | 0.012 | ok; separation pass; component ratio 1.68 |
| Ca K_abs/Ca H_abs | 3935.7/3970.5 | fit_doublet | 3942.844±23.3325/3988.404±28.2059 | -0.116773/-0.360753 | 954.9/9579.9 | 0.96 | 0.158 | warning; separation fail |
| Na D1_abs/Na D2_abs | 5892.9/5898.9 | fit_doublet | 5890.873±0.803/5900.401±0.797 | -0.162207/-0.186447 | 119.8/155.8 | 1.52 | 0.015 | ok; separation pass; component ratio 1.15 |
| [O II] | 3727.8 | fit_peak | 3716.652±1.0301 | 0.67694 | 328.2 | 1.56 | 0.023 | ok |
| Hε | 3971.0 | fit_peak | 3920.976±0.0 | 0.0 | 180.1 | 0.0 | -0.0 | warning: center_at_bound |
| Hβ | 4863.8 | fit_peak | 4813.769±3.4718 | 0.322006 | 1877.7 | 1.87 | 0.198 | warning: center_at_bound |
| Hε_abs | 3971.0 | fit_peak | 4016.957±18.996 | -0.693689 | 10202.1 | 1.6 | 0.659 | ok |
| G-band_abs | 4306.5 | fit_peak | 4256.547±46.8705 | -1.014265 | 16680.9 | 2.79 | 3.411 | warning: center_at_bound |
| Hγ_abs | 4342.7 | fit_peak | 4392.417±0.0 | -0.0 | 23248.5 | 0.0 | -0.0 | ok |
| Hβ_abs | 4863.8 | fit_peak | 4854.395±1.886 | -0.196838 | 197.0 | 1.17 | 0.008 | ok |
| Mg I_abs | 5177.8 | fit_peak | 5191.051±0.0 | -0.0 | 27146.5 | 0.0 | -0.0 | ok |
| Hα_abs | 6566.0 | fit_peak | 6573.701±2.7031 | -0.090995 | 494.8 | 1.02 | 0.021 | ok |
| CaT1_abs | 8499.9 | fit_peak | 8483.982±3.9545 | -0.069434 | 397.3 | 0.76 | 0.012 | ok |
| CaT2_abs | 8543.9 | fit_peak | 8539.594±1.115 | -0.109007 | 82.7 | 1.26 | 0.007 | ok |
| CaT3_abs | 8663.9 | fit_peak | 8700.148±1.1809 | -0.112911 | 81.1 | 1.37 | 0.008 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:oii-3727 | [O II] | 3727.8 | emission |
| line:cak-3934-abs | Ca K_abs | 3935.7 | absorption |
| line:cah-3969-abs | Ca H_abs | 3970.5 | absorption |
| line:heps-3970 | Hε | 3971.0 | emission |
| line:heps-3970-abs | Hε_abs | 3971.0 | absorption |
| line:hdel-4102 | Hδ | 4103.8 | emission |
| line:hdel-4102-abs | Hδ_abs | 4103.8 | absorption |
| line:gband-4305-abs | G-band_abs | 4306.5 | absorption |
| line:hgam-4341 | Hγ | 4342.7 | emission |
| line:hgam-4341-abs | Hγ_abs | 4342.7 | absorption |
| line:hbet-4862 | Hβ | 4863.8 | emission |
| line:hbet-4862-abs | Hβ_abs | 4863.8 | absorption |
| line:oiii-4960 | [O III]a | 4961.4 | emission |
| line:oiii-5008 | [O III]b | 5009.3 | emission |
| line:mgi-5176-abs | Mg I_abs | 5177.8 | absorption |
| line:nad1-5891-abs | Na D1_abs | 5892.9 | absorption |
| line:nad-5895-abs | Na D_abs | 5896.9 | absorption |
| line:nad2-5897-abs | Na D2_abs | 5898.9 | absorption |
| line:nii-6549 | [N II]a | 6551.2 | emission |
| line:half-6564 | Hα | 6566.0 | emission |
| line:half-6564-abs | Hα_abs | 6566.0 | absorption |
| line:nii-6585 | [N II]b | 6586.7 | emission |
| line:sii-6718 | [S II]a | 6719.8 | emission |
| line:sii-6732 | [S II]b | 6734.2 | emission |
| line:cat1-8498-abs | CaT1_abs | 8499.9 | absorption |
| line:cat2-8542-abs | CaT2_abs | 8543.9 | absorption |
| line:cat3-8662-abs | CaT3_abs | 8663.9 | absorption |

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
| fit:H4:0000 | fit_doublet | emission | 4985.746 | [O III]a | yes | — |
| fit:H4:0001 | fit_doublet | emission | 5024.961 | [O III]b | yes | — |
| fit:H4:0002 | fit_doublet | emission | 6718.803 | [S II]a | yes | — |
| fit:H4:0003 | fit_doublet | emission | 6735.083 | [S II]b | yes | — |
| fit:H4:0004 | fit_doublet | emission | 6598.157 | [N II]a | yes | — |
| fit:H4:0005 | fit_doublet | emission | 6634.073 | [N II]b | yes | — |
| fit:H4:0006 | fit_doublet | absorption | 3942.844 | Ca K_abs | yes | — |
| fit:H4:0007 | fit_doublet | absorption | 3988.404 | Ca H_abs | yes | — |
| fit:H4:0008 | fit_doublet | absorption | 5890.873 | Na D1_abs | yes | — |
| fit:H4:0009 | fit_doublet | absorption | 5900.401 | Na D2_abs | yes | — |
| fit:H4:0010 | fit_peak | emission | 3716.652 | [O II] | yes | — |
| fit:H4:0011 | fit_peak | emission | 3920.976 | Hε | no | center_at_bound |
| fit:H4:0012 | fit_peak | emission | 4813.769 | Hβ | no | center_at_bound |
| fit:H4:0013 | fit_peak | absorption | 4016.957 | Hε_abs | yes | — |
| fit:H4:0014 | fit_peak | absorption | 4256.547 | G-band_abs | no | center_at_bound |
| fit:H4:0015 | fit_peak | absorption | 4392.417 | Hγ_abs | yes | — |
| fit:H4:0016 | fit_peak | absorption | 4854.395 | Hβ_abs | yes | — |
| fit:H4:0017 | fit_peak | absorption | 5191.051 | Mg I_abs | yes | — |
| fit:H4:0018 | fit_peak | absorption | 6573.701 | Hα_abs | yes | — |
| fit:H4:0019 | fit_peak | absorption | 8483.982 | CaT1_abs | yes | — |
| fit:H4:0020 | fit_peak | absorption | 8539.594 | CaT2_abs | yes | — |
| fit:H4:0021 | fit_peak | absorption | 8700.148 | CaT3_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H4/pre_analysis/branches/main/024482a607724094aef627083e1ccf97/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H4:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blue_edge"
          ],
          "comment": "Fit centre 3716.7 vs 3727.8, offset ~11 A within strong window but low local SNR 1.6 and blue edge; weak candidate only."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H4:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "broad_width",
            "low_snr"
          ],
          "comment": "Doublet fit centre 3942.8 offset ~7 A, but separation fail and very broad width; plausible weak Ca K component retained as marginal."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H4:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "very_broad_width",
            "depth_ordering_uncertain"
          ],
          "comment": "Fit centre 3988.4 offset ~18 A, separation fail, FWHM ~9580 km/s; depth ordering (H deeper than K) uncertain, retained as plausible weak component."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Only fit is center_at_bound with zero amplitude; no credible CWT emission near 3971 A."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H4:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "very_broad_width",
            "low_snr",
            "blend"
          ],
          "comment": "Fit centre 4017 A offset ~46 A with FWHM ~10200 km/s; broad and blended, weak marginal."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_matching_feature"
          ],
          "comment": "Nearest peak 4127.2 A implies z=0.0059, offset ~23 A and no fit; no credible H-delta emission."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Troughs at 4119.2/4139.2 A are offset ~15-35 A and no targeted fit; not adopted."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_trough"
          ],
          "comment": "Only fit is center_at_bound at 4256.5 A with huge width; no credible G-band absorption."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Peak 4305.6 A implies z=-0.0083, offset ~37 A; no targeted fit; not adopted."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_cwt_trough"
          ],
          "comment": "Fit at 4392.4 A has zero amplitude and no CWT trough near 4343 A."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_peak"
          ],
          "comment": "Only fit is center_at_bound at 4813.8 A with huge width; no credible H-beta emission."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "fit:H4:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr"
          ],
          "comment": "Fit centre 4854.4 A offset ~9 A, narrow, low SNR 1.2; weak marginal absorption."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "fit:H4:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "low_snr",
            "blend"
          ],
          "comment": "Doublet fit centre 4985.7 A offset ~24 A, separation fail, ratio 0.59; weak blended marginal."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "fit:H4:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "low_snr",
            "blend"
          ],
          "comment": "Fit centre 5025.0 A offset ~16 A, separation fail, ratio inconsistent with 3:1; weak blended marginal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_cwt_trough"
          ],
          "comment": "Fit at 5191.1 A has zero amplitude; no CWT trough near 5178 A."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H4:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blend"
          ],
          "comment": "Doublet fit centre 5890.9 A offset ~2 A, separation pass but ratio 1.15 vs 2:1; blended weak marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": "fit:H4:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "shared_feature",
            "low_snr"
          ],
          "comment": "No separate measurement; Na D blend region covered by D1 fit at 5890.9 A; ambiguous shared feature."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H4:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blend"
          ],
          "comment": "Fit centre 5900.4 A offset ~1.5 A, separation pass but ratio 1.15 vs 2:1; blended weak marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H4:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_reject",
            "separation_pass",
            "low_snr"
          ],
          "comment": "Fit centre 6598.2 A offset ~47 A from 6551.2; weak and offset, marginal at best."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Peak 6504.8 A implies z=-0.0091, offset ~61 A; no targeted fit; not adopted."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H4:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr"
          ],
          "comment": "Fit centre 6573.7 A offset ~8 A, low SNR 1.0; weak marginal absorption."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H4:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_reject",
            "separation_pass",
            "low_snr"
          ],
          "comment": "Fit centre 6634.1 A offset ~47 A from 6586.7; weak and offset, marginal at best."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H4:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "zero_amplitude",
            "low_snr"
          ],
          "comment": "Fit centre 6718.8 A matches but amplitude 0.0 and SNR 0.29; essentially no signal, weak marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "fit:H4:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blend"
          ],
          "comment": "Fit centre 6735.1 A offset ~1 A, low SNR 0.29; weak blended marginal."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": "fit:H4:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8484.0 A offset ~16 A, low SNR 0.76, red edge; weak marginal."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H4:0020",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8539.6 A offset ~4 A, low SNR 1.3, red edge; weak marginal."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H4:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_reject",
            "low_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8700.1 A offset ~36 A, low SNR 1.4, red edge; weak marginal."
        }
      ]
    },
    "id": "call_00_951pnwPTiun0ryepuCin7212",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 8079,
  "output_tokens": 2390,
  "total_tokens": 10469,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 7439,
  "provider_usage": {
    "completion_tokens": 2390,
    "prompt_tokens": 8079,
    "total_tokens": 10469,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 7439
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_951pnwPTiun0ryepuCin7212`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 4, "line_id": "line:heps-3970-abs", "measurement_id": "fit:H4:0013", "reason": "measurement is outside this line's redshift window"}, {"row": 16, "line_id": "line:nad-5895-abs", "measurement_id": "fit:H4:0008", "reason": "fit belongs to another line"}, {"name": "Na D_abs", "reason": "blended label duplicates an adopted doublet component"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
I'll repair the flagged rows: Hε_abs fit is outside its window, and Na D_abs cannot reuse the D1 fit.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H4/pre_analysis/branches/main/024482a607724094aef627083e1ccf97/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H4:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blue_edge"
          ],
          "comment": "Fit centre 3716.7 vs 3727.8, offset ~11 A within strong window but low local SNR 1.6 and blue edge; weak candidate only."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H4:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "broad_width",
            "low_snr"
          ],
          "comment": "Doublet fit centre 3942.8 offset ~7 A, but separation fail and very broad width; plausible weak Ca K component retained as marginal."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H4:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "very_broad_width",
            "depth_ordering_uncertain"
          ],
          "comment": "Fit centre 3988.4 offset ~18 A, separation fail, FWHM ~9580 km/s; depth ordering (H deeper than K) uncertain, retained as plausible weak component."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Only fit is center_at_bound with zero amplitude; no credible CWT emission near 3971 A."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_cwt_trough"
          ],
          "comment": "Only fit centre 4017 A is outside the line window and very broad; no credible CWT trough near 3971 A."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_matching_feature"
          ],
          "comment": "Nearest peak 4127.2 A implies z=0.0059, offset ~23 A and no fit; no credible H-delta emission."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Troughs at 4119.2/4139.2 A are offset ~15-35 A and no targeted fit; not adopted."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_trough"
          ],
          "comment": "Only fit is center_at_bound at 4256.5 A with huge width; no credible G-band absorption."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Peak 4305.6 A implies z=-0.0083, offset ~37 A; no targeted fit; not adopted."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_cwt_trough"
          ],
          "comment": "Fit at 4392.4 A has zero amplitude and no CWT trough near 4343 A."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_peak"
          ],
          "comment": "Only fit is center_at_bound at 4813.8 A with huge width; no credible H-beta emission."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "fit:H4:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr"
          ],
          "comment": "Fit centre 4854.4 A offset ~9 A, narrow, low SNR 1.2; weak marginal absorption."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "fit:H4:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "low_snr",
            "blend"
          ],
          "comment": "Doublet fit centre 4985.7 A offset ~24 A, separation fail, ratio 0.59; weak blended marginal."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "fit:H4:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "low_snr",
            "blend"
          ],
          "comment": "Fit centre 5025.0 A offset ~16 A, separation fail, ratio inconsistent with 3:1; weak blended marginal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_cwt_trough"
          ],
          "comment": "Fit at 5191.1 A has zero amplitude; no CWT trough near 5178 A."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H4:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blend"
          ],
          "comment": "Doublet fit centre 5890.9 A offset ~2 A, separation pass but ratio 1.15 vs 2:1; blended weak marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "blend",
            "no_separate_measurement"
          ],
          "comment": "Blended Na D label; no independent measurement, region covered by D1/D2 doublet fits; not separately adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H4:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blend"
          ],
          "comment": "Fit centre 5900.4 A offset ~1.5 A, separation pass but ratio 1.15 vs 2:1; blended weak marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H4:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_reject",
            "separation_pass",
            "low_snr"
          ],
          "comment": "Fit centre 6598.2 A offset ~47 A from 6551.2; weak and offset, marginal at best."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Peak 6504.8 A implies z=-0.0091, offset ~61 A; no targeted fit; not adopted."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H4:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr"
          ],
          "comment": "Fit centre 6573.7 A offset ~8 A, low SNR 1.0; weak marginal absorption."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H4:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_reject",
            "separation_pass",
            "low_snr"
          ],
          "comment": "Fit centre 6634.1 A offset ~47 A from 6586.7; weak and offset, marginal at best."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H4:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "zero_amplitude",
            "low_snr"
          ],
          "comment": "Fit centre 6718.8 A matches but amplitude 0.0 and SNR 0.29; essentially no signal, weak marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "fit:H4:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "blend"
          ],
          "comment": "Fit centre 6735.1 A offset ~1 A, low SNR 0.29; weak blended marginal."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": "fit:H4:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8484.0 A offset ~16 A, low SNR 0.76, red edge; weak marginal."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H4:0020",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8539.6 A offset ~4 A, low SNR 1.3, red edge; weak marginal."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H4:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_reject",
            "low_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8700.1 A offset ~36 A, low SNR 1.4, red edge; weak marginal."
        }
      ]
    },
    "id": "call_00_4y8yPYE9N4UcGDmvfryn0427",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 10642,
  "output_tokens": 2383,
  "total_tokens": 13025,
  "cache_hit_tokens": 10368,
  "cache_miss_tokens": 274,
  "provider_usage": {
    "completion_tokens": 2383,
    "prompt_tokens": 10642,
    "total_tokens": 13025,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 10368
    },
    "prompt_cache_hit_tokens": 10368,
    "prompt_cache_miss_tokens": 274
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_4y8yPYE9N4UcGDmvfryn0427`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H4/pre_analysis/branches/main/024482a607724094aef627083e1ccf97/lines.csv", "n_lines": 27, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H4/pre_analysis/branches/main/024482a607724094aef627083e1ccf97/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:18:51.103140+00:00
