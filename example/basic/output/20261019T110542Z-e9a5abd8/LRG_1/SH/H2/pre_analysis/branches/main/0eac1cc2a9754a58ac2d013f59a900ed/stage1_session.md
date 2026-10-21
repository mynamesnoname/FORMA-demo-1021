# SH pre-analysis session: line review

- Run ID: `graph-6f4e6510cc5d45df9da3b7be0c8597cc`
- Hypothesis: `H2`
- Started (UTC): 2026-10-19T11:28:18.087227+00:00
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
Review every predicted line at the fixed Redrock redshift `-0.0002616156273229071`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H2/pre_analysis/branches/main/0eac1cc2a9754a58ac2d013f59a900ed/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 38.1 |

Verify the redshift hypothesis z ≈ -0.0002616156273229071.

Verification window: z ∈ [-0.0103, 0.0097]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=47.8875, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=14.3962, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=35.4907, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=34.7909, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=5.99843, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/LRG_1.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H2/pre_analysis/branches/main/0eac1cc2a9754a58ac2d013f59a900ed/lines.csv

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


## Predicted Lines at z = -0.0003

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [O II] | 3727.0 | 3726.0 | em | narrow | — |
| Ca K_abs | 3934.8 | 3933.8 | abs | absorption | — |
| Ca H_abs | 3969.6 | 3968.6 | abs | absorption | — |
| Hε | 3970.1 | 3969.1 | em | both | — |
| Hε_abs | 3970.1 | 3969.1 | abs | absorption | — |
| Hδ | 4102.9 | 4101.8 | em | both | — |
| Hδ_abs | 4102.9 | 4101.8 | abs | absorption | — |
| G-band_abs | 4305.6 | 4304.5 | abs | absorption | — |
| Hγ | 4341.7 | 4340.6 | em | both | — |
| Hγ_abs | 4341.7 | 4340.6 | abs | absorption | — |
| Hβ | 4862.7 | 4861.4 | em | both | peak@4815.2±0.8(z=-0.0098) |
| Hβ_abs | 4862.7 | 4861.4 | abs | absorption | trough@4884.8±0.8(z=0.0045) |
| [O III]a | 4960.3 | 4959.0 | em | narrow | peak@4964.0±0.8(z=0.0007) |
| [O III]b | 5008.2 | 5006.9 | em | narrow | peak@4964.0±0.8(z=-0.0088) |
| Mg I_abs | 5176.7 | 5175.3 | abs | absorption | — |
| Na D1_abs | 5891.6 | 5890.1 | abs | absorption | — |
| Na D_abs | 5895.6 | 5894.1 | abs | absorption | — |
| Na D2_abs | 5897.6 | 5896.1 | abs | absorption | — |
| [N II]a | 6549.8 | 6548.1 | em | narrow | — |
| Hα | 6564.6 | 6562.9 | em | both | — |
| Hα_abs | 6564.6 | 6562.9 | abs | absorption | trough@6583.2±0.8(z=0.0028) |
| [N II]b | 6585.3 | 6583.6 | em | narrow | — |
| [S II]a | 6718.3 | 6716.5 | em | narrow | peak@6651.2±0.8(z=-0.0100) |
| [S II]b | 6732.7 | 6730.9 | em | narrow | — |
| CaT1_abs | 8498.0 | 8495.8 | abs | absorption | — |
| CaT2_abs | 8542.0 | 8539.8 | abs | absorption | — |
| CaT3_abs | 8662.0 | 8659.7 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [S II]a/[S II]b | 6716.5/6730.9 | fit_doublet | 6726.367±2.7285/6780.939±5.916 | 0.308194/0.626326 | 523.2/7237.9 | 2.17 | 1.054 | warning: center_2_deviation_large; separation fail; component ratio 2.03 |
| [N II]a/[N II]b | 6548.1/6583.6 | fit_doublet | 6498.092±0.0/6633.575±0.0 | 0.0/0.0 | 108.6/106.4 | 0.0 | -0.0 | warning; separation fail; component ratio — |
| Ca K_abs/Ca H_abs | 3933.8/3968.6 | fit_doublet | 3937.561±2.6985/3977.105±37.1194 | -0.412392/-0.218917 | 889.4/20394.0 | 0.91 | 0.108 | ok; separation pass |
| Na D1_abs/Na D2_abs | 5890.1/5896.1 | fit_doublet | 5912.736±2.6185/5946.057±9.6384 | -0.211134/-0.217149 | 252.4/2935.4 | 0.56 | 0.029 | warning; separation fail; component ratio 1.03 |
| [O II] | 3726.0 | fit_peak | 3732.202±13.086 | 0.346216 | 6016.3 | 0.57 | 0.055 | ok |
| Hε | 3969.1 | fit_peak | 4019.049±0.0 | 0.0 | 8827.2 | 0.0 | -0.0 | warning: center_at_bound |
| Hδ | 4101.8 | fit_peak | 4151.827±14.0362 | 0.286058 | 10836.6 | 0.86 | 0.209 | warning: center_at_bound |
| Hγ | 4340.6 | fit_peak | 4360.554±1.3563 | 0.553841 | 946.5 | 1.73 | 0.077 | ok |
| Hα | 6562.9 | fit_peak | 6575.466±0.0 | 0.0 | 107.4 | 0.0 | 0.0 | ok |
| Hε_abs | 3969.1 | fit_peak | 4019.061±304.971 | -0.452506 | 35130.5 | 1.08 | 0.845 | warning: center_at_bound |
| Hδ_abs | 4101.8 | fit_peak | 4114.247±1.9533 | -0.384513 | 732.4 | 1.05 | 0.021 | ok |
| G-band_abs | 4304.5 | fit_peak | 4283.81±2.8028 | -0.359343 | 1543.6 | 1.12 | 0.052 | ok |
| Hγ_abs | 4340.6 | fit_peak | 4390.194±0.7783 | -0.411706 | 160.8 | 1.22 | 0.007 | ok |
| Mg I_abs | 5175.3 | fit_peak | 5224.846±0.0 | -0.0 | 135.2 | 0.0 | -0.0 | ok |
| CaT1_abs | 8495.8 | fit_peak | 8545.777±9.7411 | -0.175261 | 3327.6 | 0.91 | 0.147 | warning: center_at_bound |
| CaT2_abs | 8539.8 | fit_peak | 8551.932±10.0071 | -0.152326 | 3138.4 | 0.83 | 0.115 | ok |
| CaT3_abs | 8659.7 | fit_peak | 8660.576±0.7831 | -0.285123 | 81.5 | 1.68 | 0.012 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:oii-3727 | [O II] | 3726.0 | emission |
| line:cak-3934-abs | Ca K_abs | 3933.8 | absorption |
| line:cah-3969-abs | Ca H_abs | 3968.6 | absorption |
| line:heps-3970 | Hε | 3969.1 | emission |
| line:heps-3970-abs | Hε_abs | 3969.1 | absorption |
| line:hdel-4102 | Hδ | 4101.8 | emission |
| line:hdel-4102-abs | Hδ_abs | 4101.8 | absorption |
| line:gband-4305-abs | G-band_abs | 4304.5 | absorption |
| line:hgam-4341 | Hγ | 4340.6 | emission |
| line:hgam-4341-abs | Hγ_abs | 4340.6 | absorption |
| line:hbet-4862 | Hβ | 4861.4 | emission |
| line:hbet-4862-abs | Hβ_abs | 4861.4 | absorption |
| line:oiii-4960 | [O III]a | 4959.0 | emission |
| line:oiii-5008 | [O III]b | 5006.9 | emission |
| line:mgi-5176-abs | Mg I_abs | 5175.3 | absorption |
| line:nad1-5891-abs | Na D1_abs | 5890.1 | absorption |
| line:nad-5895-abs | Na D_abs | 5894.1 | absorption |
| line:nad2-5897-abs | Na D2_abs | 5896.1 | absorption |
| line:nii-6549 | [N II]a | 6548.1 | emission |
| line:half-6564 | Hα | 6562.9 | emission |
| line:half-6564-abs | Hα_abs | 6562.9 | absorption |
| line:nii-6585 | [N II]b | 6583.6 | emission |
| line:sii-6718 | [S II]a | 6716.5 | emission |
| line:sii-6732 | [S II]b | 6730.9 | emission |
| line:cat1-8498-abs | CaT1_abs | 8495.8 | absorption |
| line:cat2-8542-abs | CaT2_abs | 8539.8 | absorption |
| line:cat3-8662-abs | CaT3_abs | 8659.7 | absorption |

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
| fit:H2:0000 | fit_doublet | emission | 6726.367 | [S II]a | yes | — |
| fit:H2:0001 | fit_doublet | emission | 6780.939 | [S II]b | yes | — |
| fit:H2:0002 | fit_doublet | emission | 6498.092 | [N II]a | yes | — |
| fit:H2:0003 | fit_doublet | emission | 6633.575 | [N II]b | yes | — |
| fit:H2:0004 | fit_doublet | absorption | 3937.561 | Ca K_abs | yes | — |
| fit:H2:0005 | fit_doublet | absorption | 3977.105 | Ca H_abs | yes | — |
| fit:H2:0006 | fit_doublet | absorption | 5912.736 | Na D1_abs | yes | — |
| fit:H2:0007 | fit_doublet | absorption | 5946.057 | Na D2_abs | yes | — |
| fit:H2:0008 | fit_peak | emission | 3732.202 | [O II] | yes | — |
| fit:H2:0009 | fit_peak | emission | 4019.049 | Hε | no | center_at_bound |
| fit:H2:0010 | fit_peak | emission | 4151.827 | Hδ | no | center_at_bound |
| fit:H2:0011 | fit_peak | emission | 4360.554 | Hγ | yes | — |
| fit:H2:0012 | fit_peak | emission | 6575.466 | Hα | yes | — |
| fit:H2:0013 | fit_peak | absorption | 4019.061 | Hε_abs | no | center_at_bound |
| fit:H2:0014 | fit_peak | absorption | 4114.247 | Hδ_abs | yes | — |
| fit:H2:0015 | fit_peak | absorption | 4283.810 | G-band_abs | yes | — |
| fit:H2:0016 | fit_peak | absorption | 4390.194 | Hγ_abs | yes | — |
| fit:H2:0017 | fit_peak | absorption | 5224.846 | Mg I_abs | yes | — |
| fit:H2:0018 | fit_peak | absorption | 8545.777 | CaT1_abs | no | center_at_bound |
| fit:H2:0019 | fit_peak | absorption | 8551.932 | CaT2_abs | yes | — |
| fit:H2:0020 | fit_peak | absorption | 8660.576 | CaT3_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H2/pre_analysis/branches/main/0eac1cc2a9754a58ac2d013f59a900ed/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H2:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "blue_edge"
          ],
          "comment": "Fit centre 3732.2 vs pred 3726.0 (offset ~6 A, within window) but local SNR 0.57, FWHM ~6000 km/s and blue edge; weak, broad, unconvincing."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H2:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "blend_cah",
            "blue_edge"
          ],
          "comment": "Doublet fit centre 3937.6 (offset ~4 A) with separation pass, but local SNR 0.91 and FWHM ~890 km/s; plausible weak Ca K component, blended with Ca H."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H2:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "huge_width",
            "blend_cak",
            "blue_edge"
          ],
          "comment": "Ca H fit centre 3977.1 with very large error and FWHM ~20000 km/s; depth ordering (K deeper than H) preserved but fit is poorly constrained; plausible weak component."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Only fit attempt failed with center_at_bound (4019 A); no CWT emission feature near 3969 A."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Absorption fit failed with center_at_bound and enormous width; no credible trough near 3969 A."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Emission fit center_at_bound (4151.8 A); no CWT peak near 4102 A."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H2:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 4114.2 (offset ~12 A) with local SNR 1.05 and FWHM ~730 km/s; weak absorption, no matching CWT trough."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H2:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 4283.8 (offset ~21 A, weaker band) with local SNR 1.12 and FWHM ~1500 km/s; weak, broad, no CWT trough."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H2:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 4360.6 (offset ~20 A) with local SNR 1.73 and FWHM ~950 km/s; weak emission, no matching CWT peak."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H2:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit centre 4390.2 (offset ~50 A, weak band) with local SNR 1.22; narrow but offset large, no CWT trough."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "offset_large"
          ],
          "comment": "Nearest CWT peak 4815.2 implies z=-0.0098, ~46 A blueward; no credible Hbeta emission measurement."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "offset_large"
          ],
          "comment": "Nearest CWT trough 4884.8 implies z=+0.0045, ~23 A redward; no adopted Hbeta absorption."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "cwt:em:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width",
            "blend_oiiib"
          ],
          "comment": "CWT peak 4964.0 (offset ~5 A, z=0.0007 in window) but FWHM ~4250 km/s, far broader than narrow [O III]; shared feature with [O III]b ambiguity."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "offset_large"
          ],
          "comment": "Only nearby peak 4964.0 implies z=-0.0088, ~43 A blueward; no separate [O III]b measurement; doublet separation fails."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Fit returned zero amplitude at 5224.8 A; no CWT trough near 5175 A."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_large",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit centre 5912.7 (offset ~23 A) with separation fail and component ratio ~1; no CWT trough near 5890 A."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_large",
            "no_cwt_feature"
          ],
          "comment": "No independent measurement; Na D doublet fit failed separation and is offset; no CWT trough near 5894 A."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_large",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit centre 5946.1 with huge error and separation fail; no credible Na D2 absorption."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Doublet fit returned zero amplitudes with separation fail; no CWT peak near 6548 A."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Fit returned zero amplitude at 6575.5 A; no CWT peak near 6563 A."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "offset_large"
          ],
          "comment": "Nearest CWT trough 6583.2 implies z=+0.0028, ~20 A redward; no adopted Halpha absorption."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Doublet fit zero amplitude with separation fail; no CWT peak near 6584 A."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_large",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit centre 6726.4 (offset ~10 A) with separation fail and component ratio 2.03; nearest CWT peak 6651.2 implies z=-0.0100, outside window."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "huge_width",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit centre 6780.9 with FWHM ~7200 km/s and separation fail; no credible [S II]b measurement."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "red_edge"
          ],
          "comment": "Fit failed with center_at_bound (8545.8 A); no CWT trough near 8496 A."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H2:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "red_edge"
          ],
          "comment": "Fit centre 8551.9 (offset ~12 A) with local SNR 0.83 and FWHM ~3100 km/s; weak, broad, no CWT trough."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H2:0020",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8660.6 (offset ~1 A) with local SNR 1.68 and narrow FWHM ~80 km/s; weak but positionally consistent, no CWT trough."
        }
      ]
    },
    "id": "call_00_KyEDcKoHqNfiHL4evFAB2466",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 7032,
  "output_tokens": 2504,
  "total_tokens": 9536,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 6392,
  "provider_usage": {
    "completion_tokens": 2504,
    "prompt_tokens": 7032,
    "total_tokens": 9536,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 6392
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_KyEDcKoHqNfiHL4evFAB2466`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 9, "line_id": "line:hgam-4341-abs", "measurement_id": "fit:H2:0016", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
The Hγ_abs fit centre (4390.2 Å) falls outside the redshift window. I'll repair that row and resubmit the full set.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H2/pre_analysis/branches/main/0eac1cc2a9754a58ac2d013f59a900ed/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H2:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "blue_edge"
          ],
          "comment": "Fit centre 3732.2 vs pred 3726.0 (offset ~6 A, within window) but local SNR 0.57, FWHM ~6000 km/s and blue edge; weak, broad, unconvincing."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H2:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "blend_cah",
            "blue_edge"
          ],
          "comment": "Doublet fit centre 3937.6 (offset ~4 A) with separation pass, but local SNR 0.91 and FWHM ~890 km/s; plausible weak Ca K component, blended with Ca H."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H2:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "huge_width",
            "blend_cak",
            "blue_edge"
          ],
          "comment": "Ca H fit centre 3977.1 with very large error and FWHM ~20000 km/s; depth ordering (K deeper than H) preserved but fit is poorly constrained; plausible weak component."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Only fit attempt failed with center_at_bound (4019 A); no CWT emission feature near 3969 A."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Absorption fit failed with center_at_bound and enormous width; no credible trough near 3969 A."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "Emission fit center_at_bound (4151.8 A); no CWT peak near 4102 A."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H2:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 4114.2 (offset ~12 A) with local SNR 1.05 and FWHM ~730 km/s; weak absorption, no matching CWT trough."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H2:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 4283.8 (offset ~21 A, weaker band) with local SNR 1.12 and FWHM ~1500 km/s; weak, broad, no CWT trough."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H2:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 4360.6 (offset ~20 A) with local SNR 1.73 and FWHM ~950 km/s; weak emission, no matching CWT peak."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_large",
            "outside_window",
            "no_cwt_feature"
          ],
          "comment": "Fit centre 4390.2 implies z~+0.0114, outside the verification window; no credible Hgamma absorption measurement."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "offset_large"
          ],
          "comment": "Nearest CWT peak 4815.2 implies z=-0.0098, ~46 A blueward; no credible Hbeta emission measurement."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "offset_large"
          ],
          "comment": "Nearest CWT trough 4884.8 implies z=+0.0045, ~23 A redward; no adopted Hbeta absorption."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "cwt:em:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width",
            "blend_oiiib"
          ],
          "comment": "CWT peak 4964.0 (offset ~5 A, z=0.0007 in window) but FWHM ~4250 km/s, far broader than narrow [O III]; shared feature with [O III]b ambiguity."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "offset_large"
          ],
          "comment": "Only nearby peak 4964.0 implies z=-0.0088, ~43 A blueward; no separate [O III]b measurement; doublet separation fails."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Fit returned zero amplitude at 5224.8 A; no CWT trough near 5175 A."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_large",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit centre 5912.7 (offset ~23 A) with separation fail and component ratio ~1; no CWT trough near 5890 A."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_large",
            "no_cwt_feature"
          ],
          "comment": "No independent measurement; Na D doublet fit failed separation and is offset; no CWT trough near 5894 A."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_large",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit centre 5946.1 with huge error and separation fail; no credible Na D2 absorption."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Doublet fit returned zero amplitudes with separation fail; no CWT peak near 6548 A."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Fit returned zero amplitude at 6575.5 A; no CWT peak near 6563 A."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "offset_large"
          ],
          "comment": "Nearest CWT trough 6583.2 implies z=+0.0028, ~20 A redward; no adopted Halpha absorption."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "separation_fail"
          ],
          "comment": "Doublet fit zero amplitude with separation fail; no CWT peak near 6584 A."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "offset_large",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit centre 6726.4 (offset ~10 A) with separation fail and component ratio 2.03; nearest CWT peak 6651.2 implies z=-0.0100, outside window."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "huge_width",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit centre 6780.9 with FWHM ~7200 km/s and separation fail; no credible [S II]b measurement."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "red_edge"
          ],
          "comment": "Fit failed with center_at_bound (8545.8 A); no CWT trough near 8496 A."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H2:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "red_edge"
          ],
          "comment": "Fit centre 8551.9 (offset ~12 A) with local SNR 0.83 and FWHM ~3100 km/s; weak, broad, no CWT trough."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H2:0020",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8660.6 (offset ~1 A) with local SNR 1.68 and narrow FWHM ~80 km/s; weak but positionally consistent, no CWT trough."
        }
      ]
    },
    "id": "call_00_maQtgD0dWRhct8WG5eld2641",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 9642,
  "output_tokens": 2511,
  "total_tokens": 12153,
  "cache_hit_tokens": 9472,
  "cache_miss_tokens": 170,
  "provider_usage": {
    "completion_tokens": 2511,
    "prompt_tokens": 9642,
    "total_tokens": 12153,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 9472
    },
    "prompt_cache_hit_tokens": 9472,
    "prompt_cache_miss_tokens": 170
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_maQtgD0dWRhct8WG5eld2641`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H2/pre_analysis/branches/main/0eac1cc2a9754a58ac2d013f59a900ed/lines.csv", "n_lines": 27, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H2/pre_analysis/branches/main/0eac1cc2a9754a58ac2d013f59a900ed/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:28:34.951213+00:00
