# SH pre-analysis session: line review

- Run ID: `graph-df7434d5533647e999870708120307b0`
- Hypothesis: `H4`
- Started (UTC): 2026-10-19T11:06:07.613793+00:00
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
Review every predicted line at the fixed Redrock redshift `-0.0013673513056349023`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H4/pre_analysis/branches/main/3cd00e208e2345ca8061e56c83b52ed2/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 26.9 |

Verify the redshift hypothesis z ≈ -0.0013673513056349023.

Verification window: z ∈ [-0.0114, 0.0086]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=47.8345, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:sii: [S II]a/[S II]b (6718.3/6732.7 Å): width_3sigma=25, separation_expected_obs=14.3803, rest_separation=14.4; amp_ratio_expected=1 (component 2 / component 1); amplitude relation: a ≈ b
- doublet:nii: [N II]a/[N II]b (6549.8/6585.3 Å): width_3sigma=25, separation_expected_obs=35.4515, rest_separation=35.5; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: a:b ≈ 1:3
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=34.7524, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H
- doublet:na-d: Na D1_abs/Na D2_abs (5891.6/5897.6 Å): width_3sigma=25, separation_expected_obs=5.9918, rest_separation=6; amp_ratio_expected=2 (component 2 / component 1); amplitude relation: a:b ≈ 2:1 (fitting hint)

FITS file: /mnt/linux_share/code/FORMA/example/basic/BGS_2.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H4/pre_analysis/branches/main/3cd00e208e2345ca8061e56c83b52ed2/lines.csv

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


## Predicted Lines at z = -0.0014

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| [O II] | 3727.0 | 3721.9 | em | narrow | — |
| Ca K_abs | 3934.8 | 3929.4 | abs | absorption | — |
| Ca H_abs | 3969.6 | 3964.2 | abs | absorption | — |
| Hε | 3970.1 | 3964.7 | em | both | — |
| Hε_abs | 3970.1 | 3964.7 | abs | absorption | — |
| Hδ | 4102.9 | 4097.3 | em | both | — |
| Hδ_abs | 4102.9 | 4097.3 | abs | absorption | — |
| G-band_abs | 4305.6 | 4299.7 | abs | absorption | — |
| Hγ | 4341.7 | 4335.8 | em | both | — |
| Hγ_abs | 4341.7 | 4335.8 | abs | absorption | — |
| Hβ | 4862.7 | 4856.1 | em | both | — |
| Hβ_abs | 4862.7 | 4856.1 | abs | absorption | — |
| [O III]a | 4960.3 | 4953.5 | em | narrow | — |
| [O III]b | 5008.2 | 5001.4 | em | narrow | — |
| Mg I_abs | 5176.7 | 5169.6 | abs | absorption | — |
| Na D1_abs | 5891.6 | 5883.5 | abs | absorption | — |
| Na D_abs | 5895.6 | 5887.5 | abs | absorption | — |
| Na D2_abs | 5897.6 | 5889.5 | abs | absorption | — |
| [N II]a | 6549.8 | 6540.8 | em | narrow | — |
| Hα | 6564.6 | 6555.6 | em | both | — |
| Hα_abs | 6564.6 | 6555.6 | abs | absorption | — |
| [N II]b | 6585.3 | 6576.3 | em | narrow | — |
| [S II]a | 6718.3 | 6709.1 | em | narrow | peak@6760.8±0.8(z=0.0063) |
| [S II]b | 6732.7 | 6723.5 | em | narrow | peak@6760.8±0.8(z=0.0042) |
| CaT1_abs | 8498.0 | 8486.4 | abs | absorption | — |
| CaT2_abs | 8542.0 | 8530.3 | abs | absorption | — |
| CaT3_abs | 8662.0 | 8650.2 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| [O III]a/[O III]b | 4953.5/5001.4 | fit_doublet | 5003.518±1.6776/5018.718±0.0 | 0.299464/0.0 | 217.1/145.4 | 0.73 | 0.002 | warning: center_1_deviation_large; separation fail; component ratio 0.0 |
| [N II]a/[N II]b | 6540.8/6576.3 | fit_doublet | 6506.078±0.8025/6574.28±5.1736 | 0.450599/0.166849 | 168.5/949.8 | 1.85 | 0.028 | warning; separation fail; component ratio 0.37 |
| Ca K_abs/Ca H_abs | 3929.4/3964.2 | fit_doublet | 3933.458±659.9207/3917.937±0.6017 | -0.303636/-1.821585 | 53842.5/235.5 | 2.37 | 0.149 | warning; separation fail |
| Na D1_abs/Na D2_abs | 5883.5/5889.5 | fit_doublet | 5914.671±0.0/5920.546±0.0 | -0.0/-0.0 | 119.4/119.2 | 0.0 | 0.0 | ok; separation pass; component ratio — |
| [O II] | 3721.9 | fit_peak | 3714.38±0.4254 | 3.311998 | 190.1 | 2.59 | 0.037 | ok |
| Hε | 3964.7 | fit_peak | 3959.383±9.864 | 0.286744 | 2598.4 | 0.4 | 0.011 | ok |
| Hδ | 4097.3 | fit_peak | 4108.654±1.7603 | 0.664326 | 698.9 | 1.14 | 0.023 | ok |
| Hγ | 4335.8 | fit_peak | 4319.895±0.3359 | 2.348838 | 319.6 | 4.27 | 0.158 | ok |
| Hβ | 4856.1 | fit_peak | 4888.219±15.4268 | 0.185328 | 6171.7 | 0.44 | 0.037 | ok |
| Hα | 6555.6 | fit_peak | 6573.329±5.3861 | 0.106401 | 732.3 | 0.49 | 0.007 | ok |
| Hε_abs | 3964.7 | fit_peak | 3993.289±0.4788 | -1.536702 | 176.8 | 2.22 | 0.022 | ok |
| Hδ_abs | 4097.3 | fit_peak | 4065.287±1.5583 | -0.375603 | 173.7 | 0.64 | 0.002 | ok |
| G-band_abs | 4299.7 | fit_peak | 4297.054±0.5804 | -1.034992 | 164.3 | 1.8 | 0.014 | ok |
| Hγ_abs | 4335.8 | fit_peak | 4345.966±1.4289 | -0.666443 | 413.0 | 1.17 | 0.016 | ok |
| Hβ_abs | 4856.1 | fit_peak | 4806.051±0.8641 | -0.4798 | 146.9 | 1.08 | 0.005 | warning: center_at_bound |
| Mg I_abs | 5169.6 | fit_peak | 5168.721±5.5122 | -0.118786 | 453.0 | 0.32 | 0.002 | ok |
| Hα_abs | 6555.6 | fit_peak | 6560.356±0.4864 | -0.508259 | 139.6 | 2.44 | 0.034 | ok |
| CaT1_abs | 8486.4 | fit_peak | 8436.383±0.0 | -0.0 | 166.9 | 0.0 | 0.0 | warning: center_at_bound |
| CaT2_abs | 8530.3 | fit_peak | 8531.545±1.4038 | -0.158721 | 149.3 | 1.04 | 0.009 | ok |
| CaT3_abs | 8650.2 | fit_peak | 8600.898±1.034 | -0.170786 | 82.1 | 1.01 | 0.005 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:oii-3727 | [O II] | 3721.9 | emission |
| line:cak-3934-abs | Ca K_abs | 3929.4 | absorption |
| line:cah-3969-abs | Ca H_abs | 3964.2 | absorption |
| line:heps-3970 | Hε | 3964.7 | emission |
| line:heps-3970-abs | Hε_abs | 3964.7 | absorption |
| line:hdel-4102 | Hδ | 4097.3 | emission |
| line:hdel-4102-abs | Hδ_abs | 4097.3 | absorption |
| line:gband-4305-abs | G-band_abs | 4299.7 | absorption |
| line:hgam-4341 | Hγ | 4335.8 | emission |
| line:hgam-4341-abs | Hγ_abs | 4335.8 | absorption |
| line:hbet-4862 | Hβ | 4856.1 | emission |
| line:hbet-4862-abs | Hβ_abs | 4856.1 | absorption |
| line:oiii-4960 | [O III]a | 4953.5 | emission |
| line:oiii-5008 | [O III]b | 5001.4 | emission |
| line:mgi-5176-abs | Mg I_abs | 5169.6 | absorption |
| line:nad1-5891-abs | Na D1_abs | 5883.5 | absorption |
| line:nad-5895-abs | Na D_abs | 5887.5 | absorption |
| line:nad2-5897-abs | Na D2_abs | 5889.5 | absorption |
| line:nii-6549 | [N II]a | 6540.8 | emission |
| line:half-6564 | Hα | 6555.6 | emission |
| line:half-6564-abs | Hα_abs | 6555.6 | absorption |
| line:nii-6585 | [N II]b | 6576.3 | emission |
| line:sii-6718 | [S II]a | 6709.1 | emission |
| line:sii-6732 | [S II]b | 6723.5 | emission |
| line:cat1-8498-abs | CaT1_abs | 8486.4 | absorption |
| line:cat2-8542-abs | CaT2_abs | 8530.3 | absorption |
| line:cat3-8662-abs | CaT3_abs | 8650.2 | absorption |

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
| fit:H4:0000 | fit_doublet | emission | 5003.518 | [O III]a | yes | — |
| fit:H4:0001 | fit_doublet | emission | 5018.718 | [O III]b | yes | — |
| fit:H4:0002 | fit_doublet | emission | 6506.078 | [N II]a | yes | — |
| fit:H4:0003 | fit_doublet | emission | 6574.280 | [N II]b | yes | — |
| fit:H4:0004 | fit_doublet | absorption | 3933.458 | Ca K_abs | yes | — |
| fit:H4:0005 | fit_doublet | absorption | 3917.937 | Ca H_abs | yes | — |
| fit:H4:0006 | fit_doublet | absorption | 5914.671 | Na D1_abs | yes | — |
| fit:H4:0007 | fit_doublet | absorption | 5920.546 | Na D2_abs | yes | — |
| fit:H4:0008 | fit_peak | emission | 3714.380 | [O II] | yes | — |
| fit:H4:0009 | fit_peak | emission | 3959.383 | Hε | yes | — |
| fit:H4:0010 | fit_peak | emission | 4108.654 | Hδ | yes | — |
| fit:H4:0011 | fit_peak | emission | 4319.895 | Hγ | yes | — |
| fit:H4:0012 | fit_peak | emission | 4888.219 | Hβ | yes | — |
| fit:H4:0013 | fit_peak | emission | 6573.329 | Hα | yes | — |
| fit:H4:0014 | fit_peak | absorption | 3993.289 | Hε_abs | yes | — |
| fit:H4:0015 | fit_peak | absorption | 4065.287 | Hδ_abs | yes | — |
| fit:H4:0016 | fit_peak | absorption | 4297.054 | G-band_abs | yes | — |
| fit:H4:0017 | fit_peak | absorption | 4345.966 | Hγ_abs | yes | — |
| fit:H4:0018 | fit_peak | absorption | 4806.051 | Hβ_abs | no | center_at_bound |
| fit:H4:0019 | fit_peak | absorption | 5168.721 | Mg I_abs | yes | — |
| fit:H4:0020 | fit_peak | absorption | 6560.356 | Hα_abs | yes | — |
| fit:H4:0021 | fit_peak | absorption | 8436.383 | CaT1_abs | no | center_at_bound |
| fit:H4:0022 | fit_peak | absorption | 8531.545 | CaT2_abs | yes | — |
| fit:H4:0023 | fit_peak | absorption | 8600.898 | CaT3_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H4/pre_analysis/branches/main/3cd00e208e2345ca8061e56c83b52ed2/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H4:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_7A",
            "blue_edge"
          ],
          "comment": "Fit centre 3714.4 vs pred 3721.9 (offset ~7.5 A, within strong window); local SNR 2.6 weak, blue edge <4000 A; no CWT support. Weak candidate only."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H4:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "huge_center_error",
            "blend_cah",
            "blue_edge"
          ],
          "comment": "Doublet fit centre 3933.5 near pred 3929.4 but error 660 A and separation fail; blended with Ca H. Plausible weak Ca K component preserved as marginal."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H4:0005",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "blend_cak",
            "depth_ordering_uncertain",
            "blue_edge"
          ],
          "comment": "Fit centre 3917.9 vs pred 3964.2 (offset ~46 A, weak window); separation fail, depth ordering inverted vs Ca K. Weak Ca H component retained as marginal."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H4:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "blend_cah"
          ],
          "comment": "Fit centre 3959.4 vs pred 3964.7 (offset ~5 A); SNR 0.4, FWHM 2598 km/s implausibly broad; blended with Ca H region. Weak marginal."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H4:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_29A",
            "blend_cah",
            "blue_edge"
          ],
          "comment": "Fit centre 3993.3 vs pred 3964.7 (offset ~29 A, weaker window); SNR 2.2; likely blended with Ca H absorption. Marginal."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H4:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_11A",
            "weak_snr"
          ],
          "comment": "Fit centre 4108.7 vs pred 4097.3 (offset ~11 A); SNR 1.1, FWHM 699 km/s. Weak marginal emission."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H4:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_32A",
            "weak_snr"
          ],
          "comment": "Fit centre 4065.3 vs pred 4097.3 (offset ~32 A, weaker window); SNR 0.6. Weak marginal absorption."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H4:0016",
          "status": "LIKELY",
          "reason_codes": [
            "good_offset",
            "moderate_snr"
          ],
          "comment": "Fit centre 4297.1 vs pred 4299.7 (offset ~2.6 A, strong window); SNR 1.8, FWHM 164 km/s consistent with G-band absorption."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H4:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_16A",
            "blend_hgam_abs"
          ],
          "comment": "Fit centre 4319.9 vs pred 4335.8 (offset ~16 A, strong window); SNR 4.3, FWHM 320 km/s; adjacent to Hgamma absorption. Marginal."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H4:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_10A",
            "blend_hgam_em",
            "weak_snr"
          ],
          "comment": "Fit centre 4346.0 vs pred 4335.8 (offset ~10 A); SNR 1.2, FWHM 413 km/s; blended with Hgamma emission. Marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "fit:H4:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_32A",
            "very_broad_width",
            "weak_snr"
          ],
          "comment": "Fit centre 4888.2 vs pred 4856.1 (offset ~32 A, weaker window); SNR 0.4, FWHM 6172 km/s implausible. Weak marginal."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "fit_rejected"
          ],
          "comment": "Only fit (fit:H4:0018) has center_at_bound at 4806 A, offset ~50 A; not selectable. No credible absorption measurement adopted."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": "fit:H4:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "center_deviation_large",
            "weak_snr"
          ],
          "comment": "Doublet fit centre 5003.5 vs pred 4953.5 (offset ~50 A); separation fail, component ratio 0, SNR 0.7. Weak marginal at best."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "fit:H4:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "zero_amplitude",
            "weak_snr"
          ],
          "comment": "Doublet fit centre 5018.7 vs pred 5001.4 (offset ~17 A) but amplitude 0.0 and separation fail; degenerate component. Marginal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H4:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit centre 5168.7 vs pred 5169.6 (offset ~0.9 A, strong window); SNR 0.3, FWHM 453 km/s. Position good but very weak; marginal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H4:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "zero_amplitude",
            "offset_31A",
            "doublet_degenerate"
          ],
          "comment": "Doublet fit centre 5914.7 vs pred 5883.5 (offset ~31 A); amplitude 0.0, zero error, degenerate. Weak marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "blend_nad"
          ],
          "comment": "No dedicated fit for Na D composite; Na D1/D2 doublet fits are degenerate with zero amplitude. No credible measurement adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H4:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "zero_amplitude",
            "offset_31A",
            "doublet_degenerate"
          ],
          "comment": "Doublet fit centre 5920.5 vs pred 5889.5 (offset ~31 A); amplitude 0.0, degenerate. Weak marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H4:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_35A",
            "blend_halpha"
          ],
          "comment": "Doublet fit centre 6506.1 vs pred 6540.8 (offset ~35 A, weaker window); separation fail, ratio 0.37; blended with Halpha/[N II]b region. Marginal."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H4:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_18A",
            "weak_snr",
            "blend_nii"
          ],
          "comment": "Fit centre 6573.3 vs pred 6555.6 (offset ~18 A, strong window); SNR 0.5, FWHM 732 km/s; blended with [N II]. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H4:0020",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_5A",
            "blend_halpha_em"
          ],
          "comment": "Fit centre 6560.4 vs pred 6555.6 (offset ~4.8 A, strong window); SNR 2.4, FWHM 140 km/s; blended with Halpha emission. Marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H4:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "broad_width",
            "blend_halpha"
          ],
          "comment": "Doublet fit centre 6574.3 vs pred 6576.3 (offset ~2 A) but separation fail and FWHM 950 km/s; blended with Halpha. Marginal."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "cwt_offset",
            "blend"
          ],
          "comment": "No targeted fit; nearest CWT peak 6760.8 implies z=0.0063, offset ~52 A from pred 6709.1. No credible measurement adopted."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "cwt_offset",
            "blend"
          ],
          "comment": "No targeted fit; CWT peak 6760.8 implies z=0.0042, offset ~37 A from pred 6723.5. No credible measurement adopted."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "fit_rejected",
            "red_edge"
          ],
          "comment": "Only fit (fit:H4:0021) has center_at_bound at 8436 A with zero amplitude; not selectable. No credible measurement adopted."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H4:0022",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8531.5 vs pred 8530.3 (offset ~1.2 A, strong window); SNR 1.0, FWHM 149 km/s; red edge. Weak marginal."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H4:0023",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_49A",
            "weak_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8600.9 vs pred 8650.2 (offset ~49 A, weaker window); SNR 1.0, FWHM 82 km/s; red edge. Weak marginal."
        }
      ]
    },
    "id": "call_00_rc2l09mupPOPmXWJqjHq2706",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 5866,
  "output_tokens": 2831,
  "total_tokens": 8697,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 5226,
  "provider_usage": {
    "completion_tokens": 2831,
    "prompt_tokens": 5866,
    "total_tokens": 8697,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 5226
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_rc2l09mupPOPmXWJqjHq2706`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 2, "line_id": "line:cah-3969-abs", "measurement_id": "fit:H4:0005", "reason": "measurement is outside this line's redshift window"}, {"row": 12, "line_id": "line:oiii-4960", "measurement_id": "fit:H4:0000", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
Two measurements fall outside their line's redshift window. I'll repair those rows.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H4/pre_analysis/branches/main/3cd00e208e2345ca8061e56c83b52ed2/lines.csv",
      "lines": [
        {
          "line_id": "line:oii-3727",
          "measurement_id": "fit:H4:0008",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "offset_7A",
            "blue_edge"
          ],
          "comment": "Fit centre 3714.4 vs pred 3721.9 (offset ~7.5 A, within strong window); local SNR 2.6 weak, blue edge <4000 A; no CWT support. Weak candidate only."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H4:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "huge_center_error",
            "blend_cah",
            "blue_edge"
          ],
          "comment": "Doublet fit centre 3933.5 near pred 3929.4 but error 660 A and separation fail; blended with Ca H. Plausible weak Ca K component preserved as marginal."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "outside_redshift_window",
            "doublet_separation_fail",
            "blend_cak",
            "blue_edge"
          ],
          "comment": "Only fit (fit:H4:0005) centre 3917.9 implies z outside this line's window; separation fail and depth ordering inverted. No selectable measurement adopted."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H4:0009",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width",
            "blend_cah"
          ],
          "comment": "Fit centre 3959.4 vs pred 3964.7 (offset ~5 A); SNR 0.4, FWHM 2598 km/s implausibly broad; blended with Ca H region. Weak marginal."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": "fit:H4:0014",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_29A",
            "blend_cah",
            "blue_edge"
          ],
          "comment": "Fit centre 3993.3 vs pred 3964.7 (offset ~29 A, weaker window); SNR 2.2; likely blended with Ca H absorption. Marginal."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": "fit:H4:0010",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_11A",
            "weak_snr"
          ],
          "comment": "Fit centre 4108.7 vs pred 4097.3 (offset ~11 A); SNR 1.1, FWHM 699 km/s. Weak marginal emission."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": "fit:H4:0015",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_32A",
            "weak_snr"
          ],
          "comment": "Fit centre 4065.3 vs pred 4097.3 (offset ~32 A, weaker window); SNR 0.6. Weak marginal absorption."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": "fit:H4:0016",
          "status": "LIKELY",
          "reason_codes": [
            "good_offset",
            "moderate_snr"
          ],
          "comment": "Fit centre 4297.1 vs pred 4299.7 (offset ~2.6 A, strong window); SNR 1.8, FWHM 164 km/s consistent with G-band absorption."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H4:0011",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_16A",
            "blend_hgam_abs"
          ],
          "comment": "Fit centre 4319.9 vs pred 4335.8 (offset ~16 A, strong window); SNR 4.3, FWHM 320 km/s; adjacent to Hgamma absorption. Marginal."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": "fit:H4:0017",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_10A",
            "blend_hgam_em",
            "weak_snr"
          ],
          "comment": "Fit centre 4346.0 vs pred 4335.8 (offset ~10 A); SNR 1.2, FWHM 413 km/s; blended with Hgamma emission. Marginal."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "fit:H4:0012",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_32A",
            "very_broad_width",
            "weak_snr"
          ],
          "comment": "Fit centre 4888.2 vs pred 4856.1 (offset ~32 A, weaker window); SNR 0.4, FWHM 6172 km/s implausible. Weak marginal."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "fit_rejected"
          ],
          "comment": "Only fit (fit:H4:0018) has center_at_bound at 4806 A, offset ~50 A; not selectable. No credible absorption measurement adopted."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "outside_redshift_window",
            "doublet_separation_fail",
            "weak_snr"
          ],
          "comment": "Only fit (fit:H4:0000) centre 5003.5 implies z outside this line's window; separation fail, component ratio 0, SNR 0.7. No selectable measurement adopted."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": "fit:H4:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "zero_amplitude",
            "weak_snr"
          ],
          "comment": "Doublet fit centre 5018.7 vs pred 5001.4 (offset ~17 A) but amplitude 0.0 and separation fail; degenerate component. Marginal."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": "fit:H4:0019",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "broad_width"
          ],
          "comment": "Fit centre 5168.7 vs pred 5169.6 (offset ~0.9 A, strong window); SNR 0.3, FWHM 453 km/s. Position good but very weak; marginal."
        },
        {
          "line_id": "line:nad1-5891-abs",
          "measurement_id": "fit:H4:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "zero_amplitude",
            "offset_31A",
            "doublet_degenerate"
          ],
          "comment": "Doublet fit centre 5914.7 vs pred 5883.5 (offset ~31 A); amplitude 0.0, zero error, degenerate. Weak marginal."
        },
        {
          "line_id": "line:nad-5895-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "blend_nad"
          ],
          "comment": "No dedicated fit for Na D composite; Na D1/D2 doublet fits are degenerate with zero amplitude. No credible measurement adopted."
        },
        {
          "line_id": "line:nad2-5897-abs",
          "measurement_id": "fit:H4:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "zero_amplitude",
            "offset_31A",
            "doublet_degenerate"
          ],
          "comment": "Doublet fit centre 5920.5 vs pred 5889.5 (offset ~31 A); amplitude 0.0, degenerate. Weak marginal."
        },
        {
          "line_id": "line:nii-6549",
          "measurement_id": "fit:H4:0002",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "offset_35A",
            "blend_halpha"
          ],
          "comment": "Doublet fit centre 6506.1 vs pred 6540.8 (offset ~35 A, weaker window); separation fail, ratio 0.37; blended with Halpha/[N II]b region. Marginal."
        },
        {
          "line_id": "line:half-6564",
          "measurement_id": "fit:H4:0013",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_18A",
            "weak_snr",
            "blend_nii"
          ],
          "comment": "Fit centre 6573.3 vs pred 6555.6 (offset ~18 A, strong window); SNR 0.5, FWHM 732 km/s; blended with [N II]. Marginal."
        },
        {
          "line_id": "line:half-6564-abs",
          "measurement_id": "fit:H4:0020",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_5A",
            "blend_halpha_em"
          ],
          "comment": "Fit centre 6560.4 vs pred 6555.6 (offset ~4.8 A, strong window); SNR 2.4, FWHM 140 km/s; blended with Halpha emission. Marginal."
        },
        {
          "line_id": "line:nii-6585",
          "measurement_id": "fit:H4:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "broad_width",
            "blend_halpha"
          ],
          "comment": "Doublet fit centre 6574.3 vs pred 6576.3 (offset ~2 A) but separation fail and FWHM 950 km/s; blended with Halpha. Marginal."
        },
        {
          "line_id": "line:sii-6718",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "cwt_offset",
            "blend"
          ],
          "comment": "No targeted fit; nearest CWT peak 6760.8 implies z=0.0063, offset ~52 A from pred 6709.1. No credible measurement adopted."
        },
        {
          "line_id": "line:sii-6732",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_measurement",
            "cwt_offset",
            "blend"
          ],
          "comment": "No targeted fit; CWT peak 6760.8 implies z=0.0042, offset ~37 A from pred 6723.5. No credible measurement adopted."
        },
        {
          "line_id": "line:cat1-8498-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "center_at_bound",
            "fit_rejected",
            "red_edge"
          ],
          "comment": "Only fit (fit:H4:0021) has center_at_bound at 8436 A with zero amplitude; not selectable. No credible measurement adopted."
        },
        {
          "line_id": "line:cat2-8542-abs",
          "measurement_id": "fit:H4:0022",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8531.5 vs pred 8530.3 (offset ~1.2 A, strong window); SNR 1.0, FWHM 149 km/s; red edge. Weak marginal."
        },
        {
          "line_id": "line:cat3-8662-abs",
          "measurement_id": "fit:H4:0023",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_49A",
            "weak_snr",
            "red_edge"
          ],
          "comment": "Fit centre 8600.9 vs pred 8650.2 (offset ~49 A, weaker window); SNR 1.0, FWHM 82 km/s; red edge. Weak marginal."
        }
      ]
    },
    "id": "call_00_JA7A6lJ0dUJYxKZLSBxs5059",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 8849,
  "output_tokens": 2813,
  "total_tokens": 11662,
  "cache_hit_tokens": 8576,
  "cache_miss_tokens": 273,
  "provider_usage": {
    "completion_tokens": 2813,
    "prompt_tokens": 8849,
    "total_tokens": 11662,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 8576
    },
    "prompt_cache_hit_tokens": 8576,
    "prompt_cache_miss_tokens": 273
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_JA7A6lJ0dUJYxKZLSBxs5059`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H4/pre_analysis/branches/main/3cd00e208e2345ca8061e56c83b52ed2/lines.csv", "n_lines": 27, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H4/pre_analysis/branches/main/3cd00e208e2345ca8061e56c83b52ed2/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:06:25.791125+00:00
