# SH pre-analysis session: line review

- Run ID: `graph-6f4e6510cc5d45df9da3b7be0c8597cc`
- Hypothesis: `H3`
- Started (UTC): 2026-10-19T11:28:18.234764+00:00
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
Review every predicted line at the fixed Redrock redshift `0.2725121403358714`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H3/pre_analysis/branches/main/9d5d427fadbd4f0b8ecd2ff292570588/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 38.1 |

Verify the redshift hypothesis z ≈ 0.2725121403358714.

Verification window: z ∈ [0.2625, 0.2825]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=60.9533, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=18.3242, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=45.1742, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=44.2834, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=7.63507, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/LRG_1.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H3/pre_analysis/branches/main/9d5d427fadbd4f0b8ecd2ff292570588/lines.csv

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


## Predicted Lines at z = 0.2725

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [Ne V] | 3426.0 | 4359.6 | em | narrow | — |
| [O II] | 3727.0 | 4742.7 | em | narrow | — |
| Ca K_abs | 3934.8 | 5007.1 | abs | absorption | — |
| Ca H_abs | 3969.6 | 5051.4 | abs | absorption | trough@5049.6±0.8(z=0.2721) |
| Hε | 3970.1 | 5052.0 | em | both | — |
| Hε_abs | 3970.1 | 5052.0 | abs | absorption | trough@5049.6±0.8(z=0.2719) |
| Hδ | 4102.9 | 5221.0 | em | both | — |
| Hδ_abs | 4102.9 | 5221.0 | abs | absorption | — |
| G-band_abs | 4305.6 | 5478.9 | abs | absorption | trough@5472.0±0.8(z=0.2709) |
| Hγ | 4341.7 | 5524.9 | em | both | peak@5532.8±0.8(z=0.2743) |
| Hγ_abs | 4341.7 | 5524.9 | abs | absorption | — |
| Hβ | 4862.7 | 6187.8 | em | both | — |
| Hβ_abs | 4862.7 | 6187.8 | abs | absorption | trough@6188.8±0.8(z=0.2727) |
| [O III]a | 4960.3 | 6312.0 | em | narrow | peak@6292.0±0.8(z=0.2685) |
| [O III]b | 5008.2 | 6373.0 | em | narrow | — |
| Mg I_abs | 5176.7 | 6587.4 | abs | absorption | trough@6583.2±0.8(z=0.2717) |
| Na D1_abs | 5891.6 | 7497.1 | abs | absorption | trough@7496.8±0.8(z=0.2725) |
| Na D_abs | 5895.6 | 7502.2 | abs | absorption | trough@7496.8±0.8(z=0.2716) |
| Na D2_abs | 5897.6 | 7504.8 | abs | absorption | trough@7496.8±0.8(z=0.2712) |
| [N II]a | 6549.8 | 8334.7 | em | narrow | — |
| Hα | 6564.6 | 8353.5 | em | both | — |
| Hα_abs | 6564.6 | 8353.5 | abs | absorption | trough@8348.8±0.8(z=0.2718) |
| [N II]b | 6585.3 | 8379.9 | em | narrow | peak@8430.4±0.8(z=0.2802) |
| [S II]a | 6718.3 | 8549.1 | em | narrow | — |
| [S II]b | 6732.7 | 8567.4 | em | narrow | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 6312.0/6373.0 | fit_doublet | 6291.986±2.4907/6422.995±6.9234 | 0.655248/0.211672 | 2503.7/1982.0 | 2.26 | 0.366 | warning; separation fail; component ratio 0.32 |
| [S II]a/[S II]b | 8549.1/8567.4 | fit_doublet | 8500.695±0.0/8617.442±0.0 | 0.0/0.0 | 83.0/81.9 | 0.0 | 0.0 | warning; separation fail; component ratio — |
| [N II]a/[N II]b | 8334.7/8379.9 | fit_doublet | 8304.45±2.1971/8417.385±4.243 | 0.389639/0.281082 | 1167.7/2221.9 | 1.98 | 0.319 | warning; separation fail; component ratio 0.72 |
| Ca K_abs/Ca H_abs | 5007.1/5051.4 | fit_doublet | 5004.88±0.7148/5047.321±0.6398 | -1.932178/-1.963674 | 1192.1/978.1 | 3.77 | 0.638 | ok; separation pass |
| [Ne V] | 4359.6 | fit_peak | 4360.601±1.3274 | 0.577229 | 975.9 | 1.75 | 0.082 | ok |
| [O II] | 4742.7 | fit_peak | 4692.653±14.3374 | 0.950203 | 15798.4 | 2.66 | 3.209 | warning: center_at_bound |
| Hε | 5052.0 | fit_peak | 5102.0±2.0473 | 1.113807 | 2960.3 | 2.88 | 0.788 | warning: center_at_bound |
| Hδ | 5221.0 | fit_peak | 5170.99±5.4475 | 1.123352 | 9704.6 | 2.97 | 2.777 | warning: center_at_bound |
| Hβ | 6187.8 | fit_peak | 6236.319±2.0642 | 0.426339 | 773.4 | 1.33 | 0.054 | ok |
| Hα | 8353.5 | fit_peak | 8403.287±201.339 | 0.338298 | 15520.4 | 1.61 | 1.789 | ok |
| Hδ_abs | 5221.0 | fit_peak | 5218.02±4.6565 | -0.1928 | 368.5 | 0.43 | 0.002 | ok |
| Hγ_abs | 5524.9 | fit_peak | 5522.312±1.1618 | -0.501332 | 247.8 | 1.36 | 0.016 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:nev-3426 | [Ne V] | 4359.6 | emission |
| line:oii-3727 | [O II] | 4742.7 | emission |
| line:cak-3934-abs | Ca K_abs | 5007.1 | absorption |
| line:cah-3969-abs | Ca H_abs | 5051.4 | absorption |
| line:heps-3970 | Hε | 5052.0 | emission |
| line:heps-3970-abs | Hε_abs | 5052.0 | absorption |
| line:hdel-4102 | Hδ | 5221.0 | emission |
| line:hdel-4102-abs | Hδ_abs | 5221.0 | absorption |
| line:gband-4305-abs | G-band_abs | 5478.9 | absorption |
| line:hgam-4341 | Hγ | 5524.9 | emission |
| line:hgam-4341-abs | Hγ_abs | 5524.9 | absorption |
| line:hbet-4862 | Hβ | 6187.8 | emission |
| line:hbet-4862-abs | Hβ_abs | 6187.8 | absorption |
| line:oiii-4960 | [O III]a | 6312.0 | emission |
| line:oiii-5008 | [O III]b | 6373.0 | emission |
| line:mgi-5176-abs | Mg I_abs | 6587.4 | absorption |
| line:nad1-5891-abs | Na D1_abs | 7497.1 | absorption |
| line:nad-5895-abs | Na D_abs | 7502.2 | absorption |
| line:nad2-5897-abs | Na D2_abs | 7504.8 | absorption |
| line:nii-6549 | [N II]a | 8334.7 | emission |
| line:half-6564 | Hα | 8353.5 | emission |
| line:half-6564-abs | Hα_abs | 8353.5 | absorption |
| line:nii-6585 | [N II]b | 8379.9 | emission |
| line:sii-6718 | [S II]a | 8549.1 | emission |
| line:sii-6732 | [S II]b | 8567.4 | emission |

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
| fit:H3:0000 | fit_doublet | emission | 6291.986 | [O III]a | yes | — |
| fit:H3:0001 | fit_doublet | emission | 6422.995 | [O III]b | yes | — |
| fit:H3:0002 | fit_doublet | emission | 8500.695 | [S II]a | yes | — |
| fit:H3:0003 | fit_doublet | emission | 8617.442 | [S II]b | yes | — |
| fit:H3:0004 | fit_doublet | emission | 8304.450 | [N II]a | yes | — |
| fit:H3:0005 | fit_doublet | emission | 8417.385 | [N II]b | yes | — |
| fit:H3:0006 | fit_doublet | absorption | 5004.880 | Ca K_abs | yes | — |
| fit:H3:0007 | fit_doublet | absorption | 5047.321 | Ca H_abs | yes | — |
| fit:H3:0008 | fit_peak | emission | 4360.601 | [Ne V] | yes | — |
| fit:H3:0009 | fit_peak | emission | 4692.653 | [O II] | no | center_at_bound |
| fit:H3:0010 | fit_peak | emission | 5102.000 | Hε | no | center_at_bound |
| fit:H3:0011 | fit_peak | emission | 5170.990 | Hδ | no | center_at_bound |
| fit:H3:0012 | fit_peak | emission | 6236.319 | Hβ | yes | — |
| fit:H3:0013 | fit_peak | emission | 8403.287 | Hα | yes | — |
| fit:H3:0014 | fit_peak | absorption | 5218.020 | Hδ_abs | yes | — |
| fit:H3:0015 | fit_peak | absorption | 5522.312 | Hγ_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H3/pre_analysis/branches/main/9d5d427fadbd4f0b8ecd2ff292570588/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": "fit:H3:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "no_cwt_peak"
          ],
          "comment": "Fit centre 4360.6 A matches prediction (offset ~1 A, z in window) but local SNR 1.75 and FWHM ~976 km/s; no CWT peak at this position. Weak, broad, low-significance candidate."
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
          "comment": "Only fit is center_at_bound (4692.7 A, 50 A blueward, FWHM 15800 km/s) and unselectable; no CWT peak near 4742.7 A. No credible measurement adopted."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H3:0006",
          "status": "LIKELY",
          "reason_codes": [
            "doublet_separation_pass",
            "depth_ordering_uncertain"
          ],
          "comment": "Doublet fit centre 5004.9 A vs 5007.1 predicted (offset ~2 A, z in window), separation passes. Depth ordering (K vs H) nearly equal and uncertain, but plausible Ca K component retained."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H3:0007",
          "status": "LIKELY",
          "reason_codes": [
            "doublet_separation_pass",
            "depth_ordering_uncertain",
            "cwt_trough_support"
          ],
          "comment": "Fit centre 5047.3 A vs 5051.4 predicted (offset ~4 A, z in window); CWT trough at 5049.6 A supports. Depth ordering vs Ca K uncertain but plausible weak component retained."
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
          "comment": "Only fit is center_at_bound (5102.0 A) and unselectable; region blends with Ca H absorption. No credible emission measurement adopted."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "cwt:abs:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "blend_with_cah",
            "weak_depth"
          ],
          "comment": "CWT trough at 5049.6 A (z=0.2719, in window) is the same feature as Ca H; ambiguous blend between H-epsilon absorption and Ca H. Weak, marginal adoption."
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
          "comment": "Only fit is center_at_bound (5171.0 A, FWHM 9700 km/s) and unselectable; no CWT peak near 5221 A. No credible measurement adopted."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H3:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_amplitude",
            "low_snr"
          ],
          "comment": "Fit centre 5218.0 A vs 5221.0 predicted (offset ~3 A, z in window) but amplitude -0.19 and local SNR 0.43; very weak trough. Marginal."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "cwt:abs:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width"
          ],
          "comment": "CWT trough at 5472.0 A (z=0.2709, in window) vs 5478.9 predicted, offset ~7 A; broad FWHM ~2900 km/s. Plausible but weak G-band candidate."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "cwt:em:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_amplitude",
            "broad_width"
          ],
          "comment": "CWT peak at 5532.8 A (z=0.2743, in window) vs 5524.9 predicted, offset ~8 A; amplitude ~0.0 and broad FWHM ~4200 km/s. Weak marginal emission candidate."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H3:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_amplitude",
            "low_snr"
          ],
          "comment": "Fit centre 5522.3 A vs 5524.9 predicted (offset ~3 A, z in window) but amplitude -0.50 and local SNR 1.36; weak trough. Marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "fit:H3:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "no_cwt_peak"
          ],
          "comment": "Fit centre 6236.3 A vs 6187.8 predicted (offset ~48 A, weaker range), local SNR 1.33, no CWT peak. Weak marginal emission candidate."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "cwt:abs:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "blend_with_hbeta",
            "broad_width"
          ],
          "comment": "CWT trough at 6188.8 A (z=0.2727, in window) matches prediction closely; broad FWHM ~3400 km/s and coincides with H-beta emission region. Marginal absorption candidate."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "fit:H3:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "ratio_mismatch",
            "blend"
          ],
          "comment": "Fit centre 6292.0 A vs 6312.0 predicted (offset ~20 A, weaker range); CWT peak at 6292.0 A. Doublet separation fails and component ratio 0.32 far from 3:1; blended/ambiguous. Marginal."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "fit:H3:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend"
          ],
          "comment": "Fit centre 6423.0 A vs 6373.0 predicted (offset ~50 A, weaker range); doublet separation fails and ratio inconsistent. Ambiguous blend with [O III]a. Marginal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "cwt:abs:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width"
          ],
          "comment": "CWT trough at 6583.2 A (z=0.2717, in window) vs 6587.4 predicted, offset ~4 A; broad FWHM ~2900 km/s. Plausible weak Mg I candidate."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "cwt:abs:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_blend",
            "shared_feature"
          ],
          "comment": "CWT trough at 7496.8 A (z=0.2725, in window) matches Na D1 prediction; shared with Na D/D2 components (unresolved blend). Marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": "cwt:abs:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_blend",
            "shared_feature"
          ],
          "comment": "Same CWT trough at 7496.8 A (z=0.2716) serves Na D; unresolved blend with D1/D2. Marginal."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "cwt:abs:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_blend",
            "shared_feature"
          ],
          "comment": "Same CWT trough at 7496.8 A (z=0.2712) serves Na D2; unresolved blend with D1/D. Marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H3:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend"
          ],
          "comment": "Fit centre 8304.5 A vs 8334.7 predicted (offset ~30 A, weaker range); doublet separation fails, ratio 0.72 inconsistent with 1:3. Blended with H-alpha/[N II]b. Marginal."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H3:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "huge_uncertainty",
            "broad_width",
            "blend"
          ],
          "comment": "Fit centre 8403.3 A vs 8353.5 predicted (offset ~50 A) with error ±201 A and FWHM 15500 km/s; blended with [N II]. Weak, highly uncertain. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "cwt:abs:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "blend_with_halpha",
            "weak_amplitude"
          ],
          "comment": "CWT trough at 8348.8 A (z=0.2718, in window) vs 8353.5 predicted, offset ~5 A; weak amplitude and coincides with H-alpha emission region. Marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H3:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend"
          ],
          "comment": "Fit centre 8417.4 A vs 8379.9 predicted (offset ~37 A, weaker range); CWT peak at 8430.4 A (z=0.2802, near window edge). Doublet separation fails; blended. Marginal."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "separation_fail",
            "no_cwt_peak"
          ],
          "comment": "Doublet fit returned zero amplitude with separation fail and no CWT peak near 8549 A. No credible measurement adopted."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "separation_fail",
            "no_cwt_peak"
          ],
          "comment": "Doublet fit returned zero amplitude with separation fail and no CWT peak near 8567 A. No credible measurement adopted."
        }
      ]
    },
    "id": "call_00_fUgSboCDcRj6bqKcCBJA5794",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 6608,
  "output_tokens": 2723,
  "total_tokens": 9331,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 5968,
  "provider_usage": {
    "completion_tokens": 2723,
    "prompt_tokens": 6608,
    "total_tokens": 9331,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 5968
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_fUgSboCDcRj6bqKcCBJA5794`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"name": "Na D_abs", "reason": "blended label duplicates an adopted doublet component"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
The tool rejects adopting the same CWT feature for the Na D middle component. I'll set Na D_abs to NOT_FOUND (the shared trough is adopted for D1 and D2) and resubmit.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H3/pre_analysis/branches/main/9d5d427fadbd4f0b8ecd2ff292570588/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": "fit:H3:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "no_cwt_peak"
          ],
          "comment": "Fit centre 4360.6 A matches prediction (offset ~1 A, z in window) but local SNR 1.75 and FWHM ~976 km/s; no CWT peak at this position. Weak, broad, low-significance candidate."
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
          "comment": "Only fit is center_at_bound (4692.7 A, 50 A blueward, FWHM 15800 km/s) and unselectable; no CWT peak near 4742.7 A. No credible measurement adopted."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H3:0006",
          "status": "LIKELY",
          "reason_codes": [
            "doublet_separation_pass",
            "depth_ordering_uncertain"
          ],
          "comment": "Doublet fit centre 5004.9 A vs 5007.1 predicted (offset ~2 A, z in window), separation passes. Depth ordering (K vs H) nearly equal and uncertain, but plausible Ca K component retained."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H3:0007",
          "status": "LIKELY",
          "reason_codes": [
            "doublet_separation_pass",
            "depth_ordering_uncertain",
            "cwt_trough_support"
          ],
          "comment": "Fit centre 5047.3 A vs 5051.4 predicted (offset ~4 A, z in window); CWT trough at 5049.6 A supports. Depth ordering vs Ca K uncertain but plausible weak component retained."
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
          "comment": "Only fit is center_at_bound (5102.0 A) and unselectable; region blends with Ca H absorption. No credible emission measurement adopted."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "cwt:abs:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "blend_with_cah",
            "weak_depth"
          ],
          "comment": "CWT trough at 5049.6 A (z=0.2719, in window) is the same feature as Ca H; ambiguous blend between H-epsilon absorption and Ca H. Weak, marginal adoption."
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
          "comment": "Only fit is center_at_bound (5171.0 A, FWHM 9700 km/s) and unselectable; no CWT peak near 5221 A. No credible measurement adopted."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H3:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_amplitude",
            "low_snr"
          ],
          "comment": "Fit centre 5218.0 A vs 5221.0 predicted (offset ~3 A, z in window) but amplitude -0.19 and local SNR 0.43; very weak trough. Marginal."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "cwt:abs:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width"
          ],
          "comment": "CWT trough at 5472.0 A (z=0.2709, in window) vs 5478.9 predicted, offset ~7 A; broad FWHM ~2900 km/s. Plausible but weak G-band candidate."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "cwt:em:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_amplitude",
            "broad_width"
          ],
          "comment": "CWT peak at 5532.8 A (z=0.2743, in window) vs 5524.9 predicted, offset ~8 A; amplitude ~0.0 and broad FWHM ~4200 km/s. Weak marginal emission candidate."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H3:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_amplitude",
            "low_snr"
          ],
          "comment": "Fit centre 5522.3 A vs 5524.9 predicted (offset ~3 A, z in window) but amplitude -0.50 and local SNR 1.36; weak trough. Marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "fit:H3:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_snr",
            "no_cwt_peak"
          ],
          "comment": "Fit centre 6236.3 A vs 6187.8 predicted (offset ~48 A, weaker range), local SNR 1.33, no CWT peak. Weak marginal emission candidate."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "cwt:abs:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "blend_with_hbeta",
            "broad_width"
          ],
          "comment": "CWT trough at 6188.8 A (z=0.2727, in window) matches prediction closely; broad FWHM ~3400 km/s and coincides with H-beta emission region. Marginal absorption candidate."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "fit:H3:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "ratio_mismatch",
            "blend"
          ],
          "comment": "Fit centre 6292.0 A vs 6312.0 predicted (offset ~20 A, weaker range); CWT peak at 6292.0 A. Doublet separation fails and component ratio 0.32 far from 3:1; blended/ambiguous. Marginal."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "fit:H3:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend"
          ],
          "comment": "Fit centre 6423.0 A vs 6373.0 predicted (offset ~50 A, weaker range); doublet separation fails and ratio inconsistent. Ambiguous blend with [O III]a. Marginal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "cwt:abs:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width"
          ],
          "comment": "CWT trough at 6583.2 A (z=0.2717, in window) vs 6587.4 predicted, offset ~4 A; broad FWHM ~2900 km/s. Plausible weak Mg I candidate."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "cwt:abs:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_blend",
            "shared_feature"
          ],
          "comment": "CWT trough at 7496.8 A (z=0.2725, in window) matches Na D1 prediction; shared with Na D/D2 components (unresolved blend). Marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "blend_with_nad1_nad2",
            "no_separate_measurement"
          ],
          "comment": "Na D middle component has no separate measurement; the single CWT trough at 7496.8 A is adopted for D1 and D2. No independent measurement adopted here."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "cwt:abs:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_blend",
            "shared_feature"
          ],
          "comment": "Same CWT trough at 7496.8 A (z=0.2712) serves Na D2; unresolved blend with D1/D. Marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H3:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend"
          ],
          "comment": "Fit centre 8304.5 A vs 8334.7 predicted (offset ~30 A, weaker range); doublet separation fails, ratio 0.72 inconsistent with 1:3. Blended with H-alpha/[N II]b. Marginal."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H3:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "huge_uncertainty",
            "broad_width",
            "blend"
          ],
          "comment": "Fit centre 8403.3 A vs 8353.5 predicted (offset ~50 A) with error ±201 A and FWHM 15500 km/s; blended with [N II]. Weak, highly uncertain. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "cwt:abs:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "blend_with_halpha",
            "weak_amplitude"
          ],
          "comment": "CWT trough at 8348.8 A (z=0.2718, in window) vs 8353.5 predicted, offset ~5 A; weak amplitude and coincides with H-alpha emission region. Marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H3:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_weak",
            "blend"
          ],
          "comment": "Fit centre 8417.4 A vs 8379.9 predicted (offset ~37 A, weaker range); CWT peak at 8430.4 A (z=0.2802, near window edge). Doublet separation fails; blended. Marginal."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "separation_fail",
            "no_cwt_peak"
          ],
          "comment": "Doublet fit returned zero amplitude with separation fail and no CWT peak near 8549 A. No credible measurement adopted."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "separation_fail",
            "no_cwt_peak"
          ],
          "comment": "Doublet fit returned zero amplitude with separation fail and no CWT peak near 8567 A. No credible measurement adopted."
        }
      ]
    },
    "id": "call_00_84XsAwZ4dV8nzoHR859t6945",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 9413,
  "output_tokens": 2753,
  "total_tokens": 12166,
  "cache_hit_tokens": 9216,
  "cache_miss_tokens": 197,
  "provider_usage": {
    "completion_tokens": 2753,
    "prompt_tokens": 9413,
    "total_tokens": 12166,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 9216
    },
    "prompt_cache_hit_tokens": 9216,
    "prompt_cache_miss_tokens": 197
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_84XsAwZ4dV8nzoHR859t6945`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H3/pre_analysis/branches/main/9d5d427fadbd4f0b8ecd2ff292570588/lines.csv", "n_lines": 25, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/LRG_1/SH/H3/pre_analysis/branches/main/9d5d427fadbd4f0b8ecd2ff292570588/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:28:38.115807+00:00
