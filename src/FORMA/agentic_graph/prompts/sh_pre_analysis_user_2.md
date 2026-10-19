# SH pre-analysis · second user message (draft)

The CSV and report for this hypothesis were written successfully. Inject the value of the report's `Preliminary classification:` line into the current `hypothesis_pre_analysis` node. The only tool available now is `submit_preliminary_classification`. Call it with exactly one argument in this JSON shape:

```json
{"classification":"Type 1 QSO"}
```

The value may instead be exactly `"Type 2 QSO"`, `"ELG"`, or `"LRG/BGS"`. If the report line is `Preliminary classification: null`, pass JSON `null`:

```json
{"classification":null}
```

Do not include a node key, hypothesis identifier, redshift, report path, or any other field. Match the report's spelling, capitalization, and spaces exactly. Do not use aliases such as `Unknown`, `QSO`, or `Galaxy`. If the tool returns `ok: false`, use its error to correct the argument and call it again. The injection is complete only when the tool returns `ok: true`.
