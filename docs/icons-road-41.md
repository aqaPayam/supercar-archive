# Independent supercars and the original electric Roadster: batch 41

Reviewed 2026-10-29 against 705 records. Four additions bring the working
catalogue to 709: 314 additions in 41 curated road-icon batches since the
preserved 395-record baseline. The goal remains 1,000 qualifying icons;
the full baseline eligibility and semantic-identity audit remains outstanding.

| Selected road reference | Admission basis |
| --- | --- |
| Vector W8, 1991 factory sales/specification sheet | Distinctive American aerospace-influenced semi-monocoque/composite supercar programme |
| Bristol Fighter, original 2004–2011 manual road programme | Bespoke V10 supercar focused on aerodynamic efficiency, compact packaging and access |
| Isdera Imperator 108i, Series 2 AMG interview-page reference | Substantially re-engineered production evolution of Schulz's CW311 concept |
| Tesla Roadster, 2008 owner manual revised January 2009 | Foundational Tesla production sports-car programme and high-performance electric identity |

## Identity and evidence

The complete 705-car inventory was reviewed using Vector/W8, Bristol/Fighter,
Isdera/Imperator/108i/CW311 and Tesla/Roadster identities and aliases. These
four road families were absent. Existing AC Ace Bristol is a different
manufacturer/model, and other marques' Roadsters are unrelated. One reference
represents each family; no optional output grades, model years, prototypes,
new final-series builds or cosmetic editions are counted. Same-generation
variant counting and dedicated racing/prototype scope remain pending user
boundaries. All four additions fit the confirmed performance-icon scope.

The [manifest](../data/icons-road-41.json) maps attributes, facts and media to
their evidence. The source types distinguish original manufacturer documents
from original interviews and publisher-supplied technical companions.

- Vector uses both actual sides of its original 1991 sales/specification sheet,
  visually read from the public hosted scans. The sheet explicitly says W8 is
  in production. It documents the construction, twin Garrett induction,
  injection, de Dion rear layout, brakes, tyres and Gleason-Torsen differential.
  Development-car test values, unspecified-rating 600-plus horsepower, build
  totals, speed claims and the airbag claim are omitted. A separate 1992
  brochure was found but supplies no imported fields. W2/WX3 prototypes and
  the later M12 are excluded.
- Bristol uses evo's first-hand Toby Silverton interview and account of the
  original programme. Original 2004 deliveries and engineering are separated
  from the 2026 final-series discussion. The selected naturally aspirated
  manual reference does not inherit Fighter S or projected Fighter T values.
  The interview says no T was built; it is not added as a delivered road car.
  Inconsistent mass/output-rpm figures, ram-pressure gains and build totals
  are omitted. Current-company historical transcriptions are research context,
  not substituted for the interview's original-programme evidence.
- Isdera uses Motorikonen's original Schulz interview page. Its technical
  companion explicitly selects Series 2 AMG, M119 V8, 6.0-litre class and ZF
  five-speed, with tubular frame, glassfibre panels and gullwing doors. The
  table gives no build year, so both year fields remain unset. The stated
  1984 family origin is not assigned to the later AMG reference. The website
  already displays an unknown year cleanly. CW311's M100, early-series engine
  data, current-brand malformed numeric tiles, performance and build totals
  are excluded. This is one family entry, not an extra count for each series.
- Tesla uses the actual factory manual with a 2008 Roadster cover and
  27 January 2009 revision-AB imprint. The cover, owner introduction, tyre
  table and subsystem pages 11-17–19 were rendered and visually read. The
  selected configuration is explicitly single-speed; it is not presented as
  the configuration of every early delivery. Conflicting or differently based
  power/torque ratings and ratio stages are omitted. Motor, battery chemistry
  and cell count, steering, suspension, brakes and tyres come from the manual.
  A separately mapped Tesla filing establishes early-2008 introduction and
  distinguishes July 2009 Roadster 2/Sport and July 2010 2.5. Those versions
  and the future new Roadster provide no technical data for this record.

## Images and held research

Four Commons images were visually inspected, with source pages, creators,
licence links and unchanged downloaded-byte hashes retained. Captions qualify
build date, market, gearbox, engine specification, retrofit status and current
condition. The Imperator image illustrates later production-body treatment
without claiming that a photograph authenticates an AMG engine. The Tesla
photographer identifies a 2008 UK registration at a 2009 Dutch show; that does
not authenticate the exact owner-manual powertrain or early retrofit status.
Aircraft search results for Bristol Fighter were excluded. Unclear display
identities and early-body Imperator images were not selected for the late
technical reference.

Venturi 400 GT remains research only. Original brochure previews were located
and viewed on a public literature listing, but its small cover/inside images
do not expose enough readable technical detail. Listings, compiled spec tables
and Trophy racing hardware do not replace a readable road-model document.
Other hosts returned access errors and were not bypassed. No purchase or
contact with a seller was made. Eighth-generation Galant VR-4, Racing Puma,
Ginetta G4 and Chevette HS remain earlier research candidates.

## Validation

All pre-batch database rows and candidate-queue entries were preserved, including
an independent comparison with saved snapshots. Repeat import changed nothing.
Integrity, foreign keys, complete source fields/types, attribute/fact mappings,
media credits and hashes, and website-export equality passed.

All 18 regression tests passed in 403.361 seconds:
`python -m unittest test_startup test_jdm_import test_supercars_import test_curated_import -v`.
Coverage includes reconstruction of all 41 curated batches, collision rejection,
rollback, repeat safety, startup preservation and import portability.
Separately, 86 read-only LF/CRLF replays across all 43 saved batches left the
actual catalogue database byte-for-byte unchanged. The new marker matches the
canonical LF digest. There are 314 distinct curated identifiers and 395 preserved
baseline records; no exact normalized identity-text collision was found.
These checks do not complete the baseline eligibility or semantic-identity audit.
No new interactive-browser or native-Linux run is claimed.

A subsequent [baseline F50 credit correction](baseline-media-credits-01.md)
is tracked separately: three older photographs receive verified attribution
and source notes without changing car records or the catalogue count.
