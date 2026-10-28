# British road icons: batch 04

Reviewed 2026-10-28 against 417 records. Fourteen additions bring the raw
catalogue count to 431. The goal remains 1,000 qualifying records; the
baseline still needs its final eligibility audit.

| Record | Admission basis |
| --- | --- |
| Jaguar E-type Series 1 3.8 OTS | Racing-derived structure and enduring design/cultural significance |
| Jaguar XK120 OTS | Production introduction of the twin-cam XK sports-car lineage |
| Aston Martin DB4 | New Marek-engine/Touring Superleggera grand-touring architecture |
| Aston Martin DB5 | Developed straight-six GT and exceptional cultural legacy |
| Original Aston Martin V8 Vantage | Engine breathing and aerodynamic development of the classic flagship |
| Lotus Elan S1 | Backbone chassis, composite body and independent suspension |
| Lotus Europa Special | Lightweight mid-engined road-car architecture with Big Valve development |
| Lotus Seven S1 | Foundational minimal roadster formula, continuing through Caterham |
| Lotus Elise S1 | Bonded extruded-aluminium chassis construction |
| Lotus Exige S1 | Sport Elise racing programme translated into a road coupe |
| Lotus Esprit S1 | Influential Giugiaro wedge and Lotus mid-engined powertrain |
| Austin-Healey 3000 Mk III | Developed six-cylinder Big Healey and competition heritage |
| Triumph TR6 UK PI | Traditional six-cylinder roadster, injection and Karmann styling |
| Lotus Elite Type 14 | Load-bearing fibreglass monocoque construction |

The Seven and Elite qualify through engineering influence, not power or
rarity. Existing modern Vantage, Elise Cup 250, V6 Exige and Esprit V8
records were checked explicitly. These additions represent their missing
original generations. No extra reference years, paint editions, second
body styles or competing engine choices within the selected generation
are imported. DB4 and DB5 are distinct factory models, with one standard
coupe reference for each.

## Evidence and specification boundaries

Every attribute has an individual source reference in
`data/icons-road-04.json`. Primary evidence comes from Lotus and Aston
Martin model histories, the Jaguar Daimler Heritage Trust, the British
Motor Museum and the Ural Ataman museum's own collection record.

- Jaguar: use general production descriptions, not press-car modifications
  or a certification of the restored individual examples. XK120 is the
  standard steel-bodied OTS; early aluminium, SE and competition tuning
  are excluded. E-type is a road 3.8, not a lightweight racer or 2+2.
- Aston Martin: standard manual DB4/DB5 coupes. DB5 Vantage Weber tuning,
  film gadgets and modern continuations are excluded. Broad retrospective
  options and unqualified weight figures are not treated as exact early
  model specifications. The V8 Vantage record excludes X-Pack, Zagato,
  Volante and cosmetic conversions; its photo is an early 1978 example.
- Elan: preserve the S1 engine-capacity range explicitly. Inconsistent
  manufacturer output descriptions and undefined weight basis are withheld.
- Europa: the five-speed Big Valve Special is the sole original-family
  reference. Earlier 105-bhp Twin-Cam and Renault-powered S1 figures are
  not transferred. JPS paint does not produce an additional record.
- Elise: use the original 118-bhp launch narrative, not the heritage page's
  broad multi-variant/multi-year power and weight ranges. Exige uses the
  standard 177-bhp road engine, not the 190-bhp track pack. The heritage
  page's single-centre-seat sentence is excluded from the road specification.
- Esprit: original naturally aspirated 907 engine, not a submarine prop,
  Turbo or later Stevens/V8 specification. Elite is a base Type 14 road
  coupe, not a racing or Super 95 tune. Seven is the original Ford 100E
  S1, not a later Caterham or engine conversion.
- Healey: the museum's BJ8 Mk III Phase II reference; no works rally power
  or shipping-to-kerb-weight substitution.
- TR6: 1974 UK injection, not an early 150-bhp PI or a US carburetted car.
  The museum describes a car rebuilt with a Heritage shell in 1992. Its
  record supports period model specifications, not an untouched survivor.
  Inconsistent paired speed-unit rounding and optional equipment are withheld.

Historical advertised power remains qualified. Elise and Exige kW values
are calculated from manufacturer bhp using 0.745699872 kW/bhp, with that
derivation retained in their source notes. No undefined mass is presented
as kerb weight.

## Photographs and held candidates

All selected photos were visually inspected and retain creators, original
Commons pages, licences and byte digests. They represent the intended
generation/body; captions do not certify installed engines or factory
identity. Different pictured years and visible event/accessory equipment
are not silently treated as exact factory specification.

Rejected photo candidates included an E-type interior, several competition
Elites and a V8 labelled by its photographer as a cosmetic Vantage. The
chosen Elite has road bodywork without competition numbers. A Cobra is
held for further road-specification/photo research: the sources reviewed
included competition cars and a museum car with replacement engines.
It does not count as an addition.

## Validation

All 15 regression tests passed, including replay of every curated manifest
for collisions, repeat safety and baseline preservation. Every pre-existing
row was preserved; integrity, foreign keys and repeated startup passed on
the 431-car database. All 14 public admission facts, attribute evidence,
28 source/export image hashes and exact local/static payload parity passed.
The new cars inherit no technical attributes from later-generation records.
Browser automation remains unavailable; no new interactive browser test
is claimed.
