from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "supercars.db"
WEB_DIR = ROOT / "web"
ASSET_DIR = ROOT / "assets"

CHILD_TABLES = {
    "attributes": "sort_order, id",
    "facts": "id",
    "price_records": "observation_date, id",
    "sources": "publisher, title, id",
    "media": "is_primary DESC, id",
    "color_records": "color_type, color_name, id",
    "country_distribution": "distribution_type, country, id",
}


def rows_as_dicts(db: sqlite3.Connection, query: str, params: tuple[object, ...] = ()) -> list[dict[str, object]]:
    return [dict(row) for row in db.execute(query, params)]


def export(output_dir: Path) -> None:
    if not DB_PATH.is_file():
        raise SystemExit(f"Database not found: {DB_PATH}")
    if not WEB_DIR.is_dir():
        raise SystemExit(f"Public website source not found: {WEB_DIR}")

    db = sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    try:
        integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise SystemExit(f"Database integrity check failed: {integrity}")

        cars = rows_as_dicts(
            db,
            """SELECT * FROM cars
               ORDER BY manufacturer, model_family, model_year_from, variant""",
        )
        for car in cars:
            for table, order_by in CHILD_TABLES.items():
                car[table] = rows_as_dicts(
                    db,
                    f"SELECT * FROM {table} WHERE car_id = ? ORDER BY {order_by}",
                    (car["id"],),
                )

        updated_at = db.execute("SELECT MAX(updated_at) FROM cars").fetchone()[0]
        payload = {
            "archive": {
                "title": "Supercar Archive",
                "car_count": len(cars),
                "manufacturer_count": len({car["manufacturer"] for car in cars}),
                "last_record_update": updated_at,
            },
            "cars": cars,
        }
    finally:
        db.close()

    if output_dir.exists():
        shutil.rmtree(output_dir)
    shutil.copytree(WEB_DIR, output_dir)
    shutil.copytree(ASSET_DIR, output_dir / "assets")
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    (output_dir / "data.json").write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Exported {len(cars)} cars to {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the read-only Supercar Archive website")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    export(args.output.resolve())


if __name__ == "__main__":
    main()
