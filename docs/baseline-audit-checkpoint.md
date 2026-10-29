# Baseline eligibility audit checkpoint

Snapshot: 2026-10-29, 657 working records. This is an inventory checkpoint,
not a completed eligibility or semantic duplicate audit.

The 33 reviewed road-icon manifests contain 262 distinct identifiers. Subtracting
those identifiers from the actual database leaves the preserved 395-record
baseline. Its records have not automatically been approved under the new policy.
The raw 657 count must not be presented as 657 proven qualifying icons.

An exact case-folded, whitespace-trimmed comparison of manufacturer, model,
generation and variant found no identical baseline identity-text tuples. That
check cannot establish semantic uniqueness: aliases, body styles, optional
packages and differently described versions still require per-car review.
Same-generation variant counting remains a pending user boundary.

## Existing non-road flags

The baseline has 22 records whose stored road_legal flag is zero. The list below
reports existing data; it does not independently authenticate each car's legal
status or decide its admission. Dedicated racers/prototypes and production track
derivatives need the pending scope decision and individual review. No record
has been removed or recategorized on this basis.

| Identifier | Existing manufacturer / model | Existing variant |
| --- | --- | --- |
| AST-VULCAN-TRACK | Aston Martin Vulcan | Vulcan — original specification |
| BUG-BOLIDE-PRODUCTION | Bugatti Bolide | Production track car — 1600 PS |
| FER-296-CHALLENGE | Ferrari 296 | Challenge — non-hybrid race car |
| FER-599XX-EVO | Ferrari 599 | 599XX Evo |
| FER-599XX-TRACK | Ferrari 599 | 599XX |
| FER-FXX-TRACK | Ferrari FXX | FXX |
| FER-FXX-K-EVO | Ferrari FXX K | FXX K Evo |
| FER-FXX-K-TRACK | Ferrari FXX K | FXX K |
| FOR-GT-MKIV-TRACK | Ford GT | Mk IV — modern track-only |
| JAG-XJR15-RACE | Jaguar XJR-15 | Intercontinental Challenge competition car |
| KOE-CCGT-TRACK | Koenigsegg CCGT | CCGT — original GT1 prototype |
| LAM-ESSENZA-SCV12 | Lamborghini Essenza SCV12 | Essenza SCV12 |
| LAM-GAL-ST-2009 | Lamborghini Gallardo | Super Trofeo — original 2009 race car |
| LAM-HUR-ST-620 | Lamborghini Huracán | LP 620-2 Super Trofeo — original race car |
| LAM-SESTO-TRACK | Lamborghini Sesto Elemento | Track-only |
| MCL-P1-GTR-TRACK | McLaren P1 | P1 GTR |
| MCL-SENNA-GTR | McLaren Senna | Senna GTR |
| MCL-SOLUS-GT | McLaren Solus GT | Solus GT |
| PAG-HUA-R-EVO | Pagani Huayra | R Evo Roadster |
| PAG-HUA-R-TRACK | Pagani Huayra | R — original 850 CV track car |
| PAG-ZON-R-TRACK | Pagani Zonda | R — original track specification |
| PAG-ZON-REV-TRACK | Pagani Zonda | Revolución — track specification |

## Outstanding decisions and evidence

The existing Hyundai Verna Iran 1.5 manual is already flagged outside the
confirmed performance-icon scope in [the admission policy](curation1000.md).
It remains preserved rather than becoming precedent for ordinary additions.
A final qualifying total requires a record-by-record significance and identity
review of the baseline, resolution of the variant/racing boundaries and checks
of technical provenance, road/competition separation and representative image
licensing. Neither the absence of identical strings nor passing import tests
proves these historical and editorial requirements.
