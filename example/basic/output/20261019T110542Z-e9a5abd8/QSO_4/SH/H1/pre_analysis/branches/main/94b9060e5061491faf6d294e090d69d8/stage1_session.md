# SH pre-analysis session: line review

- Run ID: `graph-853b617a68f04c36bd82f06bdb770ac4`
- Hypothesis: `H1`
- Started (UTC): 2026-10-19T11:39:49.823366+00:00
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
Review every predicted line at the fixed Redrock redshift `0.23787248591105023`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H1/pre_analysis/branches/main/94b9060e5061491faf6d294e090d69d8/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 46.6 |

Verify the redshift hypothesis z ≈ 0.23787248591105023.

Verification window: z ∈ [0.2279, 0.2479]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=59.2941, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=17.8254, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=43.9445, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=43.078, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=7.42723, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/QSO_4.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H1/pre_analysis/branches/main/94b9060e5061491faf6d294e090d69d8/lines.csv

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


## Predicted Lines at z = 0.2379

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [Ne V] | 3426.0 | 4241.0 | em | narrow | peak@4242.4±0.8(z=0.2383) |
| [O II] | 3727.0 | 4613.6 | em | narrow | peak@4616.8±0.8(z=0.2387) |
| Ca K_abs | 3934.8 | 4870.8 | abs | absorption | trough@4868.0±0.8(z=0.2372) |
| Ca H_abs | 3969.6 | 4913.9 | abs | absorption | — |
| Hε | 3970.1 | 4914.5 | em | both | peak@4912.8±0.8(z=0.2374) |
| Hε_abs | 3970.1 | 4914.5 | abs | absorption | — |
| Hδ | 4102.9 | 5078.9 | em | both | peak@5079.2±0.8(z=0.2380) |
| Hδ_abs | 4102.9 | 5078.9 | abs | absorption | trough@5075.2±0.8(z=0.2370) |
| G-band_abs | 4305.6 | 5329.8 | abs | absorption | trough@5333.6±0.8(z=0.2388) |
| Hγ | 4341.7 | 5374.5 | em | both | peak@5387.2±0.8(z=0.2408) |
| Hγ_abs | 4341.7 | 5374.5 | abs | absorption | trough@5333.6±0.8(z=0.2285) |
| Hβ | 4862.7 | 6019.4 | em | both | peak@6020.0±0.8(z=0.2380) |
| Hβ_abs | 4862.7 | 6019.4 | abs | absorption | trough@6010.4±0.8(z=0.2360), trough@6031.2±0.8(z=0.2403) |
| [O III]a | 4960.3 | 6140.2 | em | narrow | peak@6140.8±0.8(z=0.2380) |
| [O III]b | 5008.2 | 6199.5 | em | narrow | peak@6200.0±0.8(z=0.2380) |
| Mg I_abs | 5176.7 | 6408.1 | abs | absorption | — |
| Na D1_abs | 5891.6 | 7293.0 | abs | absorption | — |
| Na D_abs | 5895.6 | 7298.0 | abs | absorption | — |
| Na D2_abs | 5897.6 | 7300.5 | abs | absorption | — |
| [N II]a | 6549.8 | 8107.8 | em | narrow | peak@8127.2±0.8(z=0.2408) |
| Hα | 6564.6 | 8126.1 | em | both | peak@8127.2±0.8(z=0.2380) |
| Hα_abs | 6564.6 | 8126.1 | abs | absorption | trough@8120.0±0.8(z=0.2369) |
| [N II]b | 6585.3 | 8151.8 | em | narrow | peak@8127.2±0.8(z=0.2341) |
| [S II]a | 6718.3 | 8316.4 | em | narrow | peak@8318.4±0.8(z=0.2382), peak@8336.0±0.8(z=0.2408) |
| [S II]b | 6732.7 | 8334.2 | em | narrow | peak@8336.0±0.8(z=0.2381), peak@8318.4±0.8(z=0.2355) |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| Ca K_abs/Ca H_abs | 4870.8/4913.9 | fit_doublet | 4869.584±6.4267/4863.859±445.4542 | -0.727676/-0.687574 | 1990.4/43543.0 | 2.31 | 4.33 | warning; separation fail |
| Na D1_abs/Na D2_abs | 7293.0/7300.5 | fit_doublet | 7298.536±1.1701/7306.344±0.6931 | -0.253332/-0.174349 | 422.6/96.6 | 2.33 | 0.097 | ok; separation pass; component ratio 0.69 |
| Hε_abs | 4914.5 | fit_peak | 4869.032±3.187 | -0.787534 | 2323.5 | 3.06 | 0.664 | ok |
| Mg I_abs | 6408.1 | fit_peak | 6358.094±19.2726 | -0.910532 | 13242.9 | 4.54 | 10.464 | warning: center_at_bound |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:nev-3426 | [Ne V] | 4241.0 | emission |
| line:oii-3727 | [O II] | 4613.6 | emission |
| line:cak-3934-abs | Ca K_abs | 4870.8 | absorption |
| line:cah-3969-abs | Ca H_abs | 4913.9 | absorption |
| line:heps-3970 | Hε | 4914.5 | emission |
| line:heps-3970-abs | Hε_abs | 4914.5 | absorption |
| line:hdel-4102 | Hδ | 5078.9 | emission |
| line:hdel-4102-abs | Hδ_abs | 5078.9 | absorption |
| line:gband-4305-abs | G-band_abs | 5329.8 | absorption |
| line:hgam-4341 | Hγ | 5374.5 | emission |
| line:hgam-4341-abs | Hγ_abs | 5374.5 | absorption |
| line:hbet-4862 | Hβ | 6019.4 | emission |
| line:hbet-4862-abs | Hβ_abs | 6019.4 | absorption |
| line:oiii-4960 | [O III]a | 6140.2 | emission |
| line:oiii-5008 | [O III]b | 6199.5 | emission |
| line:mgi-5176-abs | Mg I_abs | 6408.1 | absorption |
| line:nad1-5891-abs | Na D1_abs | 7293.0 | absorption |
| line:nad-5895-abs | Na D_abs | 7298.0 | absorption |
| line:nad2-5897-abs | Na D2_abs | 7300.5 | absorption |
| line:nii-6549 | [N II]a | 8107.8 | emission |
| line:half-6564 | Hα | 8126.1 | emission |
| line:half-6564-abs | Hα_abs | 8126.1 | absorption |
| line:nii-6585 | [N II]b | 8151.8 | emission |
| line:sii-6718 | [S II]a | 8316.4 | emission |
| line:sii-6732 | [S II]b | 8334.2 | emission |

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
| fit:H1:0000 | fit_doublet | absorption | 4869.584 | Ca K_abs | yes | — |
| fit:H1:0001 | fit_doublet | absorption | 4863.859 | Ca H_abs | yes | — |
| fit:H1:0002 | fit_doublet | absorption | 7298.536 | Na D1_abs | yes | — |
| fit:H1:0003 | fit_doublet | absorption | 7306.344 | Na D2_abs | yes | — |
| fit:H1:0004 | fit_peak | absorption | 4869.032 | Hε_abs | yes | — |
| fit:H1:0005 | fit_peak | absorption | 6358.094 | Mg I_abs | no | center_at_bound |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H1/pre_analysis/branches/main/94b9060e5061491faf6d294e090d69d8/lines.csv",
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
          "comment": "Peak 4242.4 (z=0.2383) within 1.4 A of prediction; SNR 21.3, ridge 19, FWHM 1917 km/s broad but credible."
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
          "comment": "Peak 4616.8 (z=0.2387), offset 3.2 A, SNR 76.2, ridge 24; strong narrow feature."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "cwt:abs:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "weak_depth",
            "blend",
            "doublet_separation_fail"
          ],
          "comment": "Trough 4868.0 (z=0.2372) offset 2.8 A; doublet fit gave Ca K 4869.6 but Ca H component failed separation (huge error). Weak depth, plausible Ca K component retained."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "doublet_separation_fail",
            "unreliable_fit"
          ],
          "comment": "No CWT trough near 4913.9; doublet fit Ca H center 4863.9 with 445 A error and separation fail, not adoptable."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "cwt:em:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "weak_amp",
            "blend"
          ],
          "comment": "Peak 4912.8 (z=0.2374) offset 1.7 A; low amp 1.3, SNR 10.7, ridge 14; blended with Ca H region, weak but plausible."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_offset_large"
          ],
          "comment": "No trough at 4914.5; fit_peak center 4869.0 is 45 A off and belongs to Ca K region, not adoptable."
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
          "comment": "Peak 5079.2 (z=0.2380) offset 0.3 A; SNR 16.2, ridge 24, narrow FWHM 999 km/s."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "cwt:abs:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "weak_depth",
            "low_ridge"
          ],
          "comment": "Trough 5075.2 (z=0.2370) offset 3.7 A; amp -0.2, ridge 4, SNR 8.8; weak but positionally consistent."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "cwt:abs:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "broad_weak",
            "low_ridge"
          ],
          "comment": "Trough 5333.6 (z=0.2388) offset 3.8 A; broad FWHM 3268 km/s, amp -0.5, ridge 5; plausible G-band but weak."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "cwt:em:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad",
            "low_ridge"
          ],
          "comment": "Peak 5387.2 (z=0.2408) offset 12.7 A, within 20 A but broad FWHM 4736 km/s, amp 0.7, ridge 7; marginal."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "offset_reject"
          ],
          "comment": "No trough near 5374.5; nearest trough 5333.6 implies z=0.2285, 41 A off, not adoptable."
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
          "comment": "Peak 6020.0 (z=0.2380) offset 0.6 A; SNR 36.2, ridge 21, narrow FWHM 631 km/s."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "cwt:abs:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "blend",
            "weak_depth"
          ],
          "comment": "Trough 6010.4 (z=0.2360) offset 9 A; adjacent trough 6031.2 (z=0.2403) also present; blended absorption, weak depth."
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
          "comment": "Peak 6140.8 (z=0.2380) offset 0.6 A; SNR 66.3, ridge 19, narrow FWHM 511 km/s."
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
          "comment": "Peak 6200.0 (z=0.2380) offset 0.5 A; SNR 133.7, ridge 24; b:a amplitude ratio ~2.8 consistent with 3:1."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound"
          ],
          "comment": "No CWT trough near 6408.1; fit_peak center 6358.1 flagged center_at_bound and 50 A off, not adoptable."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H1:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "fit_offset_ok",
            "weak_depth",
            "doublet_ratio_off"
          ],
          "comment": "Doublet fit center 7298.5, offset 5.5 A; weak amp -0.25, local SNR 2.3; component ratio 0.69 vs expected 2, but position consistent."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "blend",
            "unresolved_doublet"
          ],
          "comment": "No distinct CWT trough at 7298.0; Na D region only resolved as blended doublet fit, no separate measurement for this component."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H1:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "fit_offset_ok",
            "weak_depth",
            "doublet_ratio_off"
          ],
          "comment": "Doublet fit center 7306.3, offset 5.8 A; weak amp -0.17, local SNR 2.3; ratio inconsistent with 2:1 but position plausible."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "blend_with_halpha"
          ],
          "comment": "No CWT peak at 8107.8; nearest peak 8127.2 is Halpha (z=0.2380), 19 A away and blended; no separate [N II]a measurement."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "cwt:em:0012",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "ridge_persistent",
            "blend"
          ],
          "comment": "Peak 8127.2 (z=0.2380) offset 1.1 A; SNR 22.7, ridge 22; blended with [N II] but dominant Halpha component."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "cwt:abs:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_ok",
            "weak_depth",
            "low_ridge"
          ],
          "comment": "Trough 8120.0 (z=0.2369) offset 6.1 A; amp -3.5 but ridge 5, SNR 9.5; plausible weak absorption."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "blend_with_halpha"
          ],
          "comment": "No CWT peak at 8151.8; only 8127.2 Halpha peak present, 24.6 A away; no separate [N II]b measurement."
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
          "comment": "Peak 8318.4 (z=0.2382) offset 2.0 A; SNR 31.8, ridge 23; a component of S II doublet with 8336.0."
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
          "comment": "Peak 8336.0 (z=0.2381) offset 1.8 A; SNR 27.2, ridge 12; b component, amplitude comparable to a as expected."
        }
      ]
    },
    "id": "call_00_IPWBKRhZOYJ1atYJpdID5653",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 7406,
  "output_tokens": 2702,
  "total_tokens": 10108,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 6766,
  "provider_usage": {
    "completion_tokens": 2702,
    "prompt_tokens": 7406,
    "total_tokens": 10108,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 6766
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_IPWBKRhZOYJ1atYJpdID5653`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H1/pre_analysis/branches/main/94b9060e5061491faf6d294e090d69d8/lines.csv", "n_lines": 25, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H1/pre_analysis/branches/main/94b9060e5061491faf6d294e090d69d8/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 2
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:40:00.616181+00:00
