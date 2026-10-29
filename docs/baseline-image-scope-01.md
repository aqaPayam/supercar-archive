# Baseline photograph scope repair 01

Reviewed 29 October 2026 against the stored photographs and their linked
Commons descriptions. The guarded old/new values, source bindings and SHA-256
asset hashes are recorded in `data/baseline-image-scope-01.json`.

Five existing media rows change only captions or lead-image flags:

| Media | Review and correction |
| --- | --- |
| 61 | The red Countach museum car visibly has wide arch extensions and a front spoiler. Its source filename calls it LP400, but does not establish standard narrow-body specification. Retain it as a qualified illustration and remove its lead-image flag. No Walter Wolf chassis identity is inferred. |
| 62 | Make the existing yellow, narrow-body LP400 front three-quarter photograph the lead image. Correctly describe its visible view; the historical filename ending in `rear` remains unchanged. |
| 89–90 | The Commons descriptions identify a Pagani Zonda without establishing the original C12's 6.0-litre specification. Describe these as family illustrations, not evidence of that engine variant. The profile's other photographs and lead image remain unchanged. |
| 103 | Describe the visible 911 GT1 intake/windscreen detail and documented Paris 2018 setting. Remove unsupported 1997-specification and carbon-material assertions from the caption. |

Lamborghini's [factory Countach retrospective](https://www.lamborghini.com/es-en/noticias/50-years-ago-the-first-countach-in-santagata-bolognese)
distinguishes the original LP400's unextended arches from the later S body
treatment. That distinction supports the conservative lead-image choice; it
does not identify the red display car's individual history.

All 717 car rows, every source/credit record, all other database fields and all
image bytes are preserved. The repair adds no cars and certifies no remaining
baseline technical fields. Guarded replay changes zero rows; database integrity,
foreign keys, the single LP400 lead image, public export equality and original/
exported asset hashes were checked. The startup preservation tests also pass.

The full baseline eligibility, semantic uniqueness and provenance audit remains
open. Qualified illustrative images must not be treated as technical proof of
the profile's precise variant.
