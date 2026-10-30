# Italian road and rally icons: batch 07

Reviewed 2026-10-28 against 461 existing records. Nine absent production
road model families bring the raw catalogue count to 470. The goal remains
1,000 qualifying cars, subject to the existing baseline's eligibility audit.

| Selected record | Admission basis |
| --- | --- |
| Lancia Aurelia B20 first series | Pioneering V6 grand tourer with international sporting history |
| Lancia Thema 8.32 | Ferrari-developed 32-valve V8 in a discreet performance saloon |
| Fiat Dino Coupé 2400 | Ferrari V6 collaboration and original Formula 2 engine-production programme |
| Fiat 124 Abarth Rally road car | Lightweight homologation foundation of the successful rally programme |
| Alfa Romeo 1600 Spider Duetto | Pininfarina sports-roadster design and enduring film/cultural identity |
| De Tomaso Pantera | Italian mid-engined chassis and Ford V8 supercar formula |
| De Tomaso Mangusta | Giugiaro mid-engined V8 design and backbone chassis |
| Bizzarrini 5300 GT Strada | Competition-led front-mid-engine weight distribution in a road GT |
| Iso Grifo GL | Bertone two-seat GT with Corvette 327 power |

## Duplicate review

The complete 461-car inventory was checked for family, generation and aliases.
None of these nine families existed. The 124 Abarth is distinct from the
existing 131 Abarth road homologation car. The Fiat Dino is distinct from
Ferrari's Dino 246; Mangusta, Pantera, Iso Grifo and Bizzarrini Strada are
distinct manufacturers/models despite shared engineering and American engines.
No second body, extra reference year or cosmetic edition adds to the count.

`data/icons-road-07.json` records public admission reasons, source mapping,
exact specification boundaries, photo credits and image hashes. Research
candidates do not count as imported records.

## Evidence boundaries

- Aurelia: the manufacturer's Padua 2022 reference specifically describes
  the 1951 first-series B20. Its rounded 2000-cc description is represented
  as a 2.0-litre class, without a fabricated exact displacement. The entry
  does not borrow later 2.5-litre or modified Nardi specifications. The photo
  identifies a first-series car; its repaint and coachbuilder are not certified.
- Thema: core 8.32 V8 engineering comes from Lancia's own retrospectives.
  Four valves per cylinder is derived from eight cylinders and 32 valves.
  A separate source supports the modified crankshaft. Catalyst-dependent
  output and performance, optional suspension, powered rear seats and
  cosmetic Limited Edition details are withheld.
- Dino: the January 1972 Fiat Kundendienst sheet was rendered and visually
  inspected. Page 1 explicitly covers the Coupé 2400, with 180 DIN PS at
  6800 rpm and 204 km/h. Its 180 metric PS converts to 132.39 kW. Page 2
  is headed Spider and is excluded. The manufacturer's heritage press kit
  supports Bertone design and the original engine programme's Formula 2
  purpose; this is not described as a new 2.4-litre homologation programme.
- 124 Abarth: FIA base Group 3 form 3059 was rendered and its identity and
  specification pages inspected. It identifies the production 124 CSA and
  132 AC.4 engine, starting in September 1972. Pages 4–7 supply suspension,
  brakes, engine, carburettors and explicit 128 DIN CV at 6200 rpm, converted
  to 94.14 kW. Optional/evolution sheets are excluded. The Heritage story's
  separate works Group 4 table (1995 cc, injection, 215 HP) is not imported.
  A greater-than-190-km/h claim is not turned into an exact maximum.
- Spider: the manufacturer museum supplies the original 1570-cc car's
  technical details, including its live rear axle. The 2026 Rétromobile
  manufacturer article supports the 1966 identity and The Graduate history.
  Undefined weight and the museum's unitless speed field are omitted.
- Pantera: original narrow-body production road architecture, supported
  by the manufacturer's narrative and consistent core chassis specifications.
  The current page has a wrong date heading and a fibreglass-body claim;
  both are rejected. Exact displacement, output, performance, dimensions
  and tyres that may combine versions are withheld. The original US brochure
  transcription was also read as corroboration of the steel monocoque,
  midship Ford V8, independent suspension, five-speed gearbox and disc brakes.
- Mangusta: the manufacturer's historical narrative supports Giugiaro/Ghia,
  backbone chassis, Ford V8, limited-slip differential and twin rear covers.
  Its narrative and table disagree about five/six speeds, so no transmission
  specification is imported. Fibreglass-body wording, exact 289/302 engine,
  power, mass and market-specific headlamps are withheld.
- Bizzarrini: Audrain's own 1968 Strada record supplies the road-car chassis
  and 327-cu-in V8 details. The rear De Dion axle is not called independent.
  Competition, America, modern Revival and Iso A3/C figures are excluded.
  The museum's historical power and performance conditions are undefined;
  they are not imported or converted to modern net figures.
- Grifo: the original Iso multilingual brochure was rendered and inspected.
  Only the Grifo side (PDF page 1) applies; the reverse is another model,
  the four-seat Rivolta GT. It identifies the 350-rated Corvette 327 option,
  Bertone coachwork, two seats and dimensions. Multilingual power units and
  metric/imperial performance columns disagree, so no net-kW conversion or
  exact universal maximum speed is imported. A separate Auto-Becker leaflet
  reprints a road test of the 365-rated car; those values were not mixed in.

All nine chosen photos were visually checked for the intended model/body.
A Pantera image explicitly described as performance-modified was rejected
and replaced. A 1750 Spider result was rejected in favour of the museum's
1966 1600. Creators and licences are retained, with unaltered image bytes;
photos do not certify original engines, equipment or trim.

## Validation

All 15 regression tests passed, including full curated-batch replay,
duplicate rejection, previous-row preservation, repeat safety and rollback.
The actual import preserves every earlier table row. Integrity and foreign
keys pass. The 470-car website export equals the local payload, and all nine
new admission facts, source mappings, photo credits and source/export image
hashes were verified. Startup preservation also passes on the final database.
No fresh interactive browser test is claimed.
