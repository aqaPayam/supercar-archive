# Distinctive road sports-car engineering: batch 35

Reviewed 2026-10-29 against 665 records. Seven additions bring the working
catalogue to 672: 277 additions across 35 curated batches since the preserved
395-record baseline. This is progress toward 1,000 qualifying icons; the full
baseline eligibility and semantic-identity audit remains outstanding.

| Selected road reference | Admission basis |
| --- | --- |
| Triumph Stag, May 1970 UK launch brochure | Distinctive V8, open 2+2 grand-touring identity |
| Triumph TR8, 1980 USA non-California | Factory aluminium-V8 wedge sports-car programme |
| Jensen-Healey Mark II, four-speed brochure | Healey/Jensen lineage with Lotus sixteen-valve engineering |
| Marcos 1800, April 1965 production road assessment | Wooden-monocoque road GT construction |
| TVR Grantura Mark IIA, standard 1622-cc MGA brochure | Foundational tubular-chassis, glass-fibre TVR coupe |
| Caterham CSR 260, June 2005 road assessment | Substantial chassis and independent-suspension development of Seven |
| Panoz AIV Roadster, 1998 USA certification | Aluminium-intensive American sports-roadster programme |

## Identity review

The complete inventory was checked for Stag, TR7/TR8, Jensen-Healey/Healey II,
Marcos/1800, Grantura/Mk IIA, Caterham/CSR/Seven and Panoz/AIV aliases. Existing
Triumph TR2/TR4/TR6, GT6, Spitfire and Dolomite Sprint records do not cover the
Stag or wedge family. The existing Jensen FF and Jensen-assembled Volvo P1800
are distinct models. Existing later TVRs do not cover the Grantura.

The CSR is admitted for its substantially reworked chassis generation, not
because the Lotus Seven name changed manufacturer. No rebadged Series 3 or
additional CSR tune is counted. The TR8 represents the absent TR7/TR8 wedge
family; a different engine badge will not automatically justify a second entry.
No additional body, model year, gearbox choice or optional axle creates an extra
record. Pending variant and racer decisions remain unresolved.

## Evidence boundaries

Each technical field and admission fact maps to a source in
[the manifest](../data/icons-road-35.json). Original brochures and certification
pages were visually read, not inferred from search excerpts.

- Stag: all four original scanned pages of brochure 438/570/ENG read. Technical
  claims stay within that launch reference. The separate register history
  documents early reliability problems; inclusion does not deny them.
- TR8: all three original spreads rendered; the February 1980 technical spread
  enlarged and read. California bracketed figures, private conversions and
  competition specifications are excluded.
- Jensen-Healey: all eight brochure pages rendered; engine/specification pages
  enlarged. The host's 1974 catalogue label does not authenticate an unprinted
  issue date, so year is unset. Native brochure power has no invented test standard.
- Marcos: identified contemporary first-hand production-road assessment,
  cross-checked with its club-hosted reprint. Exact-cc inconsistency, speculative
  performance and optional tuning are omitted.
- Grantura: all 12 original brochure pages rendered; technical spread enlarged.
  Year is unset because no issue date is printed. Alternative engines and later
  suspension developments are excluded.
- CSR: the final road/development assessment supplies the selected specification.
  The earlier Lowflying announcement was inspected but its differing output,
  differential and tyre claims are not substituted.
- Panoz: all three certification pages rendered; the supplemental model sheet
  enlarged and read. Test weight is not kerb weight. Preproduction performance,
  broader first claims and introduction-date disputes are excluded. The factory
  history separately supports the admission explanation.

## Photographs and held research

All seven Commons photographs were visually reviewed. Their source pages,
creators, licences and unchanged downloaded-byte hashes are retained. Captions
distinguish representative bodies from proof of engine, gearbox, emissions
calibration, chassis originality or exact equipment. A preproduction Stag and
bonnet-open TR8 view were passed over for clearer representative road views.

Ginetta G4 remains research only: the reviewed early-road specification still
needs a suitable matching licensed photograph. The inspected later/racing views
are not used to imply that road reference. Chevette HS and other unresolved
candidates remain uncounted. No dedicated racer or prototype is added.

## Validation

Preview checked seven profiles against 665 existing records. Application preserved
every previous row across all tables; repeat import changed nothing. Integrity,
foreign keys, public export equality, seven admission facts, all source fields and
types, technical mappings, photo credits/captions and source/export image hashes
passed. Every previous research-queue entry is preserved.

All 18 regression tests passed in 344.095 seconds:
`python -m unittest test_startup test_jdm_import test_supercars_import test_curated_import -v`.
This includes rebuilding all 35 curated batches, collision rejection, rollback,
startup, preservation and repeat safety. Independently, 74 read-only LF/CRLF
replays across all 37 saved batches left the actual database byte-for-byte
unchanged. The new marker matches its canonical LF digest. All 277 curated
identifiers are distinct; the baseline remains 395 records with 22 existing
non-road flags. Exact normalized identity-text checks found no identical tuples;
the full semantic audit is still outstanding. No native Linux runtime or fresh
interactive browser test is claimed.
