# SH pre-analysis session: line review

- Run ID: `graph-6f4e6510cc5d45df9da3b7be0c8597cc`
- Hypothesis: `H1`
- Started (UTC): 2026-10-19T11:28:17.951595+00:00
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
Review every predicted line at the fixed Redrock redshift `0.2515625506820086`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H1/pre_analysis/branches/main/c47ae169db164d16a479007b831c6e8e/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 38.1 |

Verify the redshift hypothesis z ≈ 0.2515625506820086.

Verification window: z ∈ [0.2416, 0.2616]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=59.9498, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=18.0225, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=44.4305, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=43.5544, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=7.50938, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/LRG_1.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H1/pre_analysis/branches/main/c47ae169db164d16a479007b831c6e8e/lines.csv

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


## Predicted Lines at z = 0.2516

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [Ne V] | 3426.0 | 4287.9 | em | narrow | — |
| [O II] | 3727.0 | 4664.6 | em | narrow | peak@4668.8±0.8(z=0.2527) |
| Ca K_abs | 3934.8 | 4924.6 | abs | absorption | — |
| Ca H_abs | 3969.6 | 4968.2 | abs | absorption | — |
| Hε | 3970.1 | 4968.8 | em | both | peak@4964.0±0.8(z=0.2503) |
| Hε_abs | 3970.1 | 4968.8 | abs | absorption | — |
| Hδ | 4102.9 | 5135.0 | em | both | peak@5102.4±0.8(z=0.2436) |
| Hδ_abs | 4102.9 | 5135.0 | abs | absorption | — |
| G-band_abs | 4305.6 | 5388.7 | abs | absorption | — |
| Hγ | 4341.7 | 5433.9 | em | both | peak@5400.0±0.8(z=0.2438) |
| Hγ_abs | 4341.7 | 5433.9 | abs | absorption | trough@5472.0±0.8(z=0.2603) |
| Hβ | 4862.7 | 6086.0 | em | both | — |
| Hβ_abs | 4862.7 | 6086.0 | abs | absorption | — |
| [O III]a | 4960.3 | 6208.1 | em | narrow | — |
| [O III]b | 5008.2 | 6268.1 | em | narrow | peak@6292.0±0.8(z=0.2563) |
| Mg I_abs | 5176.7 | 6479.0 | abs | absorption | — |
| Na D1_abs | 5891.6 | 7373.7 | abs | absorption | — |
| Na D_abs | 5895.6 | 7378.7 | abs | absorption | — |
| Na D2_abs | 5897.6 | 7381.2 | abs | absorption | — |
| [N II]a | 6549.8 | 8197.5 | em | narrow | — |
| Hα | 6564.6 | 8216.0 | em | both | — |
| Hα_abs | 6564.6 | 8216.0 | abs | absorption | — |
| [N II]b | 6585.3 | 8241.9 | em | narrow | — |
| [S II]a | 6718.3 | 8408.4 | em | narrow | peak@8430.4±0.8(z=0.2548) |
| [S II]b | 6732.7 | 8426.4 | em | narrow | peak@8430.4±0.8(z=0.2522) |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 6208.1/6268.1 | fit_doublet | 6236.072±1.556/6292.532±1.7331 | 0.550407/0.728398 | 924.7/2019.7 | 2.36 | 0.376 | ok; separation pass; component ratio 1.32 |
| [N II]a/[N II]b | 8197.5/8241.9 | fit_doublet | 8147.484±56.5819/8234.218±3.4723 | 0.750418/0.189125 | 20113.0/584.4 | 3.56 | 8.061 | warning: center_1_deviation_large; separation fail; component ratio 0.25 |
| Ca K_abs/Ca H_abs | 4924.6/4968.2 | fit_doublet | 4926.077±5.2898/4918.203±0.0 | -1.462986/-0.0 | 16342.1/43061.9 | 3.23 | 3.507 | warning; separation fail |
| Na D1_abs/Na D2_abs | 7373.7/7381.2 | fit_doublet | 7323.707±0.0/7331.217±0.0 | -0.0/-0.0 | 96.4/96.3 | 0.0 | -0.0 | ok; separation pass; component ratio — |
| [Ne V] | 4287.9 | fit_peak | 4337.853±6.5337 | 0.233431 | 3378.7 | 0.67 | 0.041 | warning: center_at_bound |
| Hβ | 6086.0 | fit_peak | 6078.573±4.9544 | 0.444562 | 5585.2 | 1.61 | 0.55 | ok |
| Hα | 8216.0 | fit_peak | 8194.122±14.2056 | 0.194401 | 5814.5 | 0.92 | 0.255 | ok |
| Hε_abs | 4968.8 | fit_peak | 4965.398±9.2404 | -1.697013 | 16315.0 | 3.18 | 5.066 | ok |
| Hδ_abs | 5135.0 | fit_peak | 5184.536±0.0 | -0.0 | 136.4 | 0.0 | -0.0 | ok |
| G-band_abs | 5388.7 | fit_peak | 5357.08±69.6193 | -1.368236 | 26356.0 | 3.72 | 10.216 | ok |
| Hβ_abs | 6086.0 | fit_peak | 6035.975±22330.741 | -0.0 | 117.0 | 0.0 | -0.0 | warning: center_at_bound |
| Mg I_abs | 6479.0 | fit_peak | 6464.242±2.2264 | -0.389993 | 426.0 | 1.1 | 0.021 | ok |
| Hα_abs | 8216.0 | fit_peak | 8166.06±1.63 | -0.161364 | 86.5 | 0.76 | 0.003 | warning: center_at_bound |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:nev-3426 | [Ne V] | 4287.9 | emission |
| line:oii-3727 | [O II] | 4664.6 | emission |
| line:cak-3934-abs | Ca K_abs | 4924.6 | absorption |
| line:cah-3969-abs | Ca H_abs | 4968.2 | absorption |
| line:heps-3970 | Hε | 4968.8 | emission |
| line:heps-3970-abs | Hε_abs | 4968.8 | absorption |
| line:hdel-4102 | Hδ | 5135.0 | emission |
| line:hdel-4102-abs | Hδ_abs | 5135.0 | absorption |
| line:gband-4305-abs | G-band_abs | 5388.7 | absorption |
| line:hgam-4341 | Hγ | 5433.9 | emission |
| line:hgam-4341-abs | Hγ_abs | 5433.9 | absorption |
| line:hbet-4862 | Hβ | 6086.0 | emission |
| line:hbet-4862-abs | Hβ_abs | 6086.0 | absorption |
| line:oiii-4960 | [O III]a | 6208.1 | emission |
| line:oiii-5008 | [O III]b | 6268.1 | emission |
| line:mgi-5176-abs | Mg I_abs | 6479.0 | absorption |
| line:nad1-5891-abs | Na D1_abs | 7373.7 | absorption |
| line:nad-5895-abs | Na D_abs | 7378.7 | absorption |
| line:nad2-5897-abs | Na D2_abs | 7381.2 | absorption |
| line:nii-6549 | [N II]a | 8197.5 | emission |
| line:half-6564 | Hα | 8216.0 | emission |
| line:half-6564-abs | Hα_abs | 8216.0 | absorption |
| line:nii-6585 | [N II]b | 8241.9 | emission |
| line:sii-6718 | [S II]a | 8408.4 | emission |
| line:sii-6732 | [S II]b | 8426.4 | emission |

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
| fit:H1:0000 | fit_doublet | emission | 6236.072 | [O III]a | yes | — |
| fit:H1:0001 | fit_doublet | emission | 6292.532 | [O III]b | yes | — |
| fit:H1:0002 | fit_doublet | emission | 8147.484 | [N II]a | yes | — |
| fit:H1:0003 | fit_doublet | emission | 8234.218 | [N II]b | yes | — |
| fit:H1:0004 | fit_doublet | absorption | 4926.077 | Ca K_abs | yes | — |
| fit:H1:0005 | fit_doublet | absorption | 4918.203 | Ca H_abs | yes | — |
| fit:H1:0006 | fit_doublet | absorption | 7323.707 | Na D1_abs | yes | — |
| fit:H1:0007 | fit_doublet | absorption | 7331.217 | Na D2_abs | yes | — |
| fit:H1:0008 | fit_peak | emission | 4337.853 | [Ne V] | no | center_at_bound |
| fit:H1:0009 | fit_peak | emission | 6078.573 | Hβ | yes | — |
| fit:H1:0010 | fit_peak | emission | 8194.122 | Hα | yes | — |
| fit:H1:0011 | fit_peak | absorption | 4965.398 | Hε_abs | yes | — |
| fit:H1:0012 | fit_peak | absorption | 5184.536 | Hδ_abs | yes | — |
| fit:H1:0013 | fit_peak | absorption | 5357.080 | G-band_abs | yes | — |
| fit:H1:0014 | fit_peak | absorption | 6035.975 | Hβ_abs | no | center_at_bound |
| fit:H1:0015 | fit_peak | absorption | 6464.242 | Mg I_abs | yes | — |
| fit:H1:0016 | fit_peak | absorption | 8166.060 | Hα_abs | no | center_at_bound |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H1/pre_analysis/branches/main/c47ae169db164d16a479007b831c6e8e/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "low_snr"
          ],
          "comment": "No CWT peak near 4287.9; only fit attempt is center_at_bound (4337.9, unselectable) with local SNR 0.67. No credible measurement."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": "cwt:em:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_4A",
            "broad_width",
            "blend_risk"
          ],
          "comment": "CWT peak 4668.8 vs pred 4664.6, offset ~4 A (strong window), implied z=0.2527 in window. FWHM ~4839 km/s is very broad for a narrow [O II] and amplitude weak (0.3); plausible but width/blend caveat."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H1:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "blend_risk",
            "uncertain_depth_order"
          ],
          "comment": "Doublet fit centre 4926.1 (offset ~1.5 A) but separation fails and Ca H component collapsed to zero amplitude; Ca K depth plausible though ordering uncertain. Weak but plausible Ca K component retained."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H1:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "zero_amplitude_component",
            "blend_risk"
          ],
          "comment": "Ca H fit centre 4918.2 with zero amplitude and zero error; separation fails. Weak Ca H component preserved as plausible despite uncertain fitted depth ordering."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "cwt:em:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_5A",
            "broad_width",
            "blend_with_cah"
          ],
          "comment": "CWT peak 4964.0 vs pred 4968.8, offset ~5 A, implied z=0.2503 in window. FWHM ~4248 km/s broad; blended with Ca H absorption region. Weak emission candidate."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H1:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "broad_width",
            "blend_with_cah",
            "offset_3A"
          ],
          "comment": "Fit centre 4965.4, offset ~3 A, amplitude -1.70 but FWHM ~16315 km/s extremely broad; likely blended with Ca H absorption. Weak plausible absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "cwt:em:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_33A",
            "broad_width",
            "weak_amplitude"
          ],
          "comment": "CWT peak 5102.4 vs pred 5135.0, offset ~33 A (weaker window), implied z=0.2436 in window. Broad FWHM ~4132 km/s; weak emission candidate."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H1:0012",
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_trough"
          ],
          "comment": "Fit centre 5184.5 with zero amplitude and zero error; no CWT trough near 5135. No credible absorption measurement."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H1:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_32A",
            "very_broad_width",
            "high_reduced_chi2"
          ],
          "comment": "Fit centre 5357.1, offset ~32 A (weaker window), amplitude -1.37 but FWHM ~26356 km/s and dchi2/n 10.2; broad blend-like trough. Weak marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "cwt:em:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_34A",
            "broad_width",
            "weak_amplitude"
          ],
          "comment": "CWT peak 5400.0 vs pred 5433.9, offset ~34 A (weaker window), implied z=0.2438 in window. Broad FWHM ~5220 km/s; weak emission candidate."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "cwt:abs:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_38A",
            "broad_width",
            "blend_risk"
          ],
          "comment": "CWT trough 5472.0 vs pred 5433.9, offset ~38 A (weaker window), implied z=0.2603 in window. FWHM ~2909 km/s; weak absorption candidate with blend caveat."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "fit:H1:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_7A",
            "very_broad_width",
            "low_local_snr"
          ],
          "comment": "Fit centre 6078.6, offset ~7 A, amplitude 0.44 but FWHM ~5585 km/s and local SNR 1.61; no CWT peak. Weak marginal emission."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_cwt_trough"
          ],
          "comment": "Only fit attempt is center_at_bound (6036.0, unselectable) with zero amplitude; no CWT trough near 6086. No credible measurement."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "fit:H1:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_28A",
            "doublet_ratio_off",
            "broad_width"
          ],
          "comment": "Doublet fit centre 6236.1 vs pred 6208.1, offset ~28 A (weaker window); separation passes but component ratio 1.32 vs expected 3 and FWHM ~925 km/s. Weak marginal."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "cwt:em:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_24A",
            "broad_width",
            "doublet_ratio_off"
          ],
          "comment": "CWT peak 6292.0 vs pred 6268.1, offset ~24 A (weaker window), implied z=0.2563 in window; fit centre 6292.5. FWHM ~4055 km/s broad; ratio inconsistent with [O III] doublet. Marginal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H1:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_15A",
            "low_local_snr",
            "weak_amplitude"
          ],
          "comment": "Fit centre 6464.2, offset ~15 A (strong window), amplitude -0.39, FWHM ~426 km/s, local SNR 1.1. Weak but plausible absorption."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H1:0006",
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_trough"
          ],
          "comment": "Na D doublet fit centres 7323.7/7331.2 with zero amplitude and zero error; no CWT trough near 7373.7. No credible measurement."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "no_cwt_trough"
          ],
          "comment": "No CWT trough or selectable fit near 7378.7; Na D doublet fit returned zero amplitude. No credible measurement."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H1:0007",
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_trough"
          ],
          "comment": "Na D2 fit centre 7331.2 with zero amplitude and zero error; no CWT trough near 7381.2. No credible measurement."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H1:0002",
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_deviation_large",
            "separation_fail",
            "very_broad_width"
          ],
          "comment": "Fit centre 8147.5 deviates ~50 A from pred 8197.5 with FWHM ~20113 km/s and separation fail; not a credible [N II]a measurement."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H1:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_22A",
            "very_broad_width",
            "low_local_snr"
          ],
          "comment": "Fit centre 8194.1, offset ~22 A (weaker window), amplitude 0.19, FWHM ~5815 km/s, local SNR 0.92; no CWT peak. Weak marginal emission."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_cwt_trough"
          ],
          "comment": "Only fit attempt center_at_bound (8166.1, unselectable) with tiny amplitude; no CWT trough near 8216. No credible measurement."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H1:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_8A",
            "doublet_ratio_off",
            "separation_fail"
          ],
          "comment": "Fit centre 8234.2, offset ~8 A, amplitude 0.19, FWHM ~584 km/s; doublet separation fails and ratio 0.25 vs expected 3. Weak marginal, blend ambiguity with Halpha."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "cwt:em:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_22A",
            "shared_feature",
            "broad_width"
          ],
          "comment": "CWT peak 8430.4 vs pred 8408.4, offset ~22 A (weaker window), implied z=0.2548 in window. Shared feature with [S II]b; FWHM ~4045 km/s broad. Marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "cwt:em:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_4A",
            "shared_feature",
            "doublet_unresolved"
          ],
          "comment": "Same CWT peak 8430.4 vs pred 8426.4, offset ~4 A, implied z=0.2522 in window. Shared with [S II]a; doublet unresolved at this width. Marginal."
        }
      ]
    },
    "id": "call_00_XEfScnjELT6k9mjA0teO0015",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 6631,
  "output_tokens": 2776,
  "total_tokens": 9407,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 5991,
  "provider_usage": {
    "completion_tokens": 2776,
    "prompt_tokens": 6631,
    "total_tokens": 9407,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 5991
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_XEfScnjELT6k9mjA0teO0015`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 3, "line_id": "line:cah-3969-abs", "measurement_id": "fit:H1:0005", "reason": "measurement is outside this line's redshift window"}, {"row": 7, "line_id": "line:hdel-4102-abs", "reason": "unadopted line needs null measurement_id"}, {"row": 16, "line_id": "line:nad1-5891-abs", "reason": "unadopted line needs null measurement_id"}, {"row": 18, "line_id": "line:nad2-5897-abs", "reason": "unadopted line needs null measurement_id"}, {"row": 19, "line_id": "line:nii-6549", "reason": "unadopted line needs null measurement_id"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
I'll repair the flagged rows: Ca H fit is outside the window, and NOT_FOUND rows need null measurement IDs.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H1/pre_analysis/branches/main/c47ae169db164d16a479007b831c6e8e/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "low_snr"
          ],
          "comment": "No CWT peak near 4287.9; only fit attempt is center_at_bound (4337.9, unselectable) with local SNR 0.67. No credible measurement."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": "cwt:em:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_4A",
            "broad_width",
            "blend_risk"
          ],
          "comment": "CWT peak 4668.8 vs pred 4664.6, offset ~4 A (strong window), implied z=0.2527 in window. FWHM ~4839 km/s is very broad for a narrow [O II] and amplitude weak (0.3); plausible but width/blend caveat."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H1:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "blend_risk",
            "uncertain_depth_order"
          ],
          "comment": "Doublet fit centre 4926.1 (offset ~1.5 A) but separation fails and Ca H component collapsed to zero amplitude; Ca K depth plausible though ordering uncertain. Weak but plausible Ca K component retained."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_outside_window",
            "zero_amplitude_component",
            "doublet_separation_fail"
          ],
          "comment": "Ca H fit centre 4918.2 lies outside the redshift window and has zero amplitude/zero error; separation fails. No credible adopted measurement."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "cwt:em:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_5A",
            "broad_width",
            "blend_with_cah"
          ],
          "comment": "CWT peak 4964.0 vs pred 4968.8, offset ~5 A, implied z=0.2503 in window. FWHM ~4248 km/s broad; blended with Ca H absorption region. Weak emission candidate."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H1:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "broad_width",
            "blend_with_cah",
            "offset_3A"
          ],
          "comment": "Fit centre 4965.4, offset ~3 A, amplitude -1.70 but FWHM ~16315 km/s extremely broad; likely blended with Ca H absorption. Weak plausible absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "cwt:em:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_33A",
            "broad_width",
            "weak_amplitude"
          ],
          "comment": "CWT peak 5102.4 vs pred 5135.0, offset ~33 A (weaker window), implied z=0.2436 in window. Broad FWHM ~4132 km/s; weak emission candidate."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_trough"
          ],
          "comment": "Fit centre 5184.5 with zero amplitude and zero error; no CWT trough near 5135. No credible absorption measurement."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H1:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_32A",
            "very_broad_width",
            "high_reduced_chi2"
          ],
          "comment": "Fit centre 5357.1, offset ~32 A (weaker window), amplitude -1.37 but FWHM ~26356 km/s and dchi2/n 10.2; broad blend-like trough. Weak marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "cwt:em:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_34A",
            "broad_width",
            "weak_amplitude"
          ],
          "comment": "CWT peak 5400.0 vs pred 5433.9, offset ~34 A (weaker window), implied z=0.2438 in window. Broad FWHM ~5220 km/s; weak emission candidate."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "cwt:abs:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_38A",
            "broad_width",
            "blend_risk"
          ],
          "comment": "CWT trough 5472.0 vs pred 5433.9, offset ~38 A (weaker window), implied z=0.2603 in window. FWHM ~2909 km/s; weak absorption candidate with blend caveat."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "fit:H1:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_7A",
            "very_broad_width",
            "low_local_snr"
          ],
          "comment": "Fit centre 6078.6, offset ~7 A, amplitude 0.44 but FWHM ~5585 km/s and local SNR 1.61; no CWT peak. Weak marginal emission."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_cwt_trough"
          ],
          "comment": "Only fit attempt is center_at_bound (6036.0, unselectable) with zero amplitude; no CWT trough near 6086. No credible measurement."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "fit:H1:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_28A",
            "doublet_ratio_off",
            "broad_width"
          ],
          "comment": "Doublet fit centre 6236.1 vs pred 6208.1, offset ~28 A (weaker window); separation passes but component ratio 1.32 vs expected 3 and FWHM ~925 km/s. Weak marginal."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "cwt:em:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_24A",
            "broad_width",
            "doublet_ratio_off"
          ],
          "comment": "CWT peak 6292.0 vs pred 6268.1, offset ~24 A (weaker window), implied z=0.2563 in window; fit centre 6292.5. FWHM ~4055 km/s broad; ratio inconsistent with [O III] doublet. Marginal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H1:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_15A",
            "low_local_snr",
            "weak_amplitude"
          ],
          "comment": "Fit centre 6464.2, offset ~15 A (strong window), amplitude -0.39, FWHM ~426 km/s, local SNR 1.1. Weak but plausible absorption."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_trough"
          ],
          "comment": "Na D doublet fit centres 7323.7/7331.2 with zero amplitude and zero error; no CWT trough near 7373.7. No credible measurement."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "no_cwt_trough"
          ],
          "comment": "No CWT trough or selectable fit near 7378.7; Na D doublet fit returned zero amplitude. No credible measurement."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_trough"
          ],
          "comment": "Na D2 fit centre 7331.2 with zero amplitude and zero error; no CWT trough near 7381.2. No credible measurement."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_deviation_large",
            "separation_fail",
            "very_broad_width"
          ],
          "comment": "Fit centre 8147.5 deviates ~50 A from pred 8197.5 with FWHM ~20113 km/s and separation fail; not a credible [N II]a measurement."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H1:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_22A",
            "very_broad_width",
            "low_local_snr"
          ],
          "comment": "Fit centre 8194.1, offset ~22 A (weaker window), amplitude 0.19, FWHM ~5815 km/s, local SNR 0.92; no CWT peak. Weak marginal emission."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_cwt_trough"
          ],
          "comment": "Only fit attempt center_at_bound (8166.1, unselectable) with tiny amplitude; no CWT trough near 8216. No credible measurement."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H1:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_8A",
            "doublet_ratio_off",
            "separation_fail"
          ],
          "comment": "Fit centre 8234.2, offset ~8 A, amplitude 0.19, FWHM ~584 km/s; doublet separation fails and ratio 0.25 vs expected 3. Weak marginal, blend ambiguity with Halpha."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "cwt:em:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_22A",
            "shared_feature",
            "broad_width"
          ],
          "comment": "CWT peak 8430.4 vs pred 8408.4, offset ~22 A (weaker window), implied z=0.2548 in window. Shared feature with [S II]b; FWHM ~4045 km/s broad. Marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "cwt:em:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_4A",
            "shared_feature",
            "doublet_unresolved"
          ],
          "comment": "Same CWT peak 8430.4 vs pred 8426.4, offset ~4 A, implied z=0.2522 in window. Shared with [S II]a; doublet unresolved at this width. Marginal."
        }
      ]
    },
    "id": "call_00_6iSb2FECcgwxVJaiWShS8921",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 9645,
  "output_tokens": 2749,
  "total_tokens": 12394,
  "cache_hit_tokens": 9344,
  "cache_miss_tokens": 301,
  "provider_usage": {
    "completion_tokens": 2749,
    "prompt_tokens": 9645,
    "total_tokens": 12394,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 9344
    },
    "prompt_cache_hit_tokens": 9344,
    "prompt_cache_miss_tokens": 301
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_6iSb2FECcgwxVJaiWShS8921`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H1/pre_analysis/branches/main/c47ae169db164d16a479007b831c6e8e/lines.csv", "n_lines": 25, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H1/pre_analysis/branches/main/c47ae169db164d16a479007b831c6e8e/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:28:39.196497+00:00
