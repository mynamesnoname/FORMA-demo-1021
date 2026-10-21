# SH pre-analysis session: line review

- Run ID: `graph-853b617a68f04c36bd82f06bdb770ac4`
- Hypothesis: `H4`
- Started (UTC): 2026-10-19T11:39:50.160176+00:00
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
Review every predicted line at the fixed Redrock redshift `-0.0018443601090383488`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H4/pre_analysis/branches/main/e3df65bb01e943f9871ebe0e4d525d99/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 46.6 |

Verify the redshift hypothesis z ≈ -0.0018443601090383488.

Verification window: z ∈ [-0.0118, 0.0082]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=47.8117, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=14.3734, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=35.4345, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=34.7358, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=5.98893, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/QSO_4.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H4/pre_analysis/branches/main/e3df65bb01e943f9871ebe0e4d525d99/lines.csv

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


## Predicted Lines at z = -0.0018

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [O II] | 3727.0 | 3720.1 | em | narrow | — |
| Ca K_abs | 3934.8 | 3927.5 | abs | absorption | — |
| Ca H_abs | 3969.6 | 3962.3 | abs | absorption | — |
| Hε | 3970.1 | 3962.8 | em | both | — |
| Hε_abs | 3970.1 | 3962.8 | abs | absorption | — |
| Hδ | 4102.9 | 4095.3 | em | both | — |
| Hδ_abs | 4102.9 | 4095.3 | abs | absorption | — |
| G-band_abs | 4305.6 | 4297.7 | abs | absorption | trough@4274.4±0.8(z=-0.0072) |
| Hγ | 4341.7 | 4333.7 | em | both | — |
| Hγ_abs | 4341.7 | 4333.7 | abs | absorption | — |
| Hβ | 4862.7 | 4853.7 | em | both | — |
| Hβ_abs | 4862.7 | 4853.7 | abs | absorption | trough@4868.0±0.8(z=0.0011) |
| [O III]a | 4960.3 | 4951.2 | em | narrow | peak@4912.8±0.8(z=-0.0096) |
| [O III]b | 5008.2 | 4999.0 | em | narrow | — |
| Mg I_abs | 5176.7 | 5167.2 | abs | absorption | — |
| Na D1_abs | 5891.6 | 5880.7 | abs | absorption | — |
| Na D_abs | 5895.6 | 5884.7 | abs | absorption | — |
| Na D2_abs | 5897.6 | 5886.7 | abs | absorption | — |
| [N II]a | 6549.8 | 6537.7 | em | narrow | — |
| Hα | 6564.6 | 6552.5 | em | both | — |
| Hα_abs | 6564.6 | 6552.5 | abs | absorption | — |
| [N II]b | 6585.3 | 6573.2 | em | narrow | — |
| [S II]a | 6718.3 | 6705.9 | em | narrow | — |
| [S II]b | 6732.7 | 6720.3 | em | narrow | — |
| CaT1_abs | 8498.0 | 8482.3 | abs | absorption | — |
| CaT2_abs | 8542.0 | 8526.2 | abs | absorption | — |
| CaT3_abs | 8662.0 | 8646.0 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 4951.2/4999.0 | fit_doublet | 4901.151±292.4508/4996.405±0.0 | 0.134205/0.0 | 25926.7/331.5 | 0.53 | 0.142 | warning: center_1_deviation_large; separation fail; component ratio 0.0 |
| [S II]a/[S II]b | 6705.9/6720.3 | fit_doublet | 6713.925±0.7135/6670.282±182.6874 | 0.18095/0.129733 | 105.1/28093.5 | 1.42 | 0.736 | warning: center_2_deviation_large; separation fail; component ratio 0.72 |
| [N II]a/[N II]b | 6537.7/6573.2 | fit_doublet | 6536.312±1.2387/6565.897±1.6134 | 0.18983/0.28141 | 347.9/1279.0 | 2.23 | 0.2 | warning; separation fail; component ratio 1.48 |
| Ca K_abs/Ca H_abs | 3927.5/3962.3 | fit_doublet | 3977.543±0.8656/4012.279±223434.0571 | -0.0/-1.751622 | 53245.7/52784.8 | 3.66 | 9.742 | warning: center_1_deviation_large, center_2_deviation_large; separation pass |
| Na D1_abs/Na D2_abs | 5880.7/5886.7 | fit_doublet | 5905.346±207.3154/5890.505±3.7401 | -1.665024/-0.397596 | 35863.6/119.8 | 5.17 | 19.762 | warning; separation fail; component ratio 0.24 |
| [O II] | 3720.1 | fit_peak | 3769.626±0.0 | 0.0 | 187.4 | 0.0 | -0.0 | ok |
| Hε | 3962.8 | fit_peak | 3966.537±0.6463 | 0.728668 | 198.2 | 1.83 | 0.016 | ok |
| Hδ | 4095.3 | fit_peak | 4142.394±0.7409 | 1.269136 | 471.0 | 3.49 | 0.15 | ok |
| Hγ | 4333.7 | fit_peak | 4316.235±0.0 | 0.0 | 1010.8 | 0.0 | -0.0 | ok |
| Hβ | 4853.7 | fit_peak | 4803.731±1.7767 | 1.371902 | 2906.7 | 4.71 | 1.944 | warning: center_at_bound |
| Hα | 6552.5 | fit_peak | 6564.209±2.0426 | 0.255213 | 1554.1 | 1.97 | 0.249 | ok |
| Hε_abs | 3962.8 | fit_peak | 4012.778±11.49 | -0.373068 | 10334.3 | 0.92 | 0.221 | warning: center_at_bound |
| Hδ_abs | 4095.3 | fit_peak | 4045.493±33.8688 | -0.478765 | 16434.8 | 1.28 | 0.674 | ok |
| Hγ_abs | 4333.7 | fit_peak | 4335.706±7.147 | -0.24919 | 1779.0 | 0.72 | 0.025 | ok |
| Mg I_abs | 5167.2 | fit_peak | 5163.934±7.6875 | -0.197706 | 5120.1 | 1.09 | 0.196 | ok |
| Hα_abs | 6552.5 | fit_peak | 6502.495±0.0 | -0.0 | 108.6 | 0.0 | -0.0 | warning: center_at_bound |
| CaT1_abs | 8482.3 | fit_peak | 8432.327±9.0321 | -1.721819 | 8252.2 | 8.81 | 33.367 | warning: center_at_bound |
| CaT2_abs | 8526.2 | fit_peak | 8476.245±14.4719 | -1.197313 | 9474.8 | 8.11 | 32.086 | warning: center_at_bound |
| CaT3_abs | 8646.0 | fit_peak | 8696.024±480.3448 | -0.098365 | 16236.3 | 1.17 | 0.983 | warning: center_at_bound |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:oii-3727 | [O II] | 3720.1 | emission |
| line:cak-3934-abs | Ca K_abs | 3927.5 | absorption |
| line:cah-3969-abs | Ca H_abs | 3962.3 | absorption |
| line:heps-3970 | Hε | 3962.8 | emission |
| line:heps-3970-abs | Hε_abs | 3962.8 | absorption |
| line:hdel-4102 | Hδ | 4095.3 | emission |
| line:hdel-4102-abs | Hδ_abs | 4095.3 | absorption |
| line:gband-4305-abs | G-band_abs | 4297.7 | absorption |
| line:hgam-4341 | Hγ | 4333.7 | emission |
| line:hgam-4341-abs | Hγ_abs | 4333.7 | absorption |
| line:hbet-4862 | Hβ | 4853.7 | emission |
| line:hbet-4862-abs | Hβ_abs | 4853.7 | absorption |
| line:oiii-4960 | [O III]a | 4951.2 | emission |
| line:oiii-5008 | [O III]b | 4999.0 | emission |
| line:mgi-5176-abs | Mg I_abs | 5167.2 | absorption |
| line:nad1-5891-abs | Na D1_abs | 5880.7 | absorption |
| line:nad-5895-abs | Na D_abs | 5884.7 | absorption |
| line:nad2-5897-abs | Na D2_abs | 5886.7 | absorption |
| line:nii-6549 | [N II]a | 6537.7 | emission |
| line:half-6564 | Hα | 6552.5 | emission |
| line:half-6564-abs | Hα_abs | 6552.5 | absorption |
| line:nii-6585 | [N II]b | 6573.2 | emission |
| line:sii-6718 | [S II]a | 6705.9 | emission |
| line:sii-6732 | [S II]b | 6720.3 | emission |
| line:cat1-8498-abs | CaT1_abs | 8482.3 | absorption |
| line:cat2-8542-abs | CaT2_abs | 8526.2 | absorption |
| line:cat3-8662-abs | CaT3_abs | 8646.0 | absorption |

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
| fit:H4:0000 | fit_doublet | emission | 4901.151 | [O III]a | yes | — |
| fit:H4:0001 | fit_doublet | emission | 4996.405 | [O III]b | yes | — |
| fit:H4:0002 | fit_doublet | emission | 6713.925 | [S II]a | yes | — |
| fit:H4:0003 | fit_doublet | emission | 6670.282 | [S II]b | yes | — |
| fit:H4:0004 | fit_doublet | emission | 6536.312 | [N II]a | yes | — |
| fit:H4:0005 | fit_doublet | emission | 6565.897 | [N II]b | yes | — |
| fit:H4:0006 | fit_doublet | absorption | 3977.543 | Ca K_abs | yes | — |
| fit:H4:0007 | fit_doublet | absorption | 4012.279 | Ca H_abs | yes | — |
| fit:H4:0008 | fit_doublet | absorption | 5905.346 | Na D1_abs | yes | — |
| fit:H4:0009 | fit_doublet | absorption | 5890.505 | Na D2_abs | yes | — |
| fit:H4:0010 | fit_peak | emission | 3769.626 | [O II] | yes | — |
| fit:H4:0011 | fit_peak | emission | 3966.537 | Hε | yes | — |
| fit:H4:0012 | fit_peak | emission | 4142.394 | Hδ | yes | — |
| fit:H4:0013 | fit_peak | emission | 4316.235 | Hγ | yes | — |
| fit:H4:0014 | fit_peak | emission | 4803.731 | Hβ | no | center_at_bound |
| fit:H4:0015 | fit_peak | emission | 6564.209 | Hα | yes | — |
| fit:H4:0016 | fit_peak | absorption | 4012.778 | Hε_abs | no | center_at_bound |
| fit:H4:0017 | fit_peak | absorption | 4045.493 | Hδ_abs | yes | — |
| fit:H4:0018 | fit_peak | absorption | 4335.706 | Hγ_abs | yes | — |
| fit:H4:0019 | fit_peak | absorption | 5163.934 | Mg I_abs | yes | — |
| fit:H4:0020 | fit_peak | absorption | 6502.495 | Hα_abs | no | center_at_bound |
| fit:H4:0021 | fit_peak | absorption | 8432.327 | CaT1_abs | no | center_at_bound |
| fit:H4:0022 | fit_peak | absorption | 8476.245 | CaT2_abs | no | center_at_bound |
| fit:H4:0023 | fit_peak | absorption | 8696.024 | CaT3_abs | no | center_at_bound |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H4/pre_analysis/branches/main/e3df65bb01e943f9871ebe0e4d525d99/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "zero_amp_fit",
            "blue_edge"
          ],
          "comment": "No CWT peak near 3720 A; fit_peak returned zero amplitude at 3769.6 (offset ~50 A). Blue edge, no credible signal."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_deviation",
            "no_cwt_feature",
            "blend_cah"
          ],
          "comment": "Doublet fit placed Ca K at 3977.5 (offset ~50 A) with near-zero amplitude; no CWT trough at 3927.5. Not adopted."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_unconstrained",
            "huge_error",
            "blend_cak"
          ],
          "comment": "Ca H fit centre 4012.3 with error ~2e5 A and depth -1.75; unconstrained, no CWT trough at 3962.3. Not adopted."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H4:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blend_cah",
            "offset_4A"
          ],
          "comment": "Fit centre 3966.5 (offset ~4 A) amp 0.73, local SNR 1.8; weak and blended with Ca H region. Marginal."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "unselectable_fit"
          ],
          "comment": "Absorption fit centre at bound (4012.8), unselectable; no credible trough at 3962.8."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H4:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_47A",
            "weak_snr",
            "blend"
          ],
          "comment": "Fit centre 4142.4 (offset ~47 A) coincides with CWT peak 4143.2; weak SNR 3.5, large offset. Marginal."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H4:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_50A",
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit centre 4045.5 (offset ~50 A), amp -0.48, local SNR 1.3, very broad FWHM. Weak marginal."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_23A",
            "weak_feature",
            "no_fit"
          ],
          "comment": "Only nearby trough is 4274.4 (offset ~23 A, z=-0.0072), weak amp -0.4; no fit attempted. Not adopted."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amp_fit",
            "no_cwt_feature"
          ],
          "comment": "Fit_peak returned zero amplitude at 4316.2; no CWT peak near 4333.7. Not adopted."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H4:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "offset_2A"
          ],
          "comment": "Fit centre 4335.7 (offset ~2 A) amp -0.25, local SNR 0.7, broad FWHM 1779 km/s. Weak marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "unselectable_fit"
          ],
          "comment": "Fit centre at bound (4803.7), unselectable; no CWT peak at 4853.7. Not adopted."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_14A",
            "broad_absorption",
            "no_fit"
          ],
          "comment": "Nearest trough 4868.0 (offset ~14 A) is broad (4331 km/s) and likely unrelated; no targeted fit. Not adopted."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "center_deviation_large",
            "separation_fail"
          ],
          "comment": "Doublet fit centre 4901.2 with huge error, component ratio 0; separation fail. CWT peak 4912.8 is offset ~38 A. Not adopted."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Second component amplitude 0.0 in failed doublet fit; no CWT peak at 4999.0. Not adopted."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H4:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "offset_3A"
          ],
          "comment": "Fit centre 5163.9 (offset ~3 A) amp -0.20, local SNR 1.1, very broad FWHM. Weak marginal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "center_deviation_large",
            "separation_fail"
          ],
          "comment": "Na D doublet fit placed D1 at 5905.3 with error ~207 A; separation fail, ratio 0.24. Not adopted."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "blend_nad"
          ],
          "comment": "No CWT trough at 5884.7; blended Na D region unresolved by failed doublet fit. Not adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H4:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_fit_warning",
            "separation_fail",
            "blend_nad"
          ],
          "comment": "Fit centre 5890.5 (offset ~4 A) amp -0.40, local SNR 5.2; doublet separation failed and D1 unconstrained, so depth ordering unreliable. Marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H4:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_fit_warning",
            "separation_fail",
            "blend_halpha"
          ],
          "comment": "Fit centre 6536.3 (offset ~1 A) amp 0.19, local SNR 2.2; separation fail, blended with Halpha region. Marginal."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H4:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blend_nii",
            "broad_width"
          ],
          "comment": "Fit centre 6564.2 (offset ~12 A) amp 0.26, local SNR 2.0, broad FWHM; blended with [N II]. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "zero_amplitude",
            "unselectable_fit"
          ],
          "comment": "Absorption fit centre at bound (6502.5) with zero amplitude; unselectable. Not adopted."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H4:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_fit_warning",
            "separation_fail",
            "blend_halpha"
          ],
          "comment": "Fit centre 6565.9 (offset ~7 A) amp 0.28, local SNR 2.2; separation fail, blended with Halpha. Marginal."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H4:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_fit_warning",
            "separation_fail",
            "weak_snr"
          ],
          "comment": "Fit centre 6713.9 (offset ~8 A) amp 0.18, local SNR 1.4; doublet separation failed, second component unconstrained. Marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "center_deviation_large",
            "separation_fail"
          ],
          "comment": "Second S II component fit at 6670.3 with error ~183 A; separation fail. Not adopted."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "unselectable_fit",
            "red_edge"
          ],
          "comment": "Fit centre at bound (8432.3), unselectable; no CWT trough at 8482.3. Not adopted."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "unselectable_fit",
            "red_edge"
          ],
          "comment": "Fit centre at bound (8476.2), unselectable; no CWT trough at 8526.2. Not adopted."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "unselectable_fit",
            "red_edge"
          ],
          "comment": "Fit centre at bound (8696.0) with huge error; unselectable. Not adopted."
        }
      ]
    },
    "id": "call_00_vsFaAIPUXwZ07H2aFtxk3504",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 8664,
  "output_tokens": 2579,
  "total_tokens": 11243,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 8024,
  "provider_usage": {
    "completion_tokens": 2579,
    "prompt_tokens": 8664,
    "total_tokens": 11243,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 8024
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_vsFaAIPUXwZ07H2aFtxk3504`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 5, "line_id": "line:hdel-4102", "measurement_id": "fit:H4:0012", "reason": "measurement is outside this line's redshift window"}, {"row": 6, "line_id": "line:hdel-4102-abs", "measurement_id": "fit:H4:0017", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
The Hδ fits are outside the redshift window; I'll mark those as NOT_FOUND and resubmit.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H4/pre_analysis/branches/main/e3df65bb01e943f9871ebe0e4d525d99/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "zero_amp_fit",
            "blue_edge"
          ],
          "comment": "No CWT peak near 3720 A; fit_peak returned zero amplitude at 3769.6 (offset ~50 A). Blue edge, no credible signal."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_deviation",
            "no_cwt_feature",
            "blend_cah"
          ],
          "comment": "Doublet fit placed Ca K at 3977.5 (offset ~50 A) with near-zero amplitude; no CWT trough at 3927.5. Not adopted."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_unconstrained",
            "huge_error",
            "blend_cak"
          ],
          "comment": "Ca H fit centre 4012.3 with error ~2e5 A and depth -1.75; unconstrained, no CWT trough at 3962.3. Not adopted."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H4:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blend_cah",
            "offset_4A"
          ],
          "comment": "Fit centre 3966.5 (offset ~4 A) amp 0.73, local SNR 1.8; weak and blended with Ca H region. Marginal."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "unselectable_fit"
          ],
          "comment": "Absorption fit centre at bound (4012.8), unselectable; no credible trough at 3962.8."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "outside_z_window",
            "offset_47A",
            "weak_snr"
          ],
          "comment": "Only fit centre 4142.4 lies outside the redshift window (offset ~47 A); no in-window CWT peak at 4095.3. Not adopted."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "outside_z_window",
            "offset_50A",
            "weak_snr"
          ],
          "comment": "Only fit centre 4045.5 lies outside the redshift window (offset ~50 A); no in-window trough at 4095.3. Not adopted."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_23A",
            "weak_feature",
            "no_fit"
          ],
          "comment": "Only nearby trough is 4274.4 (offset ~23 A, z=-0.0072), weak amp -0.4; no fit attempted. Not adopted."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amp_fit",
            "no_cwt_feature"
          ],
          "comment": "Fit_peak returned zero amplitude at 4316.2; no CWT peak near 4333.7. Not adopted."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H4:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "offset_2A"
          ],
          "comment": "Fit centre 4335.7 (offset ~2 A) amp -0.25, local SNR 0.7, broad FWHM 1779 km/s. Weak marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "unselectable_fit"
          ],
          "comment": "Fit centre at bound (4803.7), unselectable; no CWT peak at 4853.7. Not adopted."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_14A",
            "broad_absorption",
            "no_fit"
          ],
          "comment": "Nearest trough 4868.0 (offset ~14 A) is broad (4331 km/s) and likely unrelated; no targeted fit. Not adopted."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "center_deviation_large",
            "separation_fail"
          ],
          "comment": "Doublet fit centre 4901.2 with huge error, component ratio 0; separation fail. CWT peak 4912.8 is offset ~38 A. Not adopted."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Second component amplitude 0.0 in failed doublet fit; no CWT peak at 4999.0. Not adopted."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H4:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "offset_3A"
          ],
          "comment": "Fit centre 5163.9 (offset ~3 A) amp -0.20, local SNR 1.1, very broad FWHM. Weak marginal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "center_deviation_large",
            "separation_fail"
          ],
          "comment": "Na D doublet fit placed D1 at 5905.3 with error ~207 A; separation fail, ratio 0.24. Not adopted."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "blend_nad"
          ],
          "comment": "No CWT trough at 5884.7; blended Na D region unresolved by failed doublet fit. Not adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H4:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_fit_warning",
            "separation_fail",
            "blend_nad"
          ],
          "comment": "Fit centre 5890.5 (offset ~4 A) amp -0.40, local SNR 5.2; doublet separation failed and D1 unconstrained, so depth ordering unreliable. Marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H4:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_fit_warning",
            "separation_fail",
            "blend_halpha"
          ],
          "comment": "Fit centre 6536.3 (offset ~1 A) amp 0.19, local SNR 2.2; separation fail, blended with Halpha region. Marginal."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H4:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "blend_nii",
            "broad_width"
          ],
          "comment": "Fit centre 6564.2 (offset ~12 A) amp 0.26, local SNR 2.0, broad FWHM; blended with [N II]. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "zero_amplitude",
            "unselectable_fit"
          ],
          "comment": "Absorption fit centre at bound (6502.5) with zero amplitude; unselectable. Not adopted."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H4:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_fit_warning",
            "separation_fail",
            "blend_halpha"
          ],
          "comment": "Fit centre 6565.9 (offset ~7 A) amp 0.28, local SNR 2.2; separation fail, blended with Halpha. Marginal."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H4:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_fit_warning",
            "separation_fail",
            "weak_snr"
          ],
          "comment": "Fit centre 6713.9 (offset ~8 A) amp 0.18, local SNR 1.4; doublet separation failed, second component unconstrained. Marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "center_deviation_large",
            "separation_fail"
          ],
          "comment": "Second S II component fit at 6670.3 with error ~183 A; separation fail. Not adopted."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "unselectable_fit",
            "red_edge"
          ],
          "comment": "Fit centre at bound (8432.3), unselectable; no CWT trough at 8482.3. Not adopted."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "unselectable_fit",
            "red_edge"
          ],
          "comment": "Fit centre at bound (8476.2), unselectable; no CWT trough at 8526.2. Not adopted."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "unselectable_fit",
            "red_edge"
          ],
          "comment": "Fit centre at bound (8696.0) with huge error; unselectable. Not adopted."
        }
      ]
    },
    "id": "call_00_GD6SVbqlfFxUqUhs3Rrr5721",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 11394,
  "output_tokens": 2571,
  "total_tokens": 13965,
  "cache_hit_tokens": 11136,
  "cache_miss_tokens": 258,
  "provider_usage": {
    "completion_tokens": 2571,
    "prompt_tokens": 11394,
    "total_tokens": 13965,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 11136
    },
    "prompt_cache_hit_tokens": 11136,
    "prompt_cache_miss_tokens": 258
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_GD6SVbqlfFxUqUhs3Rrr5721`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H4/pre_analysis/branches/main/e3df65bb01e943f9871ebe0e4d525d99/lines.csv", "n_lines": 27, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H4/pre_analysis/branches/main/e3df65bb01e943f9871ebe0e4d525d99/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:40:07.330055+00:00
