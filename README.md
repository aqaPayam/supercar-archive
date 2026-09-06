# Supercar Archive

A local, searchable supercar knowledge base that keeps specifications, engineering stories, market history, colors, geographic distribution, sources, and licensed media in one website.

The catalogue supports manufacturer browsing, full-text search, linked model filters, technical and market ranges, evidence-availability filters, sorting, grid/list views, pagination, and shareable filter URLs.

## Run locally

```powershell
python supercar_app.py
```

Then open [http://127.0.0.1:8765](http://127.0.0.1:8765).

The application uses Python's standard library and SQLite, so it does not require package installation. The working dataset is stored in `supercars.db`.

## Public website

The GitHub Pages edition is read-only. It keeps the local application as the private editor while publishing the catalogue, filters, car pages, sourced details, market records, and licensed images as a static website.

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
