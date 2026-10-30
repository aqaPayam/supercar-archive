# Modern Japanese performance icons: batch 20

Reviewed 2026-10-29 against 599 existing records. Three absent road references
bring the raw catalogue to 602. The 1,000-qualifying-car goal and final baseline
eligibility audit remain outstanding.

| Selected road reference | Admission basis |
| --- | --- |
| Toyota GT86, original 2012 UK manual | Accessible rear-drive sports-car revival, Toyota/Subaru boxer and D-4S engineering |
| Toyota GR Yaris, original November 2020 UK base | Rally-led bespoke three-door body/platform, turbo three and GR-Four |
| Honda Civic Type R FK8, original 2017 France | New front-drive performance chassis with dual-axis front, multi-link rear and adaptive damping |

## Identity and duplicates

The complete inventory and previous manifests were checked. No Toyota 86/GT86,
Scion FR-S, Subaru BRZ or Yaris/GR Yaris was present. One GT86 represents the
original shared road-car identity; rebadges, TRD, drift builds, cosmetic editions
and a second body/tune are not additional cars. GR Yaris is a separate bespoke
road-performance hatch rather than a GT86 derivative or ordinary Yaris trim.
Convenience/Circuit packages, Japan RS, 2024 power/automatic changes and
competition versions do not multiply this batch's count.

Existing Civic Type R entries are EK9, EP3, FD2 and FN2. The FK8 is the missing
tenth-generation Civic performance chassis, not a further year of those cars.
GT equipment, facelift, Limited Edition, TCR racer and FL5 are not added here.
Brand origin is Japan; the FK8's UK assembly is not mistaken for brand origin.

## Technical evidence

Sources and field mappings are in
[data/icons-road-20.json](../data/icons-road-20.json).

GT86 uses Toyota Europe's March 6, 2012 engine/transmission engineering account.
The migrated URL includes “2019”, but its displayed date, article and media
identify the original 2012 launch. It documents the 1998-cc Subaru boxer/Toyota
D-4S collaboration, natural aspiration, DOHC, compression, manual and Torsen.
Toyota GB's February output announcement explicitly supplies 147 kW, while the
March 30 equipment release confirms the UK road reference and July 1 deliveries.
Early anticipated launch timing is not substituted for the later release.
Automatic controls and race-team roll cage, brakes or suspension are excluded.

GR Yaris uses the original November 2020 UK full launch PDF. Pages 1–2, 7,
17 and 24–25 were rendered and visually read. The narrative explicitly states
360 Nm; the technical table's “3600” torque typo is rejected. The anomalous
gear-row heading is not used. The selected base car does not inherit optional
Circuit Pack Torsen differentials, forged wheels or suspension tuning. Original
192-kW output, six-speed and GR-Four are separate from later 2024 changes.
This records rally-led road development and homologation intent, not a claim
that this exact road specification won WRC events. A search result labelled
2020 GR Yaris instead linked a 2022 full-range price list; it was rejected.

FK8 uses Honda Motor Europe's original 2017 French launch engineering account
and technical section. Current FK8 sections are distinct from earlier Type R
history paragraphs. Native European 235 kW and 400 Nm are not mixed with US
306-hp notation. The six-speed, helical differential, revised front suspension,
new multi-link rear, adaptive damping and Brembo road brakes are documented.
The source's questionable seat-count line is omitted; no current lap-record
superlative or unsupported acceleration/weight claim is imported. The French
HTML was read locally; no PDF render of that Honda account is claimed.

## Photography

All three selected photos were visually reviewed: original GT86 in Düsseldorf
in September 2012, original GR Yaris road body identified as 2020 RZ in Germany,
and a documented 2017 Civic Type R GT at a UK Honda dealer. The GR photo does
not certify UK base equipment, market engine tune or optional differentials.
The Honda photo represents the original road body without certifying French
GT/base equipment. Captions retain those market/originality limits. Drift cars,
late-body FK8 photos with generic generation-year titles and other Type R
bodies were rejected. Creators, licences, source URLs and unchanged image bytes
are retained; factory press availability is not treated as an open image licence.

## Validation

All 18 regression tests passed on the final 602-record catalogue (200.512 seconds).
They include replaying all twenty curated batches from the 395-record baseline,
duplicate rejection, row preservation, repeat safety, export rollback, repeated
startup and both legacy-marker/line-ending directions. A changed source note
still rejects replay.

The actual three-car import preserved every previous table row and immediate
reimport changed nothing. Database integrity and foreign keys pass. Static
website export equals the local public payload. All three new admission facts,
complete source fields/types, attribute mappings, photo credits and source/export
image hashes were verified. Independently, all 22 saved manifests replayed with
LF and CRLF: 44 read-only replays left the database byte-for-byte unchanged.
No native Linux runtime or fresh interactive browser test is claimed. This
batch remains in the draft review branch and has not updated the live website.

The import portability fix is separately documented in
[the repeat-import review](import-portability.md). New markers use the LF
fingerprint; existing LF/CRLF markers remain accepted without rewriting them.
