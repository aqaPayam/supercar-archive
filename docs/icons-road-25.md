# Japanese performance generations: batch 25

Reviewed 2026-10-29 against 617 records. Four missing road generations bring the
raw catalogue to 621. Twenty-five curated batches add 226 cars to the 395-record
baseline. The 1,000-qualifying-car goal and final baseline eligibility audit remain active.

| Selected reference | Admission basis |
| --- | --- |
| Civic Type R FK2, 2015 Europe manual | First turbo Type R chapter; Dual Axis Strut, adaptive dampers and helical LSD |
| Lancer Evolution X GSR, October 2007 Japan manual | New 4B11/platform and integrated S-AWC development |
| Impreza WRX STI GRB, October 2007 Japan hatchback | Distinct five-door chassis with double-wishbone rear suspension and DCCD |
| WRX STI VA/VAB, August 2014 Japan manual | Standalone generation with reinforced body, steering/chassis changes and torque vectoring |

## Identity and duplicates

The complete inventory was searched across identifiers, manufacturers, families,
generations and variants, including FK2, CZ4A, Evolution X, GRB/GRF/GVB and VAB
aliases. Existing Honda Type Rs cover EK9, EP3, FD2, FN2 and FK8, not FK2.
Existing Evolutions I, III, V, VI and VII do not cover the new-platform X.
Subaru previously covers GC8 22B and original GDB STi; neither GRB hatchback nor
the substantially renewed standalone VA generation was present. No extra badge,
year, cosmetic trim, gearbox, sedan derivative or special edition is counted.

## Evidence boundaries

Exact mappings and public admission reasons are in
[data/icons-road-25.json](../data/icons-road-25.json).

Honda uses its full June 1, 2015 European launch kit, including the final technical
table: 1996 cc, native 310 PS at 6500 rpm, 400 Nm, direct injection, six-speed,
helical LSD, Dual Axis Strut front, H-type torsion-beam rear and adaptive damping.
Front discs are 350 mm, rear 296 mm. No later FK8 multi-link hardware, optional
GT equipment, unsupported engine code/DOHC wording or preproduction lap record
is imported. PS is not converted into an unsourced kW value.

Evolution X uses the full factory release reproduced under the explicit
Mitsubishi Press Release heading at ZerCustoms, dated Tokyo October 1, 2007 and
credited to Mitsubishi. The editorial introduction is excluded. It documents the
GSR manual launch, 4B11 aluminium block, intake/exhaust MIVEC, 16-valve DOHC,
intercooled turbo, 422 Nm at 3500 rpm, five-speed and full-time S-AWC integrating
ACD/AYC/ASC/Sport ABS. Standard Brembo ventilated discs are separate from optional
High Performance Package/Bilstein/Eibach/BBS/two-piece discs. Brake inch classes
are not rotor diameters. No exact cc or maximum-power number is supplied in this
reviewed launch text, so those fields are omitted. Later 300-PS, FQ/Final, RS and
TC-SST figures do not fill gaps in the original manual entry.

Mitsubishi's factory FACTS & FIGURES 2008 PDF was also downloaded and extracted;
PDF pages 5 and 6 (printed 3 and 4) were rendered and visually reviewed. They
independently explain Evolution X MIVEC and integrated S-AWC. Adjacent Twin Clutch
SST coverage does not apply to the selected five-speed. The old media endpoint
failed TLS negotiation, an older environmental-report host had an expired
certificate, and alternate links failed; verification was not disabled. Search
snippets from an unread environmental-report table are not numeric evidence.

GRB uses Subaru's October 24, 2007 Japan release and original six-page PDF.
The HTML was read; PDF pages 1 and 6 were rendered and visually reviewed, including
the final table's 1994 cc, 227 kW / 308 PS at 6400 rpm, 422 Nm at 4400 rpm,
16-valve DOHC Dual AVCS intercooled twin-scroll boxer and six-speed manual.
The front torque-sensitive/rear Torsen LSDs, multi-mode DCCD, strut front and
new double-wishbone rear are documented. Optional BBS/Recaro/audio, US 2.5-litre,
A-Line, GVB sedan and facelift are excluded. Earlier WRC titles and a planned
Group N application do not become victories or homologation for this road car.

VA uses Subaru's August 25, 2014 Japan release and original four-page PDF.
The HTML was read; PDF pages 1 and 4 were rendered and visually reviewed. Base
STI has the 1994-cc turbo boxer, 227 kW / 308 PS at 6400 rpm, 422 Nm at 4400 rpm,
reinforced six-speed, DCCD, inverted-strut front, reinforced body and Active Torque
Vectoring. Unstated engine code/cam/injection and rear-suspension details are not
borrowed from GRB. The factory photograph depicts Type S; its Bilstein/BBS
hardware is not imported as base equipment. S4, overseas 2.5-litre and facelift
specifications are excluded; optional LEDs are not universal standard equipment.

## Photography

All four selected images were downloaded unchanged and visually reviewed.
FK2 uses Alexandre Prevot's CC BY-SA 2.0 photograph: UK plates, GT details and a
visible club graphic are qualified. Evolution X uses baku13's CC BY-SA 3.0 Tokyo
launch-display photograph dated October 1, 2007; visible wheels do not authenticate
optional equipment or the selected manual transmission. GRB uses IFCAR's public
domain 2008 US hatchback, representing the early body without certifying Japan
2.0-litre mechanicals. VA uses Calreyn88's CC BY-SA 4.0 2015 UK pre-facelift sedan;
UK engine/trim does not establish the Japan base reference. Creator, licence,
original description URL, caption boundaries and SHA-256 are stored publicly.
Factory press availability is not treated as an open image licence.

## Validation

Actual import preserved every earlier table row. Reimport added zero and left
the full snapshot unchanged. Integrity and foreign keys passed; static export
matched the public payload. Four admission facts, attribute/source mappings,
image credits and unchanged source/export hashes passed. All 18 regression tests passed in 242.812 seconds on the final 621-record
catalogue, including rebuilding all 25 curated batches, duplicate rejection,
preservation, rollback, startup and repeat safety. All 27 saved batches passed
54 read-only LF/CRLF replays, leaving the actual database byte-for-byte unchanged.
The new marker matches its canonical LF fingerprint. Complete source fields/types,
attribute mappings and public admission facts passed final export verification.
No native Linux runtime or fresh interactive browser test is claimed. This batch remains
in draft and is not live.
