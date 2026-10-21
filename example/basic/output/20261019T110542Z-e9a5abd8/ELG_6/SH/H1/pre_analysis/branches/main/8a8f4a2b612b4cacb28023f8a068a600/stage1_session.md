# SH pre-analysis session: line review

- Run ID: `graph-fe0d30030bcc4939b88103e27753b2c1`
- Hypothesis: `H1`
- Started (UTC): 2026-10-19T11:18:35.364874+00:00
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
Review every predicted line at the fixed Redrock redshift `0.1068183112742081`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H1/pre_analysis/branches/main/8a8f4a2b612b4cacb28023f8a068a600/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 5.3 |

Verify the redshift hypothesis z ≈ 0.1068183112742081.

Verification window: z ∈ [0.0968, 0.1168]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=53.0166, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=15.9382, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=39.2921, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=38.5173, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=6.64091, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/ELG_6.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H1/pre_analysis/branches/main/8a8f4a2b612b4cacb28023f8a068a600/lines.csv

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


## Predicted Lines at z = 0.1068

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [Ne V] | 3426.0 | 3792.0 | em | narrow | — |
| [O II] | 3727.0 | 4125.1 | em | narrow | peak@4127.2±0.8(z=0.1074) |
| Ca K_abs | 3934.8 | 4355.1 | abs | absorption | — |
| Ca H_abs | 3969.6 | 4393.6 | abs | absorption | — |
| Hε | 3970.1 | 4394.2 | em | both | — |
| Hε_abs | 3970.1 | 4394.2 | abs | absorption | — |
| Hδ | 4102.9 | 4541.2 | em | both | peak@4540.8±0.8(z=0.1067) |
| Hδ_abs | 4102.9 | 4541.2 | abs | absorption | — |
| G-band_abs | 4305.6 | 4765.5 | abs | absorption | trough@4801.6±0.8(z=0.1152) |
| Hγ | 4341.7 | 4805.5 | em | both | peak@4805.6±0.8(z=0.1068) |
| Hγ_abs | 4341.7 | 4805.5 | abs | absorption | trough@4801.6±0.8(z=0.1059), trough@4812.8±0.8(z=0.1085) |
| Hβ | 4862.7 | 5382.1 | em | both | peak@5381.6±0.8(z=0.1067) |
| Hβ_abs | 4862.7 | 5382.1 | abs | absorption | trough@5372.8±0.8(z=0.1049), trough@5393.6±0.8(z=0.1092) |
| [O III]a | 4960.3 | 5490.2 | em | narrow | peak@5489.6±0.8(z=0.1067) |
| [O III]b | 5008.2 | 5543.2 | em | narrow | peak@5543.2±0.8(z=0.1068), peak@5545.6±0.8(z=0.1073) |
| Mg I_abs | 5176.7 | 5729.7 | abs | absorption | — |
| Na D1_abs | 5891.6 | 6520.9 | abs | absorption | — |
| Na D_abs | 5895.6 | 6525.4 | abs | absorption | — |
| Na D2_abs | 5897.6 | 6527.6 | abs | absorption | — |
| [N II]a | 6549.8 | 7249.4 | em | narrow | peak@7265.6±0.8(z=0.1093), peak@7288.8±0.8(z=0.1128) |
| Hα | 6564.6 | 7265.8 | em | both | peak@7265.6±0.8(z=0.1068), peak@7288.8±0.8(z=0.1103) |
| Hα_abs | 6564.6 | 7265.8 | abs | absorption | trough@7256.8±0.8(z=0.1054), trough@7285.6±0.8(z=0.1098), trough@7288.0±0.8(z=0.1102), trough@7204.0±0.8(z=0.0974) |
| [N II]b | 6585.3 | 7288.7 | em | narrow | peak@7288.8±0.8(z=0.1068), peak@7265.6±0.8(z=0.1033) |
| [S II]a | 6718.3 | 7435.9 | em | narrow | peak@7436.0±0.8(z=0.1068), peak@7452.0±0.8(z=0.1092) |
| [S II]b | 6732.7 | 7451.9 | em | narrow | peak@7452.0±0.8(z=0.1068), peak@7436.0±0.8(z=0.1045) |
| CaT1_abs | 8498.0 | 9405.7 | abs | absorption | trough@9442.4±0.8(z=0.1111), trough@9452.0±0.8(z=0.1123), trough@9462.4±0.8(z=0.1135), trough@9480.8±0.8(z=0.1157) |
| CaT2_abs | 8542.0 | 9454.4 | abs | absorption | trough@9452.0±0.8(z=0.1065), trough@9462.4±0.8(z=0.1077), trough@9442.4±0.8(z=0.1054), trough@9480.8±0.8(z=0.1099) |
| CaT3_abs | 8662.0 | 9587.3 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| Ca K_abs/Ca H_abs | 4355.1/4393.6 | fit_doublet | 4355.517±1.1141/4351.631±227.6816 | -1.23896/-0.259997 | 230.0/30909.3 | 4.26 | 0.573 | warning; separation fail |
| Na D1_abs/Na D2_abs | 6520.9/6527.6 | fit_doublet | 6527.32±1.3462/6573.809±2.7153 | -0.097152/-0.086505 | 149.0/477.0 | 1.05 | 0.016 | warning; separation fail; component ratio 0.89 |
| [Ne V] | 3792.0 | fit_peak | 3752.278±2.1951 | 0.378173 | 516.9 | 0.9 | 0.01 | ok |
| Hε | 4394.2 | fit_peak | 4395.27±0.3222 | 1.210277 | 160.6 | 4.85 | 0.104 | ok |
| Hε_abs | 4394.2 | fit_peak | 4444.178±0.0 | -0.0 | 31769.1 | 0.0 | -0.0 | warning: center_at_bound |
| Hδ_abs | 4541.2 | fit_peak | 4558.76±60.8857 | -0.030627 | 5606.0 | 0.15 | 0.004 | ok |
| Mg I_abs | 5729.7 | fit_peak | 5679.666±68.6363 | -1.925997 | 14603.9 | 5.37 | 14.482 | warning: center_at_bound |
| CaT3_abs | 9587.3 | fit_peak | 9537.271±0.0 | -0.0 | 74.0 | 0.0 | -0.0 | warning: center_at_bound |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:nev-3426 | [Ne V] | 3792.0 | emission |
| line:oii-3727 | [O II] | 4125.1 | emission |
| line:cak-3934-abs | Ca K_abs | 4355.1 | absorption |
| line:cah-3969-abs | Ca H_abs | 4393.6 | absorption |
| line:heps-3970 | Hε | 4394.2 | emission |
| line:heps-3970-abs | Hε_abs | 4394.2 | absorption |
| line:hdel-4102 | Hδ | 4541.2 | emission |
| line:hdel-4102-abs | Hδ_abs | 4541.2 | absorption |
| line:gband-4305-abs | G-band_abs | 4765.5 | absorption |
| line:hgam-4341 | Hγ | 4805.5 | emission |
| line:hgam-4341-abs | Hγ_abs | 4805.5 | absorption |
| line:hbet-4862 | Hβ | 5382.1 | emission |
| line:hbet-4862-abs | Hβ_abs | 5382.1 | absorption |
| line:oiii-4960 | [O III]a | 5490.2 | emission |
| line:oiii-5008 | [O III]b | 5543.2 | emission |
| line:mgi-5176-abs | Mg I_abs | 5729.7 | absorption |
| line:nad1-5891-abs | Na D1_abs | 6520.9 | absorption |
| line:nad-5895-abs | Na D_abs | 6525.4 | absorption |
| line:nad2-5897-abs | Na D2_abs | 6527.6 | absorption |
| line:nii-6549 | [N II]a | 7249.4 | emission |
| line:half-6564 | Hα | 7265.8 | emission |
| line:half-6564-abs | Hα_abs | 7265.8 | absorption |
| line:nii-6585 | [N II]b | 7288.7 | emission |
| line:sii-6718 | [S II]a | 7435.9 | emission |
| line:sii-6732 | [S II]b | 7451.9 | emission |
| line:cat1-8498-abs | CaT1_abs | 9405.7 | absorption |
| line:cat2-8542-abs | CaT2_abs | 9454.4 | absorption |
| line:cat3-8662-abs | CaT3_abs | 9587.3 | absorption |

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
| fit:H1:0000 | fit_doublet | absorption | 4355.517 | Ca K_abs | yes | — |
| fit:H1:0001 | fit_doublet | absorption | 4351.631 | Ca H_abs | yes | — |
| fit:H1:0002 | fit_doublet | absorption | 6527.320 | Na D1_abs | yes | — |
| fit:H1:0003 | fit_doublet | absorption | 6573.809 | Na D2_abs | yes | — |
| fit:H1:0004 | fit_peak | emission | 3752.278 | [Ne V] | yes | — |
| fit:H1:0005 | fit_peak | emission | 4395.270 | Hε | yes | — |
| fit:H1:0006 | fit_peak | absorption | 4444.178 | Hε_abs | no | center_at_bound |
| fit:H1:0007 | fit_peak | absorption | 4558.760 | Hδ_abs | yes | — |
| fit:H1:0008 | fit_peak | absorption | 5679.666 | Mg I_abs | no | center_at_bound |
| fit:H1:0009 | fit_peak | absorption | 9537.271 | CaT3_abs | no | center_at_bound |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H1/pre_analysis/branches/main/8a8f4a2b612b4cacb28023f8a068a600/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "weak_fit",
            "offset_large"
          ],
          "comment": "Only fit centre 3752.3 (delta ~40 A, low SNR 0.9, amp 0.38); no credible CWT peak near 3792. Not adopted."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": "cwt:em:0000",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 4127.2 vs pred 4125.1, delta ~2 A, z=0.1074 in window, strong SNR 88, ridge 24. Adopted."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H1:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_depth",
            "blend"
          ],
          "comment": "Doublet fit centre 4355.5 matches pred 4355.1 well (delta 0.4 A) with amp -1.24; separation failed and Ca H component degenerate, so depth ordering uncertain. Weak but plausible Ca K."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H1:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "huge_error",
            "blend"
          ],
          "comment": "Ca H fit centre 4351.6 with 227 A error and 30909 km/s width; degenerate, blended with Ca K. Preserved as plausible weak component but highly uncertain."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H1:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "fit_only",
            "no_cwt_peak",
            "weak_snr"
          ],
          "comment": "Fit centre 4395.3 vs pred 4394.2 (delta 1.1 A), amp 1.21, local SNR 4.85; no CWT peak listed. Weak marginal emission."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Fit centre at bound (4444.2, amp 0), no credible absorption feature. Not adopted."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "cwt:em:0003",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 4540.8 vs pred 4541.2, delta 0.4 A, z=0.1067, SNR 16.6, ridge 12. Adopted."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H1:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_depth",
            "huge_error",
            "no_cwt_trough"
          ],
          "comment": "Fit centre 4558.8 with 61 A error, amp -0.03, local SNR 0.15; no CWT trough at pred. Very weak, marginal at best."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_large",
            "no_match"
          ],
          "comment": "Pred 4765.5; nearest trough 4801.6 is 36 A off (z=0.1152) and likely H-gamma absorption blend. No credible G-band measurement."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "cwt:em:0005",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 4805.6 vs pred 4805.5, delta 0.1 A, z=0.1068, SNR 30, ridge 21. Adopted."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "cwt:abs:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "weak_depth",
            "offset_ok"
          ],
          "comment": "Trough 4812.8 (z=0.1085) closer than 4801.6; both weak and blended with H-gamma emission. Marginal absorption."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "cwt:em:0006",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 5381.6 vs pred 5382.1, delta 0.5 A, z=0.1067, SNR 92, ridge 22. Adopted."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "cwt:abs:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "weak_depth",
            "offset_ok"
          ],
          "comment": "Trough 5372.8 (z=0.1049) near pred, blended with H-beta emission; weak. Marginal."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "cwt:em:0007",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 5489.6 vs pred 5490.2, delta 0.6 A, z=0.1067, SNR 83, ridge 18. Adopted."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "cwt:em:0008",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok",
            "blend"
          ],
          "comment": "CWT peak 5543.2 vs pred 5543.2, exact, z=0.1068, SNR 268, ridge 24. Strong; blended with broad feature 5545.6. Adopted."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Fit centre at bound (5679.7, 50 A off), no CWT trough near 5729.7. Not adopted."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H1:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_depth",
            "blend"
          ],
          "comment": "Doublet fit centre 6527.3 vs pred 6520.9 (delta 6.4 A), amp -0.10, local SNR 1.05; separation failed, blended Na D. Marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "blend"
          ],
          "comment": "No separate measurement for the blended Na D feature; only D1/D2 fit components exist. Not adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H1:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_large",
            "weak_depth"
          ],
          "comment": "Fit centre 6573.8 vs pred 6527.6 (delta 46 A), amp -0.09, ratio 0.89 vs expected 2; separation failed. Weak marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_large",
            "blend"
          ],
          "comment": "Pred 7249.4; nearest peaks 7265.6 (16 A, H-alpha) and 7288.8 (39 A, NIIb). No credible isolated NIIa measurement; blended with H-alpha."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "cwt:em:0012",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 7265.6 vs pred 7265.8, delta 0.2 A, z=0.1068, SNR 327, ridge 24. Strong. Adopted."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "cwt:abs:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "weak_depth",
            "offset_ok"
          ],
          "comment": "Trough 7288.0 (z=0.1102) and 7256.8 nearby; blended with strong H-alpha emission, weak depth. Marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "cwt:em:0013",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok",
            "blend"
          ],
          "comment": "CWT peak 7288.8 vs pred 7288.7, delta 0.1 A, z=0.1068, SNR 18, ridge 12. Adopted; blended with H-alpha wing."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "cwt:em:0014",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 7436.0 vs pred 7435.9, delta 0.1 A, z=0.1068, SNR 43, ridge 23. Adopted."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "cwt:em:0015",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 7452.0 vs pred 7451.9, delta 0.1 A, z=0.1068, SNR 32, ridge 13. Adopted; doublet partner of SIIa."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_large",
            "edge_red"
          ],
          "comment": "Pred 9405.7; nearest troughs 9442-9481 are 37-75 A off and cluster near CaT2. No credible CaT1 measurement; red edge."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "cwt:abs:0024",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "edge_red",
            "offset_ok"
          ],
          "comment": "Trough 9452.0 vs pred 9454.4, delta 2.4 A, z=0.1065; blended with multiple nearby troughs (9442/9462/9481) and red edge. Marginal."
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
          "comment": "Fit centre at bound (9537.3, amp 0), no CWT trough near 9587.3. Not adopted."
        }
      ]
    },
    "id": "call_00_PiQucE4SOpNhSZdQJGFA0436",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 7677,
  "output_tokens": 2828,
  "total_tokens": 10505,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 7037,
  "provider_usage": {
    "completion_tokens": 2828,
    "prompt_tokens": 7677,
    "total_tokens": 10505,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 7037
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_PiQucE4SOpNhSZdQJGFA0436`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 3, "line_id": "line:cah-3969-abs", "measurement_id": "fit:H1:0001", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
The Ca H fit centre (4351.6 Å) falls outside the redshift window. I'll repair that row and resubmit the full set.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H1/pre_analysis/branches/main/8a8f4a2b612b4cacb28023f8a068a600/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "weak_fit",
            "offset_large"
          ],
          "comment": "Only fit centre 3752.3 (delta ~40 A, low SNR 0.9, amp 0.38); no credible CWT peak near 3792. Not adopted."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": "cwt:em:0000",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 4127.2 vs pred 4125.1, delta ~2 A, z=0.1074 in window, strong SNR 88, ridge 24. Adopted."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H1:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_depth",
            "blend"
          ],
          "comment": "Doublet fit centre 4355.5 matches pred 4355.1 well (delta 0.4 A) with amp -1.24; separation failed and Ca H component degenerate, so depth ordering uncertain. Weak but plausible Ca K."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "outside_window",
            "huge_error",
            "doublet_separation_fail"
          ],
          "comment": "Ca H fit centre 4351.6 with 227 A error lies outside the redshift window and is degenerate/blended with Ca K; no credible selectable measurement."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H1:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "fit_only",
            "no_cwt_peak",
            "weak_snr"
          ],
          "comment": "Fit centre 4395.3 vs pred 4394.2 (delta 1.1 A), amp 1.21, local SNR 4.85; no CWT peak listed. Weak marginal emission."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Fit centre at bound (4444.2, amp 0), no credible absorption feature. Not adopted."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "cwt:em:0003",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 4540.8 vs pred 4541.2, delta 0.4 A, z=0.1067, SNR 16.6, ridge 12. Adopted."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H1:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_depth",
            "huge_error",
            "no_cwt_trough"
          ],
          "comment": "Fit centre 4558.8 with 61 A error, amp -0.03, local SNR 0.15; no CWT trough at pred. Very weak, marginal at best."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_large",
            "no_match"
          ],
          "comment": "Pred 4765.5; nearest trough 4801.6 is 36 A off (z=0.1152) and likely H-gamma absorption blend. No credible G-band measurement."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "cwt:em:0005",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 4805.6 vs pred 4805.5, delta 0.1 A, z=0.1068, SNR 30, ridge 21. Adopted."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "cwt:abs:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "weak_depth",
            "offset_ok"
          ],
          "comment": "Trough 4812.8 (z=0.1085) closer than 4801.6; both weak and blended with H-gamma emission. Marginal absorption."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "cwt:em:0006",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 5381.6 vs pred 5382.1, delta 0.5 A, z=0.1067, SNR 92, ridge 22. Adopted."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "cwt:abs:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "weak_depth",
            "offset_ok"
          ],
          "comment": "Trough 5372.8 (z=0.1049) near pred, blended with H-beta emission; weak. Marginal."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "cwt:em:0007",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 5489.6 vs pred 5490.2, delta 0.6 A, z=0.1067, SNR 83, ridge 18. Adopted."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "cwt:em:0008",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok",
            "blend"
          ],
          "comment": "CWT peak 5543.2 vs pred 5543.2, exact, z=0.1068, SNR 268, ridge 24. Strong; blended with broad feature 5545.6. Adopted."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "failed_fit"
          ],
          "comment": "Fit centre at bound (5679.7, 50 A off), no CWT trough near 5729.7. Not adopted."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H1:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_depth",
            "blend"
          ],
          "comment": "Doublet fit centre 6527.3 vs pred 6520.9 (delta 6.4 A), amp -0.10, local SNR 1.05; separation failed, blended Na D. Marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "blend"
          ],
          "comment": "No separate measurement for the blended Na D feature; only D1/D2 fit components exist. Not adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H1:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_large",
            "weak_depth"
          ],
          "comment": "Fit centre 6573.8 vs pred 6527.6 (delta 46 A), amp -0.09, ratio 0.89 vs expected 2; separation failed. Weak marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_large",
            "blend"
          ],
          "comment": "Pred 7249.4; nearest peaks 7265.6 (16 A, H-alpha) and 7288.8 (39 A, NIIb). No credible isolated NIIa measurement; blended with H-alpha."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "cwt:em:0012",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 7265.6 vs pred 7265.8, delta 0.2 A, z=0.1068, SNR 327, ridge 24. Strong. Adopted."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "cwt:abs:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "weak_depth",
            "offset_ok"
          ],
          "comment": "Trough 7288.0 (z=0.1102) and 7256.8 nearby; blended with strong H-alpha emission, weak depth. Marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "cwt:em:0013",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok",
            "blend"
          ],
          "comment": "CWT peak 7288.8 vs pred 7288.7, delta 0.1 A, z=0.1068, SNR 18, ridge 12. Adopted; blended with H-alpha wing."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "cwt:em:0014",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 7436.0 vs pred 7435.9, delta 0.1 A, z=0.1068, SNR 43, ridge 23. Adopted."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "cwt:em:0015",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok"
          ],
          "comment": "CWT peak 7452.0 vs pred 7451.9, delta 0.1 A, z=0.1068, SNR 32, ridge 13. Adopted; doublet partner of SIIa."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_large",
            "edge_red"
          ],
          "comment": "Pred 9405.7; nearest troughs 9442-9481 are 37-75 A off and cluster near CaT2. No credible CaT1 measurement; red edge."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "cwt:abs:0024",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "edge_red",
            "offset_ok"
          ],
          "comment": "Trough 9452.0 vs pred 9454.4, delta 2.4 A, z=0.1065; blended with multiple nearby troughs (9442/9462/9481) and red edge. Marginal."
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
          "comment": "Fit centre at bound (9537.3, amp 0), no CWT trough near 9587.3. Not adopted."
        }
      ]
    },
    "id": "call_00_72mU7AsePrpEQA46lOdI3026",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 10611,
  "output_tokens": 2828,
  "total_tokens": 13439,
  "cache_hit_tokens": 10368,
  "cache_miss_tokens": 243,
  "provider_usage": {
    "completion_tokens": 2828,
    "prompt_tokens": 10611,
    "total_tokens": 13439,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 10368
    },
    "prompt_cache_hit_tokens": 10368,
    "prompt_cache_miss_tokens": 243
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_72mU7AsePrpEQA46lOdI3026`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H1/pre_analysis/branches/main/8a8f4a2b612b4cacb28023f8a068a600/lines.csv", "n_lines": 28, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/ELG_6/SH/H1/pre_analysis/branches/main/8a8f4a2b612b4cacb28023f8a068a600/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:19:03.804735+00:00
