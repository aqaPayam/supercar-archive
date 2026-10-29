# European sports-coupe icons: batch 23

Reviewed 2026-10-29 against 610 existing records. Three absent production road
references bring the raw catalogue to 613. Twenty-three curated batches now add
218 cars to the 395-record baseline. The 1,000-qualifying-car goal and final
baseline eligibility audit remain outstanding.

| Selected reference | Admission basis |
| --- | --- |
| BMW 850 CSi, 1993 European manual | Motorsport-developed V12 grand tourer and European active rear-axle engineering |
| Volkswagen Corrado G60, original 1988 Germany | Karmann sports coupe, G-Lader supercharging and active rear spoiler |
| Opel Manta 400, original 1981-on road series | Rear-drive rally homologation coupe and significant competition lineage |

## Identity and duplicates

The full inventory and earlier manifests were reviewed, including E31/850,
Corrado/Type 53i, Manta/400 and Ascona aliases. BMW 6 Series E24/E63 and Z models
do not represent the E31 platform. The other 850 matches were a Volvo estate,
Koenigsegg model and an unrelated power figure. Existing Volkswagen Golf models
are different body/platform identities from the Corrado; neither a further Golf
trim nor a Scirocco rebadge is being counted. Opel's only earlier record was the
GT 1900, with no Manta or Ascona.

One road representative is counted for each model. Further E31 engine variants,
M8 prototype, Corrado VR6/16V/year/equipment changes, Manta body kits and
competition-prepared cars do not multiply the count. The Ascona 400 remains
research only: its road technical evidence is resolved, but reviewed photo
results show rally cars or replicas rather than an adequately identified road
body. The closest titled 1981 candidate was also visually inspected: it is a
liveried Goodwood rally car with roll cage, competition cabin and open bonnet.
It is recorded in the queue and is not included in the count.

## Evidence and specification boundaries

Complete source mappings and public admission reasons are in
[data/icons-road-23.json](../data/icons-road-23.json).

BMW 850 CSi uses BMW M's November 28, 2023 dedicated engineering account and
technical table, read through the web reader after local requests timed out.
The 5576-cc S70 V12, 280 kW, 550 Nm, 5300-rpm power peak and six-speed manual
are explicit; 250 km/h is electronically limited. Native kW avoids inconsistent
hp shorthand. BMW's June 3, 2014 anniversary release, page 3, was rendered/read
and confirms the 1993-model-year reference, output/torque and European active
rear-axle technology. General E31 history, 850i/Ci engine/automatic paragraphs,
optional wing, US-specific hardware, acceleration rounding and the unbuilt M8
are not imported as CSi specifications. The later BMW M article's conflicting
general E31 first-delivery date is excluded.

Corrado uses Volkswagen Classic's Type 53i model history plus the manufacturer
archive's G60 output account. Original German 1781-cc eight-valve four, G-Lader,
118 kW, front drive, 2+2 body and German spoiler deployment above 120 km/h are
explicit. Later VR6, 16V, 2.0-litre, automatic, fuel-tank/body and interior updates
are separate. No exact torque, transmission, acceleration or production total
is inferred. The North American photograph does not establish German spoiler
logic or equipment. Marketing world-first or fastest-car superlatives are not
used as admission evidence.

Manta uses Adam Opel AG Öffentlichkeitsarbeit's June 1995 technical book
Pkw-Modellprogramm 1899–1995, hosted by Historisk Opel Klub. Publisher page 2,
Manta 400 page 141 and the held Ascona B 400 page 144 were rendered/read. The
Manta road table explicitly supplies 2410 cc, 106 kW at 5200 rpm, 210 Nm,
Bosch L-Jetronic, five-speed, rear drive, steel unit body, road suspension and
disc brakes. Opel's July 30, 2025 historical release, read through the web
reader after a local 403, distinguishes the 106-kW street tune from roughly
206-kW Phase III competition output and documents the succession and rally
lineage. No rally Weber carburettors, Kevlar panels, race weight, wheel-arch kit
or disputed production/homologation date is imported. Blank fields in the
Ascona table do not inherit Manta figures. The similar powertrains do not turn
the two differently bodied homologation models into one technical table.

## Photography

All three selected images were visually reviewed. BMW uses a photographer-
identified 1995 CSi at Greenwich Concours with a North American exterior;
European rear-steering/cooling equipment is not asserted for that pictured car.
Corrado uses a G60 body photographed in Quebec, with market lights/bumper and
windscreen graphic acknowledged. Manta uses a road-bodied car photographed
at Gaydon in 2023 and identified as a 1981 2.4; its fascia, wheels, restoration,
chassis and tune are not authenticated by this exterior image. It is distinct
from the reviewed liveried rally cars and replicas.

BMW and Corrado images have public-domain declarations; the Manta uses CC BY-SA
4.0. Creator, licence, original source URLs and unchanged image bytes are saved.
A photograph establishes representative body identity, not factory originality
or exact regional mechanical specification.

## Validation

The three-car import preserved every earlier table row. Immediate reimport
added zero and left the complete snapshot unchanged. Integrity and foreign keys
pass; static export equals the public payload. All three admission facts,
complete source fields/types, attribute mappings, image credits and source/export
hashes were checked. All 25 saved batches passed 50 read-only LF/CRLF replays,
leaving the actual database byte-for-byte unchanged. The new marker matches
the canonical LF fingerprint. All 18 regression tests passed in 226.353 seconds
on the final 613-record catalogue, including rebuilding all twenty-three curated
batches from the 395-record baseline, startup preservation, duplicate rejection,
rollback, repeat safety and both legacy-marker/checkout directions. No native
Linux runtime or fresh interactive browser test is claimed. This batch remains
in draft and is not live.
