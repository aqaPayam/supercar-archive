# Specialist supercars and electrified landmarks: batch 40

Reviewed 2026-10-29 against 701 records. Four additions bring the working
catalogue to 705: 310 additions in 40 curated road-icon batches since the
preserved 395-record baseline. The goal remains 1,000 qualifying icons;
the full baseline eligibility and semantic-identity audit remains outstanding.

| Selected road reference | Admission basis |
| --- | --- |
| Cizeta V16T, original delivered production family | Bespoke transverse sixteen-cylinder Italian supercar |
| Ascari KZ1, April 2005 road-driving reference | Purpose-built carbon structure and mid-mounted BMW V8 |
| BMW i8, original 2014 production coupe | Dedicated CFRP/aluminium plug-in-hybrid sports-car architecture |
| Porsche Taycan Turbo S, September 2019 introduction | Porsche's original electric sports-car programme, 800 V and two-speed rear drive |

## Identity and selection

The full 701-car inventory was checked for Cizeta/Moroder/V16T, Ascari/KZ1,
BMW/i8/I12 and Porsche/Taycan identities and aliases. All four families were
absent. One road reference represents each family; no extra output grades,
model years, cosmetic editions, roadsters, race versions or prototypes are counted.
Dedicated racer/prototype scope and same-generation variant counting still await
the user's boundaries. These four additions do not depend on those decisions.

Neither rarity alone nor high power alone supplies admission. The two specialist
supercars have bespoke engine/structure programmes; the electrified cars mark
substantial architectural changes in established performance marques.

## Evidence boundaries

The [manifest](../data/icons-road-40.json) maps every field and admission fact to
its source.

- Cizeta uses Ian Kuah's first-hand factory visit and Claudio Zampolli interview,
  hosted by Cizeta USA. This is attributed journalism, not an original factory
  specification sheet. It distinguishes delivered cars from the 1988 mock-up.
  Conflicting visit dates and power/torque units are not silently reconciled;
  those values, crankshaft details and build totals remain omitted. Neither US
  nor European road certification is asserted.
- Ascari uses Manek Dubash's contemporary PistonHeads drive of Klaas Zwart's
  road car around Banbury. The reported carbon structure, BMW V8, gearbox,
  tyres and brakes describe that reference. Planned production is not a verified
  build total. Unspecified mass basis and claimed acceleration/top speed are
  omitted; KZ1-R and A10 hardware are excluded.
- BMW uses its September 2013 introduction explicitly identifying the 2014
  production coupe. A separately mapped July 2014 factory report confirms
  customer deliveries. Earlier prototype estimates, changing range/battery
  figures, optional laser lighting and the 2018 update/Roadster are excluded.
- Porsche uses its actual five-page September 2019 PCNA production introduction;
  every page was rendered and visually read. The 560-kW value is explicitly
  overboost with Launch Control, and 93.4 kWh is overall battery capacity.
  EPA range was pending. Turbo, optional PDCC, facelift, Turbo GT and Cross
  Turismo data are excluded.

Vector W8, Isdera Imperator, Venturi 400 GT, Bristol Fighter and the original
Tesla Roadster remain research candidates, not imported entries. Current gaps
include development-versus-production evidence, variant-specific period documents
and the edition/date of the Roadster manual. The Bristol archive distinguishes
the original programme from new final-series cars; announced Fighter T figures
are not treated as proof of delivered production.

## Images and validation

Four Commons photographs were visually checked against the selected body
families. Original source pages, creators, licence links and unchanged downloaded
bytes are retained. Captions describe representative appearances without claiming
to authenticate exact market, build date, optional equipment or current tune.
The Cizeta photograph's Moroder naming is qualified. The i8 photograph is a
British 2014 display, while the technical reference is the US introduction.

Every pre-batch database row and candidate-queue entry was preserved, including
an independent comparison with the saved snapshots. Repeat import changed
nothing. Integrity, foreign keys, source/attribute/fact mappings, media credits
and byte hashes, and website-export equality all passed.

All 18 regression tests passed in 394.719 seconds:
`python -m unittest test_startup test_jdm_import test_supercars_import test_curated_import -v`.
Coverage includes reconstruction of all 40 curated batches, collision rejection,
repeat safety, rollback, startup preservation and import portability.
Separately, 84 read-only LF/CRLF replays across all 42 saved batches left the
actual catalogue database byte-for-byte unchanged. The new marker matches the
canonical LF digest. There are 310 distinct curated identifiers and 395 preserved
baseline records; no exact normalized identity-text collision was found.
These checks do not complete the baseline eligibility or semantic-identity
audit. No new interactive-browser or native-Linux run is claimed.
