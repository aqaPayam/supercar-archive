# British and European performance landmarks: batch 33

Reviewed 2026-10-29 against 651 records. Six absent model families bring the
working catalogue to 657: 262 additions across 33 curated batches since the
preserved 395-record baseline. The goal remains 1,000 qualifying icons; baseline
eligibility and semantic uniqueness are not yet fully audited.

| Selected road reference | Admission basis |
| --- | --- |
| Triumph GT6 Mk I, 1967 Italian brochure | Compact six-cylinder fastback development and British sporting-GT identity |
| Saab Sonett V4, 1968 USA brochure | Distinctive front-drive, freewheel, V4 and fibreglass sports-car engineering |
| Matra Djet 5, museum 1108-cc reference | Early production mid-engine sports-car pioneer and Matra Sports origins |
| Lancia Montecarlo, 1980 second-series Spider | Pininfarina mid-engine design and documented competition-project lineage |
| Vauxhall Firenza HP Droopsnoot | Aerodynamic nose, developed slant-four and Vauxhall’s first five-speed gearbox |
| Opel Kadett C GT/E 1.9, February 1976 base | Fuel-injected sporting coupe and works-rally lineage |

## Identity and evidence

The complete inventory was checked for GT6/Spitfire, Sonett, Djet/Jet/Bonnet,
Montecarlo/Monte Carlo/Scorpion, Firenza/Magnum/Droopsnoot and Kadett aliases.
The selected families were absent. Existing TR, Saab 99/900, Opel GT/Manta and
Lancia Rally 037 profiles do not cover these cars. The Montecarlo’s relationship
to 037 is recorded as development history, not the same road-model identity.
René Bonnet/Matra badges, Sonett engine changes, Montecarlo/Scorpion names,
later facelifts and transmission choices do not multiply this batch.

Exact public field/source mappings and photograph provenance are in
[data/icons-road-33.json](../data/icons-road-33.json).

GT6 uses the original nine-page Italian Standard-Triumph brochure 374/867/IT.
All pages were rendered; specification PDF2 and development PDF3 read separately.
The selected Mk I has 1998 cc, pushrod valves, twin Strombergs, four synchronised
forward gears, swing-axle rear suspension and 246-mm front discs. The native
95 CV al freno rating is retained without inventing a DIN/SAE standard. Optional
overdrive, later Rotoflex and conflicting acceleration intervals are excluded.
The Sports Six Club’s model-register overview supports the development reason;
its combined Mk I/II technical table is not blended into the period reference.

Sonett uses the original ten-page 1968 USA brochure, with the contact sheet and
PDF8/10 individually read. Its 1498-cc V4, front-wheel drive, four-speed/freewheel,
dual-circuit disc/drum brakes, GRP/steel construction and separate native
73 SAE bhp at 5000 rpm / 65 DIN bhp at 4700 rpm are preserved. No conversion,
two-stroke racing engine, Sonett III or later 1.7-litre specification is imported.
Club Sonett Sweden supplies separately identified family history rather than
overriding the USA table with approximate performance or weights.

Djet uses Lane Motor Museum’s own collection table: Renault OHV 1108-cc four,
water cooling, mid-engine/rear-drive layout and four-speed manual. The museum’s
1965 heading identifies the reference, not independent VIN authentication of a
survivor. The Matra owners’ technical reference supports the steel-backbone/GRP
construction. Differing production totals and broad date ranges are omitted;
the “world’s first” superlative is conservatively expressed as an early pioneer.
Gordini Jet 6, 5S and race tunes are excluded.

Montecarlo uses the factory Heritage account, selecting the second-series
European Targa/Spider, introduced in 1980. It retains the transverse two-litre
Lampredi twin-cam/five-speed architecture, purpose-built Pininfarina unitary body
and second-series electronic ignition. The US Scorpion, earlier SE 030 prototype
and Group 5/037 competition outputs do not become road specifications or road
victories. Inconsistent production-count arithmetic is omitted.

Firenza HP uses Vauxhall’s own 8 April 2020 heritage chapter and technical table:
2279-cc slant-four, five-speed gearbox, aero nose, native 120-mph and 7.6-second
0–60-mph claims. The account dates HP creation to 1973. Its stated extra 21 bhp
does not establish an absolute output. Flat-nose Magnum homologation and the
Firenza-derived Baby Bertha racer are excluded from the road specification.

Kadett uses original Opel/ONS FIA 5624 Group 1. The first eighteen of 53 pages
were rendered, including the original base; PDF1/4/5 read individually. The
cover’s handwritten recognition date is 1 February 1976. Selected 1897-cc,
cast-iron-head, chain-driven CIH engine and Opel four-speed base are kept apart
from Group 2 ZF five-speed alternatives and later two-litre extensions. Opel’s
2023 history supplies Bosch L-Jetronic and native 77 kW/105 PS road figures.
Works-rally power/results explain lineage without becoming this road car’s tune.

## Photographs and held candidate

All six selected Commons photographs were visually reviewed and retain creator,
licence, source-page link, unchanged downloaded bytes and SHA-256 digest. Captions
identify representative road families and limits on year, market, tune and
restoration. The Montecarlo picture identifies a 1981 second-series Targa; it is
not claimed to authenticate a 1980 build. The Kadett picture shows a yellow/black
road coupe with open bonnet, rather than the rejected flared rally conversion.
The Firenza’s raised bonnet/current wheels do not prove original mechanics.

Chevette HS is held for a more precise production-road source. Its early Group 4
paperwork and subsequent engine/gearbox changes need separation from production
equipment; this batch does not count or import it. Same-generation extra variants
and dedicated racing/prototype boundaries remain pending user decisions.

## Validation

Import preview found six new profiles against 651 records. Application preserved
every existing row across all tables, added six cars and repeated with zero
changes. Database integrity and foreign keys pass; the website export equals
the generated public payload. Source fields, admission facts, technical mappings,
image captions/credits and source/export file hashes were checked.

All 18 regression tests passed in 316.247 seconds:
`python -m unittest test_startup test_jdm_import test_supercars_import test_curated_import -v`.
These include rebuilding all 33 curated batches, collision rejection, baseline
preservation, atomic rollback, startup and repeat-import safety. Independently,
70 read-only LF/CRLF replays across all 35 saved batches left the actual catalogue
database byte-for-byte unchanged. The new manifest marker matches its canonical
LF digest; all 262 curated identifiers are distinct. No native Linux runtime or
fresh interactive browser test is claimed.
