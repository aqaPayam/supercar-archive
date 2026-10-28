# Road icons, batch 2

Research date: 2026-10-28. Baseline: 399 records. This batch targets missing
European rally homologation cars, unusual mid-engined road hatchbacks and
influential sporting saloons. Each is a new model or mechanically distinct
generation absent from the baseline; no cosmetic edition is used to pad the count.

Validated result: 11 additions, 410 exported records. Every prior row in every
table is preserved. All 15 regression tests pass, including replay of both
curated batches. SQLite integrity, foreign keys, public admission facts, all 11
exported photo checksums and exact local/static payload parity pass validation.

| Record | Why it belongs |
| --- | --- |
| Lancia Stratos HF Stradale | Purpose-built rally architecture in a road homologation car |
| Lancia Delta HF integrale Evoluzione II | Developed road representative of the championship-winning Delta lineage |
| Lancia Delta S4 Stradale | Twincharging and a mid-engine/all-wheel-drive Group B layout |
| Lancia Fulvia 1.6 HF Fanalone | Lightweight homologation special behind Lancia's early rally heritage |
| Fiat 131 Abarth Rally road car | Road counterpart of the three-title rally programme |
| Renault 5 Turbo | Original mid-engined turbo road hatch with lasting cultural and rally significance |
| Renault Clio V6 Phase I | V6 sports-car architecture replacing an ordinary hatchback's rear seating |
| Ford RS200 road car | Purpose-designed Group B road homologation special |
| Ford Sierra RS Cosworth | Original turbocharged road model behind a major competition lineage |
| BMW 2002 turbo | Early European production turbocharging landmark |
| Mercedes-Benz 190 E 2.3-16 | Four-valve sporting saloon underpinning record testing and touring-car competition |

The manifest `data/icons-road-02.json` retains public, sourced admission reasons,
technical attributes, manufacturer references, licensed photo attribution and
downloaded-image SHA-256 values. Photos are representative exteriors; exact
engine, equipment, market and year are not certified by the pictures.

## Evidence decisions

- Do not confuse the Delta S4 with an uprated front-engined integrale: their
  architecture differs fundamentally. Only one integrale road derivative is
  selected here, not every power or paint variation.
- Stratos power/speed claims from a problematic historical article are withheld.
  Its well-documented road architecture and design are recorded instead.
- The Fulvia is the first-series 115-hp Fanalone; 1016, Group 4 and later Lusso
  specifications are excluded. Road 131 Abarth carburetion and output are kept
  separate from the page's competition specification table.
- Renault's museum pages combine road/racing ranges for the 5 Turbo and contain
  inconsistent capacity, output-unit and speed descriptions for the Clio V6.
  Conflicting figures are withheld. Solid architecture and development facts
  remain sourced; no Phase II output is assigned to Phase I.
- RS200 road output and production totals remain unknown here; racing output is
  not silently substituted. The Sierra uses the original 204 PS road engine,
  excluding RS500 and Sapphire variants.
- The 190 E's Nardò record cars were modified. Their speeds and equipment are not
  assigned to the production road model. Conflicting road top-speed claims are
  left unresolved rather than choosing the highest value.
- Known metric outputs are normalized at 0.73549875 kW per PS/CV and identified
  as calculations. Ambiguous manufacturer HP notation is kept unconverted.
- The Escort RS Cosworth remains pending. The located June 1992 Ford road
  brochure could not be read, and conflicting output descriptions were not
  resolved by copying a competition specification. Its eligibility is not in
  doubt, but the profile needs stronger evidence before admission.

## Validation

```powershell
python scripts/import_curated.py --manifest data/icons-road-02.json
python scripts/import_curated.py --manifest data/icons-road-02.json --apply
python -m unittest test_startup test_jdm_import test_supercars_import test_curated_import -v
python export_public.py --output dist
```

Regression coverage now replays every `icons-road-*.json` manifest in order from
a database copy with those batches removed, verifying cross-batch collisions,
repeat safety and baseline preservation. Eligibility itself is an evidence-review
decision, not something a count or string-length check can prove.
