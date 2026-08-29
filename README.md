# Supercar Archive

A local, searchable supercar knowledge base that keeps specifications, engineering stories, market history, colors, geographic distribution, sources, and licensed media in one website.

## Run locally

```powershell
python supercar_app.py
```

Then open [http://127.0.0.1:8765](http://127.0.0.1:8765).

The application uses Python's standard library and SQLite, so it does not require package installation. The working dataset is stored in `supercars.db`.

## Repository contents

- `supercar_app.py` — website, database schema, migrations, and editing workflows
- `supercars.db` — the current dataset
- `assets/` — locally stored licensed images

Image creator, license, and original-source attribution are stored in the database and displayed in the website's gallery and Source Library.
