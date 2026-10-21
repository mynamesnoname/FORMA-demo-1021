# SH pre-analysis session: line review

- Run ID: `graph-6f4e6510cc5d45df9da3b7be0c8597cc`
- Hypothesis: `H5`
- Started (UTC): 2026-10-19T11:28:30.513139+00:00
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
Review every predicted line at the fixed Redrock redshift `0.2717824860918102`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H5/pre_analysis/branches/main/b93e4e52c42a4719b89f2b10a58f5d3b/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 38.1 |

Verify the redshift hypothesis z ≈ 0.2717824860918102.

Verification window: z ∈ [0.2618, 0.2818]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=60.9184, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=18.3137, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=45.1483, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=44.258, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=7.63069, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/LRG_1.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H5/pre_analysis/branches/main/b93e4e52c42a4719b89f2b10a58f5d3b/lines.csv

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


## Predicted Lines at z = 0.2718

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [Ne V] | 3426.0 | 4357.1 | em | narrow | — |
| [O II] | 3727.0 | 4739.9 | em | narrow | — |
| Ca K_abs | 3934.8 | 5004.2 | abs | absorption | — |
| Ca H_abs | 3969.6 | 5048.5 | abs | absorption | trough@5049.6±0.8(z=0.2721) |
| Hε | 3970.1 | 5049.1 | em | both | — |
| Hε_abs | 3970.1 | 5049.1 | abs | absorption | trough@5049.6±0.8(z=0.2719) |
| Hδ | 4102.9 | 5218.0 | em | both | — |
| Hδ_abs | 4102.9 | 5218.0 | abs | absorption | — |
| G-band_abs | 4305.6 | 5475.8 | abs | absorption | trough@5472.0±0.8(z=0.2709) |
| Hγ | 4341.7 | 5521.7 | em | both | peak@5532.8±0.8(z=0.2743) |
| Hγ_abs | 4341.7 | 5521.7 | abs | absorption | — |
| Hβ | 4862.7 | 6184.3 | em | both | — |
| Hβ_abs | 4862.7 | 6184.3 | abs | absorption | trough@6188.8±0.8(z=0.2727) |
| [O III]a | 4960.3 | 6308.4 | em | narrow | peak@6292.0±0.8(z=0.2685) |
| [O III]b | 5008.2 | 6369.3 | em | narrow | — |
| Mg I_abs | 5176.7 | 6583.6 | abs | absorption | trough@6583.2±0.8(z=0.2717) |
| Na D1_abs | 5891.6 | 7492.8 | abs | absorption | trough@7496.8±0.8(z=0.2725) |
| Na D_abs | 5895.6 | 7497.9 | abs | absorption | trough@7496.8±0.8(z=0.2716) |
| Na D2_abs | 5897.6 | 7500.5 | abs | absorption | trough@7496.8±0.8(z=0.2712) |
| [N II]a | 6549.8 | 8329.9 | em | narrow | — |
| Hα | 6564.6 | 8348.7 | em | both | — |
| Hα_abs | 6564.6 | 8348.7 | abs | absorption | trough@8348.8±0.8(z=0.2718) |
| [N II]b | 6585.3 | 8375.1 | em | narrow | peak@8430.4±0.8(z=0.2802) |
| [S II]a | 6718.3 | 8544.2 | em | narrow | — |
| [S II]b | 6732.7 | 8562.5 | em | narrow | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 6308.4/6369.3 | fit_doublet | 6292.215±2.4331/6419.341±8.449 | 0.658011/0.182595 | 2475.3/2254.7 | 2.22 | 0.346 | warning; separation fail; component ratio 0.28 |
| [S II]a/[S II]b | 8544.2/8562.5 | fit_doublet | 8495.637±1.1285/8612.117±0.0 | 0.241993/0.0 | 83.1/90.3 | 1.12 | 0.004 | warning; separation fail; component ratio 0.0 |
| [N II]a/[N II]b | 8329.9/8375.1 | fit_doublet | 8304.449±2.1886/8417.451±4.2316 | 0.390783/0.281941 | 1169.2/2230.2 | 2.01 | 0.33 | warning; separation fail; component ratio 0.72 |
| Ca K_abs/Ca H_abs | 5004.2/5048.5 | fit_doublet | 5004.88±0.7153/5047.321±0.6399 | -1.939078/-1.970934 | 1198.4/982.4 | 3.83 | 0.662 | ok; separation pass |
| [Ne V] | 4357.1 | fit_peak | 4360.589±1.3218 | 0.573016 | 970.5 | 1.79 | 0.085 | ok |
| [O II] | 4739.9 | fit_peak | 4689.933±15.0726 | 1.012228 | 16480.2 | 2.89 | 3.949 | warning: center_at_bound |
| Hε | 5049.1 | fit_peak | 5099.104±2.0546 | 1.099744 | 2803.7 | 2.66 | 0.636 | warning: center_at_bound |
| Hδ | 5218.0 | fit_peak | 5167.996±5.1489 | 1.166705 | 9685.2 | 3.06 | 2.946 | warning: center_at_bound |
| Hβ | 6184.3 | fit_peak | 6234.297±2.0711 | 0.422806 | 740.5 | 1.29 | 0.048 | warning: center_at_bound |
| Hα | 8348.7 | fit_peak | 8398.743±4.9781 | 0.228822 | 1540.8 | 1.11 | 0.101 | warning: center_at_bound |
| Hδ_abs | 5218.0 | fit_peak | 5215.641±1.7703 | -0.309637 | 135.4 | 0.67 | 0.002 | ok |
| Hγ_abs | 5521.7 | fit_peak | 5522.311±1.1598 | -0.501397 | 248.0 | 1.4 | 0.017 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:nev-3426 | [Ne V] | 4357.1 | emission |
| line:oii-3727 | [O II] | 4739.9 | emission |
| line:cak-3934-abs | Ca K_abs | 5004.2 | absorption |
| line:cah-3969-abs | Ca H_abs | 5048.5 | absorption |
| line:heps-3970 | Hε | 5049.1 | emission |
| line:heps-3970-abs | Hε_abs | 5049.1 | absorption |
| line:hdel-4102 | Hδ | 5218.0 | emission |
| line:hdel-4102-abs | Hδ_abs | 5218.0 | absorption |
| line:gband-4305-abs | G-band_abs | 5475.8 | absorption |
| line:hgam-4341 | Hγ | 5521.7 | emission |
| line:hgam-4341-abs | Hγ_abs | 5521.7 | absorption |
| line:hbet-4862 | Hβ | 6184.3 | emission |
| line:hbet-4862-abs | Hβ_abs | 6184.3 | absorption |
| line:oiii-4960 | [O III]a | 6308.4 | emission |
| line:oiii-5008 | [O III]b | 6369.3 | emission |
| line:mgi-5176-abs | Mg I_abs | 6583.6 | absorption |
| line:nad1-5891-abs | Na D1_abs | 7492.8 | absorption |
| line:nad-5895-abs | Na D_abs | 7497.9 | absorption |
| line:nad2-5897-abs | Na D2_abs | 7500.5 | absorption |
| line:nii-6549 | [N II]a | 8329.9 | emission |
| line:half-6564 | Hα | 8348.7 | emission |
| line:half-6564-abs | Hα_abs | 8348.7 | absorption |
| line:nii-6585 | [N II]b | 8375.1 | emission |
| line:sii-6718 | [S II]a | 8544.2 | emission |
| line:sii-6732 | [S II]b | 8562.5 | emission |

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
| fit:H5:0000 | fit_doublet | emission | 6292.215 | [O III]a | yes | — |
| fit:H5:0001 | fit_doublet | emission | 6419.341 | [O III]b | yes | — |
| fit:H5:0002 | fit_doublet | emission | 8495.637 | [S II]a | yes | — |
| fit:H5:0003 | fit_doublet | emission | 8612.117 | [S II]b | yes | — |
| fit:H5:0004 | fit_doublet | emission | 8304.449 | [N II]a | yes | — |
| fit:H5:0005 | fit_doublet | emission | 8417.451 | [N II]b | yes | — |
| fit:H5:0006 | fit_doublet | absorption | 5004.880 | Ca K_abs | yes | — |
| fit:H5:0007 | fit_doublet | absorption | 5047.321 | Ca H_abs | yes | — |
| fit:H5:0008 | fit_peak | emission | 4360.589 | [Ne V] | yes | — |
| fit:H5:0009 | fit_peak | emission | 4689.933 | [O II] | no | center_at_bound |
| fit:H5:0010 | fit_peak | emission | 5099.104 | Hε | no | center_at_bound |
| fit:H5:0011 | fit_peak | emission | 5167.996 | Hδ | no | center_at_bound |
| fit:H5:0012 | fit_peak | emission | 6234.297 | Hβ | no | center_at_bound |
| fit:H5:0013 | fit_peak | emission | 8398.743 | Hα | no | center_at_bound |
| fit:H5:0014 | fit_peak | absorption | 5215.641 | Hδ_abs | yes | — |
| fit:H5:0015 | fit_peak | absorption | 5522.311 | Hγ_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H5/pre_analysis/branches/main/b93e4e52c42a4719b89f2b10a58f5d3b/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": "fit:H5:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "no_cwt_peak",
            "fit_only"
          ],
          "comment": "Only targeted fit at 4360.6 (z=0.2727, in window); no CWT peak nearby, local SNR 1.79, broad 970 km/s. Weak candidate."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "no_cwt_peak"
          ],
          "comment": "Fit center_at_bound at 4689.9 (z=0.258, outside window) and unselectable; no CWT peak near 4739.9."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H5:0006",
          "status": "LIKELY",
          "reason_codes": [
            "doublet_fit_ok",
            "separation_pass"
          ],
          "comment": "Doublet fit centre 5004.9 (z=0.2718), separation passes; depth ordering vs Ca H uncertain but plausible."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H5:0007",
          "status": "LIKELY",
          "reason_codes": [
            "doublet_fit_ok",
            "separation_pass",
            "depth_ordering_uncertain"
          ],
          "comment": "Doublet fit centre 5047.3 (z=0.2716); Ca H fitted slightly deeper than Ca K, ordering uncertain but component real; CWT trough at 5049.6."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "blend_with_cah"
          ],
          "comment": "Emission fit center_at_bound at 5099.1, unselectable; region dominated by Ca H absorption trough at 5049.6."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "cwt:abs:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "blend_with_cah",
            "weak_amp"
          ],
          "comment": "Trough at 5049.6 (z=0.2719) matches, but blended with Ca H absorption; cannot separate Hε absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "no_cwt_peak"
          ],
          "comment": "Emission fit center_at_bound at 5168.0, unselectable; no CWT peak near 5218."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H5:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "narrow"
          ],
          "comment": "Fit at 5215.6 (z=0.2714), in window, but local SNR 0.67 and narrow 135 km/s; weak candidate."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "cwt:abs:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad"
          ],
          "comment": "Trough at 5472.0 (z=0.2709), offset ~4 Å from prediction; broad 2909 km/s, plausible G-band but weak."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "cwt:em:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "weak_amp",
            "blend"
          ],
          "comment": "Peak at 5532.8 (z=0.2743), offset ~11 Å; amplitude near zero, weak emission candidate."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H5:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "narrow"
          ],
          "comment": "Fit at 5522.3 (z=0.2719), in window, but local SNR 1.4 and narrow 248 km/s; weak."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "no_cwt_peak"
          ],
          "comment": "Emission fit center_at_bound at 6234.3, unselectable; no CWT peak near 6184."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "cwt:abs:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad"
          ],
          "comment": "Trough at 6188.8 (z=0.2727), offset ~4.5 Å; broad 3407 km/s, plausible Hβ absorption but weak."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "cwt:em:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend"
          ],
          "comment": "CWT peak at 6292.0 (z=0.2685), offset ~16 Å; doublet fit separation fails and ratio 0.28, so identity uncertain."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "rejected_fit",
            "no_cwt_peak"
          ],
          "comment": "Doublet fit centre 6419.3 (z=0.2818, at window edge) with separation fail; no CWT peak near 6369.3."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "cwt:abs:0007",
          "status": "LIKELY",
          "reason_codes": [
            "offset_strong",
            "ridge_persistent"
          ],
          "comment": "Trough at 6583.2 (z=0.2717), offset 0.4 Å, ridge 10, SNR 11.8; strong Mg I absorption match."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "cwt:abs:0009",
          "status": "LIKELY",
          "reason_codes": [
            "offset_strong",
            "blend_na_d"
          ],
          "comment": "Trough at 7496.8 (z=0.2725), offset ~4 Å; blended Na D doublet, component plausible."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": "cwt:abs:0009",
          "status": "LIKELY",
          "reason_codes": [
            "offset_strong",
            "blend_na_d"
          ],
          "comment": "Same trough at 7496.8 (z=0.2716) shared with Na D1/D2; blended doublet, component plausible."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "cwt:abs:0009",
          "status": "LIKELY",
          "reason_codes": [
            "offset_strong",
            "blend_na_d"
          ],
          "comment": "Same trough at 7496.8 (z=0.2712) shared with Na D1/D; blended doublet, component plausible."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H5:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend_with_halpha"
          ],
          "comment": "Fit centre 8304.4 (z=0.2681), offset ~25 Å; separation fails, ratio 0.72; blended with Hα region."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "no_cwt_peak"
          ],
          "comment": "Emission fit center_at_bound at 8398.7, unselectable; no CWT peak near 8348.7."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "cwt:abs:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_amp",
            "blend_with_nii"
          ],
          "comment": "Trough at 8348.8 (z=0.2718), offset 0.1 Å; weak amplitude, blended with N II region."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "cwt:em:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "doublet_separation_fail",
            "blend"
          ],
          "comment": "Peak at 8430.4 (z=0.2802, near window edge), offset ~55 Å; doublet fit separation fails; weak identity."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H5:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak"
          ],
          "comment": "Fit centre 8495.6 (z=0.2701), offset ~49 Å; separation fails, second component zero amplitude; weak."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "zero_amplitude",
            "rejected_fit"
          ],
          "comment": "Doublet fit second component at 8612.1 with zero amplitude and separation fail; no credible measurement."
        }
      ]
    },
    "id": "call_00_AxN5fvJRb0hXXHDVF94T1863",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 6633,
  "output_tokens": 2408,
  "total_tokens": 9041,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 5993,
  "provider_usage": {
    "completion_tokens": 2408,
    "prompt_tokens": 6633,
    "total_tokens": 9041,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 5993
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_AxN5fvJRb0hXXHDVF94T1863`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"name": "Na D_abs", "reason": "blended label duplicates an adopted doublet component"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
The tool rejects assigning the same measurement to both Na D1 and Na D (blended label duplicates an adopted doublet component). I'll keep the shared trough on Na D1 and Na D2, and mark Na D_abs as NOT_FOUND (no separate measurement adopted).
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H5/pre_analysis/branches/main/b93e4e52c42a4719b89f2b10a58f5d3b/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": "fit:H5:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "no_cwt_peak",
            "fit_only"
          ],
          "comment": "Only targeted fit at 4360.6 (z=0.2727, in window); no CWT peak nearby, local SNR 1.79, broad 970 km/s. Weak candidate."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "no_cwt_peak"
          ],
          "comment": "Fit center_at_bound at 4689.9 (z=0.258, outside window) and unselectable; no CWT peak near 4739.9."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H5:0006",
          "status": "LIKELY",
          "reason_codes": [
            "doublet_fit_ok",
            "separation_pass"
          ],
          "comment": "Doublet fit centre 5004.9 (z=0.2718), separation passes; depth ordering vs Ca H uncertain but plausible."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H5:0007",
          "status": "LIKELY",
          "reason_codes": [
            "doublet_fit_ok",
            "separation_pass",
            "depth_ordering_uncertain"
          ],
          "comment": "Doublet fit centre 5047.3 (z=0.2716); Ca H fitted slightly deeper than Ca K, ordering uncertain but component real; CWT trough at 5049.6."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "blend_with_cah"
          ],
          "comment": "Emission fit center_at_bound at 5099.1, unselectable; region dominated by Ca H absorption trough at 5049.6."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "cwt:abs:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "blend_with_cah",
            "weak_amp"
          ],
          "comment": "Trough at 5049.6 (z=0.2719) matches, but blended with Ca H absorption; cannot separate Hε absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "no_cwt_peak"
          ],
          "comment": "Emission fit center_at_bound at 5168.0, unselectable; no CWT peak near 5218."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H5:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "narrow"
          ],
          "comment": "Fit at 5215.6 (z=0.2714), in window, but local SNR 0.67 and narrow 135 km/s; weak candidate."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "cwt:abs:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad"
          ],
          "comment": "Trough at 5472.0 (z=0.2709), offset ~4 Å from prediction; broad 2909 km/s, plausible G-band but weak."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "cwt:em:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "weak_amp",
            "blend"
          ],
          "comment": "Peak at 5532.8 (z=0.2743), offset ~11 Å; amplitude near zero, weak emission candidate."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H5:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "narrow"
          ],
          "comment": "Fit at 5522.3 (z=0.2719), in window, but local SNR 1.4 and narrow 248 km/s; weak."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "no_cwt_peak"
          ],
          "comment": "Emission fit center_at_bound at 6234.3, unselectable; no CWT peak near 6184."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "cwt:abs:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad"
          ],
          "comment": "Trough at 6188.8 (z=0.2727), offset ~4.5 Å; broad 3407 km/s, plausible Hβ absorption but weak."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "cwt:em:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend"
          ],
          "comment": "CWT peak at 6292.0 (z=0.2685), offset ~16 Å; doublet fit separation fails and ratio 0.28, so identity uncertain."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "rejected_fit",
            "no_cwt_peak"
          ],
          "comment": "Doublet fit centre 6419.3 (z=0.2818, at window edge) with separation fail; no CWT peak near 6369.3."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "cwt:abs:0007",
          "status": "LIKELY",
          "reason_codes": [
            "offset_strong",
            "ridge_persistent"
          ],
          "comment": "Trough at 6583.2 (z=0.2717), offset 0.4 Å, ridge 10, SNR 11.8; strong Mg I absorption match."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "cwt:abs:0009",
          "status": "LIKELY",
          "reason_codes": [
            "offset_strong",
            "blend_na_d"
          ],
          "comment": "Trough at 7496.8 (z=0.2725), offset ~4 Å; blended Na D doublet, component plausible."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "blend_na_d",
            "no_separate_measurement"
          ],
          "comment": "Blended Na D label; the single trough at 7496.8 is adopted for Na D1/D2, no separate measurement for this label."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "cwt:abs:0009",
          "status": "LIKELY",
          "reason_codes": [
            "offset_strong",
            "blend_na_d"
          ],
          "comment": "Same trough at 7496.8 (z=0.2712) shared with Na D1; blended doublet, component plausible."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H5:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend_with_halpha"
          ],
          "comment": "Fit centre 8304.4 (z=0.2681), offset ~25 Å; separation fails, ratio 0.72; blended with Hα region."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "no_cwt_peak"
          ],
          "comment": "Emission fit center_at_bound at 8398.7, unselectable; no CWT peak near 8348.7."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "cwt:abs:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_amp",
            "blend_with_nii"
          ],
          "comment": "Trough at 8348.8 (z=0.2718), offset 0.1 Å; weak amplitude, blended with N II region."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "cwt:em:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "doublet_separation_fail",
            "blend"
          ],
          "comment": "Peak at 8430.4 (z=0.2802, near window edge), offset ~55 Å; doublet fit separation fails; weak identity."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H5:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak"
          ],
          "comment": "Fit centre 8495.6 (z=0.2701), offset ~49 Å; separation fails, second component zero amplitude; weak."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_separation_fail",
            "zero_amplitude",
            "rejected_fit"
          ],
          "comment": "Doublet fit second component at 8612.1 with zero amplitude and separation fail; no credible measurement."
        }
      ]
    },
    "id": "call_00_Qm6d1c5EpbmDghn0yPCH6004",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 9123,
  "output_tokens": 2441,
  "total_tokens": 11564,
  "cache_hit_tokens": 8960,
  "cache_miss_tokens": 163,
  "provider_usage": {
    "completion_tokens": 2441,
    "prompt_tokens": 9123,
    "total_tokens": 11564,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 8960
    },
    "prompt_cache_hit_tokens": 8960,
    "prompt_cache_miss_tokens": 163
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_Qm6d1c5EpbmDghn0yPCH6004`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H5/pre_analysis/branches/main/b93e4e52c42a4719b89f2b10a58f5d3b/lines.csv", "n_lines": 25, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H5/pre_analysis/branches/main/b93e4e52c42a4719b89f2b10a58f5d3b/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:28:47.111252+00:00
