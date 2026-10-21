# SH pre-analysis session: line review

- Run ID: `graph-df7434d5533647e999870708120307b0`
- Hypothesis: `H2`
- Started (UTC): 2026-10-19T11:06:07.447610+00:00
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
Review every predicted line at the fixed Redrock redshift `-0.0013040148452830292`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H2/pre_analysis/branches/main/280ccbf593c140f4a83fefc81c71b677/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 26.9 |

Verify the redshift hypothesis z ≈ -0.0013040148452830292.

Verification window: z ∈ [-0.0113, 0.0087]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=47.8375, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=14.3812, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=35.4537, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=34.7546, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=5.99218, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/BGS_2.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H2/pre_analysis/branches/main/280ccbf593c140f4a83fefc81c71b677/lines.csv

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


## Predicted Lines at z = -0.0013

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [O II] | 3727.0 | 3722.1 | em | narrow | — |
| Ca K_abs | 3934.8 | 3929.7 | abs | absorption | — |
| Ca H_abs | 3969.6 | 3964.4 | abs | absorption | — |
| Hε | 3970.1 | 3964.9 | em | both | — |
| Hε_abs | 3970.1 | 3964.9 | abs | absorption | — |
| Hδ | 4102.9 | 4097.5 | em | both | — |
| Hδ_abs | 4102.9 | 4097.5 | abs | absorption | — |
| G-band_abs | 4305.6 | 4300.0 | abs | absorption | — |
| Hγ | 4341.7 | 4336.0 | em | both | — |
| Hγ_abs | 4341.7 | 4336.0 | abs | absorption | — |
| Hβ | 4862.7 | 4856.4 | em | both | — |
| Hβ_abs | 4862.7 | 4856.4 | abs | absorption | — |
| [O III]a | 4960.3 | 4953.8 | em | narrow | — |
| [O III]b | 5008.2 | 5001.7 | em | narrow | — |
| Mg I_abs | 5176.7 | 5169.9 | abs | absorption | — |
| Na D1_abs | 5891.6 | 5883.9 | abs | absorption | — |
| Na D_abs | 5895.6 | 5887.9 | abs | absorption | — |
| Na D2_abs | 5897.6 | 5889.9 | abs | absorption | — |
| [N II]a | 6549.8 | 6541.3 | em | narrow | — |
| Hα | 6564.6 | 6556.0 | em | both | — |
| Hα_abs | 6564.6 | 6556.0 | abs | absorption | — |
| [N II]b | 6585.3 | 6576.7 | em | narrow | — |
| [S II]a | 6718.3 | 6709.5 | em | narrow | peak@6760.8±0.8(z=0.0063) |
| [S II]b | 6732.7 | 6723.9 | em | narrow | peak@6760.8±0.8(z=0.0042) |
| CaT1_abs | 8498.0 | 8486.9 | abs | absorption | — |
| CaT2_abs | 8542.0 | 8530.9 | abs | absorption | — |
| CaT3_abs | 8662.0 | 8650.7 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 4953.8/5001.7 | fit_doublet | 4967.196±0.0/5051.128±0.8278 | 0.0/0.488804 | 176.4/139.8 | 1.21 | 0.004 | warning; separation fail; component ratio — |
| [N II]a/[N II]b | 6541.3/6576.7 | fit_doublet | 6591.259±116.8438/6572.86±12.5439 | 0.613518/0.055761 | 32125.5/652.7 | 2.46 | 4.537 | warning: center_1_deviation_large; separation fail; component ratio 0.09 |
| Ca K_abs/Ca H_abs | 3929.7/3964.4 | fit_doublet | 3888.471±1597.8724/4012.966±22559.4269 | -0.073786/-0.24917 | 22399.9/52765.9 | 0.32 | 0.104 | warning; separation fail |
| Na D1_abs/Na D2_abs | 5883.9/5889.9 | fit_doublet | 5926.945±0.0/5891.309±0.5643 | -0.0/-0.709056 | 249.9/119.8 | 1.99 | 0.012 | warning; separation fail; component ratio — |
| [O II] | 3722.1 | fit_peak | 3714.38±0.4254 | 3.311998 | 190.1 | 2.59 | 0.037 | ok |
| Hε | 3964.9 | fit_peak | 3959.278±9.7444 | 0.290168 | 2609.2 | 0.41 | 0.011 | ok |
| Hδ | 4097.5 | fit_peak | 4108.654±1.7603 | 0.664317 | 699.0 | 1.14 | 0.023 | ok |
| Hγ | 4336.0 | fit_peak | 4319.894±0.3363 | 2.346839 | 319.4 | 4.27 | 0.158 | ok |
| Hβ | 4856.4 | fit_peak | 4888.201±15.4266 | 0.185322 | 6171.4 | 0.44 | 0.037 | ok |
| Hα | 6556.0 | fit_peak | 6573.303±5.4224 | 0.1057 | 730.5 | 0.49 | 0.007 | ok |
| Hε_abs | 3964.9 | fit_peak | 3917.943±0.4569 | -1.836395 | 239.1 | 2.66 | 0.042 | ok |
| Hδ_abs | 4097.5 | fit_peak | 4065.289±1.5583 | -0.375598 | 173.7 | 0.64 | 0.002 | ok |
| G-band_abs | 4300.0 | fit_peak | 4297.054±0.5804 | -1.034992 | 164.3 | 1.8 | 0.014 | ok |
| Hγ_abs | 4336.0 | fit_peak | 4345.966±1.427 | -0.668304 | 414.0 | 1.18 | 0.016 | ok |
| Hβ_abs | 4856.4 | fit_peak | 4806.359±1.1041 | -0.375895 | 146.9 | 0.84 | 0.003 | warning: center_at_bound |
| Mg I_abs | 5169.9 | fit_peak | 5168.722±5.5103 | -0.118816 | 452.9 | 0.32 | 0.002 | ok |
| Hα_abs | 6556.0 | fit_peak | 6560.356±0.4868 | -0.508645 | 139.7 | 2.46 | 0.035 | ok |
| CaT1_abs | 8486.9 | fit_peak | 8436.92±0.0 | -0.0 | 166.9 | 0.0 | 0.0 | warning: center_at_bound |
| CaT2_abs | 8530.9 | fit_peak | 8531.55±1.4067 | -0.158612 | 149.9 | 1.05 | 0.009 | ok |
| CaT3_abs | 8650.7 | fit_peak | 8604.108±1.0256 | -0.172155 | 82.0 | 0.99 | 0.004 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:oii-3727 | [O II] | 3722.1 | emission |
| line:cak-3934-abs | Ca K_abs | 3929.7 | absorption |
| line:cah-3969-abs | Ca H_abs | 3964.4 | absorption |
| line:heps-3970 | Hε | 3964.9 | emission |
| line:heps-3970-abs | Hε_abs | 3964.9 | absorption |
| line:hdel-4102 | Hδ | 4097.5 | emission |
| line:hdel-4102-abs | Hδ_abs | 4097.5 | absorption |
| line:gband-4305-abs | G-band_abs | 4300.0 | absorption |
| line:hgam-4341 | Hγ | 4336.0 | emission |
| line:hgam-4341-abs | Hγ_abs | 4336.0 | absorption |
| line:hbet-4862 | Hβ | 4856.4 | emission |
| line:hbet-4862-abs | Hβ_abs | 4856.4 | absorption |
| line:oiii-4960 | [O III]a | 4953.8 | emission |
| line:oiii-5008 | [O III]b | 5001.7 | emission |
| line:mgi-5176-abs | Mg I_abs | 5169.9 | absorption |
| line:nad1-5891-abs | Na D1_abs | 5883.9 | absorption |
| line:nad-5895-abs | Na D_abs | 5887.9 | absorption |
| line:nad2-5897-abs | Na D2_abs | 5889.9 | absorption |
| line:nii-6549 | [N II]a | 6541.3 | emission |
| line:half-6564 | Hα | 6556.0 | emission |
| line:half-6564-abs | Hα_abs | 6556.0 | absorption |
| line:nii-6585 | [N II]b | 6576.7 | emission |
| line:sii-6718 | [S II]a | 6709.5 | emission |
| line:sii-6732 | [S II]b | 6723.9 | emission |
| line:cat1-8498-abs | CaT1_abs | 8486.9 | absorption |
| line:cat2-8542-abs | CaT2_abs | 8530.9 | absorption |
| line:cat3-8662-abs | CaT3_abs | 8650.7 | absorption |

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
| fit:H2:0000 | fit_doublet | emission | 4967.196 | [O III]a | yes | — |
| fit:H2:0001 | fit_doublet | emission | 5051.128 | [O III]b | yes | — |
| fit:H2:0002 | fit_doublet | emission | 6591.259 | [N II]a | yes | — |
| fit:H2:0003 | fit_doublet | emission | 6572.860 | [N II]b | yes | — |
| fit:H2:0004 | fit_doublet | absorption | 3888.471 | Ca K_abs | yes | — |
| fit:H2:0005 | fit_doublet | absorption | 4012.966 | Ca H_abs | yes | — |
| fit:H2:0006 | fit_doublet | absorption | 5926.945 | Na D1_abs | yes | — |
| fit:H2:0007 | fit_doublet | absorption | 5891.309 | Na D2_abs | yes | — |
| fit:H2:0008 | fit_peak | emission | 3714.380 | [O II] | yes | — |
| fit:H2:0009 | fit_peak | emission | 3959.278 | Hε | yes | — |
| fit:H2:0010 | fit_peak | emission | 4108.654 | Hδ | yes | — |
| fit:H2:0011 | fit_peak | emission | 4319.894 | Hγ | yes | — |
| fit:H2:0012 | fit_peak | emission | 4888.201 | Hβ | yes | — |
| fit:H2:0013 | fit_peak | emission | 6573.303 | Hα | yes | — |
| fit:H2:0014 | fit_peak | absorption | 3917.943 | Hε_abs | yes | — |
| fit:H2:0015 | fit_peak | absorption | 4065.289 | Hδ_abs | yes | — |
| fit:H2:0016 | fit_peak | absorption | 4297.054 | G-band_abs | yes | — |
| fit:H2:0017 | fit_peak | absorption | 4345.966 | Hγ_abs | yes | — |
| fit:H2:0018 | fit_peak | absorption | 4806.359 | Hβ_abs | no | center_at_bound |
| fit:H2:0019 | fit_peak | absorption | 5168.722 | Mg I_abs | yes | — |
| fit:H2:0020 | fit_peak | absorption | 6560.356 | Hα_abs | yes | — |
| fit:H2:0021 | fit_peak | absorption | 8436.920 | CaT1_abs | no | center_at_bound |
| fit:H2:0022 | fit_peak | absorption | 8531.550 | CaT2_abs | yes | — |
| fit:H2:0023 | fit_peak | absorption | 8604.108 | CaT3_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H2/pre_analysis/branches/main/280ccbf593c140f4a83fefc81c71b677/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H2:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_8A",
            "blue_edge"
          ],
          "comment": "Fit centre 3714.4 vs pred 3722.1, offset ~8 A within strong window; low local SNR 2.6 and blue edge (<4000 A) make this weak/marginal."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "huge_center_error",
            "blue_edge"
          ],
          "comment": "Ca K/H doublet fit gave centres 3888/4013 with enormous errors and failed separation; no credible Ca K measurement adopted. Plausible weak component not confirmed."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "huge_center_error",
            "blue_edge"
          ],
          "comment": "Ca H from same failed doublet fit (4013 +/- 22559 A); no credible measurement. Weak Ca H component remains plausible but unconfirmed."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H2:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "blend_cah"
          ],
          "comment": "Fit centre 3959.3 vs 3964.9, offset ~6 A; local SNR 0.41 and FWHM ~2600 km/s; blended with Ca H region. Marginal."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H2:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_47A",
            "weak_snr",
            "blend_cah"
          ],
          "comment": "Absorption fit centre 3917.9 vs 3964.9, offset ~47 A (weaker window); low SNR 2.7; blended with Ca H/K region. Marginal."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H2:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_11A",
            "weak_snr"
          ],
          "comment": "Fit centre 4108.7 vs 4097.5, offset ~11 A; local SNR 1.1, weak emission. Marginal."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H2:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_32A",
            "weak_snr"
          ],
          "comment": "Absorption fit centre 4065.3 vs 4097.5, offset ~32 A (weaker window); SNR 0.64. Marginal."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H2:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_3A",
            "weak_snr"
          ],
          "comment": "Fit centre 4297.1 vs 4300.0, offset ~3 A (strong window); local SNR 1.8, modest depth. Marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H2:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_16A",
            "weak_snr"
          ],
          "comment": "Fit centre 4319.9 vs 4336.0, offset ~16 A (strong window); local SNR 4.3, moderate amplitude. Marginal."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H2:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_10A",
            "weak_snr",
            "broad_width"
          ],
          "comment": "Absorption fit centre 4346.0 vs 4336.0, offset ~10 A; SNR 1.2, broad FWHM ~414 km/s. Marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "fit:H2:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_32A",
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit centre 4888.2 vs 4856.4, offset ~32 A (weaker window); SNR 0.44, FWHM ~6200 km/s. Marginal."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit"
          ],
          "comment": "Absorption fit centre 4806.4 flagged center_at_bound; not selectable, no credible measurement."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "zero_amplitude"
          ],
          "comment": "O III doublet fit gave component 1 amplitude 0.0 and failed separation; no credible [O III]a measurement."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "offset_49A"
          ],
          "comment": "O III b fit centre 5051.1 vs 5001.7, offset ~49 A with failed separation and no counterpart; not credible."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H2:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_1A"
          ],
          "comment": "Fit centre 5168.7 vs 5169.9, offset ~1 A; local SNR 0.32, very weak depth. Marginal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "zero_amplitude"
          ],
          "comment": "Na D doublet fit component 1 amplitude 0.0 and failed separation; no credible Na D1 measurement."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "blend_nad"
          ],
          "comment": "No independent measurement for Na D_abs; only the failed Na D doublet fit exists. Not adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H2:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "blend_nad",
            "offset_1A"
          ],
          "comment": "Na D2 fit centre 5891.3 vs 5889.9, offset ~1 A; doublet separation failed and D1 component zero, so depth ratio unusable. Marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "center_deviation_large",
            "separation_fail"
          ],
          "comment": "N II doublet fit component 1 centre 6591.3 +/- 117 A, flagged center_1_deviation_large and failed separation; not credible."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H2:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_17A",
            "weak_snr",
            "blend_nii"
          ],
          "comment": "Fit centre 6573.3 vs 6556.0, offset ~17 A; local SNR 0.49, blended with N II region. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H2:0020",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_4A",
            "weak_snr"
          ],
          "comment": "Absorption fit centre 6560.4 vs 6556.0, offset ~4 A; local SNR 2.5, modest depth. Marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H2:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "blend_halpha"
          ],
          "comment": "N II b fit centre 6572.9 vs 6576.7, offset ~4 A; doublet separation failed and ratio 0.09 unreliable; blended with Halpha. Marginal."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "offset_51A",
            "blend"
          ],
          "comment": "No targeted fit; nearest CWT peak 6760.8 implies z=0.0063, offset ~51 A from 6709.5. Not adopted."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "offset_37A",
            "blend"
          ],
          "comment": "No targeted fit; CWT peak 6760.8 implies z=0.0042, offset ~37 A from 6723.9. Not adopted."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "red_edge"
          ],
          "comment": "CaT1 fit centre 8436.9 flagged center_at_bound with zero amplitude; not selectable, no credible measurement."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H2:0022",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_1A",
            "red_edge"
          ],
          "comment": "Fit centre 8531.6 vs 8530.9, offset ~1 A; local SNR 1.05, weak depth near red edge. Marginal."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H2:0023",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_47A",
            "weak_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8604.1 vs 8650.7, offset ~47 A (weaker window); SNR 0.99, weak depth near red edge. Marginal."
        }
      ]
    },
    "id": "call_00_80sXeBwjqEHQqwfIiSqT1285",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 5868,
  "output_tokens": 2619,
  "total_tokens": 8487,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 5228,
  "provider_usage": {
    "completion_tokens": 2619,
    "prompt_tokens": 5868,
    "total_tokens": 8487,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 5228
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_80sXeBwjqEHQqwfIiSqT1285`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 4, "line_id": "line:heps-3970-abs", "measurement_id": "fit:H2:0014", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
The Hε_abs fit centre (3917.9 Å) falls outside the line's redshift window. I'll set it to NOT_FOUND and resubmit.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H2/pre_analysis/branches/main/280ccbf593c140f4a83fefc81c71b677/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H2:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_8A",
            "blue_edge"
          ],
          "comment": "Fit centre 3714.4 vs pred 3722.1, offset ~8 A within strong window; low local SNR 2.6 and blue edge (<4000 A) make this weak/marginal."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "huge_center_error",
            "blue_edge"
          ],
          "comment": "Ca K/H doublet fit gave centres 3888/4013 with enormous errors and failed separation; no credible Ca K measurement adopted. Plausible weak component not confirmed."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "huge_center_error",
            "blue_edge"
          ],
          "comment": "Ca H from same failed doublet fit (4013 +/- 22559 A); no credible measurement. Weak Ca H component remains plausible but unconfirmed."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H2:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "blend_cah"
          ],
          "comment": "Fit centre 3959.3 vs 3964.9, offset ~6 A; local SNR 0.41 and FWHM ~2600 km/s; blended with Ca H region. Marginal."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "outside_z_window",
            "offset_47A",
            "weak_snr"
          ],
          "comment": "Absorption fit centre 3917.9 vs 3964.9, offset ~47 A, outside the line redshift window; not selectable. No credible measurement."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H2:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_11A",
            "weak_snr"
          ],
          "comment": "Fit centre 4108.7 vs 4097.5, offset ~11 A; local SNR 1.1, weak emission. Marginal."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H2:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_32A",
            "weak_snr"
          ],
          "comment": "Absorption fit centre 4065.3 vs 4097.5, offset ~32 A (weaker window); SNR 0.64. Marginal."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H2:0016",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_3A",
            "weak_snr"
          ],
          "comment": "Fit centre 4297.1 vs 4300.0, offset ~3 A (strong window); local SNR 1.8, modest depth. Marginal."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H2:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_16A",
            "weak_snr"
          ],
          "comment": "Fit centre 4319.9 vs 4336.0, offset ~16 A (strong window); local SNR 4.3, moderate amplitude. Marginal."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H2:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_10A",
            "weak_snr",
            "broad_width"
          ],
          "comment": "Absorption fit centre 4346.0 vs 4336.0, offset ~10 A; SNR 1.2, broad FWHM ~414 km/s. Marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "fit:H2:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_32A",
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit centre 4888.2 vs 4856.4, offset ~32 A (weaker window); SNR 0.44, FWHM ~6200 km/s. Marginal."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit"
          ],
          "comment": "Absorption fit centre 4806.4 flagged center_at_bound; not selectable, no credible measurement."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "zero_amplitude"
          ],
          "comment": "O III doublet fit gave component 1 amplitude 0.0 and failed separation; no credible [O III]a measurement."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "offset_49A"
          ],
          "comment": "O III b fit centre 5051.1 vs 5001.7, offset ~49 A with failed separation and no counterpart; not credible."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H2:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_1A"
          ],
          "comment": "Fit centre 5168.7 vs 5169.9, offset ~1 A; local SNR 0.32, very weak depth. Marginal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "separation_fail",
            "zero_amplitude"
          ],
          "comment": "Na D doublet fit component 1 amplitude 0.0 and failed separation; no credible Na D1 measurement."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "blend_nad"
          ],
          "comment": "No independent measurement for Na D_abs; only the failed Na D doublet fit exists. Not adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H2:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "blend_nad",
            "offset_1A"
          ],
          "comment": "Na D2 fit centre 5891.3 vs 5889.9, offset ~1 A; doublet separation failed and D1 component zero, so depth ratio unusable. Marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "doublet_fit_failed",
            "center_deviation_large",
            "separation_fail"
          ],
          "comment": "N II doublet fit component 1 centre 6591.3 +/- 117 A, flagged center_1_deviation_large and failed separation; not credible."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H2:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_17A",
            "weak_snr",
            "blend_nii"
          ],
          "comment": "Fit centre 6573.3 vs 6556.0, offset ~17 A; local SNR 0.49, blended with N II region. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H2:0020",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_4A",
            "weak_snr"
          ],
          "comment": "Absorption fit centre 6560.4 vs 6556.0, offset ~4 A; local SNR 2.5, modest depth. Marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H2:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "blend_halpha"
          ],
          "comment": "N II b fit centre 6572.9 vs 6576.7, offset ~4 A; doublet separation failed and ratio 0.09 unreliable; blended with Halpha. Marginal."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "offset_51A",
            "blend"
          ],
          "comment": "No targeted fit; nearest CWT peak 6760.8 implies z=0.0063, offset ~51 A from 6709.5. Not adopted."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "offset_37A",
            "blend"
          ],
          "comment": "No targeted fit; CWT peak 6760.8 implies z=0.0042, offset ~37 A from 6723.9. Not adopted."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "rejected_fit",
            "red_edge"
          ],
          "comment": "CaT1 fit centre 8436.9 flagged center_at_bound with zero amplitude; not selectable, no credible measurement."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H2:0022",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_1A",
            "red_edge"
          ],
          "comment": "Fit centre 8531.6 vs 8530.9, offset ~1 A; local SNR 1.05, weak depth near red edge. Marginal."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H2:0023",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_47A",
            "weak_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8604.1 vs 8650.7, offset ~47 A (weaker window); SNR 0.99, weak depth near red edge. Marginal."
        }
      ]
    },
    "id": "call_00_iUXe3Cj9tPjGLtU8guQr8741",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 8594,
  "output_tokens": 2621,
  "total_tokens": 11215,
  "cache_hit_tokens": 8448,
  "cache_miss_tokens": 146,
  "provider_usage": {
    "completion_tokens": 2621,
    "prompt_tokens": 8594,
    "total_tokens": 11215,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 8448
    },
    "prompt_cache_hit_tokens": 8448,
    "prompt_cache_miss_tokens": 146
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_iUXe3Cj9tPjGLtU8guQr8741`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H2/pre_analysis/branches/main/280ccbf593c140f4a83fefc81c71b677/lines.csv", "n_lines": 27, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H2/pre_analysis/branches/main/280ccbf593c140f4a83fefc81c71b677/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:06:25.095617+00:00
