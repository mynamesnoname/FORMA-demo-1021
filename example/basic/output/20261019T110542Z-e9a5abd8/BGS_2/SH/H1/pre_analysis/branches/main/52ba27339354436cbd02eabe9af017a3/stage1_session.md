# SH pre-analysis session: line review

- Run ID: `graph-df7434d5533647e999870708120307b0`
- Hypothesis: `H1`
- Started (UTC): 2026-10-19T11:06:07.320685+00:00
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
Review every predicted line at the fixed Redrock redshift `0.15896775446705771`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H1/pre_analysis/branches/main/52ba27339354436cbd02eabe9af017a3/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 26.9 |

Verify the redshift hypothesis z ≈ 0.15896775446705771.

Verification window: z ∈ [0.149, 0.169]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=55.5146, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=16.6891, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=41.1434, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=40.3321, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=6.95381, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/BGS_2.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H1/pre_analysis/branches/main/52ba27339354436cbd02eabe9af017a3/lines.csv

## CWT Detected Features

### Emission (peaks) — 3 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 4660.0 | 0.8 | 0.7 | 94.0 | 6049 | 6 | 11.5 |
| 6760.8 | 0.8 | 0.2 | 94.0 | 4169 | 6 | 12.8 |
| 7632.0 | 0.8 | 2.9 | 27.1 | 1066 | 19 | 31.6 |

### Absorption (troughs) — 5 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 6831.2 | 0.8 | -1.0 | 36.3 | 1592 | 12 | 15.1 |
| 7516.8 | 0.8 | -0.2 | 20.5 | 817 | 14 | 14.7 |
| 7648.0 | 0.8 | -0.1 | 20.5 | 803 | 12 | 15.5 |
| 7717.6 | 0.8 | -0.2 | 113.8 | 4419 | 4 | 13.7 |
| 9190.4 | 0.8 | -0.2 | 103.0 | 3358 | 5 | 12.2 |


## Predicted Lines at z = 0.1590

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [Ne V] | 3426.0 | 3970.6 | em | narrow | — |
| [O II] | 3727.0 | 4319.5 | em | narrow | — |
| Ca K_abs | 3934.8 | 4560.3 | abs | absorption | — |
| Ca H_abs | 3969.6 | 4600.6 | abs | absorption | — |
| Hε | 3970.1 | 4601.2 | em | both | — |
| Hε_abs | 3970.1 | 4601.2 | abs | absorption | — |
| Hδ | 4102.9 | 4755.1 | em | both | — |
| Hδ_abs | 4102.9 | 4755.1 | abs | absorption | — |
| G-band_abs | 4305.6 | 4990.1 | abs | absorption | — |
| Hγ | 4341.7 | 5031.9 | em | both | — |
| Hγ_abs | 4341.7 | 5031.9 | abs | absorption | — |
| Hβ | 4862.7 | 5635.7 | em | both | — |
| Hβ_abs | 4862.7 | 5635.7 | abs | absorption | — |
| [O III]a | 4960.3 | 5748.8 | em | narrow | — |
| [O III]b | 5008.2 | 5804.3 | em | narrow | — |
| Mg I_abs | 5176.7 | 5999.6 | abs | absorption | — |
| Na D1_abs | 5891.6 | 6828.2 | abs | absorption | trough@6831.2±0.8(z=0.1595) |
| Na D_abs | 5895.6 | 6832.8 | abs | absorption | trough@6831.2±0.8(z=0.1587) |
| Na D2_abs | 5897.6 | 6835.1 | abs | absorption | trough@6831.2±0.8(z=0.1583) |
| [N II]a | 6549.8 | 7591.0 | em | narrow | peak@7632.0±0.8(z=0.1652) |
| Hα | 6564.6 | 7608.2 | em | both | peak@7632.0±0.8(z=0.1626) |
| Hα_abs | 6564.6 | 7608.2 | abs | absorption | trough@7648.0±0.8(z=0.1650) |
| [N II]b | 6585.3 | 7632.2 | em | narrow | peak@7632.0±0.8(z=0.1589) |
| [S II]a | 6718.3 | 7786.3 | em | narrow | — |
| [S II]b | 6732.7 | 7803.0 | em | narrow | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 5748.8/5804.3 | fit_doublet | 5740.137±7.2841/5804.145±0.4237 | 0.137995/1.091457 | 810.7/169.9 | 2.85 | 0.039 | warning; separation fail; component ratio 7.91 |
| [S II]a/[S II]b | 7786.3/7803.0 | fit_doublet | 7786.159±0.8601/7803.824±1.0866 | 0.718526/0.596605 | 249.8/274.3 | 3.76 | 0.242 | ok; separation pass; component ratio 0.83 |
| Ca K_abs/Ca H_abs | 4560.3/4600.6 | fit_doublet | 4561.006±0.8004/4601.599±0.7006 | -1.654652/-1.754091 | 964.8/823.3 | 3.51 | 0.397 | ok; separation pass |
| [Ne V] | 3970.6 | fit_peak | 3958.779±9.163 | 0.300063 | 2642.3 | 0.42 | 0.012 | ok |
| [O II] | 4319.5 | fit_peak | 4319.898±0.3342 | 2.352743 | 320.3 | 4.25 | 0.157 | ok |
| Hε | 4601.2 | fit_peak | 4635.567±0.0 | 0.0 | 30308.0 | 0.0 | -0.0 | ok |
| Hδ | 4755.1 | fit_peak | 4705.129±12.4335 | 0.946502 | 13310.8 | 2.05 | 1.632 | warning: center_at_bound |
| Hγ | 5031.9 | fit_peak | 5081.889±0.0 | 0.0 | 138.9 | 0.0 | -0.0 | warning: center_at_bound |
| Hβ | 5635.7 | fit_peak | 5586.999±2.8876 | 0.225507 | 349.0 | 0.62 | 0.005 | ok |
| Hε_abs | 4601.2 | fit_peak | 4601.668±0.7291 | -1.691952 | 778.9 | 3.17 | 0.226 | ok |
| Hδ_abs | 4755.1 | fit_peak | 4755.292±0.8348 | -0.913404 | 293.8 | 1.91 | 0.032 | ok |
| G-band_abs | 4990.1 | fit_peak | 4989.489±0.8567 | -1.128171 | 1069.3 | 3.02 | 0.305 | ok |
| Hγ_abs | 5031.9 | fit_peak | 5033.451±1.2498 | -0.603054 | 522.7 | 1.51 | 0.038 | ok |
| Hβ_abs | 5635.7 | fit_peak | 5648.609±1.2205 | -0.714928 | 667.3 | 2.05 | 0.11 | ok |
| Mg I_abs | 5999.6 | fit_peak | 6001.203±3.1634 | -0.596081 | 2789.5 | 1.72 | 0.312 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:nev-3426 | [Ne V] | 3970.6 | emission |
| line:oii-3727 | [O II] | 4319.5 | emission |
| line:cak-3934-abs | Ca K_abs | 4560.3 | absorption |
| line:cah-3969-abs | Ca H_abs | 4600.6 | absorption |
| line:heps-3970 | Hε | 4601.2 | emission |
| line:heps-3970-abs | Hε_abs | 4601.2 | absorption |
| line:hdel-4102 | Hδ | 4755.1 | emission |
| line:hdel-4102-abs | Hδ_abs | 4755.1 | absorption |
| line:gband-4305-abs | G-band_abs | 4990.1 | absorption |
| line:hgam-4341 | Hγ | 5031.9 | emission |
| line:hgam-4341-abs | Hγ_abs | 5031.9 | absorption |
| line:hbet-4862 | Hβ | 5635.7 | emission |
| line:hbet-4862-abs | Hβ_abs | 5635.7 | absorption |
| line:oiii-4960 | [O III]a | 5748.8 | emission |
| line:oiii-5008 | [O III]b | 5804.3 | emission |
| line:mgi-5176-abs | Mg I_abs | 5999.6 | absorption |
| line:nad1-5891-abs | Na D1_abs | 6828.2 | absorption |
| line:nad-5895-abs | Na D_abs | 6832.8 | absorption |
| line:nad2-5897-abs | Na D2_abs | 6835.1 | absorption |
| line:nii-6549 | [N II]a | 7591.0 | emission |
| line:half-6564 | Hα | 7608.2 | emission |
| line:half-6564-abs | Hα_abs | 7608.2 | absorption |
| line:nii-6585 | [N II]b | 7632.2 | emission |
| line:sii-6718 | [S II]a | 7786.3 | emission |
| line:sii-6732 | [S II]b | 7803.0 | emission |

| Measurement ID | Source | Kind | Centre (Å) | Target | Selectable | Flags |
|---|---|---|---:|---|---|---|
| cwt:em:0000 | CWT | emission | 4660.000 | — | yes | — |
| cwt:em:0001 | CWT | emission | 6760.800 | — | yes | — |
| cwt:em:0002 | CWT | emission | 7632.000 | — | yes | — |
| cwt:abs:0000 | CWT | absorption | 6831.200 | — | yes | — |
| cwt:abs:0001 | CWT | absorption | 7516.800 | — | yes | — |
| cwt:abs:0002 | CWT | absorption | 7648.000 | — | yes | — |
| cwt:abs:0003 | CWT | absorption | 7717.600 | — | yes | — |
| cwt:abs:0004 | CWT | absorption | 9190.400 | — | yes | — |
| fit:H1:0000 | fit_doublet | emission | 5740.137 | [O III]a | yes | — |
| fit:H1:0001 | fit_doublet | emission | 5804.145 | [O III]b | yes | — |
| fit:H1:0002 | fit_doublet | emission | 7786.159 | [S II]a | yes | — |
| fit:H1:0003 | fit_doublet | emission | 7803.824 | [S II]b | yes | — |
| fit:H1:0004 | fit_doublet | absorption | 4561.006 | Ca K_abs | yes | — |
| fit:H1:0005 | fit_doublet | absorption | 4601.599 | Ca H_abs | yes | — |
| fit:H1:0006 | fit_peak | emission | 3958.779 | [Ne V] | yes | — |
| fit:H1:0007 | fit_peak | emission | 4319.898 | [O II] | yes | — |
| fit:H1:0008 | fit_peak | emission | 4635.567 | Hε | yes | — |
| fit:H1:0009 | fit_peak | emission | 4705.129 | Hδ | no | center_at_bound |
| fit:H1:0010 | fit_peak | emission | 5081.889 | Hγ | no | center_at_bound |
| fit:H1:0011 | fit_peak | emission | 5586.999 | Hβ | yes | — |
| fit:H1:0012 | fit_peak | absorption | 4601.668 | Hε_abs | yes | — |
| fit:H1:0013 | fit_peak | absorption | 4755.292 | Hδ_abs | yes | — |
| fit:H1:0014 | fit_peak | absorption | 4989.489 | G-band_abs | yes | — |
| fit:H1:0015 | fit_peak | absorption | 5033.451 | Hγ_abs | yes | — |
| fit:H1:0016 | fit_peak | absorption | 5648.609 | Hβ_abs | yes | — |
| fit:H1:0017 | fit_peak | absorption | 6001.203 | Mg I_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H1/pre_analysis/branches/main/52ba27339354436cbd02eabe9af017a3/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "weak_snr",
            "no_cwt_feature",
            "edge_blue"
          ],
          "comment": "Fit centre 3958.8 offset ~12 A from predicted 3970.6, local SNR 0.42, no CWT feature; blue edge. Not credible."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H1:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr",
            "no_cwt_feature",
            "edge_blue"
          ],
          "comment": "Fit centre 4319.9 matches prediction well (offset <1 A) but local SNR 4.25 and no CWT ridge; weak blue-edge detection."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H1:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "low_snr",
            "depth_ordering_uncertain"
          ],
          "comment": "Doublet fit centre 4561.0 near predicted 4560.3; Ca K depth (-1.65) slightly shallower than Ca H (-1.75), ordering uncertain; low local SNR 3.5. Plausible weak component."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H1:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "low_snr",
            "depth_ordering_uncertain"
          ],
          "comment": "Doublet fit centre 4601.6 near predicted 4600.6; blended with H-epsilon region; depth ordering vs Ca K uncertain; low SNR. Plausible weak component."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "degenerate_fit",
            "blend"
          ],
          "comment": "Fit returned zero amplitude with huge FWHM (degenerate); no CWT emission feature near 4601. No credible emission measurement."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H1:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "low_snr"
          ],
          "comment": "Absorption fit centre 4601.7 matches prediction; blended with Ca H; local SNR 3.2. Weak but plausible."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "no_cwt_feature"
          ],
          "comment": "Emission fit centre 4705.1 at bound, offset ~50 A from predicted 4755.1, FWHM 13310 km/s; unselectable. No CWT emission feature."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H1:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr"
          ],
          "comment": "Absorption fit centre 4755.3 matches predicted 4755.1 closely; local SNR 1.9, weak but positionally consistent."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H1:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr"
          ],
          "comment": "Absorption fit centre 4989.5 matches predicted 4990.1; local SNR 3.0, weak but positionally consistent."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "zero_amplitude",
            "rejected_fit"
          ],
          "comment": "Emission fit centre 5081.9 at bound with zero amplitude; unselectable. No CWT emission feature near 5032."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H1:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr"
          ],
          "comment": "Absorption fit centre 5033.5 near predicted 5031.9 (offset ~1.5 A); local SNR 1.5, weak but plausible."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "fit:H1:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr",
            "weak_amplitude"
          ],
          "comment": "Emission fit centre 5587.0 offset ~49 A from predicted 5635.7; local SNR 0.62, weak. Marginal at best."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "fit:H1:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr",
            "offset_weak"
          ],
          "comment": "Absorption fit centre 5648.6 offset ~13 A from predicted 5635.7; local SNR 2.05. Weak but plausible."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "low_snr",
            "rejected_fit"
          ],
          "comment": "Doublet fit failed separation; component a centre 5740.1 offset ~9 A, local SNR 2.85, ratio 7.9 inconsistent. No credible measurement."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "fit:H1:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "doublet_ratio_off",
            "low_snr"
          ],
          "comment": "Component b centre 5804.1 matches predicted 5804.3 well, but doublet separation failed and ratio 7.9 far from 3:1; local SNR 2.85. Marginal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H1:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr",
            "broad_width"
          ],
          "comment": "Absorption fit centre 6001.2 matches predicted 5999.6; local SNR 1.7, very broad FWHM ~2790 km/s. Weak but positionally consistent."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "cwt:abs:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "doublet_unresolved"
          ],
          "comment": "CWT trough at 6831.2 (z=0.1595) within Na D complex; Na D1/D2/D unresolved at this resolution, shared feature. Plausible but blended."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": "cwt:abs:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "doublet_unresolved"
          ],
          "comment": "Same CWT trough 6831.2 (z=0.1587) serves Na D blend; components unresolved. Plausible but ambiguous."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "cwt:abs:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "doublet_unresolved"
          ],
          "comment": "Same CWT trough 6831.2 (z=0.1583) serves Na D2; unresolved blend with D1/D. Plausible but ambiguous."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest CWT peak 7632.0 implies z=0.1652, offset ~41 A from predicted 7591.0; that peak is better matched to [N II]b. No credible [N II]a measurement."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest CWT peak 7632.0 implies z=0.1626, offset ~24 A from predicted 7608.2; peak assigned to [N II]b. No credible H-alpha measurement."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "cwt:abs:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "offset_weak"
          ],
          "comment": "CWT trough 7648.0 implies z=0.1650, offset ~40 A from predicted 7608.2; weak amplitude -0.1. Marginal, possibly blended."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "cwt:em:0002",
          "status": "LIKELY",
          "reason_codes": [
            "strong_snr",
            "ridge_persistent"
          ],
          "comment": "CWT peak 7632.0 implies z=0.1589, offset ~0.2 A from predicted 7632.2; SNR 31.6, ridge 19. Strong credible detection."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H1:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr",
            "doublet_ratio_off"
          ],
          "comment": "Doublet fit centre 7786.2 matches predicted 7786.3; separation pass but ratio 0.83 vs expected 1; local SNR 3.8. Marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "fit:H1:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr",
            "doublet_ratio_off"
          ],
          "comment": "Doublet fit centre 7803.8 matches predicted 7803.0; separation pass, ratio 0.83; local SNR 3.8. Marginal."
        }
      ]
    },
    "id": "call_00_5yd47ZOBfYV5K7WGDe8O8460",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 5360,
  "output_tokens": 2451,
  "total_tokens": 7811,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 4720,
  "provider_usage": {
    "completion_tokens": 2451,
    "prompt_tokens": 5360,
    "total_tokens": 7811,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 4720
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_5yd47ZOBfYV5K7WGDe8O8460`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 11, "line_id": "line:hbet-4862", "measurement_id": "fit:H1:0011", "reason": "measurement is outside this line's redshift window"}, {"name": "Na D_abs", "reason": "blended label duplicates an adopted doublet component"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
Two repairs needed: Hβ emission fit is outside the redshift window, and the Na D_abs blended label duplicates an adopted doublet component.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H1/pre_analysis/branches/main/52ba27339354436cbd02eabe9af017a3/lines.csv",
      "lines": [
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "weak_snr",
            "no_cwt_feature",
            "edge_blue"
          ],
          "comment": "Fit centre 3958.8 offset ~12 A from predicted 3970.6, local SNR 0.42, no CWT feature; blue edge. Not credible."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H1:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr",
            "no_cwt_feature",
            "edge_blue"
          ],
          "comment": "Fit centre 4319.9 matches prediction well (offset <1 A) but local SNR 4.25 and no CWT ridge; weak blue-edge detection."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H1:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "low_snr",
            "depth_ordering_uncertain"
          ],
          "comment": "Doublet fit centre 4561.0 near predicted 4560.3; Ca K depth (-1.65) slightly shallower than Ca H (-1.75), ordering uncertain; low local SNR 3.5. Plausible weak component."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H1:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "low_snr",
            "depth_ordering_uncertain"
          ],
          "comment": "Doublet fit centre 4601.6 near predicted 4600.6; blended with H-epsilon region; depth ordering vs Ca K uncertain; low SNR. Plausible weak component."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude",
            "degenerate_fit",
            "blend"
          ],
          "comment": "Fit returned zero amplitude with huge FWHM (degenerate); no CWT emission feature near 4601. No credible emission measurement."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H1:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "low_snr"
          ],
          "comment": "Absorption fit centre 4601.7 matches prediction; blended with Ca H; local SNR 3.2. Weak but plausible."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "no_cwt_feature"
          ],
          "comment": "Emission fit centre 4705.1 at bound, offset ~50 A from predicted 4755.1, FWHM 13310 km/s; unselectable. No CWT emission feature."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H1:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr"
          ],
          "comment": "Absorption fit centre 4755.3 matches predicted 4755.1 closely; local SNR 1.9, weak but positionally consistent."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H1:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr"
          ],
          "comment": "Absorption fit centre 4989.5 matches predicted 4990.1; local SNR 3.0, weak but positionally consistent."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "zero_amplitude",
            "rejected_fit"
          ],
          "comment": "Emission fit centre 5081.9 at bound with zero amplitude; unselectable. No CWT emission feature near 5032."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H1:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr"
          ],
          "comment": "Absorption fit centre 5033.5 near predicted 5031.9 (offset ~1.5 A); local SNR 1.5, weak but plausible."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "low_snr",
            "outside_window"
          ],
          "comment": "Emission fit centre 5587.0 offset ~49 A from predicted 5635.7 and outside redshift window; local SNR 0.62. No credible measurement."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": "fit:H1:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr",
            "offset_weak"
          ],
          "comment": "Absorption fit centre 5648.6 offset ~13 A from predicted 5635.7; local SNR 2.05. Weak but plausible."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "separation_fail",
            "low_snr",
            "rejected_fit"
          ],
          "comment": "Doublet fit failed separation; component a centre 5740.1 offset ~9 A, local SNR 2.85, ratio 7.9 inconsistent. No credible measurement."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "fit:H1:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "doublet_ratio_off",
            "low_snr"
          ],
          "comment": "Component b centre 5804.1 matches predicted 5804.3 well, but doublet separation failed and ratio 7.9 far from 3:1; local SNR 2.85. Marginal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H1:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr",
            "broad_width"
          ],
          "comment": "Absorption fit centre 6001.2 matches predicted 5999.6; local SNR 1.7, very broad FWHM ~2790 km/s. Weak but positionally consistent."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "cwt:abs:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "doublet_unresolved"
          ],
          "comment": "CWT trough at 6831.2 (z=0.1595) within Na D complex; Na D1/D2/D unresolved at this resolution, shared feature. Plausible but blended."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "blend",
            "doublet_unresolved",
            "duplicate_label"
          ],
          "comment": "Na D_abs is a blended label duplicating the adopted Na D1/D2 doublet components; no separate measurement adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "cwt:abs:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "doublet_unresolved"
          ],
          "comment": "Same CWT trough 6831.2 (z=0.1583) serves Na D2; unresolved blend with D1/D. Plausible but ambiguous."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest CWT peak 7632.0 implies z=0.1652, offset ~41 A from predicted 7591.0; that peak is better matched to [N II]b. No credible [N II]a measurement."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_reject",
            "blend"
          ],
          "comment": "Nearest CWT peak 7632.0 implies z=0.1626, offset ~24 A from predicted 7608.2; peak assigned to [N II]b. No credible H-alpha measurement."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "cwt:abs:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "blend",
            "offset_weak"
          ],
          "comment": "CWT trough 7648.0 implies z=0.1650, offset ~40 A from predicted 7608.2; weak amplitude -0.1. Marginal, possibly blended."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "cwt:em:0002",
          "status": "LIKELY",
          "reason_codes": [
            "strong_snr",
            "ridge_persistent"
          ],
          "comment": "CWT peak 7632.0 implies z=0.1589, offset ~0.2 A from predicted 7632.2; SNR 31.6, ridge 19. Strong credible detection."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": "fit:H1:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr",
            "doublet_ratio_off"
          ],
          "comment": "Doublet fit centre 7786.2 matches predicted 7786.3; separation pass but ratio 0.83 vs expected 1; local SNR 3.8. Marginal."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": "fit:H1:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "low_snr",
            "doublet_ratio_off"
          ],
          "comment": "Doublet fit centre 7803.8 matches predicted 7803.0; separation pass, ratio 0.83; local SNR 3.8. Marginal."
        }
      ]
    },
    "id": "call_00_66SMcyYwtt49fEMttK873808",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 7938,
  "output_tokens": 2453,
  "total_tokens": 10391,
  "cache_hit_tokens": 7680,
  "cache_miss_tokens": 258,
  "provider_usage": {
    "completion_tokens": 2453,
    "prompt_tokens": 7938,
    "total_tokens": 10391,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 7680
    },
    "prompt_cache_hit_tokens": 7680,
    "prompt_cache_miss_tokens": 258
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_66SMcyYwtt49fEMttK873808`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H1/pre_analysis/branches/main/52ba27339354436cbd02eabe9af017a3/lines.csv", "n_lines": 25, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H1/pre_analysis/branches/main/52ba27339354436cbd02eabe9af017a3/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:06:24.185216+00:00
