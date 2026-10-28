# Italian performance icons: batch 06

Reviewed 2026-10-28 against 453 existing records. Eight previously absent
production road models bring the raw catalogue to 461. The goal remains
1,000 qualifying cars; the baseline still needs its final eligibility audit.

| Selected record | Admission basis |
| --- | --- |
| Lamborghini 350 GT | First production Lamborghini; road-developed V12 and Superleggera body |
| Lamborghini Espada Series II | Distinctive Bertone four-seat V12 grand tourer |
| Lamborghini Urraco P250 | Foundation of Lamborghini's transverse mid-engined V8 lineage |
| Maserati 3500 GT | Foundation of Maserati's series-production grand-touring business |
| Maserati Ghibli AM115 4.7 | Giugiaro's low GT silhouette enabled by a dry-sump V8 |
| Maserati Bora 4.7 | First mid-engined Maserati production road car |
| Maserati Khamsin | Gandini/Bertone design, independent rear suspension and hydraulic steering |
| Ferrari 330 GTC | Classic Pininfarina V12/manual grand-touring coupe |

## Identity and evidence boundaries

The complete inventory was checked for model, generation and alternative
identities. Existing Ferrari records include the 330's successor-era Daytona
but no 330 GTC; existing Maseratis were MC12/MC20 derivatives. Existing
Lamborghinis include Miura and later supercars, with none of these three
earlier model families. Each addition is one road reference in a previously
absent family. No extra years, cosmetic editions or additional bodies count.

`data/icons-road-06.json` contains each public sourced admission reason,
individual attributes, source references, scope notes and photo licences.
Manufacturer history pages supply seven entries; Audrain Auto Museum's
own exhibition record supplies the 330 GTC. These are factory/museum
retrospectives, not contemporary independent performance measurements.

- The 350 GT uses production-car architecture, not 350 GTV prototype power.
  The page's broad claim about the first production DOHC engine and its
  disputed production count are excluded.
- The Espada reference is a 1971 Series II manual. The history page's
  325-CV introduction figure is not assigned to Series II; automatic,
  hydropneumatic suspension and optional equipment are not assumed.
- The Urraco is a 1974 P250 road reference, not the 1970 show prototype,
  US P111 or later DOHC P300. Lamborghini's retrospective disagrees with
  itself about production/sale start dates; no exact debut claim or total
  is imported. Its broad first-ever suspension claim is also withheld.
- The 3500 GT is the original carburetted model with four-speed manual.
  The later Lucas-injected GTI's output and five-speed update are excluded.
  The representative Touring coupe photograph does not certify its fuel system.
- Ghibli and Bora use only their 4.7-litre specification columns. The Ghibli
  is the original AM115 coupe, not a later car sharing the name. The Bora's
  hydraulic controls are not described as hydropneumatic suspension.
- Khamsin data is a general production reference, without claiming a
  separate US emissions specification. Its production total is unnecessary
  for admission and is omitted.
- Historical CV/hp figures retain the source's notation. Their gross/net
  conventions are undefined, so they are not converted into modern net kW.
  Ambiguously labelled dry/kerb weights are omitted. The 330 GTC museum's
  maximum-RPM statement is not interpreted as a power peak, and its claim
  of replacing the 500 Superfast is not repeated.

All eight photographs were visually reviewed for the intended model/body.
An initially found Urraco show-prototype photograph was rejected. An
explicitly identified 1971 Series II Espada photograph replaces generic
Espada results. Photographs remain unaltered with creators, licence links
and hashes preserved; none certifies an installed engine or original equipment.

Other researched Italian candidates remain unimported until their precise
technical references and photographs are ready. Ferrari's blocked history
pages were not bypassed. Candidates and research do not count toward the goal.

## Validation

All 15 regression tests passed, including replay of every curated batch,
duplicate rejection, repeat-import safety, rollback and startup preservation.
The actual import preserved every pre-existing table row. Database integrity
and foreign keys passed. The 461-car website export matches the local payload;
new attribute-source mappings, public admission facts, image credits and image
hashes were checked. Repeated startup also passed on the final database.
No fresh interactive browser test is claimed.
