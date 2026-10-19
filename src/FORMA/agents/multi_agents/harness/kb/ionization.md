# Ionization & Velocity Rules

> **Authority note**: executable numeric thresholds in this file are owned by
> the ontology registry (`kb/ontology_lines.generated.md` /
> `kb/ontology_rules.generated.md` via `grep_kb`); the numbers below render
> them for prompt readability and are not a second authoritative source.
## Related Knowledge

- Classification diagnostics (what to DO with ionization violations, fatal problems per class): see `kb/classification.md`
- Line rest wavelengths and doublet spacings: see `kb/lines.md`

## Systemic Redshift Anchoring Priority

Prefer a credible LIKELY line with the best available anchor priority. The ordinal priority is owned by the registry line records (`anchor_priority`); it balances ionization with known line-profile biases. It is a tiebreaker among credible lines, not a substitute for signal quality:

| Priority | Lines | Ionization | Notes |
|----------|-------|------------|-------|
| 1 | Ca K/H_abs, G-band_abs, Mg I_abs, Na D_abs, Na D1_abs/Na D2_abs | Neutral | Prefer the blended Na D label when unresolved; use resolved components only when independently credible, without counting both representations |
| 2 | [O II] 3727 | O⁺ (~13.6 eV) | Best emission anchor for ELG |
| 3 | [S II]a/b 6718/6733 | S⁺ | |
| 4 | [N II]a/b 6550/6585 | N⁺ | |
| 5 | Hα/Hβ/Hγ/Hδ/Hε | H (~13.6 eV) | |
| 6 | Mg II 2800 | Mg⁺ (~15.0 eV) | May show outflow blueshift |
| 7 | [O III]a/b 4960/5008 | O⁺⁺ (~35.1 eV) | Last in the core optical ranking; check velocity offsets |
| 8 | C III] 1909 | C⁺⁺ (~47.9 eV) | UV fallback; inspect blends before adopting the centre |
| 9 | He II 1640 | He⁺ (~54.4 eV) | UV fallback; line profile and outflow may bias the centre |
| 10 | C IV 1549 | C⁺⁺⁺ (~64.5 eV) | UV fallback; broad-line blueshift may bias the centre |
| 11 | [Ne V] 3426 | Ne⁺⁺⁺⁺ (~97.1 eV) | UV fallback; check kinematics and other lines |
| 12 | Lyα 1216 | Resonant H I (ionization energy is not an anchor ranking) | Last resort: absorption and line transfer can shift the observed centre |

**Fallback rule:** If no credible cleaner anchor exists, a credible priority 8–12 line may supply a provisional systemic-redshift proxy. Report the line identity, measured redshift, blending/absorption or velocity-offset concern, and that no calibrated systemic correction was applied. If only Lyα is credible, its redshift is especially uncertain. If no line is credible, abstain rather than manufacture an anchor.

**Perceptual guidance**: Prioritize visual signal clarity over strict priority ordering. A visually dominant, unmistakable [O II] at Priority 2 is a better anchor than a marginal, barely-visible Ca K/H at Priority 1. Do not choose a weak or blended low-priority-number line merely because of its rank.

## Ionization Consistency Rule

Higher-ionization lines of a given element imply the presence of lower-ionization lines of the same element. If a line requiring a higher ionization state is detected, the lower-ionization lines of that element MUST also be present (unless masked or at the spectrum edge).

The most important case for ELG classification:

| If detected | Then MUST also detect | Why |
|-------------|----------------------|-----|
| [O III] 4960/5008 (O⁺⁺, 35.1 eV) | [O II] 3727 (O⁺, 13.6 eV) | O⁺⁺ requires passing through O⁺ — an ionizing source strong enough to produce [O III] MUST produce abundant [O II] |

**[O III] without [O II] in clean, unmasked spectral regions is a physical contradiction.** Either:
- The [O III] identification is wrong (wrong z, wrong line ID, or OH skylines mimicking the doublet spacing), or
- [O II] is hiding in a masked/low-SNR region (check before rejecting).

Do not generalize the specific [O III]/[O II] diagnostic into a universal line-detection requirement. A high-ionization line does not imply that lower-ionization lines of the same element must be observable in this wavelength coverage and noise level. For C IV or [Ne V], look for useful corroboration when available, but do not reject a credible high-ionization identification solely because C III], [Ne IV], or other lower-ionization lines were not detected.

## Outflow Blueshift Rule

Executable window owned by `rule:formal-outflow-blueshift`.

High-ionization lines may be blueshifted relative to low-ionization lines. Use the configured reference interval as a diagnostic guide; an offset outside it warrants checking the line identifications, not automatic rejection.
Velocity offset: Δv = (z_high − z_low) / (1 + z_low) × c. Negative Δv = blueshift.
If a high-ionization line gives a LOWER z than a low-ionization line, suspect misidentification (not outflow reversal).

## Width Mismatch Policy

Executable form owned by `rule:formal-width-class-match` (flag, never a sole
veto).

- A `narrow` feature matching a `broad` line (Lyα, C IV, C III], Mg II) → flag, do not use for systemic z
- A `broad` feature matching a `narrow` line ([O II], [O III], [N II], [S II]) → flag, suspect spurious CWT feature
- An `intermediate` feature (between the two declared boundaries) is a grey zone: consistent with a `narrow`-class claim and not enough for a `broad`-class claim. It is neither a clean match nor by itself a conflict — do not flag on the band alone, and do not report it as a width match. The band names and the two boundaries are declared once in `core/reasoning/ontology/feature_width.py`, which renders this width legend in the FeatureAuditor prompt.
- Balmer lines (Hα–Hδ) and He II are `both` class → width checks do not apply
- Flag mismatches but do not veto an entire hypothesis on one width mismatch alone
- Use your visual judgment: a feature that **looks** broad (spanning tens of pixels, smooth wings) carries more weight than the exact FWHM value
