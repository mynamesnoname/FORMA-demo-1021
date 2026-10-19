# Q11 user prompt — draft for review

Prepare the QSO hypothesis analysis report from the canonical context below. The terminal graph outcome has already been decided by code. Reproduce it; do not vote, inspect new spectral windows, call fitting tools, compare other hypotheses, or change any line state or classification.

The injected JSON contains `run_id`, `branch_id`, `hypothesis_ref`, `fixed_redshift`, `preliminary_classification`, `spectrum_summary`, `terminal` (`source_node_ref`, `path_status`, `candidate_type`, `rule_id`, `rule_version`, `reason_codes`), `line_records`, `targeted_measurements`, `line_alignment`, `line_alignment_ref`, `graph_actions`, `conflicts`, `unresolved_items`, `skipped_nodes`, and `source_refs`. Each line record carries its line and measurement IDs, supplied display measurements, and separate SH/FA/cleaned/gate states; `targeted_measurements` holds lower-authority Q8 envelope proxies; `line_alignment` records report-before-write votes on shared-feature conflicts without modifying original rows or the route, and `line_alignment_ref` identifies their provenance. `source_refs` holds registered provenance. A missing value is JSON `null` or an empty list; do not infer it. The caller verifies node and artifact references and digests before injection.

```json
{{Q11_CANONICAL_CONTEXT_JSON}}
```

Write the six required Markdown sections exactly as specified in the system message. Under `### 3c. Per-Line Results`, write only `[[CANONICAL_PER_LINE_TABLE]]`; the caller inserts the authoritative table. For a Q2 Type 2 exit, report Q3–Q10 as skipped and retain any recorded broad-line or preliminary-type conflict. For a Q10 Type 1 result, report the recorded Q9 per-line gate states. Keep `Graph path status:` and `Candidate type:` identical to the canonical `terminal` fields. Return only the report Markdown.
