# Carrera GT baseline media-source repair

Reviewed 30 October 2026. The four stored Carrera GT photographs were linked to
four different photographs. This repair preserves every local image and car
record while correcting attribution, licence, source links and view captions.
The exact before/after rows and unchanged file hashes are recorded in
[data/baseline-carrera-gt-media-repair-01.json](../data/baseline-carrera-gt-media-repair-01.json).

| Media | Preserved file | Correct source | Creator | Licence |
| --- | --- | --- | --- | --- |
| 14 | `carrera_gt_exterior.jpg` | [Front](https://commons.wikimedia.org/wiki/File:Porsche_Carrera_GT_(2005)_(55082977558).jpg) | Charles from Port Chester, New York | CC0 |
| 15 | `carrera_gt_rear.jpg` | [Front/side](https://commons.wikimedia.org/wiki/File:Porsche_Carrera_GT_(2005)_(55082977573).jpg) | Charles from Port Chester, New York | CC0 |
| 16 | `carrera_gt_interior.jpg` | [Interior](https://commons.wikimedia.org/wiki/File:Porsche_Carrera_GT_Interior.JPG) | The359 | CC BY-SA 3.0 |
| 17 | `carrera_gt_engine.jpg` | [Engine-cover view](https://commons.wikimedia.org/wiki/File:2004_silver_Porsche_Carrera_GT_engine.JPG) | BrokenSphere | CC BY-SA 3.0 |

Both the previously linked photographs and the correct sources were downloaded
and visually compared against the local images. Three local JPEGs are byte-
identical to the correct current 960-pixel Commons renditions. The engine-cover
JPEG has different metadata but exactly identical decoded RGB pixels at 960 by
720. The four previous source images visibly differ. Their matching licence
names therefore did not establish correct attribution for the stored images.

The media now link to existing source rows 309, 310, 312 and 311 respectively,
with creator, exact licence URL, original credit and qualifications documented.
Old source rows 30–33 remain as historical references with notes explaining that
they are not the sources of the current local photographs. No source or image
is deleted. The filename `rear` stays unchanged; its caption accurately calls
the view front/side. The engine caption describes a closed mesh cover rather
than claiming an unobstructed view of the V10. Photographs do not certify tune,
paint code, build or original equipment.

## Validation

The exact preimages were checked before applying the four media and eight source-note updates. An all-table comparison confirms that every other row, table count and image hash is unchanged. Integrity and foreign keys pass; all corrected media source IDs/URLs resolve and the static export contains the exact credits and unchanged image bytes. Both startup preservation tests pass after the repair in 27.036 seconds. All 134 read-only line-ending replays leave the corrected database unchanged. The four-car addition separately passed all 18 import/startup tests before this attribution-only change.

This is an attribution repair, not a complete Carrera GT profile audit. Repeated
technical entries, ownership advice, recall coverage, colour/country estimates
and market evidence need separate review. No extra car contributes to the
1,000-icon count through this correction.
