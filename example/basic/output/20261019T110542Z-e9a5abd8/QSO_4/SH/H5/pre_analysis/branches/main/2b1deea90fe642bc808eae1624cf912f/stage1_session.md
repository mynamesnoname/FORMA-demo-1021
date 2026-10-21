# SH pre-analysis session: line review

- Run ID: `graph-853b617a68f04c36bd82f06bdb770ac4`
- Hypothesis: `H5`
- Started (UTC): 2026-10-19T11:40:00.664314+00:00
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
Review every predicted line at the fixed Redrock redshift `-0.0016077994367870048`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H5/pre_analysis/branches/main/2b1deea90fe642bc808eae1624cf912f/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 46.6 |

Verify the redshift hypothesis z ≈ -0.0016077994367870048.

Verification window: z ∈ [-0.0116, 0.0084]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=47.823, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=14.3768, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=35.4429, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=34.744, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=5.99035, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/QSO_4.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H5/pre_analysis/branches/main/2b1deea90fe642bc808eae1624cf912f/lines.csv

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


## Predicted Lines at z = -0.0016

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [O II] | 3727.0 | 3721.0 | em | narrow | — |
| Ca K_abs | 3934.8 | 3928.5 | abs | absorption | — |
| Ca H_abs | 3969.6 | 3963.2 | abs | absorption | — |
| Hε | 3970.1 | 3963.7 | em | both | — |
| Hε_abs | 3970.1 | 3963.7 | abs | absorption | — |
| Hδ | 4102.9 | 4096.3 | em | both | — |
| Hδ_abs | 4102.9 | 4096.3 | abs | absorption | — |
| G-band_abs | 4305.6 | 4298.7 | abs | absorption | trough@4274.4±0.8(z=-0.0072) |
| Hγ | 4341.7 | 4334.7 | em | both | — |
| Hγ_abs | 4341.7 | 4334.7 | abs | absorption | — |
| Hβ | 4862.7 | 4854.9 | em | both | — |
| Hβ_abs | 4862.7 | 4854.9 | abs | absorption | trough@4868.0±0.8(z=0.0011) |
| [O III]a | 4960.3 | 4952.3 | em | narrow | peak@4912.8±0.8(z=-0.0096) |
| [O III]b | 5008.2 | 5000.1 | em | narrow | — |
| Mg I_abs | 5176.7 | 5168.4 | abs | absorption | — |
| Na D1_abs | 5891.6 | 5882.1 | abs | absorption | — |
| Na D_abs | 5895.6 | 5886.1 | abs | absorption | — |
| Na D2_abs | 5897.6 | 5888.1 | abs | absorption | — |
| [N II]a | 6549.8 | 6539.3 | em | narrow | — |
| Hα | 6564.6 | 6554.0 | em | both | — |
| Hα_abs | 6564.6 | 6554.0 | abs | absorption | — |
| [N II]b | 6585.3 | 6574.7 | em | narrow | — |
| [S II]a | 6718.3 | 6707.5 | em | narrow | — |
| [S II]b | 6732.7 | 6721.9 | em | narrow | — |
| CaT1_abs | 8498.0 | 8484.3 | abs | absorption | — |
| CaT2_abs | 8542.0 | 8528.3 | abs | absorption | — |
| CaT3_abs | 8662.0 | 8648.1 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 4952.3/5000.1 | fit_doublet | 4902.325±322.9715/4950.603±0.0 | 0.128662/0.0 | 26395.0/142.6 | 0.51 | 0.132 | ok; separation pass; component ratio 0.0 |
| [S II]a/[S II]b | 6707.5/6721.9 | fit_doublet | 6657.498±0.844/6711.197±3.1702 | 0.162486/0.093124 | 117.3/539.4 | 1.23 | 0.012 | warning: center_1_deviation_large; separation fail; component ratio 0.57 |
| [N II]a/[N II]b | 6539.3/6574.7 | fit_doublet | 6536.296±1.2363/6565.898±1.6094 | 0.190176/0.281943 | 349.4/1282.7 | 2.24 | 0.204 | warning; separation fail; component ratio 1.48 |
| Ca K_abs/Ca H_abs | 3928.5/3963.2 | fit_doublet | 3912.517±1.0124/4013.218±127.3135 | -0.579592/-1.749302 | 180.4/52772.4 | 3.67 | 9.831 | warning: center_2_deviation_large; separation fail |
| Na D1_abs/Na D2_abs | 5882.1/5888.1 | fit_doublet | 5923.985±258.0376/5854.478±16.711 | -1.647522/-0.218051 | 35750.8/723.3 | 5.05 | 18.993 | warning; separation fail; component ratio 0.13 |
| [O II] | 3721.0 | fit_peak | 3671.009±0.0 | 0.0 | 192.3 | 0.0 | -0.0 | warning: center_at_bound |
| Hε | 3963.7 | fit_peak | 3966.532±0.6401 | 0.730996 | 199.5 | 1.83 | 0.017 | ok |
| Hδ | 4096.3 | fit_peak | 4142.393±0.7387 | 1.270292 | 471.9 | 3.48 | 0.148 | ok |
| Hγ | 4334.7 | fit_peak | 4317.66±0.0 | 0.0 | 32538.2 | 0.0 | 0.0 | ok |
| Hβ | 4854.9 | fit_peak | 4804.882±1.9316 | 1.307174 | 3039.9 | 4.52 | 1.87 | warning: center_at_bound |
| Hα | 6554.0 | fit_peak | 6564.217±2.0429 | 0.25465 | 1544.2 | 1.97 | 0.247 | ok |
| Hε_abs | 3963.7 | fit_peak | 4013.511±239.9695 | -0.546099 | 34034.8 | 1.36 | 1.312 | ok |
| Hδ_abs | 4096.3 | fit_peak | 4050.88±29.0715 | -0.427693 | 15264.0 | 1.14 | 0.505 | ok |
| Hγ_abs | 4334.7 | fit_peak | 4335.711±7.0928 | -0.252119 | 1796.1 | 0.73 | 0.026 | ok |
| Mg I_abs | 5168.4 | fit_peak | 5167.161±7.9551 | -0.202495 | 5433.3 | 1.12 | 0.222 | ok |
| Hα_abs | 6554.0 | fit_peak | 6515.026±0.0 | -0.0 | 108.4 | 0.0 | 0.0 | ok |
| CaT1_abs | 8484.3 | fit_peak | 8434.337±9.0721 | -1.717488 | 8238.8 | 8.54 | 31.322 | warning: center_at_bound |
| CaT2_abs | 8528.3 | fit_peak | 8478.266±15.3478 | -1.199726 | 9630.2 | 7.83 | 30.31 | warning: center_at_bound |
| CaT3_abs | 8648.1 | fit_peak | 8659.516±1.6783 | -0.104891 | 128.4 | 1.31 | 0.012 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:oii-3727 | [O II] | 3721.0 | emission |
| line:cak-3934-abs | Ca K_abs | 3928.5 | absorption |
| line:cah-3969-abs | Ca H_abs | 3963.2 | absorption |
| line:heps-3970 | Hε | 3963.7 | emission |
| line:heps-3970-abs | Hε_abs | 3963.7 | absorption |
| line:hdel-4102 | Hδ | 4096.3 | emission |
| line:hdel-4102-abs | Hδ_abs | 4096.3 | absorption |
| line:gband-4305-abs | G-band_abs | 4298.7 | absorption |
| line:hgam-4341 | Hγ | 4334.7 | emission |
| line:hgam-4341-abs | Hγ_abs | 4334.7 | absorption |
| line:hbet-4862 | Hβ | 4854.9 | emission |
| line:hbet-4862-abs | Hβ_abs | 4854.9 | absorption |
| line:oiii-4960 | [O III]a | 4952.3 | emission |
| line:oiii-5008 | [O III]b | 5000.1 | emission |
| line:mgi-5176-abs | Mg I_abs | 5168.4 | absorption |
| line:nad1-5891-abs | Na D1_abs | 5882.1 | absorption |
| line:nad-5895-abs | Na D_abs | 5886.1 | absorption |
| line:nad2-5897-abs | Na D2_abs | 5888.1 | absorption |
| line:nii-6549 | [N II]a | 6539.3 | emission |
| line:half-6564 | Hα | 6554.0 | emission |
| line:half-6564-abs | Hα_abs | 6554.0 | absorption |
| line:nii-6585 | [N II]b | 6574.7 | emission |
| line:sii-6718 | [S II]a | 6707.5 | emission |
| line:sii-6732 | [S II]b | 6721.9 | emission |
| line:cat1-8498-abs | CaT1_abs | 8484.3 | absorption |
| line:cat2-8542-abs | CaT2_abs | 8528.3 | absorption |
| line:cat3-8662-abs | CaT3_abs | 8648.1 | absorption |

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
| fit:H5:0000 | fit_doublet | emission | 4902.325 | [O III]a | yes | — |
| fit:H5:0001 | fit_doublet | emission | 4950.603 | [O III]b | yes | — |
| fit:H5:0002 | fit_doublet | emission | 6657.498 | [S II]a | yes | — |
| fit:H5:0003 | fit_doublet | emission | 6711.197 | [S II]b | yes | — |
| fit:H5:0004 | fit_doublet | emission | 6536.296 | [N II]a | yes | — |
| fit:H5:0005 | fit_doublet | emission | 6565.898 | [N II]b | yes | — |
| fit:H5:0006 | fit_doublet | absorption | 3912.517 | Ca K_abs | yes | — |
| fit:H5:0007 | fit_doublet | absorption | 4013.218 | Ca H_abs | yes | — |
| fit:H5:0008 | fit_doublet | absorption | 5923.985 | Na D1_abs | yes | — |
| fit:H5:0009 | fit_doublet | absorption | 5854.478 | Na D2_abs | yes | — |
| fit:H5:0010 | fit_peak | emission | 3671.009 | [O II] | no | center_at_bound |
| fit:H5:0011 | fit_peak | emission | 3966.532 | Hε | yes | — |
| fit:H5:0012 | fit_peak | emission | 4142.393 | Hδ | yes | — |
| fit:H5:0013 | fit_peak | emission | 4317.660 | Hγ | yes | — |
| fit:H5:0014 | fit_peak | emission | 4804.882 | Hβ | no | center_at_bound |
| fit:H5:0015 | fit_peak | emission | 6564.217 | Hα | yes | — |
| fit:H5:0016 | fit_peak | absorption | 4013.511 | Hε_abs | yes | — |
| fit:H5:0017 | fit_peak | absorption | 4050.880 | Hδ_abs | yes | — |
| fit:H5:0018 | fit_peak | absorption | 4335.711 | Hγ_abs | yes | — |
| fit:H5:0019 | fit_peak | absorption | 5167.161 | Mg I_abs | yes | — |
| fit:H5:0020 | fit_peak | absorption | 6515.026 | Hα_abs | yes | — |
| fit:H5:0021 | fit_peak | absorption | 8434.337 | CaT1_abs | no | center_at_bound |
| fit:H5:0022 | fit_peak | absorption | 8478.266 | CaT2_abs | no | center_at_bound |
| fit:H5:0023 | fit_peak | absorption | 8659.516 | CaT3_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H5/pre_analysis/branches/main/2b1deea90fe642bc808eae1624cf912f/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_cwt_feature",
            "blue_edge"
          ],
          "comment": "No CWT peak near 3721 A; fit_peak center at bound (3671.0) with zero amplitude, unselectable. Blue edge region."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "doublet_separation_fail",
            "center_deviation_large",
            "blue_edge"
          ],
          "comment": "No CWT trough near 3928.5 A. Doublet fit gave 3912.5 (16 A off) with separation fail and huge width; not credible."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "doublet_separation_fail",
            "center_deviation_large",
            "blue_edge"
          ],
          "comment": "No CWT trough near 3963.2 A. Doublet component 2 landed at 4013.2 with 52772 km/s width; unphysical, rejected."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H5:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blue_edge",
            "blend_cah"
          ],
          "comment": "Fit center 3966.5 A, offset ~3 A from prediction, low local SNR 1.8; near Ca H position, possible blend. Weak but plausible."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "broad_unphysical_width",
            "blue_edge"
          ],
          "comment": "No CWT trough at 3963.7 A; fit gave 4013.5 with 34035 km/s width, unphysical. Not adopted."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H5:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "weak_snr",
            "blue_edge"
          ],
          "comment": "Fit center 4142.4 A, ~46 A redward of prediction (weaker offset band); matches CWT peak cwt:em:0000 at 4143.2. Low SNR 3.5, marginal."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "broad_unphysical_width",
            "blue_edge"
          ],
          "comment": "No CWT trough near 4096 A; fit gave 4050.9 with 15264 km/s width, unphysical. Not adopted."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_matching_feature"
          ],
          "comment": "Nearest trough cwt:abs:0002 at 4274.4 A is ~24 A blueward (z=-0.0072); no credible G-band trough at 4298.7 A."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_feature"
          ],
          "comment": "No CWT peak near 4334.7 A; fit returned zero amplitude with 32538 km/s width. Not credible."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H5:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit center 4335.7 A, ~1 A from prediction, but low SNR 0.7 and 1796 km/s width; weak marginal absorption."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "No CWT peak near 4854.9 A; fit center at bound (4804.9) with 3040 km/s width, unselectable."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest trough cwt:abs:0006 at 4868.0 A is ~13 A redward with broad 4331 km/s width; not a clean Hbeta absorption match."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "center_deviation_large",
            "zero_amplitude_component"
          ],
          "comment": "Doublet fit gave 4902.3 (50 A off) with component 2 zero amplitude and separation fail; CWT peak cwt:em:0004 at 4912.8 is ~40 A blueward. Not credible."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "zero_amplitude_component",
            "no_cwt_feature"
          ],
          "comment": "No CWT peak near 5000 A; doublet component 2 had zero amplitude. Not adopted."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H5:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit center 5167.2 A, ~1 A from prediction, but low SNR 1.1 and 5433 km/s width; weak marginal absorption."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "center_deviation_large",
            "unphysical_width"
          ],
          "comment": "Na D doublet fit gave 5924.0 with 35751 km/s width and separation fail; no credible D1 trough at 5882 A."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "no_cwt_feature"
          ],
          "comment": "No CWT trough near 5886 A; Na D doublet fit failed separation and widths. Not adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "center_deviation_large"
          ],
          "comment": "Doublet component 2 at 5854.5 A, ~34 A blueward with 723 km/s width; separation fail, not credible."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "blend_halpha"
          ],
          "comment": "N II doublet fit gave 6536.3 A with separation fail and low SNR 2.2; blended with Halpha region, not credible."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H5:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "blend_nii"
          ],
          "comment": "Fit center 6564.2 A, ~10 A redward of prediction, low SNR 2.0 and 1544 km/s width; blended with N II. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_feature"
          ],
          "comment": "No CWT trough near 6554 A; fit returned zero amplitude at 6515.0. Not credible."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "blend_halpha"
          ],
          "comment": "N II doublet component 2 at 6565.9 A with 1283 km/s width and separation fail; blended with Halpha, not credible."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "center_deviation_large",
            "weak_snr"
          ],
          "comment": "S II doublet fit gave 6657.5 A (~50 A off) with separation fail and low SNR 1.2; not credible."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "broad_width",
            "weak_snr"
          ],
          "comment": "S II component 2 at 6711.2 A with 539 km/s width and separation fail; low SNR. Not adopted."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "red_edge"
          ],
          "comment": "Fit center at bound (8434.3) with 8239 km/s width; unselectable. Red edge region."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "red_edge"
          ],
          "comment": "Fit center at bound (8478.3) with 9630 km/s width; unselectable. Red edge region."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H5:0023",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "red_edge",
            "offset_weak"
          ],
          "comment": "Fit center 8659.5 A, ~11 A from prediction, but low SNR 1.3 and 128 km/s width; weak marginal absorption near red edge."
        }
      ]
    },
    "id": "call_00_Q190JP7SXj6vyScIW5sN6301",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 8629,
  "output_tokens": 2556,
  "total_tokens": 11185,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 7989,
  "provider_usage": {
    "completion_tokens": 2556,
    "prompt_tokens": 8629,
    "total_tokens": 11185,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 7989
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_Q190JP7SXj6vyScIW5sN6301`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 5, "line_id": "line:hdel-4102", "measurement_id": "fit:H5:0012", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
The Hδ fit at 4142.4 Å is outside the redshift window. I'll correct that line and resubmit.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H5/pre_analysis/branches/main/2b1deea90fe642bc808eae1624cf912f/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_cwt_feature",
            "blue_edge"
          ],
          "comment": "No CWT peak near 3721 A; fit_peak center at bound (3671.0) with zero amplitude, unselectable. Blue edge region."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "doublet_separation_fail",
            "center_deviation_large",
            "blue_edge"
          ],
          "comment": "No CWT trough near 3928.5 A. Doublet fit gave 3912.5 (16 A off) with separation fail and huge width; not credible."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "doublet_separation_fail",
            "center_deviation_large",
            "blue_edge"
          ],
          "comment": "No CWT trough near 3963.2 A. Doublet component 2 landed at 4013.2 with 52772 km/s width; unphysical, rejected."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H5:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blue_edge",
            "blend_cah"
          ],
          "comment": "Fit center 3966.5 A, offset ~3 A from prediction, low local SNR 1.8; near Ca H position, possible blend. Weak but plausible."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "broad_unphysical_width",
            "blue_edge"
          ],
          "comment": "No CWT trough at 3963.7 A; fit gave 4013.5 with 34035 km/s width, unphysical. Not adopted."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_matching_feature"
          ],
          "comment": "No CWT peak near 4096.3 A; nearest peak cwt:em:0000 at 4143.2 A is ~47 A redward (outside window). Fit at 4142.4 A also outside window. Not adopted."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "broad_unphysical_width",
            "blue_edge"
          ],
          "comment": "No CWT trough near 4096 A; fit gave 4050.9 with 15264 km/s width, unphysical. Not adopted."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_matching_feature"
          ],
          "comment": "Nearest trough cwt:abs:0002 at 4274.4 A is ~24 A blueward (z=-0.0072); no credible G-band trough at 4298.7 A."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_feature"
          ],
          "comment": "No CWT peak near 4334.7 A; fit returned zero amplitude with 32538 km/s width. Not credible."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H5:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit center 4335.7 A, ~1 A from prediction, but low SNR 0.7 and 1796 km/s width; weak marginal absorption."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "No CWT peak near 4854.9 A; fit center at bound (4804.9) with 3040 km/s width, unselectable."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest trough cwt:abs:0006 at 4868.0 A is ~13 A redward with broad 4331 km/s width; not a clean Hbeta absorption match."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "center_deviation_large",
            "zero_amplitude_component"
          ],
          "comment": "Doublet fit gave 4902.3 (50 A off) with component 2 zero amplitude and separation fail; CWT peak cwt:em:0004 at 4912.8 is ~40 A blueward. Not credible."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "zero_amplitude_component",
            "no_cwt_feature"
          ],
          "comment": "No CWT peak near 5000 A; doublet component 2 had zero amplitude. Not adopted."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H5:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit center 5167.2 A, ~1 A from prediction, but low SNR 1.1 and 5433 km/s width; weak marginal absorption."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "center_deviation_large",
            "unphysical_width"
          ],
          "comment": "Na D doublet fit gave 5924.0 with 35751 km/s width and separation fail; no credible D1 trough at 5882 A."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "no_cwt_feature"
          ],
          "comment": "No CWT trough near 5886 A; Na D doublet fit failed separation and widths. Not adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "center_deviation_large"
          ],
          "comment": "Doublet component 2 at 5854.5 A, ~34 A blueward with 723 km/s width; separation fail, not credible."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "blend_halpha"
          ],
          "comment": "N II doublet fit gave 6536.3 A with separation fail and low SNR 2.2; blended with Halpha region, not credible."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H5:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "blend_nii"
          ],
          "comment": "Fit center 6564.2 A, ~10 A redward of prediction, low SNR 2.0 and 1544 km/s width; blended with N II. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_feature"
          ],
          "comment": "No CWT trough near 6554 A; fit returned zero amplitude at 6515.0. Not credible."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "blend_halpha"
          ],
          "comment": "N II doublet component 2 at 6565.9 A with 1283 km/s width and separation fail; blended with Halpha, not credible."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "center_deviation_large",
            "weak_snr"
          ],
          "comment": "S II doublet fit gave 6657.5 A (~50 A off) with separation fail and low SNR 1.2; not credible."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "broad_width",
            "weak_snr"
          ],
          "comment": "S II component 2 at 6711.2 A with 539 km/s width and separation fail; low SNR. Not adopted."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "red_edge"
          ],
          "comment": "Fit center at bound (8434.3) with 8239 km/s width; unselectable. Red edge region."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "red_edge"
          ],
          "comment": "Fit center at bound (8478.3) with 9630 km/s width; unselectable. Red edge region."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H5:0023",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "red_edge",
            "offset_weak"
          ],
          "comment": "Fit center 8659.5 A, ~11 A from prediction, but low SNR 1.3 and 128 km/s width; weak marginal absorption near red edge."
        }
      ]
    },
    "id": "call_00_ZrNlF44Zj8ktapuSN0L53028",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 11289,
  "output_tokens": 2559,
  "total_tokens": 13848,
  "cache_hit_tokens": 11136,
  "cache_miss_tokens": 153,
  "provider_usage": {
    "completion_tokens": 2559,
    "prompt_tokens": 11289,
    "total_tokens": 13848,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 11136
    },
    "prompt_cache_hit_tokens": 11136,
    "prompt_cache_miss_tokens": 153
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_ZrNlF44Zj8ktapuSN0L53028`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H5/pre_analysis/branches/main/2b1deea90fe642bc808eae1624cf912f/lines.csv", "n_lines": 27, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H5/pre_analysis/branches/main/2b1deea90fe642bc808eae1624cf912f/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:40:18.427897+00:00
