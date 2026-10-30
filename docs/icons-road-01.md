# Road icons, batch 1

Reviewed 2026-10-28 against the 395-car baseline. Four original road models,
each absent from the catalogue, rather than additional trims of an existing
generation. These fit the confirmed performance-icon scope regardless of the
outstanding choices about variant counting and dedicated racing cars.

Imported result: 399 catalogue records. Every pre-existing row in every table
was preserved. SQLite integrity, foreign keys, public export and all four
exported image checksums passed validation. Startup preservation passed again
after importing the batch.

| New record | Admission reason |
| --- | --- |
| BMW M3 E30 | Original Group A road homologation model and foundation of the M3 lineage |
| Audi quattro B2 | Landmark permanent-all-wheel-drive performance coupe |
| Lancia Rally 037 Stradale | Road homologation counterpart of the 1983 rally constructors' championship programme |
| Peugeot 205 Turbo 16 road version | Mid-engined, all-wheel-drive Group B homologation special |

`data/icons-road-01.json` contains the manufacturer references, exact scope,
attribute-level source links, public admission facts, photograph creators,
license URLs, original Commons file pages and image checksums. The four photos
were inspected visually. The Audi photo represents another year/market; its
caption does not claim to verify the 1980 engine specification.

The 037 and M3 manufacturer HP notation is retained without an assumed metric
conversion. The 205 displacement is withheld because the consulted releases
disagree between 1700 and 1.8 litres. Road-car output is kept separate from
optional power kits and competition engine figures. Undefined weight conventions
and ambiguous rev-limit language are withheld.

The curated importer reuses the tested atomic importer, with a declared batch
size and a required admission explanation that must appear as a sourced public
fact. This checks documentation completeness; editorial eligibility still
requires evidence review. Existing fixed-size 50-car imports retain their
original default and manifest checksums.

```powershell
python scripts/import_curated.py --manifest data/icons-road-01.json
python scripts/import_curated.py --manifest data/icons-road-01.json --apply
python -m unittest test_startup test_jdm_import test_supercars_import test_curated_import -v
python export_public.py --output dist
```

Fourteen regression tests cover preservation, startup, repeat-safe imports,
collision rejection, count validation, admission documentation, read-only preview
and transactional rollback. The full 1,000-car objective remains active; the
raw count alone is not proof that every existing record meets the new policy.
