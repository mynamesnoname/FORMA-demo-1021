# SH pre-analysis session: line review

- Run ID: `graph-fe0d30030bcc4939b88103e27753b2c1`
- Hypothesis: `H6`
- Started (UTC): 2026-10-19T11:18:53.641779+00:00
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
Review every predicted line at the fixed Redrock redshift `0.4507518950523264`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H6/pre_analysis/branches/main/5191281cf53b43bcb6ef3de04f7b0f4a/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 5.3 |

Verify the redshift hypothesis z ≈ 0.4507518950523264.

Verification window: z ∈ [0.4408, 0.4608]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=69.491, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=20.8908, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=51.5017, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=50.4862, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=8.70451, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/ELG_6.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H6/pre_analysis/branches/main/5191281cf53b43bcb6ef3de04f7b0f4a/lines.csv

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


## Predicted Lines at z = 0.4508

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| Mg II | 2800.0 | 4062.1 | em | broad | — |
| Mg II_abs | 2800.0 | 4062.1 | abs | absorption | — |
| [Ne V] | 3426.0 | 4970.3 | em | narrow | — |
| [O II] | 3727.0 | 5407.0 | em | narrow | peak@5381.6±0.8(z=0.4439) |
| Ca K_abs | 3934.8 | 5708.4 | abs | absorption | — |
| Ca H_abs | 3969.6 | 5758.9 | abs | absorption | — |
| Hε | 3970.1 | 5759.6 | em | both | — |
| Hε_abs | 3970.1 | 5759.6 | abs | absorption | — |
| Hδ | 4102.9 | 5952.3 | em | both | — |
| Hδ_abs | 4102.9 | 5952.3 | abs | absorption | — |
| G-band_abs | 4305.6 | 6246.4 | abs | absorption | — |
| Hγ | 4341.7 | 6298.7 | em | both | — |
| Hγ_abs | 4341.7 | 6298.7 | abs | absorption | — |
| Hβ | 4862.7 | 7054.6 | em | both | — |
| Hβ_abs | 4862.7 | 7054.6 | abs | absorption | — |
| [O III]a | 4960.3 | 7196.2 | em | narrow | — |
| [O III]b | 5008.2 | 7265.7 | em | narrow | peak@7265.6±0.8(z=0.4507), peak@7288.8±0.8(z=0.4554) |
| Mg I_abs | 5176.7 | 7510.1 | abs | absorption | trough@7492.0±0.8(z=0.4473), trough@7463.2±0.8(z=0.4417) |
| Na D1_abs | 5891.6 | 8547.2 | abs | absorption | — |
| Na D_abs | 5895.6 | 8553.1 | abs | absorption | — |
| Na D2_abs | 5897.6 | 8556.0 | abs | absorption | — |
| [N II]a | 6549.8 | 9502.1 | em | narrow | peak@9477.6±0.8(z=0.4470), peak@9440.8±0.8(z=0.4414) |
| Hα | 6564.6 | 9523.6 | em | both | peak@9477.6±0.8(z=0.4437) |
| Hα_abs | 6564.6 | 9523.6 | abs | absorption | trough@9480.8±0.8(z=0.4442), trough@9462.4±0.8(z=0.4414) |
| [N II]b | 6585.3 | 9553.6 | em | narrow | — |
| [S II]a | 6718.3 | 9746.6 | em | narrow | — |
| [S II]b | 6732.7 | 9767.5 | em | narrow | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 7196.2/7265.7 | fit_doublet | 7204.715±4.9149/7265.679±0.0131 | 0.086332/32.514375 | 98.0/97.2 | 316.74 | 302.014 | warning; separation fail; component ratio 376.62 |
| [S II]a/[S II]b | 9746.6/9767.5 | fit_doublet | 9696.586±2301.3122/9732.982±2.1715 | 0.207814/0.095674 | 21841.4/81.8 | 1.78 | 2.774 | warning: center_1_deviation_large; separation fail; component ratio 0.46 |
| [N II]a/[N II]b | 9502.1/9553.6 | fit_doublet | 9507.316±1.2817/9582.009±65.5953 | 0.19526/0.023856 | 74.3/2781.3 | 1.82 | 0.016 | warning; separation fail; component ratio 0.12 |
| Ca K_abs/Ca H_abs | 5708.4/5758.9 | fit_doublet | 5658.419±58.2691/5808.847±261.4972 | -0.533617/-0.313728 | 5751.3/11133.3 | 1.88 | 1.046 | warning; separation fail |
| Na D1_abs/Na D2_abs | 8547.2/8556.0 | fit_doublet | 8539.594±1.237/8563.162±1.4494 | -0.10979/-0.095954 | 82.7/86.5 | 1.28 | 0.009 | warning; separation fail; component ratio 0.87 |
| Mg II | 4062.1 | fit_peak | 4112.105±4.7055 | 1.331661 | 3624.3 | 3.54 | 1.171 | warning: center_at_bound |
| [Ne V] | 4970.3 | fit_peak | 4990.192±1.329 | 0.237968 | 141.5 | 1.43 | 0.009 | ok |
| Hε | 5759.6 | fit_peak | 5805.394±1.604 | 0.109184 | 121.6 | 0.7 | 0.002 | ok |
| Hδ | 5952.3 | fit_peak | 5958.41±1.7406 | 0.124747 | 314.4 | 1.04 | 0.014 | ok |
| Hγ | 6298.7 | fit_peak | 6304.666±0.5651 | 0.179744 | 112.0 | 1.8 | 0.014 | ok |
| Hβ | 7054.6 | fit_peak | 7004.571±0.0 | 0.0 | 4920.4 | 0.0 | 0.0 | warning: center_at_bound |
| Mg II_abs | 4062.1 | fit_peak | 4057.749±17.8556 | -0.375117 | 3956.0 | 1.15 | 0.133 | ok |
| Hε_abs | 5759.6 | fit_peak | 5800.284±3.0375 | -0.120531 | 121.7 | 0.77 | 0.004 | ok |
| Hδ_abs | 5952.3 | fit_peak | 5946.732±0.5739 | -0.231889 | 118.7 | 1.93 | 0.018 | ok |
| G-band_abs | 6246.4 | fit_peak | 6245.75±1.3611 | -0.121937 | 295.9 | 1.26 | 0.018 | ok |
| Hγ_abs | 6298.7 | fit_peak | 6248.73±2.1868 | -0.08975 | 421.3 | 0.87 | 0.012 | warning: center_at_bound |
| Hβ_abs | 7054.6 | fit_peak | 7066.726±2.6975 | -0.066781 | 241.1 | 0.76 | 0.006 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:mgii-2800 | Mg II | 4062.1 | emission |
| line:mgii-2800-abs | Mg II_abs | 4062.1 | absorption |
| line:nev-3426 | [Ne V] | 4970.3 | emission |
| line:oii-3727 | [O II] | 5407.0 | emission |
| line:cak-3934-abs | Ca K_abs | 5708.4 | absorption |
| line:cah-3969-abs | Ca H_abs | 5758.9 | absorption |
| line:heps-3970 | Hε | 5759.6 | emission |
| line:heps-3970-abs | Hε_abs | 5759.6 | absorption |
| line:hdel-4102 | Hδ | 5952.3 | emission |
| line:hdel-4102-abs | Hδ_abs | 5952.3 | absorption |
| line:gband-4305-abs | G-band_abs | 6246.4 | absorption |
| line:hgam-4341 | Hγ | 6298.7 | emission |
| line:hgam-4341-abs | Hγ_abs | 6298.7 | absorption |
| line:hbet-4862 | Hβ | 7054.6 | emission |
| line:hbet-4862-abs | Hβ_abs | 7054.6 | absorption |
| line:oiii-4960 | [O III]a | 7196.2 | emission |
| line:oiii-5008 | [O III]b | 7265.7 | emission |
| line:mgi-5176-abs | Mg I_abs | 7510.1 | absorption |
| line:nad1-5891-abs | Na D1_abs | 8547.2 | absorption |
| line:nad-5895-abs | Na D_abs | 8553.1 | absorption |
| line:nad2-5897-abs | Na D2_abs | 8556.0 | absorption |
| line:nii-6549 | [N II]a | 9502.1 | emission |
| line:half-6564 | Hα | 9523.6 | emission |
| line:half-6564-abs | Hα_abs | 9523.6 | absorption |
| line:nii-6585 | [N II]b | 9553.6 | emission |
| line:sii-6718 | [S II]a | 9746.6 | emission |
| line:sii-6732 | [S II]b | 9767.5 | emission |

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
| fit:H6:0000 | fit_doublet | emission | 7204.715 | [O III]a | yes | — |
| fit:H6:0001 | fit_doublet | emission | 7265.679 | [O III]b | yes | — |
| fit:H6:0002 | fit_doublet | emission | 9696.586 | [S II]a | yes | — |
| fit:H6:0003 | fit_doublet | emission | 9732.982 | [S II]b | yes | — |
| fit:H6:0004 | fit_doublet | emission | 9507.316 | [N II]a | yes | — |
| fit:H6:0005 | fit_doublet | emission | 9582.009 | [N II]b | yes | — |
| fit:H6:0006 | fit_doublet | absorption | 5658.419 | Ca K_abs | yes | — |
| fit:H6:0007 | fit_doublet | absorption | 5808.847 | Ca H_abs | yes | — |
| fit:H6:0008 | fit_doublet | absorption | 8539.594 | Na D1_abs | yes | — |
| fit:H6:0009 | fit_doublet | absorption | 8563.162 | Na D2_abs | yes | — |
| fit:H6:0010 | fit_peak | emission | 4112.105 | Mg II | no | center_at_bound |
| fit:H6:0011 | fit_peak | emission | 4990.192 | [Ne V] | yes | — |
| fit:H6:0012 | fit_peak | emission | 5805.394 | Hε | yes | — |
| fit:H6:0013 | fit_peak | emission | 5958.410 | Hδ | yes | — |
| fit:H6:0014 | fit_peak | emission | 6304.666 | Hγ | yes | — |
| fit:H6:0015 | fit_peak | emission | 7004.571 | Hβ | no | center_at_bound |
| fit:H6:0016 | fit_peak | absorption | 4057.749 | Mg II_abs | yes | — |
| fit:H6:0017 | fit_peak | absorption | 5800.284 | Hε_abs | yes | — |
| fit:H6:0018 | fit_peak | absorption | 5946.732 | Hδ_abs | yes | — |
| fit:H6:0019 | fit_peak | absorption | 6245.750 | G-band_abs | yes | — |
| fit:H6:0020 | fit_peak | absorption | 6248.730 | Hγ_abs | no | center_at_bound |
| fit:H6:0021 | fit_peak | absorption | 7066.726 | Hβ_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H6/pre_analysis/branches/main/5191281cf53b43bcb6ef3de04f7b0f4a/lines.csv",
      "lines": [
        {
          "line_id": "line:mgii-2800",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_match"
          ],
          "comment": "Only fit is center_at_bound (4112.1, unselectable); no CWT peak near 4062.1. No credible measurement."
        },
        {
          "line_id": "line:mgii-2800-abs",
          "measurement_id": "fit:H6:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit at 4057.7 (offset ~4 A) but very broad FWHM ~3956 km/s and low SNR; weak marginal absorption."
        },
        {
          "line_id": "line:nev-3426",
          "measurement_id": "fit:H6:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "no_cwt_match"
          ],
          "comment": "Fit at 4990.2, offset ~20 A, low local SNR 1.43; no CWT peak. Weak marginal."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Nearest CWT peak 5381.6 implies z=0.4439, ~25 A blueward of 5407; no targeted fit. Not adopted."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "center_deviation_large",
            "no_cwt_match"
          ],
          "comment": "Doublet fit center 5658.4 deviates ~50 A from 5708.4 and separation fails; no CWT trough. Not adopted."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "center_deviation_large",
            "no_cwt_match"
          ],
          "comment": "Fit center 5808.8 deviates ~50 A from 5758.9, huge FWHM, separation fails; no CWT trough. Not adopted."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H6:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit at 5805.4, offset ~46 A, low SNR 0.7; weak marginal emission."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H6:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit at 5800.3, offset ~41 A, low SNR 0.77; weak marginal absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H6:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit at 5958.4, offset ~6 A, but FWHM ~314 km/s and low SNR 1.04; marginal."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H6:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr"
          ],
          "comment": "Fit at 5946.7, offset ~6 A, low SNR 1.93; weak marginal absorption."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H6:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit at 6245.8, offset ~1 A, but FWHM ~296 km/s and low SNR 1.26; marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H6:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr"
          ],
          "comment": "Fit at 6304.7, offset ~6 A, low SNR 1.8; weak marginal emission."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_match"
          ],
          "comment": "Only fit is center_at_bound (6248.7, unselectable); no CWT trough near 6298.7. Not adopted."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_match"
          ],
          "comment": "Only fit is center_at_bound with zero amplitude (7004.6, unselectable); no CWT peak near 7054.6. Not adopted."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "fit:H6:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit at 7066.7, offset ~12 A, low SNR 0.76; weak marginal absorption."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "component_ratio_fail",
            "no_cwt_match"
          ],
          "comment": "Doublet fit component 1 at 7204.7 with tiny amplitude 0.086 vs 32.5, ratio 377, separation fails; no CWT peak at 7196. Not adopted."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "cwt:em:0012",
          "status": "LIKELY",
          "reason_codes": [
            "strong_snr",
            "ridge_persistent"
          ],
          "comment": "CWT peak 7265.6 (z=0.4507) matches predicted 7265.7 within 0.1 A; SNR 327, ridge 24. Strong detection."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Nearest CWT troughs 7492.0 (z=0.4473) and 7463.2 (z=0.4417) are 18-47 A blueward of 7510.1; no targeted fit. Not adopted."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "center_deviation_large",
            "no_cwt_match"
          ],
          "comment": "Doublet fit center 8539.6 deviates ~8 A and separation fails; no CWT trough near 8547. Not adopted."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_match",
            "no_fit"
          ],
          "comment": "No CWT trough and no targeted fit at 8553.1; not adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "center_deviation_large",
            "no_cwt_match"
          ],
          "comment": "Doublet fit center 8563.2 deviates ~7 A and separation fails; no CWT trough near 8556. Not adopted."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "component_ratio_fail",
            "no_cwt_match"
          ],
          "comment": "Doublet fit component 1 at 9507.3, ratio 0.12, separation fails; CWT peaks 9440.8/9477.6 are 24-61 A blueward. Not adopted."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Nearest CWT peak 9477.6 implies z=0.4437, ~46 A blueward of 9523.6; no targeted fit. Not adopted."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "CWT troughs 9480.8/9462.4 are 43-61 A blueward of 9523.6; no targeted fit. Not adopted."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "center_deviation_large",
            "no_cwt_match"
          ],
          "comment": "Doublet fit component 2 at 9582.0 deviates ~28 A with huge FWHM, separation fails; no CWT peak near 9553.6. Not adopted."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_deviation_large",
            "separation_fail",
            "no_cwt_match"
          ],
          "comment": "Doublet fit component 1 at 9696.6 with enormous error/FWHM, separation fails; no CWT peak near 9746.6. Not adopted."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_deviation_large",
            "separation_fail",
            "no_cwt_match"
          ],
          "comment": "Doublet fit component 2 at 9733.0 deviates ~35 A, separation fails; no CWT peak near 9767.5. Not adopted."
        }
      ]
    },
    "id": "call_00_gVbWguUtipQFG6k1XOMy4323",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 8143,
  "output_tokens": 2474,
  "total_tokens": 10617,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 7503,
  "provider_usage": {
    "completion_tokens": 2474,
    "prompt_tokens": 8143,
    "total_tokens": 10617,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 7503
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_gVbWguUtipQFG6k1XOMy4323`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 6, "line_id": "line:heps-3970", "measurement_id": "fit:H6:0012", "reason": "measurement is outside this line's redshift window"}, {"row": 7, "line_id": "line:heps-3970-abs", "measurement_id": "fit:H6:0017", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
The Hε fits (5805.4, 5800.3) fall outside the redshift window for that line. I'll set those to NOT_FOUND and resubmit.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H6/pre_analysis/branches/main/5191281cf53b43bcb6ef3de04f7b0f4a/lines.csv",
      "lines": [
        {
          "line_id": "line:mgii-2800",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_match"
          ],
          "comment": "Only fit is center_at_bound (4112.1, unselectable); no CWT peak near 4062.1. No credible measurement."
        },
        {
          "line_id": "line:mgii-2800-abs",
          "measurement_id": "fit:H6:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit at 4057.7 (offset ~4 A) but very broad FWHM ~3956 km/s and low SNR; weak marginal absorption."
        },
        {
          "line_id": "line:nev-3426",
          "measurement_id": "fit:H6:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "no_cwt_match"
          ],
          "comment": "Fit at 4990.2, offset ~20 A, low local SNR 1.43; no CWT peak. Weak marginal."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Nearest CWT peak 5381.6 implies z=0.4439, ~25 A blueward of 5407; no targeted fit. Not adopted."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "center_deviation_large",
            "no_cwt_match"
          ],
          "comment": "Doublet fit center 5658.4 deviates ~50 A from 5708.4 and separation fails; no CWT trough. Not adopted."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "center_deviation_large",
            "no_cwt_match"
          ],
          "comment": "Fit center 5808.8 deviates ~50 A from 5758.9, huge FWHM, separation fails; no CWT trough. Not adopted."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "outside_window",
            "no_cwt_match"
          ],
          "comment": "Only fit at 5805.4 lies outside the line's redshift window; no CWT peak near 5759.6. Not adopted."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "outside_window",
            "no_cwt_match"
          ],
          "comment": "Only fit at 5800.3 lies outside the line's redshift window; no CWT trough near 5759.6. Not adopted."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H6:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit at 5958.4, offset ~6 A, but FWHM ~314 km/s and low SNR 1.04; marginal."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H6:0018",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr"
          ],
          "comment": "Fit at 5946.7, offset ~6 A, low SNR 1.93; weak marginal absorption."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H6:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit at 6245.8, offset ~1 A, but FWHM ~296 km/s and low SNR 1.26; marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H6:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr"
          ],
          "comment": "Fit at 6304.7, offset ~6 A, low SNR 1.8; weak marginal emission."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_match"
          ],
          "comment": "Only fit is center_at_bound (6248.7, unselectable); no CWT trough near 6298.7. Not adopted."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_match"
          ],
          "comment": "Only fit is center_at_bound with zero amplitude (7004.6, unselectable); no CWT peak near 7054.6. Not adopted."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "fit:H6:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit at 7066.7, offset ~12 A, low SNR 0.76; weak marginal absorption."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "component_ratio_fail",
            "no_cwt_match"
          ],
          "comment": "Doublet fit component 1 at 7204.7 with tiny amplitude 0.086 vs 32.5, ratio 377, separation fails; no CWT peak at 7196. Not adopted."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "cwt:em:0012",
          "status": "LIKELY",
          "reason_codes": [
            "strong_snr",
            "ridge_persistent"
          ],
          "comment": "CWT peak 7265.6 (z=0.4507) matches predicted 7265.7 within 0.1 A; SNR 327, ridge 24. Strong detection."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Nearest CWT troughs 7492.0 (z=0.4473) and 7463.2 (z=0.4417) are 18-47 A blueward of 7510.1; no targeted fit. Not adopted."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "center_deviation_large",
            "no_cwt_match"
          ],
          "comment": "Doublet fit center 8539.6 deviates ~8 A and separation fails; no CWT trough near 8547. Not adopted."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_match",
            "no_fit"
          ],
          "comment": "No CWT trough and no targeted fit at 8553.1; not adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "center_deviation_large",
            "no_cwt_match"
          ],
          "comment": "Doublet fit center 8563.2 deviates ~7 A and separation fails; no CWT trough near 8556. Not adopted."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "component_ratio_fail",
            "no_cwt_match"
          ],
          "comment": "Doublet fit component 1 at 9507.3, ratio 0.12, separation fails; CWT peaks 9440.8/9477.6 are 24-61 A blueward. Not adopted."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "Nearest CWT peak 9477.6 implies z=0.4437, ~46 A blueward of 9523.6; no targeted fit. Not adopted."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "no_fit"
          ],
          "comment": "CWT troughs 9480.8/9462.4 are 43-61 A blueward of 9523.6; no targeted fit. Not adopted."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "center_deviation_large",
            "no_cwt_match"
          ],
          "comment": "Doublet fit component 2 at 9582.0 deviates ~28 A with huge FWHM, separation fails; no CWT peak near 9553.6. Not adopted."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_deviation_large",
            "separation_fail",
            "no_cwt_match"
          ],
          "comment": "Doublet fit component 1 at 9696.6 with enormous error/FWHM, separation fails; no CWT peak near 9746.6. Not adopted."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_deviation_large",
            "separation_fail",
            "no_cwt_match"
          ],
          "comment": "Doublet fit component 2 at 9733.0 deviates ~35 A, separation fails; no CWT peak near 9767.5. Not adopted."
        }
      ]
    },
    "id": "call_00_iFY4elwfGHIPGfazRVtx0533",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 10770,
  "output_tokens": 2492,
  "total_tokens": 13262,
  "cache_hit_tokens": 10496,
  "cache_miss_tokens": 274,
  "provider_usage": {
    "completion_tokens": 2492,
    "prompt_tokens": 10770,
    "total_tokens": 13262,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 10496
    },
    "prompt_cache_hit_tokens": 10496,
    "prompt_cache_miss_tokens": 274
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_iFY4elwfGHIPGfazRVtx0533`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H6/pre_analysis/branches/main/5191281cf53b43bcb6ef3de04f7b0f4a/lines.csv", "n_lines": 27, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H6/pre_analysis/branches/main/5191281cf53b43bcb6ef3de04f7b0f4a/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:19:09.390573+00:00
