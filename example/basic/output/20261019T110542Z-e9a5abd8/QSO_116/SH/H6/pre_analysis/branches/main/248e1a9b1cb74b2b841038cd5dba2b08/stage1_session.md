# SH pre-analysis session: line review

- Run ID: `graph-325ff74c7f444efdb17e3f3b69698eea`
- Hypothesis: `H6`
- Started (UTC): 2026-10-19T11:44:56.324982+00:00
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
Review every predicted line at the fixed Redrock redshift `0.7079175775287458`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H6/pre_analysis/branches/main/248e1a9b1cb74b2b841038cd5dba2b08/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 4.7 |

Verify the redshift hypothesis z ≈ 0.7079175775287458.

Verification window: z ∈ [0.6979, 0.7179]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=81.8093, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=59.4355, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H

FITS file: /mnt/linux_share/code/FORMA/example/basic/QSO_116.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H6/pre_analysis/branches/main/248e1a9b1cb74b2b841038cd5dba2b08/lines.csv

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


## Predicted Lines at z = 0.7079

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| Mg II | 2800.0 | 4782.2 | em | broad | peak@4768.0±0.8(z=0.7029) |
| Mg II_abs | 2800.0 | 4782.2 | abs | absorption | — |
| [Ne V] | 3426.0 | 5851.3 | em | narrow | — |
| [O II] | 3727.0 | 6365.4 | em | narrow | — |
| Ca K_abs | 3934.8 | 6720.3 | abs | absorption | — |
| Ca H_abs | 3969.6 | 6779.7 | abs | absorption | — |
| Hε | 3970.1 | 6780.6 | em | both | — |
| Hε_abs | 3970.1 | 6780.6 | abs | absorption | — |
| Hδ | 4102.9 | 7007.4 | em | both | — |
| Hδ_abs | 4102.9 | 7007.4 | abs | absorption | — |
| G-band_abs | 4305.6 | 7353.6 | abs | absorption | — |
| Hγ | 4341.7 | 7415.3 | em | both | — |
| Hγ_abs | 4341.7 | 7415.3 | abs | absorption | — |
| Hβ | 4862.7 | 8305.1 | em | both | — |
| Hβ_abs | 4862.7 | 8305.1 | abs | absorption | — |
| [O III]a | 4960.3 | 8471.8 | em | narrow | — |
| [O III]b | 5008.2 | 8553.6 | em | narrow | — |
| Mg I_abs | 5176.7 | 8841.4 | abs | absorption | trough@8831.2±0.8(z=0.7060) |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 8471.8/8553.6 | fit_doublet | 8487.952±0.0/8516.551±24.4457 | 0.0/0.033034 | 7035.3/1677.8 | 0.39 | 0.009 | warning; separation fail; component ratio — |
| Ca K_abs/Ca H_abs | 6720.3/6779.7 | fit_doublet | 6670.314±9.4977/6784.746±27.3895 | -0.136758/-0.021858 | 6665.1/2403.0 | 1.42 | 0.394 | warning: center_1_deviation_large; separation fail |
| [Ne V] | 5851.3 | fit_peak | 5814.988±8.9107 | 0.115992 | 1680.3 | 0.5 | 0.016 | ok |
| [O II] | 6365.4 | fit_peak | 6374.981±0.0 | 0.0 | 136.9 | 0.0 | 0.0 | ok |
| Hε | 6780.6 | fit_peak | 6798.722±13.5106 | 0.027131 | 1201.4 | 0.27 | 0.004 | ok |
| Hδ | 7007.4 | fit_peak | 7026.638±3.8105 | 0.047665 | 309.0 | 0.54 | 0.004 | ok |
| Hγ | 7415.3 | fit_peak | 7465.266±4.0796 | 0.215022 | 3336.5 | 2.14 | 0.926 | warning: center_at_bound |
| Hβ | 8305.1 | fit_peak | 8323.558±1.481 | 0.125144 | 84.8 | 1.53 | 0.01 | ok |
| Mg II_abs | 4782.2 | fit_peak | 4832.169±0.0 | -0.0 | 146.1 | 0.0 | -0.0 | warning: center_at_bound |
| Hε_abs | 6780.6 | fit_peak | 6730.605±0.0 | -0.0 | 20973.8 | 0.0 | -0.0 | warning: center_at_bound |
| Hδ_abs | 7007.4 | fit_peak | 7010.401±32.2757 | -0.041409 | 7889.4 | 0.46 | 0.072 | ok |
| G-band_abs | 7353.6 | fit_peak | 7358.995±7.2456 | -0.10431 | 3573.9 | 1.08 | 0.21 | ok |
| Hγ_abs | 7415.3 | fit_peak | 7365.266±7.6594 | -0.102799 | 3339.1 | 1.0 | 0.204 | warning: center_at_bound |
| Hβ_abs | 8305.1 | fit_peak | 8295.764±9.4743 | -0.060477 | 813.9 | 0.74 | 0.023 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:mgii-2800 | Mg II | 4782.2 | emission |
| line:mgii-2800-abs | Mg II_abs | 4782.2 | absorption |
| line:nev-3426 | [Ne V] | 5851.3 | emission |
| line:oii-3727 | [O II] | 6365.4 | emission |
| line:cak-3934-abs | Ca K_abs | 6720.3 | absorption |
| line:cah-3969-abs | Ca H_abs | 6779.7 | absorption |
| line:heps-3970 | Hε | 6780.6 | emission |
| line:heps-3970-abs | Hε_abs | 6780.6 | absorption |
| line:hdel-4102 | Hδ | 7007.4 | emission |
| line:hdel-4102-abs | Hδ_abs | 7007.4 | absorption |
| line:gband-4305-abs | G-band_abs | 7353.6 | absorption |
| line:hgam-4341 | Hγ | 7415.3 | emission |
| line:hgam-4341-abs | Hγ_abs | 7415.3 | absorption |
| line:hbet-4862 | Hβ | 8305.1 | emission |
| line:hbet-4862-abs | Hβ_abs | 8305.1 | absorption |
| line:oiii-4960 | [O III]a | 8471.8 | emission |
| line:oiii-5008 | [O III]b | 8553.6 | emission |
| line:mgi-5176-abs | Mg I_abs | 8841.4 | absorption |

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
| fit:H6:0000 | fit_doublet | emission | 8487.952 | [O III]a | yes | — |
| fit:H6:0001 | fit_doublet | emission | 8516.551 | [O III]b | yes | — |
| fit:H6:0002 | fit_doublet | absorption | 6670.314 | Ca K_abs | yes | — |
| fit:H6:0003 | fit_doublet | absorption | 6784.746 | Ca H_abs | yes | — |
| fit:H6:0004 | fit_peak | emission | 5814.988 | [Ne V] | yes | — |
| fit:H6:0005 | fit_peak | emission | 6374.981 | [O II] | yes | — |
| fit:H6:0006 | fit_peak | emission | 6798.722 | Hε | yes | — |
| fit:H6:0007 | fit_peak | emission | 7026.638 | Hδ | yes | — |
| fit:H6:0008 | fit_peak | emission | 7465.266 | Hγ | no | center_at_bound |
| fit:H6:0009 | fit_peak | emission | 8323.558 | Hβ | yes | — |
| fit:H6:0010 | fit_peak | absorption | 4832.169 | Mg II_abs | no | center_at_bound |
| fit:H6:0011 | fit_peak | absorption | 6730.605 | Hε_abs | no | center_at_bound |
| fit:H6:0012 | fit_peak | absorption | 7010.401 | Hδ_abs | yes | — |
| fit:H6:0013 | fit_peak | absorption | 7358.995 | G-band_abs | yes | — |
| fit:H6:0014 | fit_peak | absorption | 7365.266 | Hγ_abs | no | center_at_bound |
| fit:H6:0015 | fit_peak | absorption | 8295.764 | Hβ_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H6/pre_analysis/branches/main/248e1a9b1cb74b2b841038cd5dba2b08/lines.csv",
      "lines": [
        {
          "line_id": "line:mgii-2800",
          "measurement_id": "cwt:em:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width",
            "low_snr"
          ],
          "comment": "CWT peak 4768.0 implies z=0.7029, offset ~14 A within weak window; broad FWHM 2497 km/s, SNR 13 but amplitude low; plausible Mg II but blended/uncertain."
        },
        {
          "line_id": "line:mgii-2800-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_credible_trough"
          ],
          "comment": "Only fit attempt center-at-bound with zero amplitude; no credible absorption trough near 4782 A."
        },
        {
          "line_id": "line:nev-3426",
          "measurement_id": "fit:H6:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "broad_width"
          ],
          "comment": "Fit centre 5815.0 vs 5851.3, offset ~36 A weak; local SNR 0.5, amplitude 0.12, FWHM 1680 km/s; weak candidate only."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_feature"
          ],
          "comment": "Fit returned zero amplitude at 6375 A; no CWT feature near 6365 A; no credible detection."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H6:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "center_deviation_large",
            "separation_fail",
            "weak_depth"
          ],
          "comment": "Doublet fit centre 6670.3 deviates ~50 A from 6720.3; separation fails; depth ordering K>H preserved but weak; plausible weak Ca K component retained as marginal."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H6:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "weak_depth",
            "blend_with_heps"
          ],
          "comment": "Fit centre 6784.7 near 6779.7; very shallow amplitude, separation fail; blended with Hε region; plausible weak Ca H retained as marginal."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H6:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "blend_with_cah"
          ],
          "comment": "Fit centre 6798.7 vs 6780.6, offset ~18 A; local SNR 0.27, amplitude 0.03; blended with Ca H absorption; weak marginal."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "zero_amplitude"
          ],
          "comment": "Fit center-at-bound with zero amplitude and absurd width; no credible absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H6:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit centre 7026.6 vs 7007.4, offset ~19 A; local SNR 0.54, amplitude 0.05; weak marginal emission."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H6:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_depth",
            "broad_width"
          ],
          "comment": "Fit centre 7010.4 near 7007.4; shallow amplitude -0.04, very broad FWHM; weak marginal absorption."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H6:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_depth",
            "broad_width",
            "offset_weak"
          ],
          "comment": "Fit centre 7359.0 vs 7353.6, offset ~5 A; shallow amplitude -0.10, broad FWHM 3574 km/s; weak marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_credible_peak"
          ],
          "comment": "Only fit center-at-bound; CWT peak 7474.4 implies z=0.7216 outside window; no credible Hγ emission."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound"
          ],
          "comment": "Fit center-at-bound; no credible absorption at 7415 A."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "fit:H6:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "narrow_width"
          ],
          "comment": "Fit centre 8323.6 vs 8305.1, offset ~18 A; local SNR 1.53, amplitude 0.13, FWHM 85 km/s narrow; weak marginal."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "fit:H6:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_depth",
            "offset_weak"
          ],
          "comment": "Fit centre 8295.8 vs 8305.1, offset ~9 A; shallow amplitude -0.06; weak marginal absorption."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit component 1 zero amplitude, separation fail; no CWT feature near 8472 A; no credible detection."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "weak_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit component 2 weak amplitude 0.03 with separation fail; no CWT feature near 8554 A; no credible detection."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "cwt:abs:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "narrow_width",
            "possible_blend"
          ],
          "comment": "CWT trough 8831.2 implies z=0.7060, offset ~10 A; narrow FWHM 125 km/s, SNR 27; plausible Mg I absorption but near adjacent features."
        }
      ]
    },
    "id": "call_00_pwO3hmba4Ha3nUCVU33V3721",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 6057,
  "output_tokens": 1748,
  "total_tokens": 7805,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 5417,
  "provider_usage": {
    "completion_tokens": 1748,
    "prompt_tokens": 6057,
    "total_tokens": 7805,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 5417
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_pwO3hmba4Ha3nUCVU33V3721`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 2, "line_id": "line:nev-3426", "measurement_id": "fit:H6:0004", "reason": "measurement is outside this line's redshift window"}, {"row": 4, "line_id": "line:cak-3934-abs", "measurement_id": "fit:H6:0002", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
Two measurements fall outside the redshift window. I'll repair those rows.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H6/pre_analysis/branches/main/248e1a9b1cb74b2b841038cd5dba2b08/lines.csv",
      "lines": [
        {
          "line_id": "line:mgii-2800",
          "measurement_id": "cwt:em:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "broad_width",
            "low_snr"
          ],
          "comment": "CWT peak 4768.0 implies z=0.7029, offset ~14 A within weak window; broad FWHM 2497 km/s, SNR 13 but amplitude low; plausible Mg II but blended/uncertain."
        },
        {
          "line_id": "line:mgii-2800-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_credible_trough"
          ],
          "comment": "Only fit attempt center-at-bound with zero amplitude; no credible absorption trough near 4782 A."
        },
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_outside_window",
            "weak_snr",
            "no_cwt_feature"
          ],
          "comment": "Fit centre 5815.0 implies z=0.6972, outside the verification window; local SNR 0.5; no CWT feature near 5851 A; no credible detection."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_feature"
          ],
          "comment": "Fit returned zero amplitude at 6375 A; no CWT feature near 6365 A; no credible detection."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_outside_window",
            "center_deviation_large",
            "separation_fail"
          ],
          "comment": "Doublet fit centre 6670.3 implies z=0.6952, outside window; separation fails; no credible Ca K measurement adopted."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H6:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "separation_fail",
            "weak_depth",
            "blend_with_heps"
          ],
          "comment": "Fit centre 6784.7 near 6779.7; very shallow amplitude, separation fail; blended with Hε region; plausible weak Ca H retained as marginal."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H6:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak",
            "blend_with_cah"
          ],
          "comment": "Fit centre 6798.7 vs 6780.6, offset ~18 A; local SNR 0.27, amplitude 0.03; blended with Ca H absorption; weak marginal."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "zero_amplitude"
          ],
          "comment": "Fit center-at-bound with zero amplitude and absurd width; no credible absorption."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H6:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_weak"
          ],
          "comment": "Fit centre 7026.6 vs 7007.4, offset ~19 A; local SNR 0.54, amplitude 0.05; weak marginal emission."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H6:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_depth",
            "broad_width"
          ],
          "comment": "Fit centre 7010.4 near 7007.4; shallow amplitude -0.04, very broad FWHM; weak marginal absorption."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H6:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_depth",
            "broad_width",
            "offset_weak"
          ],
          "comment": "Fit centre 7359.0 vs 7353.6, offset ~5 A; shallow amplitude -0.10, broad FWHM 3574 km/s; weak marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_credible_peak"
          ],
          "comment": "Only fit center-at-bound; CWT peak 7474.4 implies z=0.7216 outside window; no credible Hγ emission."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound"
          ],
          "comment": "Fit center-at-bound; no credible absorption at 7415 A."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "fit:H6:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "narrow_width"
          ],
          "comment": "Fit centre 8323.6 vs 8305.1, offset ~18 A; local SNR 1.53, amplitude 0.13, FWHM 85 km/s narrow; weak marginal."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "fit:H6:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_depth",
            "offset_weak"
          ],
          "comment": "Fit centre 8295.8 vs 8305.1, offset ~9 A; shallow amplitude -0.06; weak marginal absorption."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "zero_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit component 1 zero amplitude, separation fail; no CWT feature near 8472 A; no credible detection."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "weak_amplitude",
            "no_cwt_feature"
          ],
          "comment": "Doublet fit component 2 weak amplitude 0.03 with separation fail; no CWT feature near 8554 A; no credible detection."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "cwt:abs:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "narrow_width",
            "possible_blend"
          ],
          "comment": "CWT trough 8831.2 implies z=0.7060, offset ~10 A; narrow FWHM 125 km/s, SNR 27; plausible Mg I absorption but near adjacent features."
        }
      ]
    },
    "id": "call_00_9MO05f8MMQ6j6wWh1YJN9165",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 7956,
  "output_tokens": 1719,
  "total_tokens": 9675,
  "cache_hit_tokens": 7680,
  "cache_miss_tokens": 276,
  "provider_usage": {
    "completion_tokens": 1719,
    "prompt_tokens": 7956,
    "total_tokens": 9675,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 7680
    },
    "prompt_cache_hit_tokens": 7680,
    "prompt_cache_miss_tokens": 276
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_9MO05f8MMQ6j6wWh1YJN9165`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H6/pre_analysis/branches/main/248e1a9b1cb74b2b841038cd5dba2b08/lines.csv", "n_lines": 18, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H6/pre_analysis/branches/main/248e1a9b1cb74b2b841038cd5dba2b08/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:45:09.040206+00:00
