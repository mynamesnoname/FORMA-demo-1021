# SH pre-analysis session: line review

- Run ID: `graph-853b617a68f04c36bd82f06bdb770ac4`
- Hypothesis: `H6`
- Started (UTC): 2026-10-19T11:40:05.056373+00:00
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
Review every predicted line at the fixed Redrock redshift `1.902738756933621`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H6/pre_analysis/branches/main/3477d7d134a449bab694da82c3be7888/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 46.6 |

Verify the redshift hypothesis z ≈ 1.902738756933621.

Verification window: z ∈ [1.8927, 1.9127]
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

FITS file: /mnt/linux_share/code/FORMA/example/basic/QSO_4.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H6/pre_analysis/branches/main/3477d7d134a449bab694da82c3be7888/lines.csv

## CWT Detected Features

### Emission (peaks) — 22 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 4143.2 | 0.8 | 1.6 | 22.4 | 1623 | 7 | 8.9 |
| 4242.4 | 0.8 | 4.6 | 27.1 | 1917 | 19 | 21.3 |
| 4616.8 | 0.8 | 11.6 | 16.9 | 1099 | 24 | 76.2 |
| 4791.2 | 0.8 | 6.6 | 22.4 | 1403 | 21 | 17.1 |
| 4912.8 | 0.8 | 1.3 | 20.5 | 1250 | 14 | 10.7 |
| 5079.2 | 0.8 | 2.1 | 16.9 | 999 | 24 | 16.2 |
| 5387.2 | 0.8 | 0.7 | 85.1 | 4736 | 7 | 12.8 |
| 5802.4 | 0.8 | 1.3 | 11.6 | 597 | 8 | 8.6 |
| 6020.0 | 0.8 | 8.6 | 12.7 | 631 | 21 | 36.2 |
| 6140.8 | 0.8 | 20.8 | 10.5 | 511 | 19 | 66.3 |
| 6200.0 | 0.8 | 58.6 | 16.9 | 818 | 24 | 133.7 |
| 7802.4 | 0.8 | 1.9 | 20.5 | 787 | 22 | 25.5 |
| 8127.2 | 0.8 | 22.6 | 20.5 | 755 | 22 | 22.7 |
| 8318.4 | 0.8 | 3.9 | 18.5 | 668 | 23 | 31.8 |
| 8336.0 | 0.8 | 3.4 | 7.9 | 284 | 12 | 27.2 |
| 8837.6 | 0.8 | 0.9 | 12.7 | 430 | 13 | 13.0 |
| 9004.8 | 0.8 | 1.6 | 5.9 | 197 | 13 | 19.1 |
| 9068.8 | 0.8 | 0.1 | 53.1 | 1755 | 4 | 9.6 |
| 9316.8 | 0.8 | 1.3 | 2.5 | 81 | 4 | 14.2 |
| 9327.2 | 0.8 | 2.6 | 3.7 | 118 | 8 | 21.5 |
| 9379.2 | 0.8 | 4.9 | 3.3 | 107 | 7 | 39.8 |
| 9443.2 | 0.8 | 4.0 | 2.8 | 88 | 5 | 22.1 |

### Absorption (troughs) — 32 features

| λ (Å) | λ_err (Å) | Amp | FWHM (Å) | FWHM (km/s) | Ridge | SNR |
|-------|-----------|-----|----------|-------------|-------|-----|
| 4188.0 | 0.8 | -0.2 | 77.7 | 5563 | 4 | 18.8 |
| 4222.4 | 0.8 | -0.5 | 24.8 | 1759 | 8 | 13.4 |
| 4274.4 | 0.8 | -0.4 | 39.7 | 2785 | 5 | 9.6 |
| 4607.2 | 0.8 | -0.3 | 11.6 | 752 | 20 | 35.4 |
| 4625.6 | 0.8 | -0.5 | 11.6 | 749 | 18 | 35.9 |
| 4748.8 | 0.8 | -0.1 | 53.1 | 3352 | 4 | 17.9 |
| 4868.0 | 0.8 | -0.8 | 70.3 | 4331 | 7 | 24.0 |
| 5075.2 | 0.8 | -0.2 | 5.4 | 319 | 4 | 8.8 |
| 5333.6 | 0.8 | -0.5 | 58.1 | 3268 | 5 | 20.3 |
| 5439.2 | 0.8 | -0.2 | 58.1 | 3204 | 5 | 16.3 |
| 6010.4 | 0.8 | -0.8 | 12.7 | 632 | 19 | 22.2 |
| 6031.2 | 0.8 | -0.1 | 14.0 | 695 | 12 | 17.6 |
| 6084.8 | 0.8 | -0.1 | 103.0 | 5073 | 5 | 132.5 |
| 6132.0 | 0.8 | -2.0 | 9.6 | 467 | 18 | 38.7 |
| 6149.6 | 0.8 | -1.0 | 10.5 | 510 | 9 | 16.7 |
| 6191.2 | 0.8 | -5.4 | 10.5 | 507 | 19 | 35.4 |
| 6216.0 | 0.8 | -0.5 | 20.5 | 988 | 16 | 240.5 |
| 7740.8 | 0.8 | -0.0 | 77.7 | 3010 | 4 | 13.4 |
| 7790.4 | 0.8 | -0.0 | 15.3 | 589 | 7 | 10.0 |
| 7811.2 | 0.8 | -0.1 | 11.6 | 444 | 12 | 10.3 |
| 7850.4 | 0.8 | -0.1 | 64.2 | 2453 | 4 | 10.9 |
| 8120.0 | 0.8 | -3.5 | 8.6 | 319 | 5 | 9.5 |
| 8306.4 | 0.8 | -0.4 | 15.3 | 553 | 17 | 15.4 |
| 8326.4 | 0.8 | -0.4 | 8.6 | 311 | 7 | 25.3 |
| 8350.4 | 0.8 | -0.1 | 20.5 | 735 | 16 | 20.0 |
| 8829.6 | 0.8 | -0.8 | 9.6 | 324 | 4 | 9.2 |
| 9006.4 | 0.8 | -0.1 | 2.5 | 84 | 4 | 10.0 |
| 9315.2 | 0.8 | -1.6 | 2.5 | 81 | 4 | 12.2 |
| 9327.2 | 0.8 | -2.6 | 2.5 | 81 | 4 | 12.0 |
| 9376.8 | 0.8 | -0.3 | 3.0 | 97 | 6 | 29.5 |
| 9441.6 | 0.8 | -2.5 | 2.8 | 88 | 5 | 19.9 |
| 9793.6 | 0.8 | -1.2 | 4.5 | 137 | 6 | 9.0 |


## Predicted Lines at z = 1.9027

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| C IV | 1549.0 | 4496.3 | em | broad | — |
| He II | 1640.4 | 4761.7 | em | both | — |
| C III] | 1909.0 | 5541.3 | em | broad | — |
| Mg II | 2800.0 | 8127.7 | em | broad | peak@8127.2±0.8(z=1.9026) |
| Mg II_abs | 2800.0 | 8127.7 | abs | absorption | trough@8120.0±0.8(z=1.9000) |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| C IV | 4496.3 | fit_peak | 4507.146±0.0 | 0.0 | 312.5 | 0.0 | 0.0 | ok |
| He II | 4761.7 | fit_peak | 4805.927±0.0 | 0.0 | 21621.0 | 0.0 | 0.0 | ok |
| C III] | 5541.3 | fit_peak | 5503.927±0.0 | 0.0 | 6202.8 | 0.0 | 0.0 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:civ-1549 | C IV | 4496.3 | emission |
| line:heii-1640 | He II | 4761.7 | emission |
| line:ciii-1909 | C III] | 5541.3 | emission |
| line:mgii-2800 | Mg II | 8127.7 | emission |
| line:mgii-2800-abs | Mg II_abs | 8127.7 | absorption |

| Measurement ID | Source | Kind | Centre (Å) | Target | Selectable | Flags |
|---|---|---|---:|---|---|---|
| cwt:em:0000 | CWT | emission | 4143.200 | — | yes | — |
| cwt:em:0001 | CWT | emission | 4242.400 | — | yes | — |
| cwt:em:0002 | CWT | emission | 4616.800 | — | yes | — |
| cwt:em:0003 | CWT | emission | 4791.200 | — | yes | — |
| cwt:em:0004 | CWT | emission | 4912.800 | — | yes | — |
| cwt:em:0005 | CWT | emission | 5079.200 | — | yes | — |
| cwt:em:0006 | CWT | emission | 5387.200 | — | yes | — |
| cwt:em:0007 | CWT | emission | 5802.400 | — | yes | — |
| cwt:em:0008 | CWT | emission | 6020.000 | — | yes | — |
| cwt:em:0009 | CWT | emission | 6140.800 | — | yes | — |
| cwt:em:0010 | CWT | emission | 6200.000 | — | yes | — |
| cwt:em:0011 | CWT | emission | 7802.400 | — | yes | — |
| cwt:em:0012 | CWT | emission | 8127.200 | — | yes | — |
| cwt:em:0013 | CWT | emission | 8318.400 | — | yes | — |
| cwt:em:0014 | CWT | emission | 8336.000 | — | yes | — |
| cwt:em:0015 | CWT | emission | 8837.600 | — | yes | — |
| cwt:em:0016 | CWT | emission | 9004.800 | — | yes | — |
| cwt:em:0017 | CWT | emission | 9068.800 | — | yes | — |
| cwt:em:0018 | CWT | emission | 9316.800 | — | yes | — |
| cwt:em:0019 | CWT | emission | 9327.200 | — | yes | — |
| cwt:em:0020 | CWT | emission | 9379.200 | — | yes | — |
| cwt:em:0021 | CWT | emission | 9443.200 | — | yes | — |
| cwt:abs:0000 | CWT | absorption | 4188.000 | — | yes | — |
| cwt:abs:0001 | CWT | absorption | 4222.400 | — | yes | — |
| cwt:abs:0002 | CWT | absorption | 4274.400 | — | yes | — |
| cwt:abs:0003 | CWT | absorption | 4607.200 | — | yes | — |
| cwt:abs:0004 | CWT | absorption | 4625.600 | — | yes | — |
| cwt:abs:0005 | CWT | absorption | 4748.800 | — | yes | — |
| cwt:abs:0006 | CWT | absorption | 4868.000 | — | yes | — |
| cwt:abs:0007 | CWT | absorption | 5075.200 | — | yes | — |
| cwt:abs:0008 | CWT | absorption | 5333.600 | — | yes | — |
| cwt:abs:0009 | CWT | absorption | 5439.200 | — | yes | — |
| cwt:abs:0010 | CWT | absorption | 6010.400 | — | yes | — |
| cwt:abs:0011 | CWT | absorption | 6031.200 | — | yes | — |
| cwt:abs:0012 | CWT | absorption | 6084.800 | — | yes | — |
| cwt:abs:0013 | CWT | absorption | 6132.000 | — | yes | — |
| cwt:abs:0014 | CWT | absorption | 6149.600 | — | yes | — |
| cwt:abs:0015 | CWT | absorption | 6191.200 | — | yes | — |
| cwt:abs:0016 | CWT | absorption | 6216.000 | — | yes | — |
| cwt:abs:0017 | CWT | absorption | 7740.800 | — | yes | — |
| cwt:abs:0018 | CWT | absorption | 7790.400 | — | yes | — |
| cwt:abs:0019 | CWT | absorption | 7811.200 | — | yes | — |
| cwt:abs:0020 | CWT | absorption | 7850.400 | — | yes | — |
| cwt:abs:0021 | CWT | absorption | 8120.000 | — | yes | — |
| cwt:abs:0022 | CWT | absorption | 8306.400 | — | yes | — |
| cwt:abs:0023 | CWT | absorption | 8326.400 | — | yes | — |
| cwt:abs:0024 | CWT | absorption | 8350.400 | — | yes | — |
| cwt:abs:0025 | CWT | absorption | 8829.600 | — | yes | — |
| cwt:abs:0026 | CWT | absorption | 9006.400 | — | yes | — |
| cwt:abs:0027 | CWT | absorption | 9315.200 | — | yes | — |
| cwt:abs:0028 | CWT | absorption | 9327.200 | — | yes | — |
| cwt:abs:0029 | CWT | absorption | 9376.800 | — | yes | — |
| cwt:abs:0030 | CWT | absorption | 9441.600 | — | yes | — |
| cwt:abs:0031 | CWT | absorption | 9793.600 | — | yes | — |
| fit:H6:0000 | fit_peak | emission | 4507.146 | C IV | yes | — |
| fit:H6:0001 | fit_peak | emission | 4805.927 | He II | yes | — |
| fit:H6:0002 | fit_peak | emission | 5503.927 | C III] | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H6/pre_analysis/branches/main/3477d7d134a449bab694da82c3be7888/lines.csv",
      "lines": [
        {
          "line_id": "line:civ-1549",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_zero_amplitude",
            "fit_offset"
          ],
          "comment": "No CWT peak near 4496 A; nearest peaks 4242/4617 A are far off. Targeted fit at 4507.1 A has zero amplitude and no SNR, so not adoptable."
        },
        {
          "line_id": "line:heii-1640",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_zero_amplitude",
            "fit_offset"
          ],
          "comment": "No CWT peak near 4762 A (nearest 4791 A is 30 A off). Targeted fit at 4805.9 A has zero amplitude and absurd 21621 km/s width; not credible."
        },
        {
          "line_id": "line:ciii-1909",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_zero_amplitude",
            "fit_offset"
          ],
          "comment": "No CWT peak near 5541 A. Targeted fit at 5503.9 A has zero amplitude and 6203 km/s width; not adoptable."
        },
        {
          "line_id": "line:mgii-2800",
          "measurement_id": "cwt:em:0012",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_peak",
            "offset_ok",
            "strong_snr"
          ],
          "comment": "CWT peak at 8127.2 A (z=1.9026) matches predicted 8127.7 A within 0.5 A; SNR 22.7, ridge 22, FWHM 755 km/s. Red-edge caveat but credible."
        },
        {
          "line_id": "line:mgii-2800-abs",
          "measurement_id": "cwt:abs:0021",
          "status": "MARGINAL",
          "reason_codes": [
            "cwt_trough",
            "offset_weak",
            "blend_with_emission",
            "low_snr"
          ],
          "comment": "Trough at 8120.0 A (z=1.9000) is 7.7 A blueward of predicted; SNR 9.5, ridge 5. Sits in the wing of the strong Mg II emission peak at 8127.2 A, so blend ambiguity; weak but plausible absorption component."
        }
      ]
    },
    "id": "call_00_1XQvfTO1PAuB6KtJXaC30328",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 5517,
  "output_tokens": 670,
  "total_tokens": 6187,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 4877,
  "provider_usage": {
    "completion_tokens": 670,
    "prompt_tokens": 5517,
    "total_tokens": 6187,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 4877
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_1XQvfTO1PAuB6KtJXaC30328`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H6/pre_analysis/branches/main/3477d7d134a449bab694da82c3be7888/lines.csv", "n_lines": 5, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H6/pre_analysis/branches/main/3477d7d134a449bab694da82c3be7888/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 2
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:40:08.760547+00:00
