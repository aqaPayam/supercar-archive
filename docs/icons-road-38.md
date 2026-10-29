# Homologation and active-chassis road icons: batch 38

Reviewed 2026-10-29 against 688 records. Six additions bring the working
catalogue to 694: 299 additions in 38 curated road-icon batches since the
preserved 395-record baseline. The goal remains 1,000 qualifying icons;
the complete baseline eligibility and semantic-identity audit is outstanding.

| Selected road reference | Admission basis |
| --- | --- |
| Honda City Turbo II, October 1983 Japan manual | Intercooled turbo hot hatch and enduring Bulldog performance identity |
| Mitsubishi Pajero Evolution, original Japan five-speed automatic | Dedicated homologation-era MIVEC V6, strengthened chassis and independent suspension |
| Mazda Familia GT-R, original Japan road family / 1993 base homologation | Turbocharged four-wheel-drive rally-homologation hatchback engineering |
| Fiat Uno Turbo i.e., original first-series 1985 programme | Defining Italian hot hatch, intercooled turbo/electronic injection and lasting cultural significance |
| Peugeot 405 T16, 1993 French road brochure | Variable-geometry turbo, permanent AWD, viscous centre coupling and Torsen rear differential |
| Citroën Xantia Activa V6, 1999 French technical reference | Production hydraulic active roll control supplementing Hydractive suspension |

## Identity

Full 688-record identity inventory checked with City/Turbo II/AA,
Pajero/Evolution, Familia/323/GT-R/BG8, Uno/Turbo/146, 405/T16 and Xantia/Activa
aliases. No selected family was present. False substring hits for Eunos and
MC20 Nettuno are unrelated to the Uno. The Familia does not become an Astina
or 323F through an erroneous English historical translation: the original
manufacturer/JAF form identifies Familia GT-R 4WD BG8.

These are dedicated performance-road references, not ordinary City, Pajero,
Familia, Uno, 405 or Xantia records. The 405 road saloon is distinct from the
silhouette competition cars; the Pajero is distinct from the Dakar prototypes.
No additional GT-Ae, Turbo I, Uno facelift/coachbuilder, Xantia Turbo CT or
same-generation gearbox variant is counted. Same-generation variant counting
and dedicated racers/prototypes remain pending the user's boundaries.

## Evidence

Field-level mappings and native units are in [the manifest](../data/icons-road-38.json).

- City uses Honda's actual October 1983 launch specification table, with the
  Bulldog cultural/design account mapped separately. Native PS and kg-m are
  not assigned an unprinted net/gross standard. Turbo I and race-car fields,
  modern EV specifications and absolute boost-pressure superlatives are excluded.
- Pajero uses the original launch brochure facsimile, catalogued September 1997
  by Book Garage. Actual printed 8–11 were enlarged and read: MIVEC 6G74,
  ECI-Multi, INVECS-II five-speed automatic, ARMIE independent suspension,
  Super Select 4WD, ventilated discs/ABS and tyres. The image URLs are separately
  mapped. The supposed back-cover technical page proved to be an exterior
  photograph, so exact cc and an unobserved original code table are not claimed.
  A first-hand factory engineer interview supplies the road programme's context.
  GDI/ordinary Pajero and prototype specifications are excluded.
- Familia uses the original Mazda/JAF base application A-5473 within the
  FIA-hosted 82-page file. PDF13–32 reviewed in context; identity, engine,
  transmission, suspension and brake PDF13,16,24–25,27–28 enlarged individually.
  The base recognition is effective January 1993, with October 1992 JAF stamp;
  January 1992 road introduction/output come separately from Mazda history.
  Actual 1839.6 cc is distinguished from the multiplied 3127.5 competition
  capacity. Competition tune/weight, optional ratios, later annexes and the
  lighter GT-Ae are excluded. The historical mistranslated body name is not used.
- Uno uses the original-marque Heritage Hub's Italian 40th-anniversary engineering
  account. The first-series 1301-cc IHI/intercooler/injection configuration is
  kept separate from 1372-cc Garrett versions. Native CV is not relabelled with
  an unprinted test standard. Optional digital instruments, later Antiskid and
  coachbuilder conversions are not made universal. No absolute first-turbo claim.
- 405 uses eight scans of the original French brochure, all rendered/reviewed;
  PDF2,6–8 enlarged. The scan order includes split/cropped spreads. The technical
  table prints distinct CEE and DIN ratings; stored DIN ch/mkg are retained
  without normalizing the differently labelled figures. Overboost is not
  represented as continuous output. Retrospective translated bhp and acceleration
  are not mixed with the original table, and competition achievements or
  hardware are not assigned to the road saloon.
- Xantia uses the original manufacturer Carnet de poche 99, a technical handbook
  rather than a sales brochure. Actual PDF5/printed3, PDF30/95, PDF50/174,
  PDF52/187 and PDF64/216 were rendered/read for V6 Activa identity, injection,
  steering, saloon brakes and V6 manual SC/CAR applicability. Only relevant
  pages are claimed reviewed, not the whole 89-page handbook. The April 1995
  BRE 0092 F system booklet's cover and printed3–4/PDF4–5 explain Hydractive
  plus dedicated SC/CAR actuators; this supplies the chassis principle, not a
  substituted 1995 16V engine. Output, tyres and performance figures absent
  from the selected tables are omitted. Ordinary Hydractive and automatic
  Exclusive/estate columns remain separate. No moose-test record is asserted.

## Photographs and held research

Six licensed Commons photos were visually inspected. Source pages, creators,
licence links and unchanged downloaded-byte hashes remain with each car.
Captions qualify exact year, market, mechanical originality, wheels, trim and
hydraulic condition. The Uno photo is a first-series 1986 car representing the
1985-introduced family. The Xantia rear view represents the family with earlier
body detailing, without certifying the selected 1999 technical reference.
The 405 T16 GR race image, ordinary 323 GLX, RX-7 search matches and an
incorrectly labelled V6 Activa Turbo image were rejected.

Eighth-generation Galant VR-4 remains research only: the downloaded general
brochure depicts VR-G/GDI hardware and does not establish the selected VR-4's
technical reference. Racing Puma, Ginetta G4 and Chevette HS also remain
uncounted. No blocked source is treated as read or accessed through a workaround.

## Validation

Preview accepted six profiles against 688 records. Import preserved every
previous row across all tables; repeated application changed nothing. An
independent comparison with the saved pre-import database and candidate queue
also passed. Integrity, foreign keys, website-payload equality, six admission
facts, all source fields/types, technical mappings, photo credits and unchanged
source/export image hashes were verified.

All 18 regression tests passed in 372.487 seconds:
`python -m unittest test_startup test_jdm_import test_supercars_import test_curated_import -v`.
Coverage includes reconstruction of all 38 curated batches, collision rejection,
rollback, repeat safety, startup preservation and import portability.

Separately, 80 read-only LF/CRLF replays across all 40 saved batches left the
actual database byte-for-byte unchanged. The new marker matches the canonical
LF digest. The catalogue has 299 distinct curated identifiers and the preserved
395-record baseline, with no exact normalized identity-text collision. This
is not a completed semantic or baseline-eligibility audit. The baseline
checkpoint separately records the source-backed 992 GT3 winged/Touring review
and the personal-history Verna's exclusion from performance-icon goal claims.
No native Linux runtime or fresh interactive browser test is claimed.
