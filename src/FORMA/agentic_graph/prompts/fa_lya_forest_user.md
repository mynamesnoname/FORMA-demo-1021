# Lyα blueward structure review

- Claimed Lyα observed wavelength: `{{LYA_WAVELENGTH}}` Å
- Requested blueward region: `{{BLUE_REQUESTED}}` Å
- Requested redward reference: `{{RED_REQUESTED}}` Å
- Actual available region: `{{ACTUAL_RANGE}}` Å
- Coverage and valid-pixel summary: `{{COVERAGE_SUMMARY}}`
- Median per-pixel noise from positive IVAR: `{{NOISE_SUMMARY}}`

## Blueward samples

{{BLUE_SAMPLES}}

## Redward reference samples

{{RED_SAMPLES}}

Assess the pattern only in valid blueward pixels. The redward samples provide
local context, not an independent test of the claimed line identity. Explain
what structure is or is not visible, including any coverage limit, then call
`submit_lya_forest_vote` with only `answer` and `reason`.
