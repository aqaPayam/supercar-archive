# Baseline image-credit repair: Ferrari F50

Reviewed 2026-10-29. This metadata correction adds no car records and changes
no photographs, car identities, specifications, prices, colours or facts.

Three existing `FER-F50-STD` media rows used the generic creator
`Wikimedia Commons contributor` and the licence placeholder `See source page`.
Their original Commons pages identify the creators and CC BY 2.0 licence:

| Existing image | Verified creator | Original source |
| --- | --- | --- |
| `f50_exterior.jpg` | Charles from Port Chester, New York | [Ferrari F50 (1995) (52962541522).jpg](https://commons.wikimedia.org/wiki/File:Ferrari_F50_(1995)_(52962541522).jpg) |
| `f50_rear.jpg` | Axion23 | [Ferrari F50 Rear (17115768058).jpg](https://commons.wikimedia.org/wiki/File:Ferrari_F50_Rear_(17115768058).jpg) |
| `f50_engine.jpg` | Axion23 | [Ferrari f50 engine (3428493158).jpg](https://commons.wikimedia.org/wiki/File:Ferrari_f50_engine_(3428493158).jpg) |

Each work is licensed [CC BY 2.0](https://creativecommons.org/licenses/by/2.0).
Commons metadata was retrieved directly and the stored photographs were visually
compared side by side with their source images. The rear image also matched the
downloaded source bytes exactly; different resolutions of the other two images
were compared visually. No new claim that every source download is byte-identical
to the stored asset is made.

The [reviewed correction manifest](../data/baseline-media-credits-01.json) records
the existing media/source identifiers, expected previous values, source URLs,
verified credits, licence URLs and existing asset hashes. Only three media rows'
creator/licence fields and the corresponding three source rows' notes change.
The existing files, source bindings, captions and all car records are retained.

The guarded repair passed repeated application (zero changes), exact six-row
field-delta checks, integrity, foreign keys, unchanged image hashes and exported
public-credit equality. All 709 car rows and every unrelated field/row were
preserved. Both startup tests then passed in 21.615 seconds. Final new-profile
source/fact/attribute/media/export checks passed, as did 86 read-only LF/CRLF
replays across all 43 saved batches without changing the final database bytes.
The full 18-test suite passed immediately before this metadata repair;
no broader post-repair regression rerun is claimed.

This resolves three observed credit placeholders. It does not certify the
remaining F50 technical, pricing, historical or image-caption fields, and is not
a completed audit of the 395-record baseline.
