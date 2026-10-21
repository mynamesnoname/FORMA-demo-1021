# SH pre-analysis session: line review

- Run ID: `graph-853b617a68f04c36bd82f06bdb770ac4`
- Hypothesis: `H2`
- Started (UTC): 2026-10-19T11:39:49.937795+00:00
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
Review every predicted line at the fixed Redrock redshift `0.6713696831689161`. Write the complete ID based line table to `/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H2/pre_analysis/branches/main/6a3c37c19110494595eddd41e08b7b49/lines.csv`. Do not infer a different redshift or assign an object type. Use the authoritative ID tables at the end of the context. Call `write_lines_csv` and stop after it succeeds.

## Frozen spectrum context

## Spectrum Summary

| Wavelength range | 3600.0 – 9824.0 Å |
| Median SNR | 46.6 |

Verify the redshift hypothesis z ≈ 0.6713696831689161.

Verification window: z ∈ [0.6614, 0.6814]
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
- doublet:oiii: [O III]a/[O III]b (4960.3/5008.2 Å): width_3sigma=25, separation_expected_obs=80.0586, rest_separation=47.9; amp_ratio_expected=3 (component 2 / component 1); amplitude relation: b:a ≈ 3:1
- doublet:cahk: Ca K_abs/Ca H_abs (3934.8/3969.6 Å): width_3sigma=20, separation_expected_obs=58.1637, rest_separation=34.8; amplitude relation: Ca K must be deeper than Ca H

FITS file: /mnt/linux_share/code/FORMA/example/basic/QSO_4.fits
Cleaned spectrum: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/spectrum.npz
Output CSV file: /mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H2/pre_analysis/branches/main/6a3c37c19110494595eddd41e08b7b49/lines.csv

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


## Predicted Lines at z = 0.6714

| Name | λ_rest (Å) | λ_obs (Å) | Type | Width | Nearby Features (ref@λ(z); cross-ref CWT table above for details) |
|------|-----------|----------|------|-------|----------------------------------------------------------|
| Mg II | 2800.0 | 4679.8 | em | broad | — |
| Mg II_abs | 2800.0 | 4679.8 | abs | absorption | — |
| [Ne V] | 3426.0 | 5726.1 | em | narrow | — |
| [O II] | 3727.0 | 6229.2 | em | narrow | peak@6200.0±0.8(z=0.6635) |
| Ca K_abs | 3934.8 | 6576.5 | abs | absorption | — |
| Ca H_abs | 3969.6 | 6634.7 | abs | absorption | — |
| Hε | 3970.1 | 6635.5 | em | both | — |
| Hε_abs | 3970.1 | 6635.5 | abs | absorption | — |
| Hδ | 4102.9 | 6857.5 | em | both | — |
| Hδ_abs | 4102.9 | 6857.5 | abs | absorption | — |
| G-band_abs | 4305.6 | 7196.2 | abs | absorption | — |
| Hγ | 4341.7 | 7256.6 | em | both | — |
| Hγ_abs | 4341.7 | 7256.6 | abs | absorption | — |
| Hβ | 4862.7 | 8127.4 | em | both | peak@8127.2±0.8(z=0.6713) |
| Hβ_abs | 4862.7 | 8127.4 | abs | absorption | trough@8120.0±0.8(z=0.6699) |
| [O III]a | 4960.3 | 8290.5 | em | narrow | peak@8318.4±0.8(z=0.6770), peak@8336.0±0.8(z=0.6805) |
| [O III]b | 5008.2 | 8370.6 | em | narrow | peak@8336.0±0.8(z=0.6645) |
| Mg I_abs | 5176.7 | 8652.2 | abs | absorption | — |

## Targeted Gaussian Fit Attempts

Only executed fits appear here. A fit is a measurement candidate, not line confirmation.
Failed attempts have no adoptable centre; do not repeat an attempted fit merely for more digits.

| Target | Predicted λ (Å) | Method | Centre ± error (Å) | Amplitude | FWHM (km/s) | Local SNR | Δχ²/n | Outcome / flags |
|---|---:|---|---|---:|---:|---:|---:|---|
| Ca K_abs/Ca H_abs | 6576.5/6634.7 | fit_doublet | 6599.064±1.4359/6596.07±8.8846 | -0.155816/-0.02518 | 107.0/107.0 | 1.15 | 0.007 | warning; separation fail |
| Mg II | 4679.8 | fit_peak | 4629.835±318.5465 | 1.632863 | 30496.0 | 4.11 | 12.225 | warning: center_at_bound |
| [Ne V] | 5726.1 | fit_peak | 5676.128±0.0 | 0.0 | 6250.2 | 0.0 | -0.0 | warning: center_at_bound |
| Hε | 6635.5 | fit_peak | 6635.822±1.7497 | 0.148074 | 406.3 | 1.13 | 0.022 | ok |
| Hδ | 6857.5 | fit_peak | 6872.371±1.6959 | 0.107808 | 320.9 | 0.95 | 0.012 | ok |
| Hγ | 7256.6 | fit_peak | 7276.105±0.1594 | 0.770059 | 141.7 | 7.37 | 0.351 | ok |
| Mg II_abs | 4679.8 | fit_peak | 4714.97±12.9759 | -0.655469 | 4361.6 | 1.73 | 0.388 | ok |
| Hε_abs | 6635.5 | fit_peak | 6585.506±0.0 | -0.0 | 211.6 | 0.0 | -0.0 | warning: center_at_bound |
| Hδ_abs | 6857.5 | fit_peak | 6824.664±2.3078 | -0.096959 | 485.3 | 0.88 | 0.016 | ok |
| G-band_abs | 7196.2 | fit_peak | 7192.252±2.559 | -0.050389 | 98.2 | 0.43 | 0.001 | ok |
| Hγ_abs | 7256.6 | fit_peak | 7206.586±0.0 | -0.0 | 279.7 | 0.0 | -0.0 | warning: center_at_bound |
| Mg I_abs | 8652.2 | fit_peak | 8659.514±1.7045 | -0.102774 | 127.0 | 1.29 | 0.012 | ok |

The CWT table lists all pre-detected features with their quality metrics. The Predicted Lines table references nearby features by wavelength + implied_z — cross-reference with the CWT table for FWHM, ridge, and SNR details. Evaluate and adopt features per the current system prompt criteria. The predicted-line table and ontology parameters above provide the facts needed for this hypothesis.

Evaluate every listed line before writing outputs.

Phase: evaluate all lines → write CSV → stop. No report or classification in SH line review.
## Authoritative line and measurement IDs

Use the exact IDs below in `write_lines_csv`. Wavelengths here are for review only; the tool copies full-precision values from the frozen catalog.

| Line ID | Name | Predicted λ (Å) | Kind |
|---|---|---:|---|
| line:mgii-2800 | Mg II | 4679.8 | emission |
| line:mgii-2800-abs | Mg II_abs | 4679.8 | absorption |
| line:nev-3426 | [Ne V] | 5726.1 | emission |
| line:oii-3727 | [O II] | 6229.2 | emission |
| line:cak-3934-abs | Ca K_abs | 6576.5 | absorption |
| line:cah-3969-abs | Ca H_abs | 6634.7 | absorption |
| line:heps-3970 | Hε | 6635.5 | emission |
| line:heps-3970-abs | Hε_abs | 6635.5 | absorption |
| line:hdel-4102 | Hδ | 6857.5 | emission |
| line:hdel-4102-abs | Hδ_abs | 6857.5 | absorption |
| line:gband-4305-abs | G-band_abs | 7196.2 | absorption |
| line:hgam-4341 | Hγ | 7256.6 | emission |
| line:hgam-4341-abs | Hγ_abs | 7256.6 | absorption |
| line:hbet-4862 | Hβ | 8127.4 | emission |
| line:hbet-4862-abs | Hβ_abs | 8127.4 | absorption |
| line:oiii-4960 | [O III]a | 8290.5 | emission |
| line:oiii-5008 | [O III]b | 8370.6 | emission |
| line:mgi-5176-abs | Mg I_abs | 8652.2 | absorption |

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
| fit:H2:0000 | fit_doublet | absorption | 6599.064 | Ca K_abs | yes | — |
| fit:H2:0001 | fit_doublet | absorption | 6596.070 | Ca H_abs | yes | — |
| fit:H2:0002 | fit_peak | emission | 4629.835 | Mg II | no | center_at_bound |
| fit:H2:0003 | fit_peak | emission | 5676.128 | [Ne V] | no | center_at_bound |
| fit:H2:0004 | fit_peak | emission | 6635.822 | Hε | yes | — |
| fit:H2:0005 | fit_peak | emission | 6872.371 | Hδ | yes | — |
| fit:H2:0006 | fit_peak | emission | 7276.105 | Hγ | yes | — |
| fit:H2:0007 | fit_peak | absorption | 4714.970 | Mg II_abs | yes | — |
| fit:H2:0008 | fit_peak | absorption | 6585.506 | Hε_abs | no | center_at_bound |
| fit:H2:0009 | fit_peak | absorption | 6824.664 | Hδ_abs | yes | — |
| fit:H2:0010 | fit_peak | absorption | 7192.252 | G-band_abs | yes | — |
| fit:H2:0011 | fit_peak | absorption | 7206.586 | Hγ_abs | no | center_at_bound |
| fit:H2:0012 | fit_peak | absorption | 8659.514 | Mg I_abs | yes | — |


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
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H2/pre_analysis/branches/main/6a3c37c19110494595eddd41e08b7b49/lines.csv",
      "lines": [
        {
          "line_id": "line:mgii-2800",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "fit_rejected"
          ],
          "comment": "No CWT peak near 4679.8; nearest peaks 4616.8 (z=0.649) and 4791.2 (z=0.711) are outside window. Targeted fit center_at_bound (4629.8, huge error) is unselectable."
        },
        {
          "line_id": "line:mgii-2800-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "offset_too_large",
            "weak_snr"
          ],
          "comment": "No CWT trough at 4679.8; fit:H2:0007 lands at 4715.0 (offset ~35 A, weak) with low local SNR 1.73 and very broad FWHM; not credible."
        },
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "fit_rejected"
          ],
          "comment": "No CWT peak near 5726.1; nearest 5802.4 (z=0.694) outside window. Targeted fit center_at_bound with zero amplitude, unselectable."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_too_large",
            "blend_ambiguity"
          ],
          "comment": "Only nearby peak cwt:em:0010 at 6200.0 implies z=0.6635, offset ~29 A from 6229.2 (weaker offset band); no CWT feature at predicted position, so not adopted."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "doublet_separation_fail",
            "weak_snr"
          ],
          "comment": "No CWT trough near 6576.5. Doublet fit fit:H2:0000 at 6599.1 (offset ~23 A) with separation fail and local SNR 1.15; not credible."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "doublet_separation_fail",
            "weak_snr"
          ],
          "comment": "No CWT trough near 6634.7. Doublet fit fit:H2:0001 at 6596.1 with separation fail, tiny amplitude and SNR 1.15; not credible."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "weak_snr",
            "low_delta_chi2"
          ],
          "comment": "No CWT peak at 6635.5. Fit fit:H2:0004 converged at 6635.8 but amplitude 0.15, local SNR 1.13, dchi2/n 0.022; not a credible detection."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "fit_rejected"
          ],
          "comment": "No CWT trough at 6635.5; targeted fit center_at_bound with zero amplitude, unselectable."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "weak_snr",
            "low_delta_chi2"
          ],
          "comment": "No CWT peak at 6857.5. Fit fit:H2:0005 at 6872.4 (offset ~15 A) with amplitude 0.11, SNR 0.95, dchi2/n 0.012; not credible."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "weak_snr",
            "offset_too_large"
          ],
          "comment": "No CWT trough at 6857.5. Fit fit:H2:0009 at 6824.7 (offset ~33 A) with amplitude 0.10, SNR 0.88; not credible."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "weak_snr",
            "low_delta_chi2"
          ],
          "comment": "No CWT trough at 7196.2. Fit fit:H2:0010 at 7192.3 is positionally close but amplitude 0.05, local SNR 0.43, dchi2/n 0.001; not a credible detection."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": null,
          "status": "MARGINAL",
          "reason_codes": [
            "no_cwt_feature",
            "fit_only",
            "offset_weak_band",
            "narrow_width"
          ],
          "comment": "No CWT peak at 7256.6; fit fit:H2:0006 converged at 7276.1 (offset ~20 A, weaker band) with amplitude 0.77, local SNR 7.4, FWHM 142 km/s (narrower than broad guide). Weak but plausible emission; adopted as marginal."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "fit_rejected"
          ],
          "comment": "No CWT trough at 7256.6; targeted fit center_at_bound with zero amplitude, unselectable."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "cwt:em:0012",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_match",
            "strong_snr",
            "position_match"
          ],
          "comment": "CWT peak at 8127.2 implies z=0.6713, offset ~0.2 A from prediction; strong SNR 22.7, ridge 22. Credible H-beta emission."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "blend_ambiguity",
            "offset_too_large",
            "weak_snr"
          ],
          "comment": "Only nearby trough cwt:abs:0021 at 8120.0 (z=0.6699, offset ~7 A) is weak (amp -3.5, SNR 9.5) and adjacent to the strong emission peak; likely emission-wing artifact, not adopted."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_too_large",
            "blend_ambiguity",
            "doublet_ratio_fail"
          ],
          "comment": "Predicted 8290.5; nearby peaks 8318.4 (z=0.6770, offset ~28 A) and 8336.0 (z=0.6805, offset ~46 A) are outside/edge of window and inconsistent with the [O III] doublet separation; not adopted."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_too_large",
            "blend_ambiguity",
            "doublet_ratio_fail"
          ],
          "comment": "Predicted 8370.6; only peak cwt:em:0014 at 8336.0 (z=0.6645, offset ~35 A) is weak and would break the expected 80 A doublet separation; not adopted."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "weak_snr",
            "low_delta_chi2"
          ],
          "comment": "No CWT trough at 8652.2. Fit fit:H2:0012 at 8659.5 (offset ~7 A) with amplitude 0.10, local SNR 1.29, dchi2/n 0.012; not credible."
        }
      ]
    },
    "id": "call_00_AmisOa0lPxPR2ZqvU9XK9690",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 7126,
  "output_tokens": 2092,
  "total_tokens": 9218,
  "cache_hit_tokens": 640,
  "cache_miss_tokens": 6486,
  "provider_usage": {
    "completion_tokens": 2092,
    "prompt_tokens": 7126,
    "total_tokens": 9218,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 640
    },
    "prompt_cache_hit_tokens": 640,
    "prompt_cache_miss_tokens": 6486
  }
}
```

### Event 2

#### Graph update: `tools`

### Event 2 message: tool

Tool: `write_lines_csv`; call ID: `call_00_AmisOa0lPxPR2ZqvU9XK9690`

```markdown
{"path": null, "n_lines": 0, "flags": ["invalid_id_judgments"], "rows_to_repair": [{"row": 11, "line_id": "line:hgam-4341", "reason": "kept line needs a known measurement ID"}], "message": "Nothing was written. Repair and resend every predicted line."}
```

### Event 3

#### Graph update: `model`

### Event 3 message: ai

```markdown
The Hγ line needs a selectable measurement ID. The fit:H2:0006 is selectable, so I'll use it.
```

Tool calls:

```json
[
  {
    "name": "write_lines_csv",
    "args": {
      "file_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H2/pre_analysis/branches/main/6a3c37c19110494595eddd41e08b7b49/lines.csv",
      "lines": [
        {
          "line_id": "line:mgii-2800",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "fit_rejected"
          ],
          "comment": "No CWT peak near 4679.8; nearest peaks 4616.8 (z=0.649) and 4791.2 (z=0.711) are outside window. Targeted fit center_at_bound (4629.8, huge error) is unselectable."
        },
        {
          "line_id": "line:mgii-2800-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "offset_too_large",
            "weak_snr"
          ],
          "comment": "No CWT trough at 4679.8; fit:H2:0007 lands at 4715.0 (offset ~35 A, weak) with low local SNR 1.73 and very broad FWHM; not credible."
        },
        {
          "line_id": "line:nev-3426",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "fit_rejected"
          ],
          "comment": "No CWT peak near 5726.1; nearest 5802.4 (z=0.694) outside window. Targeted fit center_at_bound with zero amplitude, unselectable."
        },
        {
          "line_id": "line:oii-3727",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_too_large",
            "blend_ambiguity"
          ],
          "comment": "Only nearby peak cwt:em:0010 at 6200.0 implies z=0.6635, offset ~29 A from 6229.2 (weaker offset band); no CWT feature at predicted position, so not adopted."
        },
        {
          "line_id": "line:cak-3934-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "doublet_separation_fail",
            "weak_snr"
          ],
          "comment": "No CWT trough near 6576.5. Doublet fit fit:H2:0000 at 6599.1 (offset ~23 A) with separation fail and local SNR 1.15; not credible."
        },
        {
          "line_id": "line:cah-3969-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "doublet_separation_fail",
            "weak_snr"
          ],
          "comment": "No CWT trough near 6634.7. Doublet fit fit:H2:0001 at 6596.1 with separation fail, tiny amplitude and SNR 1.15; not credible."
        },
        {
          "line_id": "line:heps-3970",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "weak_snr",
            "low_delta_chi2"
          ],
          "comment": "No CWT peak at 6635.5. Fit fit:H2:0004 converged at 6635.8 but amplitude 0.15, local SNR 1.13, dchi2/n 0.022; not a credible detection."
        },
        {
          "line_id": "line:heps-3970-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "fit_rejected"
          ],
          "comment": "No CWT trough at 6635.5; targeted fit center_at_bound with zero amplitude, unselectable."
        },
        {
          "line_id": "line:hdel-4102",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "weak_snr",
            "low_delta_chi2"
          ],
          "comment": "No CWT peak at 6857.5. Fit fit:H2:0005 at 6872.4 (offset ~15 A) with amplitude 0.11, SNR 0.95, dchi2/n 0.012; not credible."
        },
        {
          "line_id": "line:hdel-4102-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "weak_snr",
            "offset_too_large"
          ],
          "comment": "No CWT trough at 6857.5. Fit fit:H2:0009 at 6824.7 (offset ~33 A) with amplitude 0.10, SNR 0.88; not credible."
        },
        {
          "line_id": "line:gband-4305-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "weak_snr",
            "low_delta_chi2"
          ],
          "comment": "No CWT trough at 7196.2. Fit fit:H2:0010 at 7192.3 is positionally close but amplitude 0.05, local SNR 0.43, dchi2/n 0.001; not a credible detection."
        },
        {
          "line_id": "line:hgam-4341",
          "measurement_id": "fit:H2:0006",
          "status": "MARGINAL",
          "reason_codes": [
            "no_cwt_feature",
            "fit_only",
            "offset_weak_band",
            "narrow_width"
          ],
          "comment": "No CWT peak at 7256.6; fit fit:H2:0006 converged at 7276.1 (offset ~20 A, weaker band) with amplitude 0.77, local SNR 7.4, FWHM 142 km/s (narrower than broad guide). Weak but plausible emission; adopted as marginal."
        },
        {
          "line_id": "line:hgam-4341-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "fit_center_at_bound",
            "fit_rejected"
          ],
          "comment": "No CWT trough at 7256.6; targeted fit center_at_bound with zero amplitude, unselectable."
        },
        {
          "line_id": "line:hbet-4862",
          "measurement_id": "cwt:em:0012",
          "status": "LIKELY",
          "reason_codes": [
            "cwt_match",
            "strong_snr",
            "position_match"
          ],
          "comment": "CWT peak at 8127.2 implies z=0.6713, offset ~0.2 A from prediction; strong SNR 22.7, ridge 22. Credible H-beta emission."
        },
        {
          "line_id": "line:hbet-4862-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "blend_ambiguity",
            "offset_too_large",
            "weak_snr"
          ],
          "comment": "Only nearby trough cwt:abs:0021 at 8120.0 (z=0.6699, offset ~7 A) is weak (amp -3.5, SNR 9.5) and adjacent to the strong emission peak; likely emission-wing artifact, not adopted."
        },
        {
          "line_id": "line:oiii-4960",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_too_large",
            "blend_ambiguity",
            "doublet_ratio_fail"
          ],
          "comment": "Predicted 8290.5; nearby peaks 8318.4 (z=0.6770, offset ~28 A) and 8336.0 (z=0.6805, offset ~46 A) are outside/edge of window and inconsistent with the [O III] doublet separation; not adopted."
        },
        {
          "line_id": "line:oiii-5008",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "offset_too_large",
            "blend_ambiguity",
            "doublet_ratio_fail"
          ],
          "comment": "Predicted 8370.6; only peak cwt:em:0014 at 8336.0 (z=0.6645, offset ~35 A) is weak and would break the expected 80 A doublet separation; not adopted."
        },
        {
          "line_id": "line:mgi-5176-abs",
          "measurement_id": null,
          "status": "NOT_FOUND",
          "reason_codes": [
            "no_cwt_feature",
            "weak_snr",
            "low_delta_chi2"
          ],
          "comment": "No CWT trough at 8652.2. Fit fit:H2:0012 at 8659.5 (offset ~7 A) with amplitude 0.10, local SNR 1.29, dchi2/n 0.012; not credible."
        }
      ]
    },
    "id": "call_00_q0ImsWxognkhDKPDNYyg9228",
    "type": "tool_call"
  }
]
```

Provider usage:

```json
{
  "input_tokens": 9308,
  "output_tokens": 2106,
  "total_tokens": 11414,
  "cache_hit_tokens": 9088,
  "cache_miss_tokens": 220,
  "provider_usage": {
    "completion_tokens": 2106,
    "prompt_tokens": 9308,
    "total_tokens": 11414,
    "completion_tokens_details": null,
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 9088
    },
    "prompt_cache_hit_tokens": 9088,
    "prompt_cache_miss_tokens": 220
  }
}
```

### Event 4

#### Graph update: `tools`

### Event 4 message: tool

Tool: `write_lines_csv`; call ID: `call_00_q0ImsWxognkhDKPDNYyg9228`

```markdown
{"path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H2/pre_analysis/branches/main/6a3c37c19110494595eddd41e08b7b49/lines.csv", "n_lines": 18, "judgment_path": "/mnt/linux_share/code/FORMA/example/basic/output/20261019T110542Z-e9a5abd8/QSO_4/SH/H2/pre_analysis/branches/main/6a3c37c19110494595eddd41e08b7b49/lines_judgments.json"}
```

## Session outcome

- Status: `complete`
- Returned events: 4
- Provider reasoning field returned: no
- Ended (UTC): 2026-10-19T11:40:05.014321+00:00
