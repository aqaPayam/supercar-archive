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

SCOPED_TABLES = {
    "attributes",
    "facts",
    "media",
    "color_records",
    "country_distribution",
}


def rows_as_dicts(db: sqlite3.Connection, query: str, params: tuple[object, ...] = ()) -> list[dict[str, object]]:
    return [dict(row) for row in db.execute(query, params)]


def validate_payload(payload: dict[str, object]) -> None:
    """Fail deployment rather than publish incomplete or internally broken records."""
    cars = payload["cars"]
    car_ids = {car["id"] for car in cars}
    if len(car_ids) != len(cars):
        raise SystemExit("Public archive validation failed: duplicate car IDs")
    for car in cars:
        source_ids = {int(source["id"]) for source in car["sources"]}
        for table in CHILD_TABLES:
            if table == "sources":
                continue
            for record in car[table]:
                if record.get("car_id") not in car_ids:
                    raise SystemExit(f"Public archive validation failed: unknown owner in {table}")
                if record.get("source_id") is not None and int(record["source_id"]) not in source_ids:
                    raise SystemExit(f"Public archive validation failed: unresolved source in {table}")
        for media in car["media"]:
            location = str(media.get("location") or "")
            if location.startswith(("/assets/", "assets/")):
                relative = location.removeprefix("/").removeprefix("assets/")
                if not (ASSET_DIR / relative).is_file():
                    raise SystemExit(f"Public archive validation failed: missing image {location}")


def build_payload(db: sqlite3.Connection) -> dict[str, object]:
    """Build the canonical read-only view used both locally and on GitHub Pages."""
    cars = rows_as_dicts(
        db,
        """SELECT * FROM cars
           ORDER BY manufacturer, model_family, model_year_from, variant""",
    )
    for car in cars:
        scope_params = (car["id"], car["family_id"], car["generation_id"])
        referenced_source_ids: set[int] = set()
        for table, order_by in CHILD_TABLES.items():
            if table == "sources":
                continue
            if table in SCOPED_TABLES:
                car[table] = rows_as_dicts(
                    db,
                    f"""SELECT r.* FROM {table} r
                        JOIN cars owner ON owner.id=r.car_id
                        WHERE r.car_id=?
                           OR (r.scope_level='Model family' AND owner.family_id=?)
                           OR (r.scope_level='Generation' AND owner.generation_id=?
                               AND owner.generation_id IS NOT NULL)
                        ORDER BY {order_by}""",
                    scope_params,
                )
            else:
                car[table] = rows_as_dicts(
                    db,
                    f"SELECT * FROM {table} WHERE car_id = ? ORDER BY {order_by}",
                    (car["id"],),
                )
            referenced_source_ids.update(
                int(row["source_id"])
                for row in car[table]
                if row.get("source_id") is not None
            )

        direct_sources = rows_as_dicts(
            db,
            "SELECT * FROM sources WHERE car_id = ? ORDER BY publisher, title, id",
            (car["id"],),
        )
        source_ids = {int(source["id"]) for source in direct_sources} | referenced_source_ids
        if car.get("primary_source_id") is not None:
            source_ids.add(int(car["primary_source_id"]))
        if source_ids:
            placeholders = ",".join("?" for _ in source_ids)
            car["sources"] = rows_as_dicts(
                db,
                f"SELECT * FROM sources WHERE id IN ({placeholders}) ORDER BY publisher, title, id",
                tuple(sorted(source_ids)),
            )
        else:
            car["sources"] = []

    updated_at = db.execute("SELECT MAX(updated_at) FROM cars").fetchone()[0]
    unique_counts = {
        table: db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in CHILD_TABLES
    }
    payload = {
        "archive": {
            "title": "Supercar Archive",
            "car_count": len(cars),
            "manufacturer_count": len({car["manufacturer"] for car in cars}),
            "media_count": unique_counts["media"],
            "source_count": unique_counts["sources"],
            "fact_count": unique_counts["facts"],
            "last_record_update": updated_at,
            "schema_version": 2,
        },
        "cars": cars,
    }
    validate_payload(payload)
    return payload


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

        payload = build_payload(db)
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
    print(f"Exported {len(payload['cars'])} cars to {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the read-only Supercar Archive website")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    export(args.output.resolve())


if __name__ == "__main__":
    main()
