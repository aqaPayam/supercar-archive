# Repeat imports across Windows and Linux

Verified 2026-10-29 on the 599-record catalogue before batch 20.

The saved import markers previously fingerprinted raw JSON bytes. Git checks out
LF on Linux and commonly CRLF on Windows, so a line-ending-only change caused an
unchanged batch to fail with “already applied with a different manifest”. A
read-only reproduction using batch 19 confirmed this failure before the fix.

Both original importers and the curated importer now use a shared fingerprint
helper. New imports save the LF fingerprint. Replays accept either the LF or
historical CRLF fingerprint, without modifying existing markers or catalogue
rows. JSON content, whitespace, escaping and field order remain significant;
this is not a semantic-JSON override. Validation and hashing use the same bytes.

New regression coverage checks both legacy-marker/checkout directions, read-only
preview and apply replays, whole-table preservation, new LF markers from CRLF
input, and rejection of a source-note edit after a successful import. The normal
15 catalogue checks plus these three checks passed: 18 tests in 193.010 seconds.
The GitHub Pages workflow already runs these test modules.

An independent check replayed all nineteen saved curated manifests and the two
original 50-car manifests with both line endings: 42 read-only replays passed.
The actual catalogue database remained byte-for-byte identical. This verifies
compatibility with the saved markers, not only newly imported test fixtures.
No native Linux runtime execution is claimed; both byte representations were
exercised against the saved database on Windows.
