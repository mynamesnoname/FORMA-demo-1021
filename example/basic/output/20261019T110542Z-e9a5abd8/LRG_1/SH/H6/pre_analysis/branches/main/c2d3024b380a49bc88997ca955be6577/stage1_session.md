# SH pre-analysis session: line review

- Run ID: `graph-6f4e6510cc5d45df9da3b7be0c8597cc`
- Hypothesis: `H6`
- Started (UTC): 2026-10-19T11:28:35.088085+00:00
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
Review every predicted line at the fixed Redrock redshift `0.001342809297630766`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H6/pre_analysis/branches/main/c2d3024b380a49bc88997ca955be6577/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 38.1 |

Verify the redshift hypothesis z ≈ 0.001342809297630766.

Verification window: z ∈ [-0.0087, 0.0113]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=47.9643, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=14.4193, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=35.5477, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=34.8467, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=6.00806, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/LRG_1.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H6/pre_analysis/branches/main/c2d3024b380a49bc88997ca955be6577/lines.csv

## CWT Detected Features

### Emission (peaks) — 14 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 4668.8 | 0.8 | 0.3 | 113.8 | 7305 | 4 | 12.0 |
| 4815.2 | 0.8 | 0.3 | 77.7 | 4839 | 4 | 10.5 |
| 4964.0 | 0.8 | 0.6 | 70.3 | 4248 | 7 | 11.7 |
| 5102.4 | 0.8 | 0.4 | 70.3 | 4132 | 5 | 14.7 |
| 5400.0 | 0.8 | 0.4 | 94.0 | 5220 | 6 | 14.1 |
| 5532.8 | 0.8 | 0.0 | 77.7 | 4211 | 4 | 11.8 |
| 6292.0 | 0.8 | 0.7 | 85.1 | 4055 | 7 | 15.6 |
| 6651.2 | 0.8 | -0.0 | 77.7 | 3503 | 4 | 13.4 |
| 7057.6 | 0.8 | 0.4 | 77.7 | 3301 | 6 | 11.7 |
| 8430.4 | 0.8 | -0.2 | 113.8 | 4045 | 4 | 9.3 |
| 9380.0 | 0.8 | 1.6 | 4.0 | 129 | 9 | 14.9 |
| 9442.4 | 0.8 | 4.9 | 6.5 | 207 | 14 | 16.2 |
| 9605.6 | 0.8 | 0.2 | 113.8 | 3550 | 4 | 9.4 |
| 9794.4 | 0.8 | 3.4 | 11.6 | 354 | 18 | 12.7 |

### Absorption (troughs) — 16 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 4560.8 | 0.8 | -0.4 | 113.8 | 7478 | 4 | 10.5 |
| 4884.8 | 0.8 | -0.7 | 94.0 | 5771 | 4 | 11.6 |
| 5049.6 | 0.8 | -1.8 | 32.8 | 1949 | 5 | 9.9 |
| 5472.0 | 0.8 | -1.4 | 53.1 | 2909 | 8 | 10.0 |
| 5960.0 | 0.8 | -0.4 | 113.8 | 5722 | 4 | 18.8 |
| 6188.8 | 0.8 | -1.1 | 70.3 | 3407 | 9 | 14.4 |
| 6374.4 | 0.8 | -0.3 | 94.0 | 4422 | 6 | 15.2 |
| 6583.2 | 0.8 | -1.4 | 64.2 | 2925 | 10 | 11.8 |
| 6701.6 | 0.8 | -1.2 | 36.3 | 1622 | 6 | 10.3 |
| 7496.8 | 0.8 | -1.9 | 70.3 | 2813 | 9 | 12.1 |
| 7940.8 | 0.8 | -0.5 | 94.0 | 3550 | 6 | 11.0 |
| 8348.8 | 0.8 | -0.2 | 53.1 | 1906 | 8 | 10.6 |
| 9081.6 | 0.8 | -0.3 | 113.8 | 3755 | 4 | 17.6 |
| 9376.8 | 0.8 | -0.0 | 2.8 | 88 | 5 | 10.8 |
| 9449.6 | 0.8 | -0.3 | 9.6 | 303 | 4 | 9.0 |
| 9748.8 | 0.8 | -0.3 | 77.7 | 2390 | 8 | 9.6 |


## Predicted Lines at z = 0.0013

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [O II] | 3727.0 | 3732.0 | em | narrow | — |
| Ca K_abs | 3934.8 | 3940.1 | abs | absorption | — |
| Ca H_abs | 3969.6 | 3974.9 | abs | absorption | — |
| Hε | 3970.1 | 3975.4 | em | both | — |
| Hε_abs | 3970.1 | 3975.4 | abs | absorption | — |
| Hδ | 4102.9 | 4108.4 | em | both | — |
| Hδ_abs | 4102.9 | 4108.4 | abs | absorption | — |
| G-band_abs | 4305.6 | 4311.4 | abs | absorption | — |
| Hγ | 4341.7 | 4347.5 | em | both | — |
| Hγ_abs | 4341.7 | 4347.5 | abs | absorption | — |
| Hβ | 4862.7 | 4869.2 | em | both | — |
| Hβ_abs | 4862.7 | 4869.2 | abs | absorption | trough@4884.8±0.8(z=0.0045) |
| [O III]a | 4960.3 | 4967.0 | em | narrow | peak@4964.0±0.8(z=0.0007) |
| [O III]b | 5008.2 | 5014.9 | em | narrow | — |
| Mg I_abs | 5176.7 | 5183.7 | abs | absorption | — |
| Na D1_abs | 5891.6 | 5899.5 | abs | absorption | — |
| Na D_abs | 5895.6 | 5903.5 | abs | absorption | trough@5960.0±0.8(z=0.0109) |
| Na D2_abs | 5897.6 | 5905.5 | abs | absorption | trough@5960.0±0.8(z=0.0106) |
| [N II]a | 6549.8 | 6558.6 | em | narrow | — |
| Hα | 6564.6 | 6573.4 | em | both | — |
| Hα_abs | 6564.6 | 6573.4 | abs | absorption | trough@6583.2±0.8(z=0.0028) |
| [N II]b | 6585.3 | 6594.1 | em | narrow | peak@6651.2±0.8(z=0.0100) |
| [S II]a | 6718.3 | 6727.3 | em | narrow | — |
| [S II]b | 6732.7 | 6741.7 | em | narrow | — |
| CaT1_abs | 8498.0 | 8509.4 | abs | absorption | — |
| CaT2_abs | 8542.0 | 8553.5 | abs | absorption | — |
| CaT3_abs | 8662.0 | 8673.6 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 4967.0/5014.9 | fit_doublet | 5016.461±0.0/5064.837±5.9826 | 0.0/0.106712 | 42189.7/139.4 | 0.17 | 0.0 | ok; separation pass; component ratio — |
| [S II]a/[S II]b | 6727.3/6741.7 | fit_doublet | 6726.74±2.6031/6791.741±6.1466 | 0.350201/0.636065 | 644.0/7768.7 | 2.23 | 1.22 | warning: center_2_deviation_large; separation fail; component ratio 1.82 |
| [N II]a/[N II]b | 6558.6/6594.1 | fit_doublet | 6602.356±0.0/6644.143±0.0 | 0.0/0.0 | 7996.4/106.3 | 0.0 | 0.0 | warning: center_2_deviation_large; separation fail; component ratio — |
| Ca K_abs/Ca H_abs | 3940.1/3974.9 | fit_doublet | 3937.252±2.4599/3974.657±4.0009 | -0.517955/-0.297183 | 1161.8/1002.3 | 1.14 | 0.032 | ok; separation pass |
| Na D1_abs/Na D2_abs | 5899.5/5905.5 | fit_doublet | 5940.828±2.1688/5911.147±3.8614 | -0.372805/-0.220293 | 533.9/593.9 | 0.98 | 0.019 | warning; separation fail; component ratio 0.59 |
| [O II] | 3732.0 | fit_peak | 3733.126±1.5963 | 0.873099 | 635.1 | 1.36 | 0.033 | ok |
| Hε | 3975.4 | fit_peak | 3925.535±2.3301 | 0.175752 | 179.8 | 0.42 | 0.001 | ok |
| Hδ | 4108.4 | fit_peak | 4158.409±11.2383 | 0.310144 | 10071.3 | 0.92 | 0.223 | warning: center_at_bound |
| Hγ | 4347.5 | fit_peak | 4360.565±1.3333 | 0.562874 | 957.8 | 1.75 | 0.081 | ok |
| Hβ | 4869.2 | fit_peak | 4819.23±6.6696 | 0.302873 | 2414.5 | 0.59 | 0.025 | warning: center_at_bound |
| Hα | 6573.4 | fit_peak | 6523.415±0.0 | 0.0 | 108.2 | 0.0 | -0.0 | warning: center_at_bound |
| Hε_abs | 3975.4 | fit_peak | 3978.074±1.4486 | -0.3905 | 340.7 | 0.96 | 0.008 | ok |
| Hδ_abs | 4108.4 | fit_peak | 4116.541±0.4749 | -0.785311 | 187.5 | 2.18 | 0.023 | ok |
| G-band_abs | 4311.4 | fit_peak | 4283.81±2.7477 | -0.368831 | 1587.1 | 1.16 | 0.057 | ok |
| Hγ_abs | 4347.5 | fit_peak | 4345.577±0.5144 | -0.617274 | 162.5 | 1.83 | 0.015 | ok |
| Mg I_abs | 5183.7 | fit_peak | 5233.151±0.0 | -0.0 | 134.9 | 0.0 | -0.0 | ok |
| CaT1_abs | 8509.4 | fit_peak | 8550.438±9.7671 | -0.164776 | 3286.6 | 0.85 | 0.129 | ok |
| CaT2_abs | 8553.5 | fit_peak | 8545.377±6.9288 | -0.189917 | 3585.3 | 1.09 | 0.23 | ok |
| CaT3_abs | 8673.6 | fit_peak | 8623.631±86.3814 | -0.189362 | 10642.9 | 1.14 | 0.707 | warning: center_at_bound |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:oii-3727 | [O II] | 3732.0 | emission |
| line:cak-3934-abs | Ca K_abs | 3940.1 | absorption |
| line:cah-3969-abs | Ca H_abs | 3974.9 | absorption |
| line:heps-3970 | Hε | 3975.4 | emission |
| line:heps-3970-abs | Hε_abs | 3975.4 | absorption |
| line:hdel-4102 | Hδ | 4108.4 | emission |
| line:hdel-4102-abs | Hδ_abs | 4108.4 | absorption |
| line:gband-4305-abs | G-band_abs | 4311.4 | absorption |
| line:hgam-4341 | Hγ | 4347.5 | emission |
| line:hgam-4341-abs | Hγ_abs | 4347.5 | absorption |
| line:hbet-4862 | Hβ | 4869.2 | emission |
| line:hbet-4862-abs | Hβ_abs | 4869.2 | absorption |
| line:oiii-4960 | [O III]a | 4967.0 | emission |
| line:oiii-5008 | [O III]b | 5014.9 | emission |
| line:mgi-5176-abs | Mg I_abs | 5183.7 | absorption |
| line:nad1-5891-abs | Na D1_abs | 5899.5 | absorption |
| line:nad-5895-abs | Na D_abs | 5903.5 | absorption |
| line:nad2-5897-abs | Na D2_abs | 5905.5 | absorption |
| line:nii-6549 | [N II]a | 6558.6 | emission |
| line:half-6564 | Hα | 6573.4 | emission |
| line:half-6564-abs | Hα_abs | 6573.4 | absorption |
| line:nii-6585 | [N II]b | 6594.1 | emission |
| line:sii-6718 | [S II]a | 6727.3 | emission |
| line:sii-6732 | [S II]b | 6741.7 | emission |
| line:cat1-8498-abs | CaT1_abs | 8509.4 | absorption |
| line:cat2-8542-abs | CaT2_abs | 8553.5 | absorption |
| line:cat3-8662-abs | CaT3_abs | 8673.6 | absorption |

| Measurement ID | Source | Kind | Centre (Å) | Target | Selectable | Flags |
|---|---|---|---:|---|---|---|
| cwt:em:0000 | CWT | emission | 4668.800 | — | yes | — |
| cwt:em:0001 | CWT | emission | 4815.200 | — | yes | — |
| cwt:em:0002 | CWT | emission | 4964.000 | — | yes | — |
| cwt:em:0003 | CWT | emission | 5102.400 | — | yes | — |
| cwt:em:0004 | CWT | emission | 5400.000 | — | yes | — |
| cwt:em:0005 | CWT | emission | 5532.800 | — | yes | — |
| cwt:em:0006 | CWT | emission | 6292.000 | — | yes | — |
| cwt:em:0007 | CWT | emission | 6651.200 | — | yes | — |
| cwt:em:0008 | CWT | emission | 7057.600 | — | yes | — |
| cwt:em:0009 | CWT | emission | 8430.400 | — | yes | — |
| cwt:em:0010 | CWT | emission | 9380.000 | — | yes | — |
| cwt:em:0011 | CWT | emission | 9442.400 | — | yes | — |
| cwt:em:0012 | CWT | emission | 9605.600 | — | yes | — |
| cwt:em:0013 | CWT | emission | 9794.400 | — | yes | — |
| cwt:abs:0000 | CWT | absorption | 4560.800 | — | yes | — |
| cwt:abs:0001 | CWT | absorption | 4884.800 | — | yes | — |
| cwt:abs:0002 | CWT | absorption | 5049.600 | — | yes | — |
| cwt:abs:0003 | CWT | absorption | 5472.000 | — | yes | — |
| cwt:abs:0004 | CWT | absorption | 5960.000 | — | yes | — |
| cwt:abs:0005 | CWT | absorption | 6188.800 | — | yes | — |
| cwt:abs:0006 | CWT | absorption | 6374.400 | — | yes | — |
| cwt:abs:0007 | CWT | absorption | 6583.200 | — | yes | — |
| cwt:abs:0008 | CWT | absorption | 6701.600 | — | yes | — |
| cwt:abs:0009 | CWT | absorption | 7496.800 | — | yes | — |
| cwt:abs:0010 | CWT | absorption | 7940.800 | — | yes | — |
| cwt:abs:0011 | CWT | absorption | 8348.800 | — | yes | — |
| cwt:abs:0012 | CWT | absorption | 9081.600 | — | yes | — |
| cwt:abs:0013 | CWT | absorption | 9376.800 | — | yes | — |
| cwt:abs:0014 | CWT | absorption | 9449.600 | — | yes | — |
| cwt:abs:0015 | CWT | absorption | 9748.800 | — | yes | — |
| fit:H6:0000 | fit_doublet | emission | 5016.461 | [O III]a | yes | — |
| fit:H6:0001 | fit_doublet | emission | 5064.837 | [O III]b | yes | — |
| fit:H6:0002 | fit_doublet | emission | 6726.740 | [S II]a | yes | — |
| fit:H6:0003 | fit_doublet | emission | 6791.741 | [S II]b | yes | — |
| fit:H6:0004 | fit_doublet | emission | 6602.356 | [N II]a | yes | — |
| fit:H6:0005 | fit_doublet | emission | 6644.143 | [N II]b | yes | — |
| fit:H6:0006 | fit_doublet | absorption | 3937.252 | Ca K_abs | yes | — |
| fit:H6:0007 | fit_doublet | absorption | 3974.657 | Ca H_abs | yes | — |
| fit:H6:0008 | fit_doublet | absorption | 5940.828 | Na D1_abs | yes | — |
| fit:H6:0009 | fit_doublet | absorption | 5911.147 | Na D2_abs | yes | — |
| fit:H6:0010 | fit_peak | emission | 3733.126 | [O II] | yes | — |
| fit:H6:0011 | fit_peak | emission | 3925.535 | Hε | yes | — |
| fit:H6:0012 | fit_peak | emission | 4158.409 | Hδ | no | center_at_bound |
| fit:H6:0013 | fit_peak | emission | 4360.565 | Hγ | yes | — |
| fit:H6:0014 | fit_peak | emission | 4819.230 | Hβ | no | center_at_bound |
| fit:H6:0015 | fit_peak | emission | 6523.415 | Hα | no | center_at_bound |
| fit:H6:0016 | fit_peak | absorption | 3978.074 | Hε_abs | yes | — |
| fit:H6:0017 | fit_peak | absorption | 4116.541 | Hδ_abs | yes | — |
| fit:H6:0018 | fit_peak | absorption | 4283.810 | G-band_abs | yes | — |
| fit:H6:0019 | fit_peak | absorption | 4345.577 | Hγ_abs | yes | — |
| fit:H6:0020 | fit_peak | absorption | 5233.151 | Mg I_abs | yes | — |
| fit:H6:0021 | fit_peak | absorption | 8550.438 | CaT1_abs | yes | — |
| fit:H6:0022 | fit_peak | absorption | 8545.377 | CaT2_abs | yes | — |
| fit:H6:0023 | fit_peak | absorption | 8623.631 | CaT3_abs | no | center_at_bound |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H6/pre_analysis/branches/main/c2d3024b380a49bc88997ca955be6577/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H6:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blue_edge",
            "offset_ok"
          ],
          "comment": "Fit centre 3733.1 vs pred 3732.0 (offset ~1 A, good), but local SNR 1.36 and no CWT peak; blue edge <4000 A. Weak candidate only."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H6:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blue_edge",
            "doublet_depth_ok"
          ],
          "comment": "Doublet fit centre 3937.3 vs pred 3940.1 (offset ~3 A), separation pass, Ca K deeper than Ca H as expected. Low local SNR 1.14; plausible weak component."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H6:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blue_edge",
            "blend_heps"
          ],
          "comment": "Centre 3974.7 vs pred 3974.9, separation pass; shallower than Ca K as expected. Blended with H-epsilon region; low SNR 1.14."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H6:0011",
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "weak_snr",
            "blend_cah"
          ],
          "comment": "Fit centre 3925.5 vs pred 3975.4, offset ~50 A and amplitude tiny (SNR 0.42); no credible emission peak. Region blended with Ca H."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H6:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blue_edge",
            "blend_cah"
          ],
          "comment": "Absorption fit centre 3978.1 vs pred 3975.4 (offset ~3 A), SNR 0.96; plausible weak trough but blended with Ca H absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Only fit has center_at_bound (4158.4, FWHM 10071 km/s) and is not selectable; no CWT emission peak near 4108 A."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H6:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_ok"
          ],
          "comment": "Absorption centre 4116.5 vs pred 4108.4 (offset ~8 A), SNR 2.18, narrow width; plausible weak trough."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H6:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "offset_weak"
          ],
          "comment": "Centre 4283.8 vs pred 4311.4 (offset ~28 A, weaker range), FWHM 1587 km/s broad; SNR 1.16. Weak marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H6:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Emission fit centre 4360.6 vs pred 4347.5 (offset ~13 A), SNR 1.75; no matching CWT peak. Weak candidate."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H6:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_ok"
          ],
          "comment": "Absorption centre 4345.6 vs pred 4347.5 (offset ~2 A), narrow, SNR 1.83; plausible weak trough."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Only fit center_at_bound (4819.2) and not selectable; no CWT emission peak at 4869 A."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest trough cwt:abs:0001 at 4884.8 implies z=0.0045, offset ~16 A but broad/weak; no adopted measurement at predicted position."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "cwt:em:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "doublet_fit_failed",
            "blend"
          ],
          "comment": "CWT peak 4964.0 vs pred 4967.0 (offset ~3 A, z=0.0007 in window), SNR 11.7, ridge 7. Doublet fit gave zero-amplitude component 1 and failed separation; adopt CWT peak as marginal."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "no_cwt_peak"
          ],
          "comment": "Doublet fit component 2 at 5064.8 (offset ~50 A) with separation fail and zero component 1; no CWT peak near 5014.9. Not credible."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H6:0020",
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "offset_reject"
          ],
          "comment": "Fit centre 5233.2 with amplitude 0.0 and offset ~50 A; no credible absorption signal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_reject",
            "blend"
          ],
          "comment": "Na D doublet fit failed separation (5940.8/5911.1, ratio 0.59); centres far from predicted 5899.5. No adopted measurement."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_reject",
            "blend"
          ],
          "comment": "Na D blend unresolved; doublet fit separation fail and centres offset ~40 A. No credible measurement at 5903.5."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_reject",
            "blend"
          ],
          "comment": "Na D2 fit centre 5911.1 offset ~6 A but doublet separation fail and ratio inverted; not adoptable."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "separation_fail",
            "blend_halpha"
          ],
          "comment": "N II doublet fit gave zero amplitudes and separation fail (6602.4/6644.1); no credible component near 6558.6."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Only fit center_at_bound (6523.4) with zero amplitude and not selectable; no CWT emission peak at 6573 A."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest trough cwt:abs:0007 at 6583.2 implies z=0.0028, offset ~10 A but broad and blended with N II region; no adopted measurement."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "separation_fail",
            "blend"
          ],
          "comment": "CWT peak 6651.2 implies z=0.0100, offset ~57 A; doublet fit separation fail. Not credible."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H6:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "weak_snr",
            "blend"
          ],
          "comment": "Fit centre 6726.7 vs pred 6727.3 (offset <1 A) but doublet separation fail and local SNR 2.23; component 2 badly deviated. Weak marginal for component a."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_reject",
            "failed_fit"
          ],
          "comment": "Component 2 fit at 6791.7 (offset ~50 A) with FWHM 7769 km/s and separation fail; not credible."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": "fit:H6:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "red_edge"
          ],
          "comment": "Centre 8550.4 vs pred 8509.4 (offset ~41 A, weak range), FWHM 3287 km/s, SNR 0.85; red edge. Weak marginal."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H6:0022",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "red_edge",
            "blend_cat1"
          ],
          "comment": "Centre 8545.4 vs pred 8553.5 (offset ~8 A), FWHM 3585 km/s, SNR 1.09; blended with CaT1. Weak marginal."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Only fit center_at_bound (8623.6, FWHM 10643 km/s) and not selectable; no credible measurement near 8673.6."
        }
      ]
    },
    "id": "call_00_SvP8uoyfTa6OHAzScTK40527",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 7258,
  "output_tokens": 2646,
  "total_tokens": 9904,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 6618,
  "provider_usage": {
    "completion_tokens": 2646,
    "prompt_tokens": 7258,
    "total_tokens": 9904,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 6618
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_SvP8uoyfTa6OHAzScTK40527`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 3, "line_id": "line:heps-3970", "reason": "unadopted line needs null measurement_id"}, {"row": 14, "line_id": "line:mgi-5176-abs", "reason": "unadopted line needs null measurement_id"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
I need to set measurement_id to null for NOT_FOUND rows.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H6/pre_analysis/branches/main/c2d3024b380a49bc88997ca955be6577/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H6:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blue_edge",
            "offset_ok"
          ],
          "comment": "Fit centre 3733.1 vs pred 3732.0 (offset ~1 A, good), but local SNR 1.36 and no CWT peak; blue edge <4000 A. Weak candidate only."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H6:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blue_edge",
            "doublet_depth_ok"
          ],
          "comment": "Doublet fit centre 3937.3 vs pred 3940.1 (offset ~3 A), separation pass, Ca K deeper than Ca H as expected. Low local SNR 1.14; plausible weak component."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H6:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blue_edge",
            "blend_heps"
          ],
          "comment": "Centre 3974.7 vs pred 3974.9, separation pass; shallower than Ca K as expected. Blended with H-epsilon region; low SNR 1.14."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "weak_snr",
            "blend_cah"
          ],
          "comment": "Fit centre 3925.5 vs pred 3975.4, offset ~50 A and amplitude tiny (SNR 0.42); no credible emission peak. Region blended with Ca H."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H6:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blue_edge",
            "blend_cah"
          ],
          "comment": "Absorption fit centre 3978.1 vs pred 3975.4 (offset ~3 A), SNR 0.96; plausible weak trough but blended with Ca H absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Only fit has center_at_bound (4158.4, FWHM 10071 km/s) and is not selectable; no CWT emission peak near 4108 A."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H6:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_ok"
          ],
          "comment": "Absorption centre 4116.5 vs pred 4108.4 (offset ~8 A), SNR 2.18, narrow width; plausible weak trough."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H6:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "offset_weak"
          ],
          "comment": "Centre 4283.8 vs pred 4311.4 (offset ~28 A, weaker range), FWHM 1587 km/s broad; SNR 1.16. Weak marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H6:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Emission fit centre 4360.6 vs pred 4347.5 (offset ~13 A), SNR 1.75; no matching CWT peak. Weak candidate."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H6:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_ok"
          ],
          "comment": "Absorption centre 4345.6 vs pred 4347.5 (offset ~2 A), narrow, SNR 1.83; plausible weak trough."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Only fit center_at_bound (4819.2) and not selectable; no CWT emission peak at 4869 A."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest trough cwt:abs:0001 at 4884.8 implies z=0.0045, offset ~16 A but broad/weak; no adopted measurement at predicted position."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "cwt:em:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "doublet_fit_failed",
            "blend"
          ],
          "comment": "CWT peak 4964.0 vs pred 4967.0 (offset ~3 A, z=0.0007 in window), SNR 11.7, ridge 7. Doublet fit gave zero-amplitude component 1 and failed separation; adopt CWT peak as marginal."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "no_cwt_peak"
          ],
          "comment": "Doublet fit component 2 at 5064.8 (offset ~50 A) with separation fail and zero component 1; no CWT peak near 5014.9. Not credible."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "offset_reject"
          ],
          "comment": "Fit centre 5233.2 with amplitude 0.0 and offset ~50 A; no credible absorption signal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_reject",
            "blend"
          ],
          "comment": "Na D doublet fit failed separation (5940.8/5911.1, ratio 0.59); centres far from predicted 5899.5. No adopted measurement."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_reject",
            "blend"
          ],
          "comment": "Na D blend unresolved; doublet fit separation fail and centres offset ~40 A. No credible measurement at 5903.5."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_reject",
            "blend"
          ],
          "comment": "Na D2 fit centre 5911.1 offset ~6 A but doublet separation fail and ratio inverted; not adoptable."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "separation_fail",
            "blend_halpha"
          ],
          "comment": "N II doublet fit gave zero amplitudes and separation fail (6602.4/6644.1); no credible component near 6558.6."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Only fit center_at_bound (6523.4) with zero amplitude and not selectable; no CWT emission peak at 6573 A."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest trough cwt:abs:0007 at 6583.2 implies z=0.0028, offset ~10 A but broad and blended with N II region; no adopted measurement."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "separation_fail",
            "blend"
          ],
          "comment": "CWT peak 6651.2 implies z=0.0100, offset ~57 A; doublet fit separation fail. Not credible."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H6:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "weak_snr",
            "blend"
          ],
          "comment": "Fit centre 6726.7 vs pred 6727.3 (offset <1 A) but doublet separation fail and local SNR 2.23; component 2 badly deviated. Weak marginal for component a."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_reject",
            "failed_fit"
          ],
          "comment": "Component 2 fit at 6791.7 (offset ~50 A) with FWHM 7769 km/s and separation fail; not credible."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": "fit:H6:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "red_edge"
          ],
          "comment": "Centre 8550.4 vs pred 8509.4 (offset ~41 A, weak range), FWHM 3287 km/s, SNR 0.85; red edge. Weak marginal."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H6:0022",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "red_edge",
            "blend_cat1"
          ],
          "comment": "Centre 8545.4 vs pred 8553.5 (offset ~8 A), FWHM 3585 km/s, SNR 1.09; blended with CaT1. Weak marginal."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Only fit center_at_bound (8623.6, FWHM 10643 km/s) and not selectable; no credible measurement near 8673.6."
        }
      ]
    },
    "id": "call_00_pEZos59fMNeo6oghEiNn8899",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 10028,
  "output_tokens": 2628,
  "total_tokens": 12656,
  "cache_hit_tokens": 9856,
  "cache_miss_tokens": 172,
  "provider_usage": {
    "completion_tokens": 2628,
    "prompt_tokens": 10028,
    "total_tokens": 12656,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 9856
    },
    "prompt_cache_hit_tokens": 9856,
    "prompt_cache_miss_tokens": 172
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_pEZos59fMNeo6oghEiNn8899`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H6/pre_analysis/branches/main/c2d3024b380a49bc88997ca955be6577/lines.csv", "n_lines": 27, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H6/pre_analysis/branches/main/c2d3024b380a49bc88997ca955be6577/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:28:54.025543+00:00
