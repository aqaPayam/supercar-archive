# Supercar Archive

A local, searchable supercar knowledge base that keeps specifications, engineering stories, market history, colors, geographic distribution, sources, and licensed media in one website.

The catalogue supports manufacturer browsing, full-text search, linked model filters, technical and market ranges, evidence-availability filters, sorting, grid/list views, pagination, and shareable filter URLs.

## Run locally

```powershell
python supercar_app.py
```

Then open [http://127.0.0.1:8765](http://127.0.0.1:8765). This is the canonical viewer: the same HTML, CSS, JavaScript, effective scoped records, charts, and evidence details are deployed online.

Open [http://127.0.0.1:8765/admin](http://127.0.0.1:8765/admin) to add or edit database records. Management remains local so the public archive is read-only.

The application uses Python's standard library and SQLite, so it does not require package installation. The working dataset is stored in `supercars.db`.

## Public website

The GitHub Pages edition is read-only. It publishes the exact same canonical viewer used at the local root URL, while the local `/admin` area remains the private editor. A shared data builder applies variant, generation, and model-family scope consistently in both environments.

Build it locally with:

```powershell
python export_public.py
python -m http.server 8000 --directory dist
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000). Every push to `main` runs `.github/workflows/pages.yml`, rebuilds the site from `supercars.db`, and deploys it to GitHub Pages.

## Repository contents

- `supercar_app.py` — website, database schema, migrations, and editing workflows
- `supercars.db` — the current dataset
- `assets/` — locally stored licensed images
- `export_public.py` — deterministic static-site exporter
- `web/` — public read-only website source

Image creator, license, and original-source attribution are stored in the database and displayed in the website's gallery and Source Library.

## JDM research batch

The database includes 50 additional Japan-market road variants with manufacturer
evidence and licensed representative photography. See [the batch review](docs/jdm50.md)
for the car list, duplicate audit, evidence limitations and repeatable import checks.

## Supercar research batch

The next 50 additions cover road supercars, open-top derivatives and explicitly
labeled factory track cars. See [the batch review](docs/supercars50.md) for the
variant list, manufacturer sources, photo attributions and validation commands.

## Curated expansion toward 1,000 cars

New additions follow the [performance-icon admission policy](docs/curation1000.md).
Each car needs a sourced explanation of its significance, alongside its technical
evidence and licensed photograph. Fifty-one reviewed road-icon batches add 379 cars
to the 395-record baseline, bringing the working catalogue to 774 records.
The latest [Ginetta, Alvis, SSK and Duesenberg road-icons batch](docs/icons-road-51.md)
adds four absent road families, following the
[TVR, Maserati and lightweight road-icons batch](docs/icons-road-50.md). Individual reviews and
evidence boundaries
are recorded in [the documentation](docs), with repeatable manifests in `data`.
The 1,000-qualifying-car goal remains active: existing records still need the
final eligibility audit, and quality takes priority over the numerical count.
The [baseline audit checkpoint](docs/baseline-audit-checkpoint.md) records the
remaining scope and identity review without changing existing records.
The [first baseline credit repair](docs/baseline-media-credits-01.md) resolves
three F50 attribution placeholders while preserving the photographs and car data.
A [second credit repair](docs/baseline-media-credits-02.md) resolves 27 more
placeholders across ten profiles. A [photograph scope repair](docs/baseline-image-scope-01.md)
qualifies five captions/lead-image flags while preserving all photographs and car data.

Import fingerprints normalize LF/CRLF line endings for Windows/Linux portability.
Existing LF and CRLF import markers remain accepted without rewriting the database.
Other manifest edits still require review and are rejected on repeat import.
