# SH pre-analysis session: line review

- Run ID: `graph-325ff74c7f444efdb17e3f3b69698eea`
- Hypothesis: `H2`
- Started (UTC): 2026-10-19T11:44:43.295747+00:00
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
Review every predicted line at the fixed Redrock redshift `0.2121167421507701`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H2/pre_analysis/branches/main/ff924c2a3824454da961cf0304e0c4c6/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 4.7 |

Verify the redshift hypothesis z ≈ 0.2121167421507701.

Verification window: z ∈ [0.2021, 0.2221]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=58.0604, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=17.4545, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=43.0301, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=42.1817, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=7.2727, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/QSO_116.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H2/pre_analysis/branches/main/ff924c2a3824454da961cf0304e0c4c6/lines.csv

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


## Predicted Lines at z = 0.2121

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [Ne V] | 3426.0 | 4152.7 | em | narrow | — |
| [O II] | 3727.0 | 4517.6 | em | narrow | — |
| Ca K_abs | 3934.8 | 4769.4 | abs | absorption | — |
| Ca H_abs | 3969.6 | 4811.6 | abs | absorption | — |
| Hε | 3970.1 | 4812.2 | em | both | — |
| Hε_abs | 3970.1 | 4812.2 | abs | absorption | — |
| Hδ | 4102.9 | 4973.2 | em | both | — |
| Hδ_abs | 4102.9 | 4973.2 | abs | absorption | — |
| G-band_abs | 4305.6 | 5218.9 | abs | absorption | — |
| Hγ | 4341.7 | 5262.6 | em | both | — |
| Hγ_abs | 4341.7 | 5262.6 | abs | absorption | — |
| Hβ | 4862.7 | 5894.2 | em | both | — |
| Hβ_abs | 4862.7 | 5894.2 | abs | absorption | — |
| [O III]a | 4960.3 | 6012.5 | em | narrow | — |
| [O III]b | 5008.2 | 6070.5 | em | narrow | peak@6072.0±0.8(z=0.2124) |
| Mg I_abs | 5176.7 | 6274.8 | abs | absorption | — |
| Na D1_abs | 5891.6 | 7141.3 | abs | absorption | — |
| Na D_abs | 5895.6 | 7146.2 | abs | absorption | — |
| Na D2_abs | 5897.6 | 7148.6 | abs | absorption | — |
| [N II]a | 6549.8 | 7939.1 | em | narrow | — |
| Hα | 6564.6 | 7957.1 | em | both | — |
| Hα_abs | 6564.6 | 7957.1 | abs | absorption | — |
| [N II]b | 6585.3 | 7982.2 | em | narrow | — |
| [S II]a | 6718.3 | 8143.4 | em | narrow | — |
| [S II]b | 6732.7 | 8160.8 | em | narrow | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 6012.5/6070.5 | fit_doublet | 5996.352±4.2526/6074.503±0.7794 | 0.224537/1.615506 | 2275.1/3731.3 | 10.97 | 12.628 | warning; separation fail; component ratio 7.19 |
| [S II]a/[S II]b | 8143.4/8160.8 | fit_doublet | 8093.364±37.7156/8209.874±3.2476 | 0.040709/0.053115 | 5869.0/86.0 | 0.61 | 0.045 | warning; separation fail; component ratio 1.3 |
| [N II]a/[N II]b | 7939.1/7982.2 | fit_doublet | 7927.67±4.7438/8032.152±34.7366 | 0.057196/0.038656 | 359.8/6436.1 | 0.62 | 0.046 | warning; separation fail; component ratio 0.68 |
| Ca K_abs/Ca H_abs | 4769.4/4811.6 | fit_doublet | 4819.437±0.0/4861.618±0.0 | -0.0/-0.0 | 146.5/145.2 | 0.0 | -0.0 | warning: center_1_deviation_large; separation pass |
| Na D1_abs/Na D2_abs | 7141.3/7148.6 | fit_doublet | 7116.539±79.5308/7190.098±9.7846 | -0.347906/-0.031556 | 29759.9/764.8 | 3.83 | 10.984 | warning; separation fail; component ratio 0.09 |
| [Ne V] | 4152.7 | fit_peak | 4151.15±4.9455 | 0.137187 | 509.8 | 0.34 | 0.002 | ok |
| [O II] | 4517.6 | fit_peak | 4567.558±0.0 | 0.0 | 445.7 | 0.0 | -0.0 | warning: center_at_bound |
| Hε | 4812.2 | fit_peak | 4774.448±1.3328 | 2.916274 | 3754.6 | 5.97 | 4.011 | ok |
| Hδ | 4973.2 | fit_peak | 5023.193±0.0 | 0.0 | 140.5 | 0.0 | -0.0 | warning: center_at_bound |
| Hγ | 5262.6 | fit_peak | 5212.647±0.0 | 0.0 | 169.0 | 0.0 | 0.0 | warning: center_at_bound |
| Hβ | 5894.2 | fit_peak | 5844.161±0.0 | 0.0 | 120.8 | 0.0 | -0.0 | warning: center_at_bound |
| Hα | 7957.1 | fit_peak | 7910.86±0.0 | 0.0 | 13022.1 | 0.0 | -0.0 | ok |
| Hε_abs | 4812.2 | fit_peak | 4862.225±0.0 | -0.0 | 158.0 | 0.0 | -0.0 | warning: center_at_bound |
| Hδ_abs | 4973.2 | fit_peak | 4923.194±12.7132 | -1.721428 | 19188.1 | 9.16 | 46.729 | warning: center_at_bound |
| G-band_abs | 5218.9 | fit_peak | 5168.89±0.0 | -0.0 | 390.0 | 0.0 | -0.0 | warning: center_at_bound |
| Hγ_abs | 5262.6 | fit_peak | 5267.704±4.121 | -0.064488 | 506.0 | 0.45 | 0.003 | ok |
| Hβ_abs | 5894.2 | fit_peak | 5944.16±3.5846 | -1.044064 | 9439.1 | 5.0 | 9.675 | warning: center_at_bound |
| Mg I_abs | 6274.8 | fit_peak | 6224.765±6.348 | -1.076244 | 11915.1 | 6.51 | 19.268 | warning: center_at_bound |
| Hα_abs | 7957.1 | fit_peak | 7956.525±3.0816 | -0.072339 | 201.5 | 0.75 | 0.006 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:nev-3426 | [Ne V] | 4152.7 | emission |
| line:oii-3727 | [O II] | 4517.6 | emission |
| line:cak-3934-abs | Ca K_abs | 4769.4 | absorption |
| line:cah-3969-abs | Ca H_abs | 4811.6 | absorption |
| line:heps-3970 | Hε | 4812.2 | emission |
| line:heps-3970-abs | Hε_abs | 4812.2 | absorption |
| line:hdel-4102 | Hδ | 4973.2 | emission |
| line:hdel-4102-abs | Hδ_abs | 4973.2 | absorption |
| line:gband-4305-abs | G-band_abs | 5218.9 | absorption |
| line:hgam-4341 | Hγ | 5262.6 | emission |
| line:hgam-4341-abs | Hγ_abs | 5262.6 | absorption |
| line:hbet-4862 | Hβ | 5894.2 | emission |
| line:hbet-4862-abs | Hβ_abs | 5894.2 | absorption |
| line:oiii-4960 | [O III]a | 6012.5 | emission |
| line:oiii-5008 | [O III]b | 6070.5 | emission |
| line:mgi-5176-abs | Mg I_abs | 6274.8 | absorption |
| line:nad1-5891-abs | Na D1_abs | 7141.3 | absorption |
| line:nad-5895-abs | Na D_abs | 7146.2 | absorption |
| line:nad2-5897-abs | Na D2_abs | 7148.6 | absorption |
| line:nii-6549 | [N II]a | 7939.1 | emission |
| line:half-6564 | Hα | 7957.1 | emission |
| line:half-6564-abs | Hα_abs | 7957.1 | absorption |
| line:nii-6585 | [N II]b | 7982.2 | emission |
| line:sii-6718 | [S II]a | 8143.4 | emission |
| line:sii-6732 | [S II]b | 8160.8 | emission |

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
| fit:H2:0000 | fit_doublet | emission | 5996.352 | [O III]a | yes | — |
| fit:H2:0001 | fit_doublet | emission | 6074.503 | [O III]b | yes | — |
| fit:H2:0002 | fit_doublet | emission | 8093.364 | [S II]a | yes | — |
| fit:H2:0003 | fit_doublet | emission | 8209.874 | [S II]b | yes | — |
| fit:H2:0004 | fit_doublet | emission | 7927.670 | [N II]a | yes | — |
| fit:H2:0005 | fit_doublet | emission | 8032.152 | [N II]b | yes | — |
| fit:H2:0006 | fit_doublet | absorption | 4819.437 | Ca K_abs | yes | — |
| fit:H2:0007 | fit_doublet | absorption | 4861.618 | Ca H_abs | yes | — |
| fit:H2:0008 | fit_doublet | absorption | 7116.539 | Na D1_abs | yes | — |
| fit:H2:0009 | fit_doublet | absorption | 7190.098 | Na D2_abs | yes | — |
| fit:H2:0010 | fit_peak | emission | 4151.150 | [Ne V] | yes | — |
| fit:H2:0011 | fit_peak | emission | 4567.558 | [O II] | no | center_at_bound |
| fit:H2:0012 | fit_peak | emission | 4774.448 | Hε | yes | — |
| fit:H2:0013 | fit_peak | emission | 5023.193 | Hδ | no | center_at_bound |
| fit:H2:0014 | fit_peak | emission | 5212.647 | Hγ | no | center_at_bound |
| fit:H2:0015 | fit_peak | emission | 5844.161 | Hβ | no | center_at_bound |
| fit:H2:0016 | fit_peak | emission | 7910.860 | Hα | yes | — |
| fit:H2:0017 | fit_peak | absorption | 4862.225 | Hε_abs | no | center_at_bound |
| fit:H2:0018 | fit_peak | absorption | 4923.194 | Hδ_abs | no | center_at_bound |
| fit:H2:0019 | fit_peak | absorption | 5168.890 | G-band_abs | no | center_at_bound |
| fit:H2:0020 | fit_peak | absorption | 5267.704 | Hγ_abs | yes | — |
| fit:H2:0021 | fit_peak | absorption | 5944.160 | Hβ_abs | no | center_at_bound |
| fit:H2:0022 | fit_peak | absorption | 6224.765 | Mg I_abs | no | center_at_bound |
| fit:H2:0023 | fit_peak | absorption | 7956.525 | Hα_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H2/pre_analysis/branches/main/ff924c2a3824454da961cf0304e0c4c6/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": "fit:H2:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_ok",
            "low_amp"
          ],
          "comment": "Fit centre 4151.15 vs pred 4152.7 (offset ~1.5 A, within window); local SNR 0.34, amplitude 0.14, no CWT peak. Weak, marginal at best."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Only fit is center_at_bound (4567.6, amp 0) and unselectable; no CWT peak near 4517.6. No credible measurement."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "failed_fit",
            "zero_amplitude",
            "blend_cah"
          ],
          "comment": "Doublet fit gave zero amplitude, centre 4819.4 offset ~50 A from pred 4769.4; no CWT trough at 4769. Ca K/H region blended with H-eps emission; no credible absorption measurement."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "failed_fit",
            "zero_amplitude",
            "blend_heps"
          ],
          "comment": "Fit centre 4861.6, zero amplitude, offset ~50 A; coincides with H-eps emission blend. No credible Ca H absorption adopted."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H2:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width",
            "blend_cah"
          ],
          "comment": "Fit centre 4774.4 vs pred 4812.2 (offset ~38 A, weaker band); CWT peak at 4768.0 (SNR 13) nearby. Broad FWHM ~3750 km/s; blended with Ca H region. Marginal."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_trough"
          ],
          "comment": "Fit center_at_bound (4862.2, amp 0), unselectable; no CWT trough near 4812. No credible absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Fit center_at_bound (5023.2, amp 0), unselectable; no CWT peak near 4973.2."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Fit center_at_bound (4923.2) with huge width 19188 km/s, unselectable; no CWT trough near 4973.2."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_trough"
          ],
          "comment": "Fit center_at_bound (5168.9, amp 0), unselectable; no CWT trough near 5218.9."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Fit center_at_bound (5212.6, amp 0), unselectable; no CWT peak near 5262.6."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H2:0020",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_amp",
            "low_snr",
            "offset_ok"
          ],
          "comment": "Fit centre 5267.7 vs pred 5262.6 (offset ~5 A, good); amplitude -0.06, local SNR 0.45. Very weak but positionally consistent; marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Fit center_at_bound (5844.2, amp 0), unselectable; no CWT peak near 5894.2."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Fit center_at_bound (5944.2) with huge width 9439 km/s, unselectable; no credible trough near 5894.2."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "ratio_fail",
            "blend_oiiib"
          ],
          "comment": "Doublet fit component 1 at 5996.4 (offset ~16 A) but separation fail and ratio 7.19; the real signal is the 6072 peak assigned to [O III]b. No credible independent [O III]a measurement."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "cwt:em:0002",
          "status": "LIKELY",
          "reason_codes": [
            "strong_cwt",
            "offset_ok",
            "blend_oiiia"
          ],
          "comment": "CWT peak 6072.0 (SNR 23, ridge 9) vs pred 6070.5, offset ~1.5 A; fit centre 6074.5. Strong credible emission; blended doublet partner [O III]a unresolved."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Fit center_at_bound (6224.8) with huge width 11915 km/s, unselectable; no CWT trough near 6274.8."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "failed_fit",
            "blend_nad"
          ],
          "comment": "Na D doublet fit separation fail, component 1 at 7116.5 with 29760 km/s width; no CWT trough near 7141.3. No credible Na D1 measurement."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "blend_nad",
            "no_cwt_trough"
          ],
          "comment": "Blended Na D complex; doublet fit failed separation and no CWT trough near 7146.2. No credible measurement for the middle component."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "failed_fit",
            "blend_nad"
          ],
          "comment": "Fit component 2 at 7190.1 (offset ~42 A) with separation fail and ratio 0.09; no CWT trough near 7148.6. No credible Na D2 measurement."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "low_snr",
            "blend_halpha"
          ],
          "comment": "Doublet fit component 1 at 7927.7 (offset ~11 A) but separation fail, local SNR 0.62; no CWT peak near 7939.1. No credible [N II]a."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Fit centre 7910.9 with zero amplitude and 13022 km/s width; no CWT peak near 7957.1. No credible H-alpha emission."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H2:0023",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_amp",
            "low_snr",
            "offset_ok"
          ],
          "comment": "Fit centre 7956.5 vs pred 7957.1 (offset ~0.6 A, excellent); amplitude -0.07, local SNR 0.75. Very weak but positionally consistent; marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "failed_fit",
            "blend_halpha"
          ],
          "comment": "Doublet fit component 2 at 8032.2 (offset ~50 A) with 6436 km/s width, separation fail; no CWT peak near 7982.2. No credible [N II]b."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "low_snr",
            "failed_fit"
          ],
          "comment": "Doublet fit component 1 at 8093.4 (offset ~50 A) with 5869 km/s width, separation fail, local SNR 0.61; no CWT peak near 8143.4. No credible [S II]a."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "failed_fit",
            "low_snr"
          ],
          "comment": "Doublet fit component 2 at 8209.9 (offset ~49 A), separation fail, local SNR 0.61; no CWT peak near 8160.8. No credible [S II]b."
        }
      ]
    },
    "id": "call_00_sbxmrNIB9SeBg75Nsh5i0846",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 7247,
  "output_tokens": 2518,
  "total_tokens": 9765,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 6607,
  "provider_usage": {
    "completion_tokens": 2518,
    "prompt_tokens": 7247,
    "total_tokens": 9765,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 6607
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_sbxmrNIB9SeBg75Nsh5i0846`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H2/pre_analysis/branches/main/ff924c2a3824454da961cf0304e0c4c6/lines.csv", "n_lines": 25, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H2/pre_analysis/branches/main/ff924c2a3824454da961cf0304e0c4c6/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 2
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:44:53.089957+00:00
