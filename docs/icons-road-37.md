# Distinctive Japanese performance engineering: batch 37

Reviewed 2026-10-29 against 681 records. Seven additions bring the working
catalogue to 688: 293 additions in 37 curated road-icon batches since the
preserved 395-record baseline. The goal remains 1,000 qualifying icons;
the full baseline eligibility and semantic-identity audit remains outstanding.

| Selected road reference | Admission basis |
| --- | --- |
| Nissan Stagea Autech 260RS, January 1998 Japan brochure | RB26DETT performance estate with dedicated drivetrain, brakes and chassis |
| Nissan March Super Turbo EK10, 1990 heritage reference | Combined supercharger/turbocharger and March R road-car lineage |
| Honda Ballade Sports CR-X AS Si, August 1987 Japan manual | Foundational lightweight Honda sports-coupe generation and ZC DOHC engine |
| Suzuki Alto Works RS-R CC72V, February 1987 | Original Works kei-performance lineage, intercooled DOHC turbo and full-time 4WD |
| Honda CR-X del Sol EG2 SiR manual, 1999 archive | Distinct removable-roof two-seat VTEC sports generation |
| Toyota Celica T230 SS-II base manual, September 1999 | Final Celica generation, high-revving 2ZZ-GE VVTL-i and six-speed gearbox |
| Mazda Luce R130, original 1969 production reference | Dedicated 13A twin-rotor, front-drive Italian-styled grand tourer |

## Identity

Complete inventory and aliases checked: Stagea/260RS/WC34, March/Super Turbo/EK10,
CR-X/CRX/Ballade/AS/del Sol/EG2, Alto/Works/CC72V, Celica/ZZT231/T230,
Luce/R130. The existing CR-X is the second-generation EF8, distinct from the
first-generation coupe and third-generation removable-roof two-seater. Existing
Celicas cover earlier A20/ST165/ST185/ST205 generations and Celica XX/Supra A60;
none is the T230. The shared Skyline engine does not make the Stagea the same
named production model. These seven records stand for absent road families or
generations, not additional model years, cosmetic packages or engine tunes.
Extra same-generation variants and dedicated racers remain pending user boundaries.

## Evidence

Field-level sources are preserved in [the manifest](../data/icons-road-37.json).

- Stagea: original five-spread Autech brochure, all rendered, final technical
  spread enlarged and read. The actual footer dates the specification to January
  1998 despite the host's 1997 filename. Native power and torque are retained
  without an inferred rating standard. Conflicting museum table figures and
  tyre width are excluded. Autech's anniversary history separately supports
  the enduring following and RB26-powered estate programme.
- March: Nissan heritage reference No.433 identifies the production 1990 EK10.
  The separate 1987 Little Dynamite Cup rental racer supplies no technical fields.
  Gearbox is omitted because the selected road reference does not state it.
- First CR-X: Honda's August 1987 archived Si manual table. Native PS and kg-m
  are not silently relabelled net/gross. The rear-track typo and option-dependent
  weights are omitted. The original 1983 factory factbook separately documents
  the generation's lightweight front-drive sports-car concept.
- Alto: Suzuki's one-page digital-heritage sheet was rendered and visually read.
  It is a retrospective specification sheet, not a period brochure. RS-R 4WD
  and RS-X front-drive columns are distinguished. Later 660-cc engines,
  unspecified ventilated front brakes and fixed four-seat occupancy are excluded.
- Del Sol: Honda's 1999 archived SiR manual specification and equipment tables.
  The archive date is not asserted to be a manufacture year. The selected late
  reference lists a manual removable roof and roof holder; TransTop and optional
  ABS/TCS/LSD are not made standard. Automatic and VXi figures are excluded.
- Celica: original Toyota September 1999 release and its actual linked technical
  image, visually read. The base SS-II six-speed column is distinguished from
  the optional Super Strut package and automatic. Earlier GT-Four competition
  achievements and drivetrain are not attributed to this naturally aspirated car.
- Luce: Mazda's 2017 rotary booklet, printed 27/PDF15, first-production Japan
  appendix. The R130 block and manual-transmission line were enlarged and read.
  The original twin-chamber displacement notation is retained; JIS gross is
  attached only where printed. RX-87 prototype, later RX-4 and absolute first-FWD
  claims are excluded. The manufacturer's model history corroborates the identity.

## Photography and held research

All seven licensed Commons images were visually inspected. Original source pages,
creators, licence links and unchanged downloaded-byte hashes are preserved.
Captions identify representative body families and qualify exact year, trim,
mechanical originality, wheels and roof/transmission equipment. The first CR-X
uses a labelled E-AS Si exterior rather than the racing CRX search results;
March uses a road hatchback rather than the Little Dynamite Cup racer. The Alto
is the original angular RS-R displayed at Suzuki Plaza, not the later rounded body.

Familia GT-R, Pajero Evolution, eighth-generation Galant VR-4 and City Turbo II
remain research only. FIA competition annexes, wrong-trim GDI brochure spreads,
and road/race reference differences require further checks before admission.
Racing Puma, Ginetta G4 and Chevette HS remain uncounted from earlier research.

## Validation

Preview accepted seven profiles against 681 existing records. Import preserved
all previous rows in every table, and repeat application changed nothing.
Integrity, foreign keys, public export equality, seven admission facts, all source
fields/types, technical mappings, photo credits and source/export image hashes
were checked. Every previous candidate-queue entry remains preserved.

All 18 regression tests passed in 363.682 seconds:
`python -m unittest test_startup test_jdm_import test_supercars_import test_curated_import -v`.
This includes reconstructing all 37 curated batches, collision rejection,
rollback, repeat safety, startup preservation and import portability.

Separately, 78 read-only LF/CRLF replays across all 39 saved batches left the
actual database byte-for-byte unchanged. The new marker matches the canonical
LF digest. The catalogue contains 293 unique curated identifiers plus the 395
preserved baseline records; no exact normalized identity-text collision was
found. This is not a completed semantic or baseline-eligibility audit.
No native Linux runtime or fresh interactive browser test is claimed.
