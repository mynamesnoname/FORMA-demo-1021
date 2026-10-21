# SH pre-analysis session: line review

- Run ID: `graph-df7434d5533647e999870708120307b0`
- Hypothesis: `H5`
- Started (UTC): 2026-10-19T11:06:23.013303+00:00
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
Review every predicted line at the fixed Redrock redshift `1.418867070771408`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H5/pre_analysis/branches/main/61c4d4b5796f4955b054c686843b3609/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 26.9 |

Verify the redshift hypothesis z ≈ 1.418867070771408.

Verification window: z ∈ [1.4089, 1.4289]
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
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=84.1766, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H

FITS file: /mnt/linux_share/code/FORMA/example/basic/BGS_2.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H5/pre_analysis/branches/main/61c4d4b5796f4955b054c686843b3609/lines.csv

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


## Predicted Lines at z = 1.4189

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| C IV | 1549.0 | 3746.8 | em | broad | — |
| He II | 1640.4 | 3967.9 | em | both | — |
| C III] | 1909.0 | 4617.6 | em | broad | — |
| Mg II | 2800.0 | 6772.8 | em | broad | peak@6760.8±0.8(z=1.4146) |
| Mg II_abs | 2800.0 | 6772.8 | abs | absorption | — |
| [Ne V] | 3426.0 | 8287.0 | em | narrow | — |
| [O II] | 3727.0 | 9015.1 | em | narrow | — |
| Ca K_abs | 3934.8 | 9517.8 | abs | absorption | — |
| Ca H_abs | 3969.6 | 9601.9 | abs | absorption | — |
| Hε | 3970.1 | 9603.1 | em | both | — |
| Hε_abs | 3970.1 | 9603.1 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| Ca K_abs/Ca H_abs | 9517.8/9601.9 | fit_doublet | 9505.281±0.3269/9599.668±0.0 | -0.763722/-0.0 | 74.3/6118.0 | 3.59 | 0.041 | warning; separation fail |
| C IV | 3746.8 | fit_peak | 3796.825±92.5929 | 0.114276 | 8508.7 | 0.1 | 0.002 | warning: center_at_bound |
| He II | 3967.9 | fit_peak | 3958.852±9.1402 | 0.305307 | 2656.0 | 0.43 | 0.012 | ok |
| C III] | 4617.6 | fit_peak | 4665.666±4.1713 | 0.723135 | 4415.0 | 1.48 | 0.283 | ok |
| [Ne V] | 8287.0 | fit_peak | 8248.835±0.0 | 0.0 | 4212.4 | 0.0 | 0.0 | ok |
| [O II] | 9015.1 | fit_peak | 9065.118±7.9775 | 0.18086 | 4147.6 | 1.14 | 0.308 | warning: center_at_bound |
| Hε | 9603.1 | fit_peak | 9570.173±10.3448 | 0.118601 | 1642.2 | 0.6 | 0.036 | ok |
| Mg II_abs | 6772.8 | fit_peak | 6822.828±1.4749 | -0.66233 | 1365.0 | 2.79 | 0.456 | warning: center_at_bound |
| Hε_abs | 9603.1 | fit_peak | 9653.138±0.0 | -0.0 | 145.9 | 0.0 | 0.0 | warning: center_at_bound |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:civ-1549 | C IV | 3746.8 | emission |
| line:heii-1640 | He II | 3967.9 | emission |
| line:ciii-1909 | C III] | 4617.6 | emission |
| line:mgii-2800 | Mg II | 6772.8 | emission |
| line:mgii-2800-abs | Mg II_abs | 6772.8 | absorption |
| line:nev-3426 | [Ne V] | 8287.0 | emission |
| line:oii-3727 | [O II] | 9015.1 | emission |
| line:cak-3934-abs | Ca K_abs | 9517.8 | absorption |
| line:cah-3969-abs | Ca H_abs | 9601.9 | absorption |
| line:heps-3970 | Hε | 9603.1 | emission |
| line:heps-3970-abs | Hε_abs | 9603.1 | absorption |

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
| fit:H5:0000 | fit_doublet | absorption | 9505.281 | Ca K_abs | yes | — |
| fit:H5:0001 | fit_doublet | absorption | 9599.668 | Ca H_abs | yes | — |
| fit:H5:0002 | fit_peak | emission | 3796.825 | C IV | no | center_at_bound |
| fit:H5:0003 | fit_peak | emission | 3958.852 | He II | yes | — |
| fit:H5:0004 | fit_peak | emission | 4665.666 | C III] | yes | — |
| fit:H5:0005 | fit_peak | emission | 8248.835 | [Ne V] | yes | — |
| fit:H5:0006 | fit_peak | emission | 9065.118 | [O II] | no | center_at_bound |
| fit:H5:0007 | fit_peak | emission | 9570.173 | Hε | yes | — |
| fit:H5:0008 | fit_peak | absorption | 6822.828 | Mg II_abs | no | center_at_bound |
| fit:H5:0009 | fit_peak | absorption | 9653.138 | Hε_abs | no | center_at_bound |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H5/pre_analysis/branches/main/61c4d4b5796f4955b054c686843b3609/lines.csv",
      "lines": [
        {
          "line_id": "line:civ-1549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "low_snr"
          ],
          "comment": "No CWT feature near 3746.8; targeted fit center_at_bound (3796.8, err 92.6, SNR 0.1) is unselectable and not credible."
        },
        {
          "line_id": "line:heii-1640",
          "measurement_id": "fit:H5:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "no_cwt_feature",
            "broad_width"
          ],
          "comment": "Fit converged at 3958.9 (offset ~9 A, within window) but local SNR 0.43 and no CWT support; weak marginal emission candidate."
        },
        {
          "line_id": "line:ciii-1909",
          "measurement_id": "cwt:em:0000",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_ridge",
            "offset_ok",
            "broad_width"
          ],
          "comment": "CWT peak 4660.0 (z=1.4406) vs pred 4617.6, offset ~42 A (weaker band); ridge 6, SNR 11.5, FWHM broad. Fit 4665.7 consistent. Adopt CWT."
        },
        {
          "line_id": "line:mgii-2800",
          "measurement_id": "cwt:em:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_amplitude",
            "blend_ambiguity"
          ],
          "comment": "CWT peak 6760.8 (z=1.4146) vs pred 6772.8, offset ~12 A; low amplitude 0.2, SNR 12.8, broad. Weak marginal; possible blend with Mg II_abs region."
        },
        {
          "line_id": "line:mgii-2800-abs",
          "measurement_id": "cwt:abs:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "fit_center_at_bound",
            "blend_ambiguity"
          ],
          "comment": "CWT trough 6831.2 (z=1.4397) vs pred 6772.8, offset ~58 A (weaker band); fit 6822.8 center_at_bound unselectable. Adopt CWT trough as marginal; blended with Mg II emission region."
        },
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_feature"
          ],
          "comment": "No CWT feature near 8287; fit at 8248.8 has zero amplitude and SNR 0.0, not a real signal."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "No CWT feature near 9015; fit center_at_bound at 9065.1 (SNR 1.14) unselectable and not credible."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H5:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "edge_red"
          ],
          "comment": "Doublet fit gives Ca K at 9505.3 (offset ~12 A) with depth -0.76, but separation check failed and Ca H component degenerate (FWHM 6118, amp 0). Plausible weak Ca K component preserved as marginal; red edge."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H5:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "degenerate_fit",
            "zero_amplitude",
            "edge_red"
          ],
          "comment": "Ca H fit at 9599.7 but amplitude 0.0 and error 0.0 (degenerate); depth ordering vs Ca K uncertain. Preserve as plausible weak component, marginal; red edge."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H5:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "no_cwt_feature",
            "edge_red"
          ],
          "comment": "Fit at 9570.2 (offset ~33 A) with SNR 0.6, no CWT support; weak marginal emission candidate near red edge, blended with Ca H region."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "zero_amplitude"
          ],
          "comment": "Fit center_at_bound at 9653.1 with zero amplitude and SNR 0.0; no credible absorption measurement."
        }
      ]
    },
    "id": "call_00_E7J9EXBbYMg79jDL5iRK9784",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 3679,
  "output_tokens": 1279,
  "total_tokens": 4958,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 3039,
  "provider_usage": {
    "completion_tokens": 1279,
    "prompt_tokens": 3679,
    "total_tokens": 4958,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 3039
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_E7J9EXBbYMg79jDL5iRK9784`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 2, "line_id": "line:ciii-1909", "measurement_id": "cwt:em:0000", "reason": "measurement is outside this line's redshift window"}, {"row": 4, "line_id": "line:mgii-2800-abs", "measurement_id": "cwt:abs:0000", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
Two measurements fall outside the redshift window. Let me correct those rows.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H5/pre_analysis/branches/main/61c4d4b5796f4955b054c686843b3609/lines.csv",
      "lines": [
        {
          "line_id": "line:civ-1549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "low_snr"
          ],
          "comment": "No CWT feature near 3746.8; targeted fit center_at_bound (3796.8, err 92.6, SNR 0.1) is unselectable and not credible."
        },
        {
          "line_id": "line:heii-1640",
          "measurement_id": "fit:H5:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "no_cwt_feature",
            "broad_width"
          ],
          "comment": "Fit converged at 3958.9 (offset ~9 A, within window) but local SNR 0.43 and no CWT support; weak marginal emission candidate."
        },
        {
          "line_id": "line:ciii-1909",
          "measurement_id": "fit:H5:0004",
          "status": "MARGINAL",
          "reason_codes": [
            "cwt_outside_window",
            "weak_snr",
            "broad_width"
          ],
          "comment": "CWT peak 4660.0 implies z=1.4406, outside the verification window, so not adoptable. Targeted fit at 4665.7 (offset ~48 A, weaker band) with SNR 1.48; weak marginal only."
        },
        {
          "line_id": "line:mgii-2800",
          "measurement_id": "cwt:em:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_amplitude",
            "blend_ambiguity"
          ],
          "comment": "CWT peak 6760.8 (z=1.4146) vs pred 6772.8, offset ~12 A; low amplitude 0.2, SNR 12.8, broad. Weak marginal; possible blend with Mg II_abs region."
        },
        {
          "line_id": "line:mgii-2800-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "cwt_outside_window",
            "fit_center_at_bound",
            "blend_ambiguity"
          ],
          "comment": "CWT trough 6831.2 implies z=1.4397, outside window, not adoptable; fit 6822.8 center_at_bound unselectable. No credible in-window absorption measurement."
        },
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_feature"
          ],
          "comment": "No CWT feature near 8287; fit at 8248.8 has zero amplitude and SNR 0.0, not a real signal."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "No CWT feature near 9015; fit center_at_bound at 9065.1 (SNR 1.14) unselectable and not credible."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H5:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "edge_red"
          ],
          "comment": "Doublet fit gives Ca K at 9505.3 (offset ~12 A) with depth -0.76, but separation check failed and Ca H component degenerate (FWHM 6118, amp 0). Plausible weak Ca K component preserved as marginal; red edge."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H5:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "degenerate_fit",
            "zero_amplitude",
            "edge_red"
          ],
          "comment": "Ca H fit at 9599.7 but amplitude 0.0 and error 0.0 (degenerate); depth ordering vs Ca K uncertain. Preserve as plausible weak component, marginal; red edge."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H5:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "no_cwt_feature",
            "edge_red"
          ],
          "comment": "Fit at 9570.2 (offset ~33 A) with SNR 0.6, no CWT support; weak marginal emission candidate near red edge, blended with Ca H region."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "zero_amplitude"
          ],
          "comment": "Fit center_at_bound at 9653.1 with zero amplitude and SNR 0.0; no credible absorption measurement."
        }
      ]
    },
    "id": "call_00_sB2RowjOlKKzRDlHGbQg1632",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 5113,
  "output_tokens": 1244,
  "total_tokens": 6357,
  "cache_hit_tokens": 4864,
  "cache_miss_tokens": 249,
  "provider_usage": {
    "completion_tokens": 1244,
    "prompt_tokens": 5113,
    "total_tokens": 6357,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 4864
    },
    "prompt_cache_hit_tokens": 4864,
    "prompt_cache_miss_tokens": 249
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_sB2RowjOlKKzRDlHGbQg1632`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 2, "line_id": "line:ciii-1909", "measurement_id": "fit:H5:0004", "reason": "measurement is outside this line's redshift window"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 5

#### Graph update: `model`

### Event 5 message: ai

```markdown
The C III] fit at 4665.7 also falls outside the window. I'll mark it NOT_FOUND.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H5/pre_analysis/branches/main/61c4d4b5796f4955b054c686843b3609/lines.csv",
      "lines": [
        {
          "line_id": "line:civ-1549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "low_snr"
          ],
          "comment": "No CWT feature near 3746.8; targeted fit center_at_bound (3796.8, err 92.6, SNR 0.1) is unselectable and not credible."
        },
        {
          "line_id": "line:heii-1640",
          "measurement_id": "fit:H5:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "no_cwt_feature",
            "broad_width"
          ],
          "comment": "Fit converged at 3958.9 (offset ~9 A, within window) but local SNR 0.43 and no CWT support; weak marginal emission candidate."
        },
        {
          "line_id": "line:ciii-1909",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "cwt_outside_window",
            "fit_outside_window",
            "weak_snr"
          ],
          "comment": "CWT peak 4660.0 (z=1.4406) and fit 4665.7 both imply redshifts outside the verification window; no in-window credible measurement adopted."
        },
        {
          "line_id": "line:mgii-2800",
          "measurement_id": "cwt:em:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_amplitude",
            "blend_ambiguity"
          ],
          "comment": "CWT peak 6760.8 (z=1.4146) vs pred 6772.8, offset ~12 A; low amplitude 0.2, SNR 12.8, broad. Weak marginal; possible blend with Mg II_abs region."
        },
        {
          "line_id": "line:mgii-2800-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "cwt_outside_window",
            "fit_center_at_bound",
            "blend_ambiguity"
          ],
          "comment": "CWT trough 6831.2 implies z=1.4397, outside window, not adoptable; fit 6822.8 center_at_bound unselectable. No credible in-window absorption measurement."
        },
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "zero_amplitude_fit",
            "no_cwt_feature"
          ],
          "comment": "No CWT feature near 8287; fit at 8248.8 has zero amplitude and SNR 0.0, not a real signal."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "no_cwt_feature"
          ],
          "comment": "No CWT feature near 9015; fit center_at_bound at 9065.1 (SNR 1.14) unselectable and not credible."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": "fit:H5:0000",
          "status": "MARGINAL",
          "reason_codes": [
            "doublet_separation_fail",
            "weak_snr",
            "edge_red"
          ],
          "comment": "Doublet fit gives Ca K at 9505.3 (offset ~12 A) with depth -0.76, but separation check failed and Ca H component degenerate (FWHM 6118, amp 0). Plausible weak Ca K component preserved as marginal; red edge."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": "fit:H5:0001",
          "status": "MARGINAL",
          "reason_codes": [
            "degenerate_fit",
            "zero_amplitude",
            "edge_red"
          ],
          "comment": "Ca H fit at 9599.7 but amplitude 0.0 and error 0.0 (degenerate); depth ordering vs Ca K uncertain. Preserve as plausible weak component, marginal; red edge."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": "fit:H5:0007",
          "status": "MARGINAL",
          "reason_codes": [
            "weak_snr",
            "no_cwt_feature",
            "edge_red"
          ],
          "comment": "Fit at 9570.2 (offset ~33 A) with SNR 0.6, no CWT support; weak marginal emission candidate near red edge, blended with Ca H region."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "fit_center_at_bound",
            "zero_amplitude"
          ],
          "comment": "Fit center_at_bound at 9653.1 with zero amplitude and SNR 0.0; no credible absorption measurement."
        }
      ]
    },
    "id": "call_00_rLaYzg6q8rLg7SvphdRo3153",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 6462,
  "output_tokens": 1236,
  "total_tokens": 7698,
  "cache_hit_tokens": 6272,
  "cache_miss_tokens": 190,
  "provider_usage": {
    "completion_tokens": 1236,
    "prompt_tokens": 6462,
    "total_tokens": 7698,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 6272
    },
    "prompt_cache_hit_tokens": 6272,
    "prompt_cache_miss_tokens": 190
  }
}
```

### Event 6

#### Graph update: `tools`

### Event 6 message: tool

Tool: `write_lines_csv`; call ID: `call_00_rLaYzg6q8rLg7SvphdRo3153`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H5/pre_analysis/branches/main/61c4d4b5796f4955b054c686843b3609/lines.csv", "n_lines": 11, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/BGS_2/SH/H5/pre_analysis/branches/main/61c4d4b5796f4955b054c686843b3609/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 6
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:06:37.113279+00:00
