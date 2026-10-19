# One observed feature for independent review (template)

Decide whether the target is a coherent observed feature. The target has no
line identification in this session. Review this target only.

- Signal type: `{{emission_or_absorption}}`
- Candidate centre: `{{candidate_center_angstrom}}` Å
- Candidate measured FWHM: `{{measured_fwhm_angstrom}}` Å (`{{measured_fwhm_km_s}}` km/s)
- Window requested: `{{requested_window_angstrom}}` Å
- Actual wavelength coverage: `{{actual_window_angstrom}}` Å
- Valid-pixel and mask summary: `{{validity_summary}}`
- Local noise summary: `{{local_noise_summary}}`

## Complete local spectrum window

{{all_window_samples_with_wavelength_flux_and_usability}}

Use the supplied window to compare the target with nearby fluctuations.
Explain briefly what in the pixels supports your answer. Then call
`submit_feature_reality` with exactly `{"answer":"yes"}` or
`{"answer":"no"}`. The tool associates your answer with this session's
target; no feature identifier is needed in the tool arguments.
