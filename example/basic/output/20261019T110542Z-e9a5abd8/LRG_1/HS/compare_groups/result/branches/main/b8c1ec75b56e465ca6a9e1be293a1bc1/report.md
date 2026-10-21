# HS group comparison

Decision: provisional hs.cross/H3+H5
RA review: pending
Reason: hs.cross/H3+H5 is the only eligible group (merged, no type recheck) and has a coherent, FA-supported LRG/BGS absorption pattern: a doublet-supported Ca H/K pair (3/3 yes for both H3 and H5) plus several distinct FA signal_present absorption features (Mg I, H-beta, Na D, and the shared cwt:abs:0003). hs.merge/H1 is type_recheck_required and cannot win; its Ca H/K doublet review returned 0/3 and its only selected pairs are the shared cwt:abs:0003 (identified as H-gamma absorption) and an emission feature at cwt:em:0004, with no corroborating doublet support. The shared feature cwt:abs:0003 is a single observed signal whose line identity is contested (H-gamma-abs vs g-band-4305-abs), so it does not independently favour either group; the decisive advantage is the additional distinct, FA-confirmed Ca H/K doublet and other absorption features supporting H3+H5.

Identity competition: cwt:abs:0003 — hs.merge/H1: line:hgam-4341-abs; hs.cross/H3+H5: line:gband-4305-abs

## hs.merge/H1

Type: LRG/BGS
Members: H1
Merged anchor redshift: 0.2515625506820086
Merge status: singleton
Comparison status: type_recheck_required
Type recheck required: True
Comparison: Shares cwt:abs:0003 with hs.cross/H3+H5 under a competing line identity; the shared feature is one observed signal and does not count twice. H1 lacks the distinct Ca H/K doublet support that the rival group has.
Supports: line:hgam-4341-abs @ cwt:abs:0003, line:hgam-4341 @ cwt:em:0004
Excluded pair citations: none
Comparative advantages: cwt:abs:0003 is FA signal_present and is assigned to H-gamma absorption at a small descriptive offset (+38.09 A).; cwt:em:0004 is FA signal_present and assigned to H-gamma emission.
Comparative disadvantages: Group is type_recheck_required and therefore ineligible to win this pass.; Ca H/K doublet review returned 0/3 yes (orphan mode), and OIII, SII, NII doublet reviews also returned 0/3, giving no doublet corroboration.; The only absorption support is the shared cwt:abs:0003, which the rival group identifies as g-band-4305-abs; no distinct FA-confirmed absorption feature supports this interpretation.
Evidence limitations: The H-gamma emission/absorption pair at cwt:em:0004 and cwt:abs:0003 are not an independently confirmed doublet; the emission feature has no corroborating partner.; No uncertainty model is supplied, so the +38.09 A offset cannot be judged statistically.
Open questions: Whether cwt:abs:0003 is physically H-gamma absorption or g-band-4305 absorption cannot be settled from the dossier alone.; Whether the type recheck would retain the LRG/BGS classification is unknown.

## hs.cross/H3+H5

Type: LRG/BGS
Members: H3, H5
Merged anchor redshift: 0.2719528311477075
Merge status: cross_merge
Comparison status: merged
Type recheck required: False
Comparison: The Ca H/K doublet is the strongest distinct discriminator: it is FA pair-supported for both H3 and H5, whereas H1's Ca H/K review was 0/3. The shared cwt:abs:0003 is a single contested signal and is not counted as independent support for either side.
Supports: line:cak-3934-abs @ fit:H3:0006, line:cah-3969-abs @ fit:H3:0007, line:gband-4305-abs @ cwt:abs:0003, line:hbet-4862-abs @ cwt:abs:0005, line:mgi-5176-abs @ cwt:abs:0007, line:nad1-5891-abs @ cwt:abs:0009
Excluded pair citations: line:cak-3934-abs @ fit:H5:0006, line:cah-3969-abs @ fit:H5:0007, line:nad2-5897-abs @ cwt:abs:0009
Comparative advantages: Ca H/K doublet review is pair-supported 3/3 yes for both H3 and H5, with measured separation 42.44 A close to the expected ~44.3 A.; Multiple distinct FA signal_present absorption features (cwt:abs:0005 H-beta, cwt:abs:0007 Mg I, cwt:abs:0009 Na D) provide separate observational support beyond the shared cwt:abs:0003.; Group is merged with no type recheck required, making it eligible.
Comparative disadvantages: Na D doublet review returned 0/3 yes (measured separation 0.0 A), and OIII and NII doublet reviews also returned 0/3, so those doublets are not corroborated.; Ca K/Ca H amplitude ratio is ~0.98, whereas the advisory note expects Ca K deeper than Ca H; this is advisory only.
Evidence limitations: The Na D pair cwt:abs:0009 is assignment tbd and its doublet review was negative; it should be weighted weakly.; The shared cwt:abs:0003 identity as g-band-4305-abs is a working interpretation, not independent proof.; No uncertainty model is supplied for the small offsets.
Open questions: Whether cwt:abs:0003 is g-band-4305 absorption or H-gamma absorption remains contested.; Whether the Na D feature cwt:abs:0009 is a real doublet or a single blended line is unresolved given the 0/3 doublet vote.

Cross-merge: accepted; H3 and H5 are nearly identical redshift solutions (0.27251 vs 0.27178) that share the same coherent LRG/BGS absorption structure: both have Ca K and Ca H fit_doublet detections at essentially the same observed wavelengths (Ca K ~5004.88 Å, Ca H ~5047.32 Å), both have FA-supported Ca H/K doublets (3/3 yes), and both assign the same shared CWT features (cwt:abs:0003 G band, cwt:abs:0005 H-beta, cwt:abs:0007 Mg I, cwt:abs:0009 Na D) with small offsets. The Ca K/Ca H diagnostics are the type-diagnostic lines here and agree closely in observed position, so these are plausibly one observed structure described by two nearly degenerate hypotheses rather than independent galaxies.
