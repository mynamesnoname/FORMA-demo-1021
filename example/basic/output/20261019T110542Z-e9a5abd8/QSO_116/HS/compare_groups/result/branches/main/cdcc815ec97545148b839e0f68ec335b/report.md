# HS group comparison

Decision: provisional hs.merge/H5
RA review: pending
Reason: H5 and H6 both identify the same observed CWT feature cwt:em:0000, but as different lines (Lyα at z=2.92 vs Mg II at z=0.708). H5 has a second, distinct FA-confirmed broad feature (cwt:em:0002, C IV, signal_present 2/3) with a very small positional residual (+0.39 Å), giving it an additional independent observational support that H6 lacks. H6's Mg II assignment has a larger descriptive offset (-14.17 Å) and only a MARGINAL SH status, and its Ca H/K doublet review returned pair-supported=no (0/3). H5's Lyα forest review returned not_seen, which is a limitation rather than a rejection. On balance H5's pattern (two broad, FA-confirmed features at consistent positions) is the more credible provisional interpretation.

Identity competition: cwt:em:0000 — hs.merge/H5: line:lya-1216; hs.merge/H6: line:mgii-2800

## hs.merge/H5

Type: Type 1 QSO
Members: H5
Merged anchor redshift: 2.9196962422694117
Merge status: singleton
Comparison status: merged
Type recheck required: False
Comparison: H5 and H6 share the exact observed feature cwt:em:0000 but assign it to different lines at very different redshifts. H5 additionally uses cwt:em:0002 (C IV), a distinct FA-confirmed feature not claimed by H6, which is the main discriminator in H5's favour.
Supports: line:lya-1216 @ cwt:em:0000, line:civ-1549 @ cwt:em:0002
Excluded pair citations: none
Comparative advantages: Two distinct FA-confirmed broad features: cwt:em:0000 (Lyα, signal_present 3/3 assured) and cwt:em:0002 (C IV, signal_present 2/3 contested) with FWHM ~2497 and ~3473 km/s, both above the strict broad threshold.; C IV positional residual is very small (+0.39 Å) and the Q10 formal gate recorded type1_supported with both lines paired and usable coverage.; The second feature cwt:em:0002 is not used by H6, so it provides additional support unique to this interpretation.
Comparative disadvantages: C IV FA vote is contested (2 yes / 1 no), so its signal presence is less secure than Lyα's.; C III] measurement was rejected (signal_absent 0/3), though this does not prove absence.
Evidence limitations: Lyα forest advisory review returned not_seen (0/3 yes) over an assessable blueward window, so positive Lyα-forest corroboration was not obtained.; The Lyα identification of cwt:em:0000 competes directly with H6's Mg II identification of the same feature; positional agreement alone does not establish line identity.; No uncertainty model is supplied, so the +2.94 Å Lyα residual cannot be given a calibrated significance.
Open questions: Whether cwt:em:0000 is genuinely Lyα (H5) or Mg II (H6) cannot be settled from position alone; the Lyα forest not_seen result leaves no positive blueward corroboration.; The contested C IV vote (2/3) leaves the second supporting feature somewhat less secure.

## hs.merge/H6

Type: Type 1 QSO
Members: H6
Merged anchor redshift: 0.7079175775287458
Merge status: singleton
Comparison status: merged
Type recheck required: False
Comparison: H6 rests entirely on the shared feature cwt:em:0000 reinterpreted as Mg II. It lacks the distinct second FA-confirmed feature that supports H5, and its doublet advisory review was negative (pair supported = no).
Supports: line:mgii-2800 @ cwt:em:0000
Excluded pair citations: none
Comparative advantages: cwt:em:0000 is FA signal_present with an assured 3/3 vote and broad FWHM (~2497 km/s), and Mg II coverage is usable.; The formal Type 1 gate recorded type1_supported on the paired Mg II line.
Comparative disadvantages: Only one selected feature supports this interpretation; it is the same observed feature contested by H5.; The Mg II positional residual is larger (-14.17 Å) and the SH status is MARGINAL rather than a clean detection label.; The Ca H/K doublet advisory review returned pair supported = no (0/3 yes), and all other candidate lines (Ca H, Hε, Hδ, G-band, Hβ, Mg I) were FA signal_absent (0/3).
Evidence limitations: Lyα, C IV, and C III] fall outside the reported wavelength range on this path, so the features H5 uses were not evaluated here; this is missing coverage, not evidence against H6.; No Q8 targeted measurements were supplied, so no envelope proxies or strength votes are available.; No uncertainty model is supplied for the -14.17 Å offset.
Open questions: Whether the single broad feature cwt:em:0000 is Mg II rather than Lyα remains open; H6 has no second independent FA-confirmed feature to corroborate the redshift.; The absence of coverage for Lyα/C IV on this path means H6 cannot be positively excluded, only left less supported.
