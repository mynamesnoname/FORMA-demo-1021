# SH pre-analysis · first user message (draft)

Evaluate this Redrock hypothesis using the single-hypothesis rules. The hypothesis redshift for the report is fixed at `{{HYPOTHESIS_REDSHIFT}}`; do not derive it from spectral lines. Write the CSV to `{{CSV_PATH}}` and the report to `{{REPORT_PATH}}`.

Evaluate every predicted line, then call `write_lines_csv` with only line IDs, measurement IDs, statuses, reason codes and comments, followed by `write_report`. The authoritative ID tables appear at the end of the spectrum context. Do not copy numeric measurements into the CSV tool call. The first non-empty line under `### 3a. Spectrum Summary` must be `Hypothesis redshift: {{HYPOTHESIS_REDSHIFT}}`. The first non-empty line under `### 3e. Classification` must be `Preliminary classification: <Type 1 QSO | Type 2 QSO | ELG | LRG/BGS | null>`, replacing the angle-bracketed placeholder with exactly one allowed value. After the report tool succeeds, stop and wait for the next user message.

## Spectrum context for this hypothesis

{{SH_CONTEXT}}
