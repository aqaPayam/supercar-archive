# Compact performance and distinctive coupes: batch 36

Reviewed 2026-10-29 against 672 records. Nine additions bring the working
catalogue to 681: 286 additions across 36 curated batches since the preserved
395-record baseline. The goal remains 1,000 qualifying icons; the baseline's
full eligibility and semantic-identity audit is still outstanding.

| Selected road reference | Admission basis |
| --- | --- |
| Original Fiat-Abarth 595, 1963 programme | Foundational small-car engine development and enduring Abarth identity |
| Modern Abarth 500, 2008 European reference | Revival of the compact Scorpion performance formula |
| Mazda Eunos Cosmo 20B-REW, original JC road family | Production three-rotor rotary and sequential turbocharging |
| Honda Civic EG6 SiR II, September 1991 Japan manual | High-revving DOHC VTEC and double-wishbone sporting hatchback |
| Alfa Romeo 147 GTA, March 2003 UK manual | Naturally aspirated V6 hot hatch with dedicated chassis/driveline development |
| Alfa Romeo GTV 916 3.0 V6 24V, March 1999 | Distinctive V6 coupe, six-speed gearbox and factory aerodynamic package |
| Fiat Coupé 20V Turbo Plus, September 1999 | Period Fiat performance flagship and coordinated Plus equipment |
| Volkswagen Golf II GTI 16V, Swedish brochure | Defining sixteen-valve development of the second-generation GTI |
| Audi RS 3 Sportback 8P, 2011 European introduction | First compact RS model with five-cylinder turbo/dual-clutch/quattro package |

## Identity

The complete inventory and alias searches covered Abarth/Fiat 595 and modern
500, Cosmo/Eunos/20B, Civic/EG6, 147/GTA, GTV/916, Coupé/175, Golf/Mk2/16V and
RS3/RS 3/8P. No selected model/generation was present. Earlier GTV6 Type 116 and
Cosmo Sport L10A do not cover their later road families. Existing Golfs represent
Mk1, Mk4, Mk5 and Mk7; existing Civics do not include the EG generation.

Classic and modern Abarths represent separate generations. The original 595
stands for the absent 500 D-based Abarth family; no additional SS/695 tune or
body is counted. The 147 GTA shares an engine with the existing 156 GTA but is
a separate named production model. A shared engine alone neither creates nor
collapses an identity. No year, wheel choice, gearbox or aerodynamic package
creates a second entry. Extra same-generation variants and dedicated racers
remain pending user boundaries.

## Evidence

Public field mappings are in [the manifest](../data/icons-road-36.json).

- Classic 595 uses the manufacturer historical engineering account. Its malformed
  speed unit is omitted; SS/695 specifications and original-build provenance
  are not inferred.
- Modern 500 uses the original hardware brief, with output separately mapped to
  the German production-market introduction. Ambiguous translated horsepower,
  conflicting power-peak rpm and the early variable-geometry claim are excluded.
- Cosmo uses the factory 2017 rotary booklet. All 23 spreads rendered; printed
  15–16/PDF9 and 31–32/PDF17 enlarged. The three-rotor description conflicts with
  the table's displacement notation, so capacity is omitted. The separate
  production history supplies chassis information. Navigation/trim is not made
  universal, and race engines are excluded.
- Civic uses the original Japan three-door specification and engine account.
  Manual/automatic, EG6/EG9 and optional-equipment columns are distinguished.
- 147 uses its original UK dossier, with native kW separately mapped to the
  international introduction. Conflicting exact-cc entries and erroneous
  all-round-caliper wording are excluded, as are later revisions/conversions.
- GTV and Fiat use their period production-model show dossiers with the selected
  version clearly identified. Adjacent Spider and Barchetta specifications are
  not borrowed. Optional equipment stays separate from standard Plus equipment.
- Golf uses the six-page V.A.G Sverige brochure. All pages rendered; camshaft
  and technical pages enlarged. Its unprinted date remains unset, while the
  manufacturer chronology separately identifies the generation. The precise
  table takes precedence over approximate cover wording.
- Audi uses the full manufacturer launch release, explicitly identified as a
  company press release by its host. Fields map to that narrative rather than
  the host's compiled table. Inaccessible brochure images are not treated as
  visually checked evidence. Later generations, optional packages and mass
  comparisons are excluded.

## Photographs and held candidates

All nine Commons images were visually reviewed and retain their original source
pages, creators, licences and unchanged downloaded-byte hashes. Captions qualify
exact year, trim, wheels, mechanical originality and conversions. The museum
Cosmo photo illustrates the JC body without claiming the exterior proves rotor
count. An earlier GTV photo represents the correct body family without certifying
the selected later gearbox/aerodynamic equipment. Fiat uses a full rear view of
a labelled Turbo Plus rather than a badge, headlamp or cabin detail. A later
enlarged-grille GTV and blurred Civic view were rejected.

Racing Puma remains research only: reviewed exterior photographs do not resolve
the outstanding original-road technical reference. A manual behind a captcha
was not accessed or treated as read. Ginetta G4 and Chevette HS also remain
uncounted. No dedicated racer, prototype or extra same-generation tune is added.

## Validation

Preview checked nine profiles against 672 records. Import preserved all previous
rows across every table; repeat application changed nothing. Integrity, foreign
keys, public export equality, nine admission facts, complete source fields/types,
technical mappings, captions/credits and source/export image hashes passed.
Every previous research-queue entry is preserved.

All 18 regression tests passed in 349.999 seconds:
`python -m unittest test_startup test_jdm_import test_supercars_import test_curated_import -v`.
This includes rebuilding all 36 curated batches, collision rejection, rollback,
startup, preservation and repeat safety. Independently, 76 read-only LF/CRLF
replays across 38 saved batches left the actual database byte-for-byte unchanged.
The new marker matches its canonical LF digest. All 286 curated identifiers are
distinct; the baseline remains 395 records with 22 existing non-road flags.
Exact normalized identity-text checks found no identical tuples, while the full
semantic audit remains outstanding. No native Linux runtime or fresh interactive
browser test is claimed.
