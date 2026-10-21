# SH pre-analysis session: line review

- Run ID: `graph-325ff74c7f444efdb17e3f3b69698eea`
- Hypothesis: `H5`
- Started (UTC): 2026-10-19T11:44:53.177133+00:00
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
Review every predicted line at the fixed Redrock redshift `2.9196962422694117`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H5/pre_analysis/branches/main/22064fb1635b431bbb1aab530eacd033/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 4.7 |

Verify the redshift hypothesis z ≈ 2.9196962422694117.

Verification window: z ∈ [2.9097, 2.9297]
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
- No complete registered doublet is in nominal coverage.

FITS file: /mnt/linux_share/code/FORMA/example/basic/QSO_116.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H5/pre_analysis/branches/main/22064fb1635b431bbb1aab530eacd033/lines.csv

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


## Predicted Lines at z = 2.9197

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| Lyα | 1215.7 | 4765.1 | em | broad | peak@4768.0±0.8(z=2.9221) |
| C IV | 1549.0 | 6071.6 | em | broad | peak@6072.0±0.8(z=2.9199) |
| He II | 1640.4 | 6429.9 | em | both | — |
| C III] | 1909.0 | 7482.7 | em | broad | peak@7474.4±0.8(z=2.9153) |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| He II | 6429.9 | fit_peak | 6479.87±33.5428 | 0.166733 | 12175.1 | 1.42 | 0.97 | warning: center_at_bound |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:lya-1216 | Lyα | 4765.1 | emission |
| line:civ-1549 | C IV | 6071.6 | emission |
| line:heii-1640 | He II | 6429.9 | emission |
| line:ciii-1909 | C III] | 7482.7 | emission |

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
| fit:H5:0000 | fit_peak | emission | 6479.870 | He II | no | center_at_bound |


```

## Returned events

### Event 1

#### Graph update: `model`

### Event 1 message: ai


Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H5/pre_analysis/branches/main/22064fb1635b431bbb1aab530eacd033/lines.csv",
      "lines": [
        {
          "line_id": "line:lya-1216",
          "measurement_id": "cwt:em:0000",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "broad_width"
          ],
          "comment": "CWT peak 4768.0 A, implied z=2.9221 within window; offset +2.9 A; SNR 13, ridge 15, FWHM ~2500 km/s consistent with broad Ly-alpha."
        },
        {
          "line_id": "line:civ-1549",
          "measurement_id": "cwt:em:0002",
          "status": "LIKELY",
          "reason_codes": [
            "offset_ok",
            "snr_strong",
            "broad_width"
          ],
          "comment": "CWT peak 6072.0 A, implied z=2.9199; offset +0.4 A; SNR 23, ridge 9, FWHM ~3470 km/s consistent with broad C IV."
        },
        {
          "line_id": "line:heii-1640",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "fit_rejected"
          ],
          "comment": "No CWT feature near 6430 A; targeted fit 6479.9 A is center_at_bound and unselectable, offset ~50 A. No credible measurement adopted."
        },
        {
          "line_id": "line:ciii-1909",
          "measurement_id": "cwt:em:0003",
          "status": "MARGINAL",
          "reason_codes": [
            "offset_weak",
            "low_amplitude",
            "broad_width"
          ],
          "comment": "CWT peak 7474.4 A, implied z=2.9153 within window; offset -8.3 A; SNR 20 but low amplitude 0.3 and FWHM ~3400 km/s; plausible but weak C III] candidate."
        }
      ]
    },
    "id": "call_00_uWdXgcomUcneg7juLsid3703",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 4092,
  "output_tokens": 543,
  "total_tokens": 4635,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 3452,
  "provider_usage": {
    "completion_tokens": 543,
    "prompt_tokens": 4092,
    "total_tokens": 4635,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 3452
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_uWdXgcomUcneg7juLsid3703`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H5/pre_analysis/branches/main/22064fb1635b431bbb1aab530eacd033/lines.csv", "n_lines": 4, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_116/SH/H5/pre_analysis/branches/main/22064fb1635b431bbb1aab530eacd033/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 2
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:44:56.262346+00:00
