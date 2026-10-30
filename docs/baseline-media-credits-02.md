# Baseline image-credit repair: 27 works across ten cars

Reviewed 2026-10-29 against the 709-record catalogue. This resolves the remaining
27 obvious generic-creator/licence placeholders found by the targeted inventory.
It adds no cars and changes no photographs, car records or technical data.

| Existing profile | Images reviewed |
| --- | ---: |
| Lamborghini Diablo SV | 2 |
| Mercedes-Benz SLR McLaren coupe | 4 |
| Lamborghini Countach LP400 | 3 |
| Bugatti EB110 GT | 2 |
| Jaguar XJ220 | 1 |
| Pagani Zonda C12 | 4 |
| Koenigsegg CC8S | 3 |
| Lamborghini Miura P400 | 3 |
| Porsche 911 GT1 1997 | 2 |
| Maserati MC12 Stradale | 3 |

All 27 original Commons works were retrieved through the public API, including
named creators, specific CC BY/CC BY-SA versions and licence links. Every stored
image was compared visually side by side with its source image in five review
sheets. Composition matched in all 27 cases. Downloaded source resolutions and
compression vary; no blanket claim of byte identity between source downloads
and stored files is made.

The [reviewed correction manifest](../data/baseline-media-credits-02.json) records
every media/source identifier, original source URL, expected previous values,
verified replacement credits, licence URL and existing asset SHA-256. One older
Commons licence link uses HTTP; its original link is retained rather than silently
replacing the reported metadata. All source-page URLs remain HTTPS.

The guarded repair changed only the creator/licence fields of 27 media rows and
the notes of their 27 linked source rows. Every one of the 709 car rows and all
other fields/rows were preserved. Repeat application made zero changes. Database
integrity, foreign keys, exact row/field deltas, exported public credits, export
equality and unchanged local/exported image hashes passed.
Both startup tests then passed in 21.440 seconds. A subsequent targeted query
found no remaining blank/generic-contributor/`See source page` credit fields.
The later eight-car batch preserves all these corrected rows; its final
regression and replay results are recorded in [batch 42](icons-road-42.md).

## Limits of this review

A named reusable-image licence does not authenticate factory specification,
engine tune, body modifications, model year or original build provenance. This
is a credit repair, not a completed representative-image or technical audit.
The targeted placeholder search is not a comprehensive audit of every licence
or credit string in the archive.

Visual review flags the Countach image in media row 61 for separate assessment
of its spoiler/wheels/body treatment against the standard LP400 reference.
Generic Zonda source descriptions in rows 89 and 90 do not establish the stored
original 6.0-litre specification. The tightly cropped GT1 roof-intake photograph
in row 103 does not establish the year claimed by its existing caption. Their
credits are now specific, but their variant/caption boundaries remain part of
the baseline audit. No car is counted again for this maintenance work.
