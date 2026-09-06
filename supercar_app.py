from __future__ import annotations

import argparse
import html
import json
import os
import sqlite3
import uuid
from collections import defaultdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlencode, urlparse

from export_public import build_payload


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "supercars.db"
ASSET_DIR = ROOT / "assets"
WEB_DIR = ROOT / "web"


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS model_families (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer TEXT NOT NULL,
    name TEXT NOT NULL,
    origin_country TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(manufacturer, name)
);

CREATE TABLE IF NOT EXISTS generations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    family_id INTEGER NOT NULL REFERENCES model_families(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    year_from INTEGER,
    year_to INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(family_id, name)
);

CREATE TABLE IF NOT EXISTS cars (
    id TEXT PRIMARY KEY,
    family_id INTEGER REFERENCES model_families(id),
    generation_id INTEGER REFERENCES generations(id),
    manufacturer TEXT NOT NULL,
    model_family TEXT NOT NULL,
    generation TEXT,
    variant TEXT NOT NULL DEFAULT 'Standard',
    model_year_from INTEGER,
    model_year_to INTEGER,
    production_start TEXT,
    production_end TEXT,
    body_style TEXT,
    category TEXT,
    road_legal INTEGER NOT NULL DEFAULT 1,
    origin_country TEXT,
    engine_code TEXT,
    engine_configuration TEXT,
    displacement_cc INTEGER,
    aspiration TEXT,
    power_kw REAL,
    torque_nm REAL,
    transmission TEXT,
    drivetrain TEXT,
    curb_weight_kg REAL,
    zero_to_100_s REAL,
    top_speed_kmh REAL,
    production_total INTEGER,
    production_scope TEXT,
    specification_market TEXT,
    summary TEXT,
    primary_source_url TEXT,
    primary_source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id TEXT NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    category TEXT,
    explanation TEXT NOT NULL,
    why_it_matters TEXT,
    source_url TEXT,
    source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    scope_level TEXT NOT NULL DEFAULT 'Variant',
    confidence TEXT DEFAULT 'High',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS price_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id TEXT NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    observation_date TEXT,
    price_type TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    market TEXT,
    venue TEXT,
    serial_number TEXT,
    mileage TEXT,
    source_url TEXT,
    source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id TEXT NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    publisher TEXT,
    title TEXT NOT NULL,
    source_type TEXT,
    url TEXT NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id TEXT NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    media_type TEXT NOT NULL DEFAULT 'Exterior image',
    location TEXT NOT NULL,
    caption TEXT,
    creator TEXT,
    license TEXT,
    source_url TEXT,
    source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    scope_level TEXT NOT NULL DEFAULT 'Variant',
    is_primary INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id TEXT NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    section TEXT NOT NULL,
    label TEXT NOT NULL,
    value TEXT NOT NULL,
    unit TEXT,
    source_url TEXT,
    source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    scope_level TEXT NOT NULL DEFAULT 'Variant',
    sort_order INTEGER NOT NULL DEFAULT 100,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS color_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id TEXT NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    color_name TEXT NOT NULL,
    color_code TEXT,
    color_type TEXT NOT NULL DEFAULT 'Exterior',
    swatch_hex TEXT,
    availability_scope TEXT,
    production_count INTEGER,
    production_percentage REAL,
    count_scope TEXT,
    source_url TEXT,
    source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    scope_level TEXT NOT NULL DEFAULT 'Variant',
    confidence TEXT NOT NULL DEFAULT 'Verified',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS country_distribution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id TEXT NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    distribution_type TEXT NOT NULL,
    country TEXT NOT NULL,
    region TEXT,
    vehicle_count INTEGER,
    share_percentage REAL,
    denominator INTEGER,
    as_of_date TEXT,
    source_url TEXT,
    source_id INTEGER REFERENCES sources(id) ON DELETE SET NULL,
    scope_level TEXT NOT NULL DEFAULT 'Variant',
    confidence TEXT NOT NULL DEFAULT 'Verified',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_cars_manufacturer_model
ON cars(manufacturer, model_family);

CREATE INDEX IF NOT EXISTS idx_cars_category
ON cars(category);

CREATE INDEX IF NOT EXISTS idx_facts_car_id
ON facts(car_id);

CREATE INDEX IF NOT EXISTS idx_prices_car_date
ON price_records(car_id, observation_date);

CREATE INDEX IF NOT EXISTS idx_sources_car_id
ON sources(car_id);

CREATE UNIQUE INDEX IF NOT EXISTS idx_sources_car_url_unique
ON sources(car_id, url);

CREATE INDEX IF NOT EXISTS idx_media_car_primary
ON media(car_id, is_primary);

CREATE INDEX IF NOT EXISTS idx_attributes_car_section
ON attributes(car_id, section, sort_order);

CREATE INDEX IF NOT EXISTS idx_colors_car_type
ON color_records(car_id, color_type);

CREATE INDEX IF NOT EXISTS idx_country_distribution_car_type
ON country_distribution(car_id, distribution_type);
"""


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def ensure_column(db: sqlite3.Connection, table: str, column: str, definition: str) -> None:
    existing = {row["name"] for row in db.execute(f"PRAGMA table_info({table})")}
    if column not in existing:
        db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def migrate_schema(db: sqlite3.Connection) -> None:
    ensure_column(db, "cars", "family_id", "INTEGER REFERENCES model_families(id)")
    ensure_column(db, "cars", "generation_id", "INTEGER REFERENCES generations(id)")
    ensure_column(db, "cars", "primary_source_id", "INTEGER REFERENCES sources(id) ON DELETE SET NULL")
    for table in ("facts", "price_records", "media", "attributes", "color_records", "country_distribution"):
        ensure_column(db, table, "source_id", "INTEGER REFERENCES sources(id) ON DELETE SET NULL")
    for table in ("facts", "media", "attributes", "color_records", "country_distribution"):
        ensure_column(db, table, "scope_level", "TEXT NOT NULL DEFAULT 'Variant'")
    db.execute(
        """CREATE INDEX IF NOT EXISTS idx_cars_family_generation
           ON cars(family_id, generation_id, model_year_from, variant)"""
    )


def migrate_hierarchy(db: sqlite3.Connection) -> None:
    cars = db.execute("SELECT * FROM cars").fetchall()
    for car in cars:
        family = db.execute(
            "SELECT id FROM model_families WHERE manufacturer = ? AND name = ?",
            (car["manufacturer"], car["model_family"]),
        ).fetchone()
        if family:
            family_id = family[0]
        else:
            cursor = db.execute(
                """INSERT INTO model_families(manufacturer,name,origin_country)
                   VALUES(?,?,?)""",
                (car["manufacturer"], car["model_family"], car["origin_country"]),
            )
            family_id = cursor.lastrowid
        generation_id = None
        if car["generation"]:
            generation = db.execute(
                "SELECT id FROM generations WHERE family_id = ? AND name = ?",
                (family_id, car["generation"]),
            ).fetchone()
            if generation:
                generation_id = generation[0]
            else:
                cursor = db.execute(
                    """INSERT INTO generations(family_id,name,year_from,year_to)
                       VALUES(?,?,?,?)""",
                    (family_id, car["generation"], car["model_year_from"], car["model_year_to"]),
                )
                generation_id = cursor.lastrowid
        if car["family_id"] != family_id or car["generation_id"] != generation_id:
            db.execute(
                "UPDATE cars SET family_id = ?, generation_id = ? WHERE id = ?",
                (family_id, generation_id, car["id"]),
            )


def get_or_create_source(db: sqlite3.Connection, car_id: str, url: str) -> int:
    existing = db.execute(
        "SELECT id FROM sources WHERE car_id = ? AND url = ?", (car_id, url)
    ).fetchone()
    if existing:
        return existing[0]
    host = urlparse(url).netloc.removeprefix("www.") or "External source"
    db.execute(
        """INSERT INTO sources(car_id,publisher,title,source_type,url,notes)
           VALUES(?,?,?,?,?,?)""",
        (car_id, host, host, "Evidence source", url, "Migrated from a record-level reference."),
    )
    return db.execute(
        "SELECT id FROM sources WHERE car_id = ? AND url = ?", (car_id, url)
    ).fetchone()[0]


def migrate_source_references(db: sqlite3.Connection) -> None:
    source_columns = [
        ("cars", "primary_source_url", "primary_source_id", "id"),
        ("facts", "source_url", "source_id", "car_id"),
        ("price_records", "source_url", "source_id", "car_id"),
        ("media", "source_url", "source_id", "car_id"),
        ("attributes", "source_url", "source_id", "car_id"),
        ("color_records", "source_url", "source_id", "car_id"),
        ("country_distribution", "source_url", "source_id", "car_id"),
    ]
    for table, legacy_column, source_column, car_column in source_columns:
        rows = db.execute(
            f"SELECT id, {car_column} AS car_id, {legacy_column} AS url FROM {table} "
            f"WHERE {legacy_column} IS NOT NULL AND {legacy_column} != ''"
        ).fetchall()
        for row in rows:
            source_id = get_or_create_source(db, row["car_id"], row["url"])
            db.execute(
                f"UPDATE {table} SET {source_column} = ?, {legacy_column} = NULL WHERE id = ?",
                (source_id, row["id"]),
            )


def localize_lfa_media(db: sqlite3.Connection) -> None:
    local_by_source = {
        "https://commons.wikimedia.org/wiki/File:Lexus_LFA_(5220373328).jpg": "/assets/lfa_exterior.jpg",
        "https://commons.wikimedia.org/wiki/File:Lexus_LFA_interior_(4275610758).jpg": "/assets/lfa_interior.jpg",
        "https://commons.wikimedia.org/wiki/File:The_rearview_of_Lexus_LFA.JPG": "/assets/lfa_rear.jpg",
        "https://commons.wikimedia.org/wiki/File:Lexus_LFA_010_engine.JPG": "/assets/lfa_engine.jpg",
    }
    for source_url, location in local_by_source.items():
        if not (ASSET_DIR / location.removeprefix("/assets/")).is_file():
            continue
        source = db.execute(
            "SELECT id FROM sources WHERE car_id = 'LEX-LFA-STD' AND url = ?", (source_url,)
        ).fetchone()
        if source:
            db.execute(
                """UPDATE media SET location = ?
                   WHERE car_id = 'LEX-LFA-STD' AND source_id = ? AND location != ?""",
                (location, source[0], location),
            )


def deduplicate_media(db: sqlite3.Connection) -> None:
    duplicates = db.execute(
        """SELECT car_id,source_id,location,MIN(id) AS keep_id
           FROM media WHERE source_id IS NOT NULL
           GROUP BY car_id,source_id,location HAVING COUNT(*) > 1"""
    ).fetchall()
    for duplicate in duplicates:
        db.execute(
            "DELETE FROM media WHERE car_id = ? AND source_id = ? AND location = ? AND id != ?",
            (duplicate["car_id"], duplicate["source_id"], duplicate["location"], duplicate["keep_id"]),
        )


def migrate_technical_specs(db: sqlite3.Connection) -> None:
    cars = db.execute("SELECT * FROM cars").fetchall()
    for car in cars:
        for field, (section, label, unit) in TECHNICAL_SPECS.items():
            value = car[field]
            if value in (None, ""):
                continue
            existing = db.execute(
                """SELECT 1 FROM attributes
                   WHERE car_id = ? AND section = ? AND label = ?
                     AND COALESCE(unit, '') = COALESCE(?, '')""",
                (car["id"], section, label, unit),
            ).fetchone()
            if not existing:
                next_sort = db.execute(
                    "SELECT COALESCE(MAX(sort_order), 0) + 10 FROM attributes WHERE car_id = ? AND section = ?",
                    (car["id"], section),
                ).fetchone()[0]
                db.execute(
                    """INSERT INTO attributes(
                           car_id,section,label,value,unit,source_id,scope_level,sort_order
                       ) VALUES(?,?,?,?,?,?,?,?)""",
                    (car["id"], section, label, str(value), unit, car["primary_source_id"], "Variant", next_sort),
                )
        populated_fields = [field for field in TECHNICAL_SPECS if car[field] is not None]
        if populated_fields:
            assignments = ", ".join(f"{field} = NULL" for field in populated_fields)
            db.execute(f"UPDATE cars SET {assignments} WHERE id = ?", (car["id"],))


def sync_technical_attributes(db: sqlite3.Connection, car_id: str, form: dict[str, str]) -> None:
    car = db.execute("SELECT primary_source_id FROM cars WHERE id = ?", (car_id,)).fetchone()
    source_id = car["primary_source_id"] if car else None
    for field, (section, label, unit) in TECHNICAL_SPECS.items():
        value = form.get(field)
        if value in (None, ""):
            continue
        existing = db.execute(
            """SELECT id FROM attributes
               WHERE car_id = ? AND section = ? AND label = ?
                 AND COALESCE(unit, '') = COALESCE(?, '')
               ORDER BY id LIMIT 1""",
            (car_id, section, label, unit),
        ).fetchone()
        if existing:
            db.execute(
                "UPDATE attributes SET value = ?, source_id = COALESCE(source_id, ?) WHERE id = ?",
                (value, source_id, existing[0]),
            )
        else:
            next_sort = db.execute(
                "SELECT COALESCE(MAX(sort_order), 0) + 10 FROM attributes WHERE car_id = ? AND section = ?",
                (car_id, section),
            ).fetchone()[0]
            db.execute(
                """INSERT INTO attributes(
                       car_id,section,label,value,unit,source_id,scope_level,sort_order
                   ) VALUES(?,?,?,?,?,?,?,?)""",
                (car_id, section, label, value, unit, source_id, "Variant", next_sort),
            )


def initialize_database() -> None:
    ASSET_DIR.mkdir(exist_ok=True)
    with connect() as db:
        db.executescript(SCHEMA)
        migrate_schema(db)
        db.execute(
            """INSERT INTO meta(key, value) VALUES('schema_version', '3')
               ON CONFLICT(key) DO UPDATE SET value=excluded.value
               WHERE meta.value != excluded.value"""
        )
        count = db.execute("SELECT COUNT(*) FROM cars").fetchone()[0]
        if count == 0:
            seed_lfa(db)
        seed_missing_lfa_details(db)
        migrate_hierarchy(db)
        migrate_source_references(db)
        migrate_technical_specs(db)
        localize_lfa_media(db)
        deduplicate_media(db)
        db.execute("UPDATE color_records SET scope_level = 'Model family' WHERE car_id = 'LEX-LFA-STD' AND scope_level != 'Model family'")
        db.execute("UPDATE country_distribution SET scope_level = 'Model family' WHERE car_id = 'LEX-LFA-STD' AND scope_level != 'Model family'")
        db.execute("UPDATE facts SET scope_level = 'Generation' WHERE car_id = 'LEX-LFA-STD' AND scope_level != 'Generation'")
        db.execute("PRAGMA optimize")


def seed_lfa(db: sqlite3.Connection) -> None:
    car_id = "LEX-LFA-STD"
    db.execute(
        """
        INSERT INTO cars (
            id, manufacturer, model_family, generation, variant,
            model_year_from, model_year_to, production_start, production_end,
            body_style, category, road_legal, origin_country, engine_code,
            engine_configuration, displacement_cc, aspiration, power_kw,
            torque_nm, transmission, drivetrain, curb_weight_kg,
            zero_to_100_s, top_speed_kmh, production_total, production_scope,
            specification_market, summary, primary_source_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            car_id, "Lexus", "LFA", "First / only production generation", "Standard",
            2012, 2012, "2010-12", "2012-12", "2-door coupe", "Supercar", 1,
            "Japan", "1LR-GUE", "4.8 L naturally aspirated DOHC V10", 4805,
            "Naturally aspirated", 412, 480, "6-speed ASG automated sequential",
            "Front-engine, rear-wheel drive", 1480, 3.7, 325, 500,
            "All LFA variants combined", "Europe",
            "Lexus's limited-production, carbon-fiber V10 supercar. European-market specifications are used for this record.",
            "https://global.toyota/en/detail/308263",
        ),
    )


def seed_missing_lfa_details(db: sqlite3.Connection) -> None:
    car_id = "LEX-LFA-STD"
    if not db.execute("SELECT 1 FROM cars WHERE id = ?", (car_id,)).fetchone():
        return
    toyota = "https://global.toyota/en/detail/308263"
    lexus_media = "https://media.lexus.co.uk/lexus-lfa/"
    details = [
        ("Identity", "Manufacturer", "Lexus", None, toyota, 10),
        ("Identity", "Model family", "LFA", None, toyota, 20),
        ("Identity", "Variant", "Standard production model", None, toyota, 30),
        ("Identity", "Body style", "Two-seat, two-door coupe", None, toyota, 40),
        ("Identity", "Country of origin", "Japan", None, toyota, 50),
        ("Powertrain", "Engine code", "1LR-GUE", None, toyota, 10),
        ("Powertrain", "Configuration", "Naturally aspirated DOHC V10", None, toyota, 20),
        ("Powertrain", "Displacement", "4,805", "cc", toyota, 30),
        ("Powertrain", "Maximum power", "412", "kW", toyota, 40),
        ("Powertrain", "Maximum power", "560", "PS", toyota, 50),
        ("Powertrain", "Power peak", "8,700", "rpm", toyota, 60),
        ("Powertrain", "Maximum torque", "480", "Nm", toyota, 70),
        ("Powertrain", "Torque peak", "6,800", "rpm", toyota, 80),
        ("Powertrain", "Redline", "9,000", "rpm", toyota, 90),
        ("Powertrain", "Transmission", "Six-speed ASG automated sequential", None, toyota, 100),
        ("Powertrain", "Driven wheels", "Rear", None, toyota, 110),
        ("Performance", "0–100 km/h", "3.7", "seconds", toyota, 10),
        ("Performance", "Maximum speed", "325", "km/h", toyota, 20),
        ("Performance", "Power-to-weight", "278.4", "kW/tonne", toyota, 30),
        ("Dimensions", "Length", "4,505", "mm", toyota, 10),
        ("Dimensions", "Width", "1,895", "mm", toyota, 20),
        ("Dimensions", "Height", "1,220", "mm", toyota, 30),
        ("Dimensions", "Wheelbase", "2,605", "mm", toyota, 40),
        ("Dimensions", "Front track", "1,580", "mm", toyota, 50),
        ("Dimensions", "Rear track", "1,570", "mm", toyota, 60),
        ("Dimensions", "Vehicle weight", "1,480", "kg", toyota, 70),
        ("Dimensions", "Weight distribution", "48:52", "front:rear", toyota, 80),
        ("Chassis & dynamics", "Cabin structure", "Carbon-fiber-reinforced plastic", None, toyota, 10),
        ("Chassis & dynamics", "Front suspension", "Double wishbone", None, toyota, 20),
        ("Chassis & dynamics", "Rear suspension", "Multilink", None, toyota, 30),
        ("Chassis & dynamics", "Brakes", "Carbon ceramic material discs", None, toyota, 40),
        ("Chassis & dynamics", "Front tires", "265/35 ZR20 (95Y)", None, toyota, 50),
        ("Chassis & dynamics", "Rear tires", "305/30 ZR20 (99Y)", None, toyota, 60),
        ("Chassis & dynamics", "Aerodynamics", "Flat underbody, diffuser and speed-controlled rear wing", None, toyota, 70),
        ("Production & rarity", "Total announced production", "500", "cars", toyota, 10),
        ("Production & rarity", "Production period", "December 2010 – December 2012", None, toyota, 20),
        ("Production & rarity", "Announced US MSRP", "375,000", "USD", "https://pressroom.lexus.com/?generate_pdf=54738", 30),
        ("Technology & experience", "Instrument display", "Color TFT with LCD tachometer needle and movable ring", None, lexus_media, 10),
        ("Technology & experience", "Throttle system", "Ten individually controlled electronic throttle bodies", None, toyota, 20),
        ("Technology & experience", "Exhaust", "Equal-length manifolds and dual exhaust with titanium main muffler", None, toyota, 30),
        ("Technology & experience", "Driving modes", "Four selectable modes with seven shift-speed settings", None, toyota, 40),
    ]
    if db.execute("SELECT COUNT(*) FROM attributes WHERE car_id = ?", (car_id,)).fetchone()[0] == 0:
        db.executemany(
            """INSERT INTO attributes(car_id, section, label, value, unit, source_url, sort_order)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [(car_id, *row) for row in details],
        )

    facts = [
        ("LCD tachometer needle", "Instrumentation",
         "The instrument panel combines an LCD display with a color TFT and uses an LCD tachometer needle; the display turns red above 9,000 rpm.",
         "It communicates the unusually fast-revving character of the V10 and supports rapid shift decisions.",
         "https://media.lexus.co.uk/lexus-lfa/", "High"),
        ("Lexus-developed CFRP cabin", "Materials",
         "Lexus developed its own carbon-fiber-reinforced-plastic production and joining technology for the LFA cabin, reported as 100 kg lighter than a comparable aluminum cabin.",
         "The program developed manufacturing expertise as well as reducing vehicle mass.",
         "https://global.toyota/en/detail/308263", "High"),
        ("Compact 9,000-rpm V10", "Engine",
         "The 4.8-liter 1LR-GUE V10 uses titanium valves, lightweight rocker arms and ten individually controlled throttle bodies, with a 9,000-rpm redline.",
         "The design prioritizes response, compact packaging and a wide high-rpm operating range.",
         "https://global.toyota/en/detail/308263", "High"),
        ("Engine sound was deliberately engineered", "Sound engineering",
         "Equal-length exhaust manifolds, an equal-length dual exhaust and an acoustically tuned surge tank were coordinated to shape the induction and exhaust sound.",
         "Sound was treated as an engineering output, not merely a by-product.",
         "https://global.toyota/en/detail/308263", "High"),
    ]
    if db.execute("SELECT COUNT(*) FROM facts WHERE car_id = ?", (car_id,)).fetchone()[0] == 0:
        db.executemany(
            """INSERT INTO facts(car_id, title, category, explanation, why_it_matters, source_url, confidence)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [(car_id, *row) for row in facts],
        )

    prices = [
        ("2010", "Announced MSRP", 375000, "USD", "United States", "Lexus", None, None,
         "https://pressroom.lexus.com/?generate_pdf=54738", "Base MSRP; options and taxes excluded."),
        ("2013", "Auction sale", 319000, "USD", "United States", "RM Sotheby's Fort Lauderdale", "LFA 069", "400 miles",
         "https://rmsothebys.com/auctions/fl13/lots/r319-2012-lexus-lfa/", "Individual vehicle; not directly comparable."),
        ("2018", "Auction sale", 434000, "USD", "United States", "RM Sotheby's Monterey", "LFA 479", "Just over 120 miles",
         "https://rmsothebys.com/auctions/mo18/lots/r0147-2012-lexus-lfa/", "Individual vehicle; not directly comparable."),
        ("2021", "Auction sale", 720000, "USD", "United States", "RM Sotheby's Amelia Island", "LFA 430", "Under 500 miles",
         "https://rmsothebys.com/auctions/am21/lots/r0026-2012-lexus-lfa/", "Individual vehicle; not directly comparable."),
        ("2021", "Auction sale", 819000, "USD", "United States", "RM Sotheby's Monterey", "LFA 054", "Under 3,850 miles",
         "https://backoffice.rmsothebys.com/auctions/mo21/lots/r0064-2012-lexus-lfa/", "Individual vehicle; not directly comparable."),
        ("2023", "Auction sale", 675000, "USD", "United States", "RM Sotheby's Arizona", "LFA 075", "Under 7,400 miles",
         "https://rmsothebys.com/auctions/az23/lots/r0003-2012-lexus-lfa/", "Individual vehicle; not directly comparable."),
        ("2023", "Auction sale", 1105000, "USD", "United States", "RM Sotheby's Monterey", "LFA 188", None,
         "https://rmsothebys.com/auctions/mo23/lots/r0025-2012-lexus-lfa/", "Individual vehicle; not directly comparable."),
    ]
    if db.execute("SELECT COUNT(*) FROM price_records WHERE car_id = ?", (car_id,)).fetchone()[0] == 0:
        db.executemany(
            """INSERT INTO price_records(
                   car_id, observation_date, price_type, amount, currency, market,
                   venue, serial_number, mileage, source_url, notes
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [(car_id, *row) for row in prices],
        )

    sources = [
        ("Toyota Motor Corporation", "Lexus Debuts LFA", "Manufacturer release",
         "https://global.toyota/en/detail/308263", "Primary specifications and engineering information."),
        ("Lexus UK Media", "Lexus LFA", "Manufacturer media guide",
         "https://media.lexus.co.uk/lexus-lfa/", "Instrumentation and detailed technical description."),
        ("Lexus USA Newsroom", "Lexus Announces Price of All-New LFA Supercar", "Manufacturer pricing release",
         "https://pressroom.lexus.com/?generate_pdf=54738", "US MSRP."),
    ]
    if db.execute("SELECT COUNT(*) FROM sources WHERE car_id = ?", (car_id,)).fetchone()[0] == 0:
        db.executemany(
            """INSERT INTO sources(car_id, publisher, title, source_type, url, notes)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [(car_id, *row) for row in sources],
        )

    if db.execute("SELECT COUNT(*) FROM media WHERE car_id = ?", (car_id,)).fetchone()[0] == 0:
        db.execute(
            """INSERT INTO media(
                   car_id, media_type, location, caption, creator, license, source_url, is_primary
               ) VALUES (?, ?, ?, ?, ?, ?, ?, 1)""",
            (
                car_id,
                "Exterior image",
                "https://commons.wikimedia.org/wiki/Special:Redirect/file/Lexus%20LFA%20%285220373328%29.jpg",
                "Standard Lexus LFA at the 2010 Greater Los Angeles Auto Show",
                "Christian Flores / CFlo Photography",
                "CC BY-SA 2.0",
                "https://commons.wikimedia.org/wiki/File:Lexus_LFA_(5220373328).jpg",
            ),
        )

    gallery = [
        (
            "Interior image",
            "https://commons.wikimedia.org/wiki/Special:Redirect/file/Lexus%20LFA%20interior%20%284275610758%29.jpg",
            "LFA cockpit and digital instrument display",
            "Jay Clark",
            "CC BY 2.0",
            "https://commons.wikimedia.org/wiki/File:Lexus_LFA_interior_(4275610758).jpg",
        ),
        (
            "Rear image",
            "https://commons.wikimedia.org/wiki/Special:Redirect/file/The%20rearview%20of%20Lexus%20LFA.JPG",
            "Rear three-quarter view of a red Lexus LFA",
            "Tokumeigakarinoaoshima",
            "CC0 1.0",
            "https://commons.wikimedia.org/wiki/File:The_rearview_of_Lexus_LFA.JPG",
        ),
        (
            "Engine image",
            "https://commons.wikimedia.org/wiki/Special:Redirect/file/Lexus%20LFA%20010%20engine.JPG",
            "The 1LR-GUE V10 engine",
            "Tennen-Gas / Altair78",
            "CC BY-SA 3.0",
            "https://commons.wikimedia.org/wiki/File:Lexus_LFA_010_engine.JPG",
        ),
    ]
    for row in gallery:
        if not db.execute(
            """SELECT 1 FROM media m LEFT JOIN sources s ON s.id=m.source_id
               WHERE m.car_id = ? AND (m.location = ? OR m.source_url = ? OR s.url = ?)""",
            (car_id, row[1], row[5], row[5]),
        ).fetchone():
            db.execute(
                """INSERT INTO media(car_id,media_type,location,caption,creator,license,source_url,is_primary)
                   VALUES(?,?,?,?,?,?,?,0)""",
                (car_id, *row),
            )

    color_source = "https://pressroom.lexus.com/lexus-introduces-2012-lfa-nurburgring-package/"
    colors = [
        ("Whitest White", None, "Exterior", "#f1f0e8", "Nürburgring Package palette", None, None, "50-package production run", color_source, "Manufacturer reported", "Availability verified; individual production count not published."),
        ("Orange", None, "Exterior", "#e6531f", "Nürburgring Package palette", None, None, "50-package production run", color_source, "Manufacturer reported", "Availability verified; individual production count not published."),
        ("Black", None, "Exterior", "#161616", "Nürburgring Package palette", None, None, "50-package production run", color_source, "Manufacturer reported", "Availability verified; individual production count not published."),
        ("Matte Black", None, "Exterior", "#343434", "Nürburgring Package palette", None, None, "50-package production run", color_source, "Manufacturer reported", "Availability verified; individual production count not published."),
        ("Black", None, "Interior", "#171717", "Nürburgring Package palette", None, None, "50-package production run", color_source, "Manufacturer reported", None),
        ("Red", None, "Interior", "#9f2324", "Nürburgring Package palette", None, None, "50-package production run", color_source, "Manufacturer reported", None),
        ("Violet", None, "Interior", "#59415f", "Nürburgring Package palette", None, None, "50-package production run", color_source, "Manufacturer reported", None),
    ]
    if db.execute("SELECT COUNT(*) FROM color_records WHERE car_id = ?", (car_id,)).fetchone()[0] == 0:
        db.executemany(
            """INSERT INTO color_records(
                   car_id,color_name,color_code,color_type,swatch_hex,availability_scope,
                   production_count,production_percentage,count_scope,source_url,confidence,notes
               ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
            [(car_id, *row) for row in colors],
        )

    delivery_source = "https://media.lexus.co.uk/final-lexus-lfa-delivery-in-europe/"
    geography = [
        ("Original delivery · global region", "Europe", "Europe", 40, 8.0, 500, "2013-03-26", delivery_source, "Manufacturer reported", "Forty of the 500 completed cars were delivered to European clients."),
        ("Original delivery · European market", "Germany", "Europe", 15, 37.5, 40, "2013-03-26", delivery_source, "Manufacturer reported", "Largest European LFA market."),
        ("Original delivery · European market", "Switzerland", "Europe", 6, 15.0, 40, "2013-03-26", delivery_source, "Manufacturer reported", None),
        ("Original delivery · European market", "United Kingdom", "Europe", 5, 12.5, 40, "2013-03-26", delivery_source, "Manufacturer reported", None),
        ("Original delivery · European market", "Netherlands", "Europe", 4, 10.0, 40, "2013-03-26", delivery_source, "Manufacturer reported", None),
        ("Original delivery · European market", "France", "Europe", 3, 7.5, 40, "2013-03-26", delivery_source, "Manufacturer reported", "The source names the five largest markets; seven other European deliveries are not broken out by country."),
    ]
    if db.execute("SELECT COUNT(*) FROM country_distribution WHERE car_id = ?", (car_id,)).fetchone()[0] == 0:
        db.executemany(
            """INSERT INTO country_distribution(
                   car_id,distribution_type,country,region,vehicle_count,share_percentage,
                   denominator,as_of_date,source_url,confidence,notes
               ) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
            [(car_id, *row) for row in geography],
        )


def esc(value: object | None) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def value_or_dash(value: object | None, suffix: str = "") -> str:
    if value in (None, ""):
        return '<span class="muted">—</span>'
    return f"{esc(value)}{esc(suffix)}"


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} · Supercar Archive</title>
  <style>
    :root {{ --ink:#101826; --muted:#667085; --paper:#f5f2eb; --card:#fffdf8;
      --line:#ded9cf; --accent:#a63d2f; --accent2:#183b49; --gold:#b78b43; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font:15px/1.5 Inter,Segoe UI,Arial,sans-serif; color:var(--ink); background:var(--paper); }}
    a {{ color:var(--accent2); }}
    header {{ background:var(--ink); color:white; padding:18px 0; border-bottom:4px solid var(--gold); }}
    .wrap {{ width:min(1280px, calc(100% - 36px)); margin:auto; }}
    .brand {{ display:flex; align-items:center; justify-content:space-between; gap:16px; }}
    .brand a {{ color:white; text-decoration:none; font:700 20px Georgia,serif; letter-spacing:.4px; }}
    nav a {{ font:600 14px Inter,Arial,sans-serif; margin-left:18px; }}
    main {{ padding:28px 0 56px; }}
    h1,h2,h3 {{ font-family:Georgia,serif; line-height:1.15; margin-top:0; }}
    h1 {{ font-size:34px; margin-bottom:8px; }} h2 {{ font-size:23px; }} h3 {{ font-size:18px; }}
    .eyebrow {{ color:var(--accent); font-weight:800; text-transform:uppercase; letter-spacing:.1em; font-size:12px; }}
    .muted {{ color:var(--muted); }} .small {{ font-size:12px; }}
    .toolbar {{ display:flex; flex-wrap:wrap; gap:12px; align-items:center; justify-content:space-between; margin:20px 0; }}
    .search {{ display:flex; gap:8px; flex:1; max-width:680px; }}
    input,select,textarea {{ width:100%; padding:10px 11px; border:1px solid #cfc8bc; border-radius:7px; background:white; color:var(--ink); font:inherit; }}
    textarea {{ min-height:92px; resize:vertical; }}
    button,.button {{ display:inline-block; border:0; border-radius:7px; padding:10px 15px; background:var(--accent); color:white; font-weight:700; text-decoration:none; cursor:pointer; }}
    .button.secondary, button.secondary {{ background:var(--accent2); }}
    .button.ghost {{ background:transparent; color:var(--accent2); border:1px solid var(--line); }}
    .card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:20px; box-shadow:0 3px 12px rgba(16,24,38,.04); }}
    .stats {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; margin:18px 0; }}
    .stat strong {{ display:block; font:700 26px Georgia,serif; }}
    .catalog-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:16px; margin:18px 0 26px; }}
    .car-card {{ padding:0; overflow:hidden; text-decoration:none; color:var(--ink); transition:transform .18s ease,box-shadow .18s ease; }}
    .car-card:hover {{ transform:translateY(-3px); box-shadow:0 10px 24px rgba(16,24,38,.11); }}
    .car-card img {{ width:100%; aspect-ratio:16/9; object-fit:cover; display:block; background:#d9d5cc; }}
    .car-card-body {{ padding:16px; }} .car-card h3 {{ margin:5px 0 4px; font-size:21px; }}
    .mini-specs {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:13px; }}
    .mini-specs span {{ background:#eee8de; border-radius:999px; padding:5px 9px; font-size:12px; font-weight:700; }}
    .manufacturer-strip {{ display:grid; grid-auto-flow:column; grid-auto-columns:minmax(215px,1fr); gap:12px; overflow-x:auto; padding:2px 2px 10px; margin:12px 0 24px; scroll-snap-type:x proximity; }}
    .manufacturer-card {{ scroll-snap-align:start; min-height:118px; display:flex; flex-direction:column; justify-content:space-between; color:var(--ink); text-decoration:none; background:linear-gradient(145deg,var(--card),#eee8de); }}
    .manufacturer-card:hover {{ border-color:var(--gold); }}
    .manufacturer-card h3 {{ font-size:21px; margin:5px 0; }}
    .manufacturer-meta {{ display:flex; justify-content:space-between; gap:8px; color:var(--muted); font-size:12px; }}
    .filter-panel {{ padding:16px; margin:20px 0 14px; }}
    .filter-search {{ display:grid; grid-template-columns:1fr auto; gap:8px; margin-bottom:12px; }}
    .filter-search input {{ font-size:16px; padding:12px 13px; }}
    .quick-filters,.advanced-filter-grid {{ display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:10px; }}
    .filter-field label {{ display:block; margin-bottom:4px; color:var(--muted); font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:.04em; }}
    .filter-panel details {{ box-shadow:none; margin:12px 0 0; background:#f8f4ed; }}
    .filter-panel details form {{ padding:0; }}
    .advanced-filter-grid {{ padding:0 14px 14px; grid-template-columns:repeat(4,minmax(0,1fr)); }}
    .range-pair {{ display:grid; grid-template-columns:1fr 1fr; gap:7px; }}
    .check-grid {{ display:flex; flex-wrap:wrap; gap:9px; grid-column:1/-1; }}
    .check-option {{ display:flex; align-items:center; gap:7px; padding:8px 10px; border:1px solid var(--line); border-radius:7px; background:white; font-size:13px; font-weight:700; }}
    .check-option input {{ width:auto; margin:0; }}
    .filter-actions {{ display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px; margin-top:13px; }}
    .filter-actions-left {{ display:flex; flex-wrap:wrap; gap:8px; }}
    .filter-note {{ color:var(--muted); font-size:12px; }}
    .result-bar {{ display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px; margin:16px 0 8px; }}
    .result-tools {{ display:flex; align-items:center; gap:8px; }}
    .view-switch {{ display:flex; border:1px solid var(--line); border-radius:7px; overflow:hidden; background:var(--card); }}
    .view-switch a {{ padding:7px 10px; text-decoration:none; font-size:12px; font-weight:800; border-right:1px solid var(--line); }}
    .view-switch a:last-child {{ border-right:0; }} .view-switch a.active {{ color:white; background:var(--accent2); }}
    .filter-chips {{ display:flex; flex-wrap:wrap; gap:7px; margin:8px 0 14px; }}
    .filter-chip {{ display:inline-flex; align-items:center; gap:6px; padding:6px 9px; border-radius:999px; background:#e8e1d5; color:var(--ink); text-decoration:none; font-size:12px; font-weight:750; }}
    .filter-chip b {{ color:var(--accent); font-size:15px; line-height:1; }}
    .coverage-note {{ margin:10px 0 0; padding:9px 11px; border-left:3px solid var(--gold); background:#f4eee3; color:#65594b; font-size:12px; }}
    .pagination {{ display:flex; flex-wrap:wrap; justify-content:center; gap:6px; margin:22px 0; }}
    .pagination a,.pagination span {{ min-width:35px; padding:7px 9px; text-align:center; border:1px solid var(--line); border-radius:7px; background:var(--card); text-decoration:none; font-weight:750; }}
    .pagination span {{ color:white; background:var(--accent2); }}
    .table-wrap {{ overflow:auto; border:1px solid var(--line); border-radius:10px; background:var(--card); }}
    table {{ width:100%; border-collapse:collapse; white-space:nowrap; }}
    th {{ text-align:left; font-size:12px; text-transform:uppercase; letter-spacing:.06em; color:#5f5549; background:#eee8de; }}
    th,td {{ padding:12px 14px; border-bottom:1px solid var(--line); }} tr:last-child td {{ border-bottom:0; }}
    tbody tr:hover {{ background:#faf6ef; }}
    .car-link {{ font-weight:800; text-decoration:none; }}
    .hero {{ display:grid; grid-template-columns:minmax(340px,1.1fr) minmax(340px,1fr); gap:22px; align-items:stretch; margin:20px 0; }}
    .hero-image {{ min-height:360px; background:#d8d4cc; border-radius:10px; overflow:hidden; border:1px solid var(--line); }}
    .hero-image img {{ width:100%; height:100%; object-fit:cover; display:block; }}
    .breadcrumb {{ display:flex; flex-wrap:wrap; gap:7px; align-items:center; color:var(--muted); font-size:13px; margin-bottom:12px; }}
    .breadcrumb a {{ text-decoration:none; font-weight:700; }} .breadcrumb span {{ color:#aaa096; }}
    .gallery-main {{ position:relative; }}
    .gallery-count {{ position:absolute; right:12px; bottom:12px; padding:5px 9px; border-radius:999px; color:white; background:rgba(16,24,38,.78); font-size:12px; font-weight:800; }}
    .gallery-caption {{ min-height:36px; margin:8px 2px 0; }}
    .gallery-strip {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; margin-top:10px; }}
    .gallery-thumb {{ position:relative; padding:0; overflow:hidden; border:2px solid transparent; border-radius:8px; background:#d8d4cc; aspect-ratio:4/3; }}
    .gallery-thumb:hover,.gallery-thumb.active {{ border-color:var(--accent); transform:none; }}
    .gallery-thumb img {{ width:100%; height:100%; object-fit:cover; display:block; }}
    .gallery-thumb span {{ position:absolute; left:5px; bottom:5px; padding:2px 6px; background:rgba(16,24,38,.78); color:white; border-radius:4px; font-size:10px; }}
    .specs {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1px; background:var(--line); border:1px solid var(--line); border-radius:8px; overflow:hidden; }}
    .spec {{ background:var(--card); padding:11px 13px; }} .spec span {{ display:block; color:var(--muted); font-size:12px; }}
    .section {{ margin-top:28px; }}
    .anchor-nav {{ position:sticky; top:0; z-index:10; display:flex; gap:6px; overflow:auto; padding:9px; margin:0 0 22px; background:rgba(245,242,235,.94); border:1px solid var(--line); border-radius:10px; backdrop-filter:blur(10px); }}
    .anchor-nav a {{ flex:0 0 auto; padding:7px 10px; border-radius:7px; text-decoration:none; font-size:12px; font-weight:800; }}
    .anchor-nav a:hover {{ background:#e8e1d5; }}
    .section-head {{ display:flex; align-items:end; justify-content:space-between; gap:10px; margin-bottom:12px; }}
    .attribute-sections {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }}
    .attribute-card h3 {{ padding-bottom:10px; border-bottom:1px solid var(--line); margin-bottom:4px; }}
    .attribute-row {{ display:grid; grid-template-columns:minmax(110px,.8fr) 1.2fr; gap:14px; padding:9px 0; border-bottom:1px solid #eee9df; }}
    .attribute-row:last-child {{ border-bottom:0; }} .attribute-label {{ color:var(--muted); font-size:13px; }}
    .attribute-value {{ font-weight:750; text-align:right; }} .attribute-value a {{ margin-left:5px; font-size:11px; }}
    .fact-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }}
    .fact {{ border-left:4px solid var(--gold); }}
    .pill {{ display:inline-block; padding:3px 8px; border-radius:999px; background:#ece6db; color:#574c41; font-size:11px; font-weight:700; }}
    .confidence {{ background:#e5f1eb; color:#2d6247; }}
    .scope {{ background:#e7edf4; color:#334f70; }}
    .record-actions {{ display:flex; align-items:center; gap:9px; margin-top:9px; font-size:12px; }}
    .record-actions a {{ font-weight:800; text-decoration:none; }}
    form.inline {{ display:inline; padding:0; margin:0; }}
    button.link-danger {{ display:inline; padding:0; border:0; background:transparent; color:#a32f2f; font:800 12px/1.4 Inter,Arial,sans-serif; }}
    .evidence-strip {{ display:flex; flex-wrap:wrap; gap:7px; align-items:center; margin-top:12px; padding:10px 12px; border:1px solid var(--line); border-radius:8px; background:#f1ede5; font-size:12px; }}
    .evidence-strip a {{ font-weight:750; text-decoration:none; }}
    .family-flow {{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; }}
    .family-node {{ padding:10px 13px; border:1px solid var(--line); border-radius:8px; background:var(--card); font-weight:800; }}
    .family-arrow {{ color:var(--gold); font-weight:900; }}
    .family-list {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:10px; margin-top:14px; }}
    .family-variant {{ text-decoration:none; color:var(--ink); }} .family-variant.current {{ border-color:var(--gold); box-shadow:inset 0 0 0 1px var(--gold); }}
    .color-grid {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; }}
    .color-card {{ padding:12px; }} .color-swatch {{ height:74px; border-radius:7px; border:1px solid rgba(16,24,38,.16); margin-bottom:10px; }}
    .color-card h3 {{ margin:0 0 3px; font-size:16px; }} .color-card p {{ margin:4px 0; }}
    .distribution-groups {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }}
    .distribution-row {{ margin:13px 0; }}
    .distribution-label {{ display:flex; justify-content:space-between; gap:10px; margin-bottom:5px; }}
    .distribution-track {{ height:9px; background:#ebe5db; border-radius:99px; overflow:hidden; }}
    .distribution-fill {{ height:100%; border-radius:99px; background:linear-gradient(90deg,var(--accent2),#3f7887); }}
    .empty-state {{ padding:22px; border:1px dashed #c9c0b3; border-radius:9px; text-align:center; color:var(--muted); background:rgba(255,255,255,.35); }}
    .market-overview {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; margin-bottom:14px; }}
    .market-number strong {{ display:block; font:700 29px Georgia,serif; margin-top:4px; }}
    .price-bars {{ display:flex; align-items:end; gap:8px; height:190px; padding:16px 14px 8px; border-bottom:1px solid var(--line); }}
    .price-bar-item {{ flex:1; min-width:42px; height:100%; display:flex; flex-direction:column; justify-content:end; align-items:center; gap:5px; }}
    .price-bar {{ width:min(38px,80%); border-radius:5px 5px 0 0; background:linear-gradient(180deg,var(--gold),var(--accent)); min-height:4px; }}
    .price-bar-item small {{ font-size:10px; color:var(--muted); }}
    details {{ margin-top:14px; border:1px solid var(--line); border-radius:9px; background:var(--card); }}
    summary {{ cursor:pointer; padding:13px 16px; font-weight:800; }}
    details form {{ padding:0 16px 16px; }}
    .form-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:13px; }}
    .field.full {{ grid-column:1/-1; }} label {{ display:block; font-weight:700; margin-bottom:5px; font-size:13px; }}
    .form-actions {{ grid-column:1/-1; display:flex; gap:10px; margin-top:5px; }}
    .notice {{ padding:12px 14px; border-radius:8px; background:#fff5dc; border:1px solid #e5c98e; }}
    @media (max-width:1100px) {{ .quick-filters {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} .advanced-filter-grid {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} }}
    @media (max-width:1000px) {{ .color-grid {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} .family-list {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
    @media (max-width:900px) {{ .catalog-grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
    @media (max-width:800px) {{ .hero,.fact-grid,.form-grid,.stats,.attribute-sections,.market-overview,.distribution-groups {{ grid-template-columns:1fr; }} .catalog-grid,.family-list {{ grid-template-columns:1fr; }} .quick-filters,.advanced-filter-grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} .color-grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} .hero-image {{ min-height:260px; }} h1 {{ font-size:29px; }} .attribute-row {{ grid-template-columns:1fr; gap:3px; }} .attribute-value {{ text-align:left; }} .gallery-strip {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} }}
    @media (max-width:560px) {{ .quick-filters,.advanced-filter-grid,.filter-search {{ grid-template-columns:1fr; }} .filter-search button {{ width:100%; }} .result-bar,.filter-actions {{ align-items:stretch; }} .result-tools {{ justify-content:space-between; width:100%; }} }}
    @media (max-width:480px) {{ .color-grid {{ grid-template-columns:1fr; }} .gallery-strip {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} .wrap {{ width:min(100% - 22px,1280px); }} }}
  </style>
</head>
<body>
  <header><div class="wrap brand"><a href="/admin">Supercar Archive Admin</a><nav><a href="/">Public viewer</a><a href="/admin">Manage cars</a><a href="/new">Add car</a></nav></div></header>
  <main><div class="wrap">{body}</div></main>
  <script>
    document.addEventListener('click', function(event) {{
      const thumb = event.target.closest('[data-gallery-src]');
      if (!thumb) return;
      const main = document.getElementById('gallery-main-image');
      const caption = document.getElementById('gallery-caption');
      const count = document.getElementById('gallery-count');
      if (!main) return;
      document.querySelectorAll('[data-gallery-src]').forEach(item => item.classList.remove('active'));
      thumb.classList.add('active');
      main.src = thumb.dataset.gallerySrc;
      main.alt = thumb.dataset.galleryAlt || '';
      if (caption) caption.textContent = thumb.dataset.galleryCaption || '';
      if (count) count.textContent = (thumb.dataset.galleryIndex || '1') + ' of ' + count.dataset.total;
    }});
    const catalogueFilters = document.getElementById('catalog-filters');
    if (catalogueFilters) {{
      const manufacturer = catalogueFilters.querySelector('[name="manufacturer"]');
      const model = catalogueFilters.querySelector('[name="model_family"]');
      if (manufacturer && model) manufacturer.addEventListener('change', function() {{ model.value = ''; }});
      catalogueFilters.addEventListener('submit', function() {{
        catalogueFilters.querySelectorAll('input,select').forEach(function(control) {{
          const isEmpty = control.value === '' || (control.type === 'checkbox' && !control.checked);
          const isDefault = (control.name === 'view' && control.value === 'grid') || (control.name === 'sort' && control.value === 'name');
          if (isEmpty || isDefault) control.disabled = true;
        }});
      }});
    }}
  </script>
</body>
</html>"""


def get_form(handler: BaseHTTPRequestHandler) -> dict[str, str]:
    length = int(handler.headers.get("Content-Length", "0"))
    raw = handler.rfile.read(length).decode("utf-8")
    parsed = parse_qs(raw, keep_blank_values=True)
    return {key: values[0].strip() for key, values in parsed.items()}


def as_int(value: str | None) -> int | None:
    try:
        return int(value) if value not in (None, "") else None
    except ValueError:
        return None


def as_float(value: str | None) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except ValueError:
        return None


CAR_FIELDS = [
    "manufacturer", "model_family", "generation", "variant", "model_year_from", "model_year_to",
    "production_start", "production_end", "body_style", "category", "origin_country",
    "specification_market", "summary", "primary_source_url",
]

TECHNICAL_SPECS = {
    "engine_code": ("Powertrain", "Engine code", None),
    "engine_configuration": ("Powertrain", "Configuration", None),
    "displacement_cc": ("Powertrain", "Displacement", "cc"),
    "aspiration": ("Powertrain", "Aspiration", None),
    "power_kw": ("Powertrain", "Maximum power", "kW"),
    "torque_nm": ("Powertrain", "Maximum torque", "Nm"),
    "transmission": ("Powertrain", "Transmission", None),
    "drivetrain": ("Powertrain", "Drivetrain", None),
    "curb_weight_kg": ("Dimensions", "Vehicle weight", "kg"),
    "zero_to_100_s": ("Performance", "0–100 km/h", "seconds"),
    "top_speed_kmh": ("Performance", "Maximum speed", "km/h"),
    "production_total": ("Production & rarity", "Total announced production", "cars"),
    "production_scope": ("Production & rarity", "Production scope", None),
}

CHILD_CONFIG = {
    "attribute": {
        "table": "attributes", "anchor": "specifications", "title": "specification",
        "fields": [
            ("section", "Section", "text"), ("label", "Label", "text"),
            ("value", "Value", "text"), ("unit", "Unit", "text"),
            ("scope_level", "Applies to", "scope"), ("source_id", "Evidence source", "source"),
        ],
    },
    "fact": {
        "table": "facts", "anchor": "stories", "title": "engineering story",
        "fields": [
            ("title", "Title", "text"), ("category", "Category", "text"),
            ("explanation", "Explanation", "textarea"), ("why_it_matters", "Why it matters", "textarea"),
            ("confidence", "Evidence quality", "confidence"), ("scope_level", "Applies to", "scope"),
            ("source_id", "Evidence source", "source"),
        ],
    },
    "price": {
        "table": "price_records", "anchor": "market", "title": "price observation",
        "fields": [
            ("observation_date", "Date or year", "text"), ("price_type", "Price type", "text"),
            ("amount", "Amount", "float"), ("currency", "Currency", "text"),
            ("market", "Market", "text"), ("venue", "Venue", "text"),
            ("serial_number", "Serial number", "text"), ("mileage", "Mileage", "text"),
            ("notes", "Notes", "textarea"), ("source_id", "Evidence source", "source"),
        ],
    },
    "source": {
        "table": "sources", "anchor": "sources", "title": "source",
        "fields": [
            ("publisher", "Publisher", "text"), ("title", "Title", "text"),
            ("source_type", "Source type", "text"), ("url", "URL", "url"),
            ("notes", "Notes", "textarea"),
        ],
    },
    "media": {
        "table": "media", "anchor": "gallery", "title": "gallery image",
        "fields": [
            ("media_type", "View or type", "text"), ("location", "Local asset path", "text"),
            ("caption", "Caption", "text"), ("creator", "Creator", "text"),
            ("license", "License", "text"), ("is_primary", "Primary image", "boolean"),
            ("scope_level", "Applies to", "scope"), ("source_id", "Attribution source", "source"),
        ],
    },
    "color": {
        "table": "color_records", "anchor": "colors", "title": "color record",
        "fields": [
            ("color_name", "Official color name", "text"), ("color_code", "Paint / trim code", "text"),
            ("color_type", "Type", "text"), ("swatch_hex", "Swatch color", "text"),
            ("availability_scope", "Availability scope", "text"), ("production_count", "Production count", "int"),
            ("production_percentage", "Percentage", "float"), ("count_scope", "Count scope", "text"),
            ("confidence", "Evidence quality", "confidence"), ("scope_level", "Applies to", "scope"),
            ("notes", "Notes", "textarea"), ("source_id", "Evidence source", "source"),
        ],
    },
    "geography": {
        "table": "country_distribution", "anchor": "geography", "title": "geographic record",
        "fields": [
            ("distribution_type", "Distribution type", "text"), ("country", "Country or region", "text"),
            ("region", "Parent region", "text"), ("vehicle_count", "Vehicle count", "int"),
            ("share_percentage", "Share percentage", "float"), ("denominator", "Denominator", "int"),
            ("as_of_date", "As-of date", "text"), ("confidence", "Evidence quality", "confidence"),
            ("scope_level", "Applies to", "scope"), ("notes", "Notes", "textarea"),
            ("source_id", "Evidence source", "source"),
        ],
    },
}


def record_actions(car_id: str, kind: str, record_id: int, anchor: str) -> str:
    return f'''<div class="record-actions">
      <a href="/car/{quote(car_id)}/{kind}/{record_id}/edit">Edit</a>
      <form class="inline" method="post" action="/car/{quote(car_id)}/{kind}/{record_id}/delete" onsubmit="return confirm('Delete this record? This cannot be undone.')">
        <button class="link-danger" type="submit">Delete</button>
      </form>
    </div>'''


def car_form(action: str, car: sqlite3.Row | dict[str, object] | None = None, heading: str = "Add a car") -> str:
    data = dict(car) if car else {}
    def inp(name: str, label: str, input_type: str = "text", placeholder: str = "", full: bool = False) -> str:
        return f'<div class="field{" full" if full else ""}"><label for="{name}">{esc(label)}</label><input id="{name}" name="{name}" type="{input_type}" value="{esc(data.get(name, ""))}" placeholder="{esc(placeholder)}"></div>'

    road = int(data.get("road_legal", 1) or 0)
    return f"""
    <div class="eyebrow">Single-entry workflow</div>
    <h1>{esc(heading)}</h1>
    <p class="muted">Create one sellable model-year variant. Unknown optional fields can remain blank.</p>
    <form method="post" action="{esc(action)}" class="card form-grid">
      {inp('manufacturer','Manufacturer','text','Lexus')}
      {inp('model_family','Model family','text','LFA')}
      {inp('generation','Generation','text','992.2')}
      {inp('variant','Variant / trim','text','GT3')}
      {inp('model_year_from','Model year from','number','2025')}
      {inp('model_year_to','Model year to','number','2025')}
      {inp('production_start','Production start','text','2024-09')}
      {inp('production_end','Production end','text','2026-06')}
      {inp('body_style','Body style','text','2-door coupe')}
      <div class="field"><label for="category">Category</label><select id="category" name="category">
        {''.join(f'<option value="{esc(option)}" {"selected" if data.get("category") == option else ""}>{esc(option)}</option>' for option in ['', 'Sports car', 'Supercar', 'Hypercar', 'GT', 'Track-only', 'Race car', 'Concept'])}
      </select></div>
      {inp('origin_country','Country of origin','text','Japan')}
      <div class="field"><label for="road_legal">Road legal</label><select id="road_legal" name="road_legal"><option value="1" {'selected' if road else ''}>Yes</option><option value="0" {'selected' if not road else ''}>No</option></select></div>
      {inp('engine_code','Engine code','text','1LR-GUE')}
      {inp('engine_configuration','Engine configuration','text','4.8 L naturally aspirated V10')}
      {inp('displacement_cc','Displacement (cc)','number','4805')}
      {inp('aspiration','Aspiration','text','Naturally aspirated')}
      {inp('power_kw','Power (kW)','number','412')}
      {inp('torque_nm','Torque (Nm)','number','480')}
      {inp('transmission','Transmission','text','6-speed automated sequential')}
      {inp('drivetrain','Drivetrain','text','Front-engine, rear-wheel drive')}
      {inp('curb_weight_kg','Curb weight (kg)','number','1480')}
      {inp('zero_to_100_s','0–100 km/h (seconds)','number','3.7')}
      {inp('top_speed_kmh','Top speed (km/h)','number','325')}
      {inp('production_total','Production total','number','500')}
      {inp('production_scope','Production-count scope','text','All variants combined')}
      {inp('specification_market','Specification market','text','Europe')}
      <div class="field full"><label for="summary">Short summary</label><textarea id="summary" name="summary">{esc(data.get('summary',''))}</textarea></div>
      {inp('primary_source_url','Primary source URL','url','https://manufacturer.example/car',True)}
      <div class="form-actions"><button type="submit">Save car</button><a class="button ghost" href="{esc('/car/'+data['id'] if data.get('id') else '/')}">Cancel</a></div>
    </form>"""


class AppHandler(BaseHTTPRequestHandler):
    def send_html(self, content: str, status: int = 200) -> None:
        payload = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, location: str) -> None:
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        parts = [p for p in path.split("/") if p]
        if path == "/":
            self.serve_web_file("index.html")
        elif path == "/admin":
            raw_filters = parse_qs(parsed.query, keep_blank_values=True)
            self.show_index({key: values[0].strip() for key, values in raw_filters.items()})
        elif path == "/data.json":
            self.serve_data()
        elif path in {"/app.js", "/styles.css"}:
            self.serve_web_file(path.removeprefix("/"))
        elif path == "/new":
            self.send_html(page("Add car", car_form("/cars")))
        elif len(parts) == 3 and parts[0] == "car" and parts[2] == "edit":
            self.show_edit(parts[1])
        elif len(parts) == 5 and parts[0] == "car" and parts[4] == "edit":
            self.show_child_edit(parts[1], parts[2], as_int(parts[3]))
        elif len(parts) == 2 and parts[0] == "car":
            self.show_car(parts[1])
        elif path.startswith("/assets/"):
            self.serve_asset(path.removeprefix("/assets/"))
        else:
            self.send_html(page("Not found", "<h1>Not found</h1>"), 404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path == "/cars":
            self.create_car()
            return
        parts = [p for p in path.split("/") if p]
        if len(parts) == 3 and parts[0] == "car":
            car_id, action = parts[1], parts[2]
            if action == "update": self.update_car(car_id)
            elif action == "fact": self.add_fact(car_id)
            elif action == "price": self.add_price(car_id)
            elif action == "source": self.add_source(car_id)
            elif action == "media": self.add_media(car_id)
            elif action == "attribute": self.add_attribute(car_id)
            elif action == "color": self.add_color(car_id)
            elif action == "geography": self.add_geography(car_id)
            else: self.send_html(page("Not found", "<h1>Not found</h1>"), 404)
        elif len(parts) == 5 and parts[0] == "car" and parts[4] in {"update", "delete"}:
            car_id, kind, record_id, action = parts[1], parts[2], as_int(parts[3]), parts[4]
            if record_id is None or kind not in CHILD_CONFIG:
                self.send_html(page("Not found", "<h1>Record not found</h1>"), 404)
            elif action == "update":
                self.update_child(car_id, kind, record_id)
            else:
                self.delete_child(car_id, kind, record_id)
        else:
            self.send_html(page("Not found", "<h1>Not found</h1>"), 404)

    def show_index(self, filters: dict[str, str]) -> None:
        filters = {key: value for key, value in filters.items() if value != ""}
        query = filters.get("q", "")
        selected_make = filters.get("manufacturer", "")
        selected_model = filters.get("model_family", "")
        view = filters.get("view", "grid") if filters.get("view") in {"grid", "list"} else "grid"
        sort = filters.get("sort", "name")

        with connect() as db:
            catalog_rows = db.execute(
                """SELECT c.*,
                          (SELECT location FROM media m WHERE m.car_id=c.id ORDER BY is_primary DESC,id LIMIT 1) AS primary_image,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label='Maximum power' AND a.unit='kW' ORDER BY a.id LIMIT 1) AS display_power_kw,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label='Maximum torque' AND a.unit='Nm' ORDER BY a.id LIMIT 1) AS display_torque_nm,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label='Vehicle weight' AND a.unit='kg' ORDER BY a.id LIMIT 1) AS display_weight_kg,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label='0–100 km/h' ORDER BY a.id LIMIT 1) AS display_zero_to_100,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label='Maximum speed' AND a.unit='km/h' ORDER BY a.id LIMIT 1) AS display_top_speed,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label='Total announced production' ORDER BY a.id LIMIT 1) AS display_production,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label='Configuration' ORDER BY a.id LIMIT 1) AS display_configuration,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label='Aspiration' ORDER BY a.id LIMIT 1) AS display_aspiration,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label='Transmission' ORDER BY a.id LIMIT 1) AS display_transmission,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label IN ('Driven wheels','Drivetrain') ORDER BY CASE a.label WHEN 'Driven wheels' THEN 0 ELSE 1 END,a.id LIMIT 1) AS display_drivetrain,
                          (SELECT GROUP_CONCAT(a.label || ' ' || a.value,' ') FROM attributes a WHERE a.car_id=c.id) AS search_attributes,
                          (SELECT GROUP_CONCAT(f.title || ' ' || f.explanation || ' ' || COALESCE(f.why_it_matters,''),' ') FROM facts f WHERE f.car_id=c.id) AS search_facts,
                          (SELECT GROUP_CONCAT(s.publisher || ' ' || s.title,' ') FROM sources s WHERE s.car_id=c.id) AS search_sources,
                          (SELECT GROUP_CONCAT(p.venue || ' ' || COALESCE(p.serial_number,'') || ' ' || COALESCE(p.notes,''),' ') FROM price_records p WHERE p.car_id=c.id) AS search_prices,
                          (SELECT GROUP_CONCAT(r.color_name,'|') FROM color_records r WHERE r.car_id=c.id) AS search_colors,
                          (SELECT GROUP_CONCAT(g.country,'|') FROM country_distribution g WHERE g.car_id=c.id) AS search_geography,
                          (SELECT COUNT(*) FROM media m WHERE m.car_id=c.id) AS media_count,
                          (SELECT COUNT(*) FROM price_records p WHERE p.car_id=c.id) AS price_count,
                          (SELECT COUNT(*) FROM sources s WHERE s.car_id=c.id) AS source_count,
                          (SELECT COUNT(*) FROM attributes a WHERE a.car_id=c.id AND a.section='Ownership & dealer notes') AS dealer_note_count,
                          (SELECT p.amount FROM price_records p WHERE p.car_id=c.id AND p.currency='USD' ORDER BY p.observation_date DESC,p.id DESC LIMIT 1) AS latest_usd_price,
                          (SELECT p.observation_date FROM price_records p WHERE p.car_id=c.id AND p.currency='USD' ORDER BY p.observation_date DESC,p.id DESC LIMIT 1) AS latest_usd_date
                   FROM cars c
                   ORDER BY c.manufacturer,c.model_family,c.model_year_from,c.variant"""
            ).fetchall()
            all_cars = [dict(row) for row in catalog_rows]
            fact_count = db.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
            price_count = db.execute("SELECT COUNT(*) FROM price_records").fetchone()[0]
            color_options = [row[0] for row in db.execute("SELECT DISTINCT color_name FROM color_records ORDER BY color_name")]
            geography_options = [row[0] for row in db.execute("SELECT DISTINCT country FROM country_distribution ORDER BY country")]

        def number(value: object | None) -> float | None:
            try:
                return float(str(value).replace(",", "")) if value not in (None, "") else None
            except ValueError:
                return None

        def exact_values(car: dict[str, object], key: str) -> set[str]:
            return {part.strip() for part in str(car.get(key) or "").split("|") if part.strip()}

        q_tokens = [token for token in query.casefold().split() if token]
        numeric_ranges = [
            ("power_min", "power_max", "display_power_kw"),
            ("weight_min", "weight_max", "display_weight_kg"),
            ("speed_min", "speed_max", "display_top_speed"),
            ("production_min", "production_max", "display_production"),
            ("price_min", "price_max", "latest_usd_price"),
        ]

        def matches(car: dict[str, object]) -> bool:
            haystack = " ".join(str(car.get(key) or "") for key in (
                "manufacturer", "model_family", "generation", "variant", "engine_code", "body_style",
                "category", "origin_country", "summary", "search_attributes", "search_facts", "search_sources",
                "search_prices", "search_colors", "search_geography",
            )).casefold()
            if q_tokens and not all(token in haystack for token in q_tokens):
                return False
            text_filters = {
                "manufacturer": "manufacturer", "model_family": "model_family", "generation": "generation",
                "category": "category", "origin": "origin_country", "body": "body_style",
                "configuration": "display_configuration", "aspiration": "display_aspiration",
                "transmission": "display_transmission", "drivetrain": "display_drivetrain",
            }
            if any(filters.get(param) and str(car.get(column) or "") != filters[param] for param, column in text_filters.items()):
                return False
            if filters.get("color") and filters["color"] not in exact_values(car, "search_colors"):
                return False
            if filters.get("geography") and filters["geography"] not in exact_values(car, "search_geography"):
                return False
            start = as_int(filters.get("year_from"))
            end = as_int(filters.get("year_to"))
            if start and (car.get("model_year_to") is None or int(car["model_year_to"]) < start):
                return False
            if end and (car.get("model_year_from") is None or int(car["model_year_from"]) > end):
                return False
            if filters.get("road_legal") in {"1", "0"} and int(car.get("road_legal") or 0) != int(filters["road_legal"]):
                return False
            for minimum_key, maximum_key, column in numeric_ranges:
                minimum = as_float(filters.get(minimum_key))
                maximum = as_float(filters.get(maximum_key))
                current = number(car.get(column))
                if minimum is not None and (current is None or current < minimum):
                    return False
                if maximum is not None and (current is None or current > maximum):
                    return False
            if filters.get("has_gallery") == "1" and int(car.get("media_count") or 0) < 4:
                return False
            if filters.get("has_prices") == "1" and int(car.get("price_count") or 0) == 0:
                return False
            if filters.get("has_dealer") == "1" and int(car.get("dealer_note_count") or 0) == 0:
                return False
            if filters.get("has_sources") == "1" and int(car.get("source_count") or 0) == 0:
                return False
            return True

        cars = [car for car in all_cars if matches(car)]
        sorters = {
            "name": lambda car: (str(car.get("manufacturer") or ""), str(car.get("model_family") or ""), int(car.get("model_year_from") or 9999), str(car.get("variant") or "")),
            "newest": lambda car: -(int(car.get("model_year_from") or -1)),
            "oldest": lambda car: int(car.get("model_year_from") or 9999),
            "power": lambda car: -(number(car.get("display_power_kw")) or -1),
            "speed": lambda car: -(number(car.get("display_top_speed")) or -1),
            "lightest": lambda car: number(car.get("display_weight_kg")) if number(car.get("display_weight_kg")) is not None else float("inf"),
            "rarest": lambda car: number(car.get("display_production")) if number(car.get("display_production")) is not None else float("inf"),
            "latest_price": lambda car: -(number(car.get("latest_usd_price")) or -1),
            "recently_added": lambda car: str(car.get("created_at") or ""),
        }
        cars.sort(key=sorters.get(sort, sorters["name"]), reverse=(sort == "recently_added"))

        manufacturers = sorted({str(car["manufacturer"]) for car in all_cars})
        models = sorted({str(car["model_family"]) for car in all_cars if not selected_make or car["manufacturer"] == selected_make})
        generations = sorted({str(car["generation"]) for car in all_cars if car.get("generation") and (not selected_make or car["manufacturer"] == selected_make) and (not selected_model or car["model_family"] == selected_model)})

        def distinct(key: str) -> list[str]:
            return sorted({str(car[key]) for car in all_cars if car.get(key)})

        option_sets = {
            "manufacturer": manufacturers,
            "model_family": models,
            "generation": generations,
            "category": distinct("category"),
            "origin": distinct("origin_country"),
            "body": distinct("body_style"),
            "configuration": distinct("display_configuration"),
            "aspiration": distinct("display_aspiration"),
            "transmission": distinct("display_transmission"),
            "drivetrain": distinct("display_drivetrain"),
            "color": color_options,
            "geography": geography_options,
        }

        def options(name: str, placeholder: str) -> str:
            current = filters.get(name, "")
            rendered = [f'<option value="">{esc(placeholder)}</option>']
            rendered.extend(
                f'<option value="{esc(value)}"{" selected" if value == current else ""}>{esc(value)}</option>'
                for value in option_sets[name]
            )
            return "".join(rendered)

        def query_url(changes: dict[str, object | None]) -> str:
            params = {key: value for key, value in filters.items() if value != "" and key != "page"}
            for key, value in changes.items():
                if value in (None, ""):
                    params.pop(key, None)
                else:
                    params[key] = str(value)
            return "/" + ("?" + urlencode(params) if params else "")

        manufacturer_groups: dict[str, list[dict[str, object]]] = defaultdict(list)
        for car in all_cars:
            manufacturer_groups[str(car["manufacturer"])].append(car)

        def manufacturer_year_span(make_cars: list[dict[str, object]]) -> str:
            starts = [int(car["model_year_from"]) for car in make_cars if car.get("model_year_from")]
            ends = [int(car.get("model_year_to") or car["model_year_from"]) for car in make_cars if car.get("model_year_from")]
            return f"{min(starts)}–{max(ends)}" if starts and ends else "Years not recorded"

        manufacturer_cards = "".join(
            f"""<a class="card manufacturer-card" href="/?{urlencode({'manufacturer': make})}">
              <div><div class="eyebrow">Manufacturer</div><h3>{esc(make)}</h3></div>
              <div class="manufacturer-meta"><span>{len({str(car['model_family']) for car in make_cars})} model families · {len(make_cars)} variants</span><span>{esc(manufacturer_year_span(make_cars))}</span></div>
            </a>"""
            for make, make_cars in sorted(manufacturer_groups.items())
        )

        active_labels = {
            "q": "Search", "manufacturer": "Manufacturer", "model_family": "Model", "generation": "Generation",
            "year_from": "From year", "year_to": "To year", "category": "Category", "origin": "Origin",
            "body": "Body", "configuration": "Engine", "aspiration": "Aspiration", "transmission": "Transmission",
            "drivetrain": "Driven wheels", "color": "Color", "geography": "Geography",
            "road_legal": "Road legal", "power_min": "Min power", "power_max": "Max power",
            "weight_min": "Min weight", "weight_max": "Max weight", "speed_min": "Min speed",
            "speed_max": "Max speed", "production_min": "Min production", "production_max": "Max production",
            "price_min": "Min latest USD sale", "price_max": "Max latest USD sale", "has_gallery": "Complete gallery",
            "has_prices": "Price history", "has_dealer": "Dealer checks", "has_sources": "Sources",
        }
        chips = "".join(
            f'<a class="filter-chip" href="{esc(query_url({key: None}))}">{esc(label)}: {esc("Yes" if value == "1" and key.startswith("has_") else "Road legal" if key == "road_legal" and value == "1" else "Not road legal" if key == "road_legal" else value)} <b>×</b></a>'
            for key, label in active_labels.items() if (value := filters.get(key))
        )

        advanced_keys = set(active_labels) - {"q", "manufacturer", "model_family", "year_from", "year_to", "category"}
        advanced_open = " open" if any(filters.get(key) for key in advanced_keys) else ""
        checked = lambda key: " checked" if filters.get(key) == "1" else ""
        selected = lambda key, value: " selected" if filters.get(key) == value else ""

        sort_options = [
            ("name", "Name A–Z"), ("newest", "Newest first"), ("oldest", "Oldest first"),
            ("power", "Most powerful"), ("speed", "Fastest"), ("lightest", "Lightest"),
            ("rarest", "Rarest first"), ("latest_price", "Highest latest USD sale"),
            ("recently_added", "Recently added"),
        ]
        sort_html = "".join(f'<option value="{key}"{" selected" if sort == key else ""}>{label}</option>' for key, label in sort_options)

        page_size = 24
        page_count = max(1, (len(cars) + page_size - 1) // page_size)
        page_number = min(max(1, as_int(filters.get("page")) or 1), page_count)
        shown_cars = cars[(page_number - 1) * page_size:page_number * page_size]

        def year_range(car: dict[str, object]) -> str:
            start, end = car.get("model_year_from"), car.get("model_year_to")
            return str(start) if start == end or not end else f"{start}–{end}"

        def usd_price(car: dict[str, object]) -> str:
            amount = number(car.get("latest_usd_price"))
            if amount is None:
                return "—"
            display = f"${amount / 1_000_000:.2f}M" if amount >= 1_000_000 else f"${amount:,.0f}"
            return f"{display} ({esc(car.get('latest_usd_date'))})" if car.get("latest_usd_date") else display

        rows = "".join(
            f"""<tr>
              <td><a class="car-link" href="/car/{quote(str(car['id']))}">{esc(car['manufacturer'])} {esc(car['model_family'])}</a><div class="small muted">{esc(car['generation'])}</div></td>
              <td>{esc(car['variant'])}</td><td>{esc(year_range(car))}</td><td>{value_or_dash(car['category'])}</td>
              <td>{value_or_dash(car['display_power_kw'],' kW')}</td><td>{value_or_dash(car['display_weight_kg'],' kg')}</td>
              <td>{value_or_dash(car['display_top_speed'],' km/h')}</td><td>{value_or_dash(car['display_production'])}</td><td>{usd_price(car)}</td>
            </tr>""" for car in shown_cars
        ) or '<tr><td colspan="9" class="muted">No cars match these filters.</td></tr>'

        cards = "".join(
            f"""<a class="card car-card" href="/car/{quote(str(car['id']))}">
              {f'<img src="{esc(car["primary_image"])}" alt="{esc(car["manufacturer"])} {esc(car["model_family"])}">' if car['primary_image'] else '<div style="aspect-ratio:16/9;background:#d9d5cc"></div>'}
              <div class="car-card-body"><div class="eyebrow">{esc(car['category'] or 'Car')} · {esc(year_range(car))}</div>
                <h3>{esc(car['manufacturer'])} {esc(car['model_family'])}</h3>
                <div class="muted">{esc(car['generation'])} · {esc(car['variant'])}</div>
                <div class="mini-specs"><span>{value_or_dash(car['display_power_kw'],' kW')}</span><span>{value_or_dash(car['display_zero_to_100'],' s')}</span><span>{value_or_dash(car['display_top_speed'],' km/h')}</span><span>{value_or_dash(car['display_production'],' built')}</span></div>
              </div></a>""" for car in shown_cars
        )

        pagination = ""
        if page_count > 1:
            links = []
            for number_value in range(1, page_count + 1):
                links.append(f'<span>{number_value}</span>' if number_value == page_number else f'<a href="{esc(query_url({"page": number_value}))}">{number_value}</a>')
            pagination = f'<nav class="pagination" aria-label="Catalogue pages">{"".join(links)}</nav>'

        title = f"{selected_make} cars" if selected_make else "Explore the collection"
        result_text = f"{len(cars)} matching variant{'s' if len(cars) != 1 else ''}"
        if selected_make:
            result_text += f" from {selected_make}"

        filters_html = f"""
        <form method="get" class="card filter-panel" id="catalog-filters">
          <input type="hidden" name="view" value="{esc(view)}">
          <div class="filter-search"><input name="q" value="{esc(query)}" placeholder="Search cars, engines, internal codes, features, facts, chassis or sources" aria-label="Search the catalogue"><button class="secondary">Search</button></div>
          <div class="quick-filters">
            <div class="filter-field"><label for="manufacturer">Manufacturer</label><select id="manufacturer" name="manufacturer">{options('manufacturer','All manufacturers')}</select></div>
            <div class="filter-field"><label for="model-family">Model family</label><select id="model-family" name="model_family">{options('model_family','All models')}</select></div>
            <div class="filter-field"><label for="year-from">From year</label><input id="year-from" type="number" name="year_from" value="{esc(filters.get('year_from',''))}" placeholder="1980"></div>
            <div class="filter-field"><label for="year-to">To year</label><input id="year-to" type="number" name="year_to" value="{esc(filters.get('year_to',''))}" placeholder="2026"></div>
            <div class="filter-field"><label for="category">Category</label><select id="category" name="category">{options('category','All categories')}</select></div>
            <div class="filter-field"><label for="sort">Sort results</label><select id="sort" name="sort">{sort_html}</select></div>
          </div>
          <details{advanced_open}><summary>Advanced filters</summary>
            <div class="advanced-filter-grid">
              <div class="filter-field"><label>Generation</label><select name="generation">{options('generation','All generations')}</select></div>
              <div class="filter-field"><label>Country of origin</label><select name="origin">{options('origin','All origins')}</select></div>
              <div class="filter-field"><label>Body style</label><select name="body">{options('body','All body styles')}</select></div>
              <div class="filter-field"><label>Engine configuration</label><select name="configuration">{options('configuration','All configurations')}</select></div>
              <div class="filter-field"><label>Aspiration</label><select name="aspiration">{options('aspiration','All aspiration types')}</select></div>
              <div class="filter-field"><label>Transmission</label><select name="transmission">{options('transmission','All transmissions')}</select></div>
              <div class="filter-field"><label>Driven wheels</label><select name="drivetrain">{options('drivetrain','All drivetrains')}</select></div>
              <div class="filter-field"><label>Road legality</label><select name="road_legal"><option value="">Any</option><option value="1"{selected('road_legal','1')}>Road legal</option><option value="0"{selected('road_legal','0')}>Not road legal</option></select></div>
              <div class="filter-field"><label>Factory color evidence</label><select name="color">{options('color','Any documented color')}</select></div>
              <div class="filter-field"><label>Documented geography</label><select name="geography">{options('geography','Any documented country')}</select></div>
              <div class="filter-field"><label>Power (kW)</label><div class="range-pair"><input type="number" name="power_min" value="{esc(filters.get('power_min',''))}" placeholder="Min"><input type="number" name="power_max" value="{esc(filters.get('power_max',''))}" placeholder="Max"></div></div>
              <div class="filter-field"><label>Weight (kg)</label><div class="range-pair"><input type="number" name="weight_min" value="{esc(filters.get('weight_min',''))}" placeholder="Min"><input type="number" name="weight_max" value="{esc(filters.get('weight_max',''))}" placeholder="Max"></div></div>
              <div class="filter-field"><label>Top speed (km/h)</label><div class="range-pair"><input type="number" name="speed_min" value="{esc(filters.get('speed_min',''))}" placeholder="Min"><input type="number" name="speed_max" value="{esc(filters.get('speed_max',''))}" placeholder="Max"></div></div>
              <div class="filter-field"><label>Production count</label><div class="range-pair"><input type="number" name="production_min" value="{esc(filters.get('production_min',''))}" placeholder="Min"><input type="number" name="production_max" value="{esc(filters.get('production_max',''))}" placeholder="Max"></div></div>
              <div class="filter-field"><label>Latest USD sale</label><div class="range-pair"><input type="number" name="price_min" value="{esc(filters.get('price_min',''))}" placeholder="Min"><input type="number" name="price_max" value="{esc(filters.get('price_max',''))}" placeholder="Max"></div></div>
              <div class="check-grid">
                <label class="check-option"><input type="checkbox" name="has_gallery" value="1"{checked('has_gallery')}> Four-image gallery</label>
                <label class="check-option"><input type="checkbox" name="has_prices" value="1"{checked('has_prices')}> Price history</label>
                <label class="check-option"><input type="checkbox" name="has_dealer" value="1"{checked('has_dealer')}> Dealer checks</label>
                <label class="check-option"><input type="checkbox" name="has_sources" value="1"{checked('has_sources')}> Source library</label>
              </div>
            </div>
          </details>
          <div class="filter-actions"><div class="filter-actions-left"><button>Apply filters</button><a class="button ghost" href="/">Clear all</a></div><span class="filter-note">Numeric filters exclude cars with missing values; missing data is never treated as zero.</span></div>
        </form>"""

        results_html = f'<div class="catalog-grid">{cards}</div>' if view == "grid" and cards else (
            '<div class="empty-state"><h3>No matching cars</h3><p>Remove one or more filters, or clear the catalogue and try a broader search.</p></div>' if not cars else
            f'<div class="table-wrap"><table><thead><tr><th>Car</th><th>Variant</th><th>Years</th><th>Category</th><th>Power</th><th>Weight</th><th>Top speed</th><th>Production</th><th>Latest USD sale</th></tr></thead><tbody>{rows}</tbody></table></div>'
        )

        body = f"""
        <div class="eyebrow">Living automotive knowledge base</div><h1>{esc(title)}</h1>
        <p class="muted">Search every variant and filter the collection without losing the difference between verified values, partial evidence and missing data.</p>
        <div class="stats">
          <div class="card stat"><span class="muted">Recorded variants</span><strong>{len(all_cars)}</strong></div>
          <div class="card stat"><span class="muted">Engineering facts</span><strong>{fact_count}</strong></div>
          <div class="card stat"><span class="muted">Price records</span><strong>{price_count}</strong></div>
        </div>
        <div class="section-head"><div><div class="eyebrow">Start broad</div><h2>Browse by manufacturer</h2></div><span class="muted">Select a marque to see every recorded model</span></div>
        <div class="manufacturer-strip">{manufacturer_cards}</div>
        {filters_html}
        {f'<div class="filter-chips">{chips}</div>' if chips else ''}
        <div class="result-bar"><div><h2 style="margin:0">Catalogue results</h2><span class="muted">{esc(result_text)} · page {page_number} of {page_count}</span></div>
          <div class="result-tools"><a class="button ghost" href="/new">+ Add car</a><div class="view-switch" aria-label="Result view"><a class="{'active' if view == 'grid' else ''}" href="{esc(query_url({'view':'grid'}))}">Grid</a><a class="{'active' if view == 'list' else ''}" href="{esc(query_url({'view':'list'}))}">List</a></div></div>
        </div>
        <div class="coverage-note">Color and geography filters return documented evidence only. They do not imply a complete factory color breakdown or the present location of every surviving car.</div>
        {results_html}
        {pagination}
        """
        self.send_html(page(title, body))

    def show_car(self, car_id: str) -> None:
        with connect() as db:
            car = db.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
            if not car:
                self.send_html(page("Not found", "<h1>Car not found</h1>"), 404); return
            scope_params = (car_id, car["family_id"], car["generation_id"])
            facts = db.execute(
                """SELECT f.* FROM facts f JOIN cars owner ON owner.id=f.car_id
                   WHERE f.car_id=? OR (f.scope_level='Model family' AND owner.family_id=?)
                     OR (f.scope_level='Generation' AND owner.generation_id=? AND owner.generation_id IS NOT NULL)
                   ORDER BY f.id""", scope_params
            ).fetchall()
            prices = db.execute("SELECT * FROM price_records WHERE car_id = ? ORDER BY observation_date, id", (car_id,)).fetchall()
            sources = db.execute("SELECT * FROM sources WHERE car_id = ? ORDER BY id", (car_id,)).fetchall()
            all_sources = db.execute(
                """SELECT s.* FROM sources s JOIN cars owner ON owner.id=s.car_id
                   WHERE owner.family_id=? ORDER BY s.publisher,s.title""", (car["family_id"],)
            ).fetchall()
            media = db.execute(
                """SELECT m.* FROM media m JOIN cars owner ON owner.id=m.car_id
                   WHERE m.car_id=? OR (m.scope_level='Model family' AND owner.family_id=?)
                     OR (m.scope_level='Generation' AND owner.generation_id=? AND owner.generation_id IS NOT NULL)
                   ORDER BY m.is_primary DESC,m.id""", scope_params
            ).fetchall()
            colors = db.execute(
                """SELECT r.* FROM color_records r JOIN cars owner ON owner.id=r.car_id
                   WHERE r.car_id=? OR (r.scope_level='Model family' AND owner.family_id=?)
                     OR (r.scope_level='Generation' AND owner.generation_id=? AND owner.generation_id IS NOT NULL)
                   ORDER BY r.color_type,r.id""", scope_params
            ).fetchall()
            geography = db.execute(
                """SELECT r.* FROM country_distribution r JOIN cars owner ON owner.id=r.car_id
                   WHERE r.car_id=? OR (r.scope_level='Model family' AND owner.family_id=?)
                     OR (r.scope_level='Generation' AND owner.generation_id=? AND owner.generation_id IS NOT NULL)
                   ORDER BY r.distribution_type,r.vehicle_count DESC,r.country""", scope_params
            ).fetchall()
            related = db.execute(
                """SELECT c.*,
                          (SELECT location FROM media m WHERE m.car_id = c.id ORDER BY is_primary DESC, id LIMIT 1) AS primary_image,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label='Maximum power' AND a.unit='kW' ORDER BY id LIMIT 1) AS display_power_kw,
                          (SELECT value FROM attributes a WHERE a.car_id=c.id AND a.label='Total announced production' ORDER BY id LIMIT 1) AS display_production
                   FROM cars c WHERE c.family_id = ?
                   ORDER BY model_year_from, generation, variant""",
                (car["family_id"],),
            ).fetchall()
            attributes = db.execute(
                """SELECT a.* FROM attributes a JOIN cars owner ON owner.id=a.car_id
                   WHERE a.car_id=? OR (a.scope_level='Model family' AND owner.family_id=?)
                     OR (a.scope_level='Generation' AND owner.generation_id=? AND owner.generation_id IS NOT NULL)
                   ORDER BY CASE a.section
                     WHEN 'Identity' THEN 1 WHEN 'Powertrain' THEN 2 WHEN 'Performance' THEN 3
                     WHEN 'Dimensions' THEN 4 WHEN 'Chassis & dynamics' THEN 5
                     WHEN 'Technology & experience' THEN 6 WHEN 'Production & rarity' THEN 7 ELSE 99 END,
                   a.sort_order, a.id""",
                scope_params,
            ).fetchall()

        primary = media[0] if media else None
        source_map = {source["id"]: source for source in all_sources}

        def evidence_html(records: list[sqlite3.Row] | sqlite3.Row, label: str = "Evidence") -> str:
            record_list = list(records) if not isinstance(records, sqlite3.Row) else [records]
            source_ids = []
            for record in record_list:
                if "source_id" in record.keys() and record["source_id"] and record["source_id"] not in source_ids:
                    source_ids.append(record["source_id"])
            links = "".join(
                f'<a href="#source-{source_id}">{esc(source_map[source_id]["publisher"] or source_map[source_id]["title"])}</a>'
                for source_id in source_ids if source_id in source_map
            )
            return f'<div class="evidence-strip"><strong>{esc(label)}:</strong>{links}</div>' if links else ""

        source_options = '<option value="">No source selected</option>' + "".join(
            f'<option value="{source["id"]}">{esc(source["publisher"] or "Source")} — {esc(source["title"])}</option>'
            for source in sources
        )
        image = f'<img id="gallery-main-image" src="{esc(primary["location"])}" alt="{esc(primary["caption"] or (car["manufacturer"]+" "+car["model_family"]))}">' if primary else '<div class="muted" style="padding:30px">No image added</div>'
        gallery_thumbs = "".join(
            f'''<button type="button" class="gallery-thumb {'active' if index == 0 else ''}"
                 data-gallery-src="{esc(item['location'])}"
                 data-gallery-alt="{esc(item['caption'] or item['media_type'])}"
                 data-gallery-index="{index + 1}"
                 data-gallery-caption="{esc(' · '.join(part for part in [item['caption'], item['creator'], item['license']] if part))}">
                 <img src="{esc(item['location'])}" alt="{esc(item['caption'] or item['media_type'])}" loading="lazy">
                 <span>{esc(item['media_type'])}</span></button>'''
            for index, item in enumerate(media)
        )
        gallery_management = "".join(
            f'''<div class="attribute-row"><div class="attribute-label">{esc(item['media_type'])}<div class="small muted">{esc(item['creator'] or 'Creator unknown')} · {esc(item['license'] or 'License unknown')}</div></div>
                 <div class="attribute-value">{esc(item['caption'] or 'Untitled image')}{record_actions(item['car_id'], 'media', item['id'], 'gallery')}</div></div>'''
            for item in media
        )
        primary_caption = " · ".join(part for part in ([primary["caption"], primary["creator"], primary["license"]] if primary else []) if part)

        def attribute_value(labels: str | tuple[str, ...], unit: str | None = None) -> object | None:
            wanted = (labels,) if isinstance(labels, str) else labels
            match = next(
                (
                    item for item in attributes
                    if item["label"] in wanted and (unit is None or item["unit"] == unit)
                ),
                None,
            )
            return match["value"] if match else None

        specs = [
            ("Generation", car["generation"], ""), ("Variant", car["variant"], ""),
            ("Model year", car["model_year_from"], ""), ("Category", car["category"], ""),
            ("Engine", attribute_value("Configuration"), ""), ("Power", attribute_value("Maximum power", "kW"), " kW"),
            ("Torque", attribute_value("Maximum torque", "Nm"), " Nm"), ("Curb weight", attribute_value("Vehicle weight", "kg"), " kg"),
            ("0–100 km/h", attribute_value("0–100 km/h"), " s"), ("Top speed", attribute_value("Maximum speed", "km/h"), " km/h"),
            ("Transmission", attribute_value("Transmission"), ""), ("Drivetrain", attribute_value(("Drivetrain", "Driven wheels")), ""),
            ("Production", attribute_value("Total announced production"), ""), ("Production scope", attribute_value("Production scope") or car["production_scope"], ""),
        ]
        spec_html = "".join(f'<div class="spec"><span>{esc(label)}</span><strong>{value_or_dash(value,suffix)}</strong></div>' for label,value,suffix in specs)
        fact_html = "".join(
            f"""<article class="card fact"><span class="pill">{esc(f['category'] or 'Fact')}</span> <span class="pill scope">{esc(f['scope_level'])}</span>
            <h3>{esc(f['title'])}</h3><p>{esc(f['explanation'])}</p>
            {f'<p class="muted"><strong>Why it matters:</strong> {esc(f["why_it_matters"])}</p>' if f['why_it_matters'] else ''}
            {record_actions(f['car_id'], 'fact', f['id'], 'stories')}</article>""" for f in facts
        ) or '<p class="muted">No facts added yet.</p>'
        price_rows = "".join(
            f"""<tr><td>{value_or_dash(p['observation_date'])}</td><td>{esc(p['price_type'])}</td><td>{p['amount']:,.0f} {esc(p['currency'])}</td>
            <td>{value_or_dash(p['market'])}</td><td>{value_or_dash(p['venue'])}</td><td>{value_or_dash(p['mileage'])}</td>
            <td>{esc(source_map[p['source_id']]['publisher']) if p['source_id'] in source_map else '—'}</td><td>{record_actions(car_id, 'price', p['id'], 'market')}</td></tr>""" for p in prices
        ) or '<tr><td colspan="8" class="muted">No prices added yet.</td></tr>'
        source_html = "".join(
            f'<li id="source-{s["id"]}"><a href="{esc(s["url"])}" target="_blank" rel="noreferrer"><strong>{esc(s["title"])}</strong></a> <span class="muted">— {esc(s["publisher"] or "Unknown publisher")}</span>{record_actions(car_id, "source", s["id"], "sources")}</li>'
            for s in sources
        ) or '<li class="muted">No sources added yet.</li>'

        attribute_groups: dict[str, list[sqlite3.Row]] = defaultdict(list)
        for attribute in attributes:
            attribute_groups[attribute["section"]].append(attribute)
        attribute_cards: list[str] = []
        for section, items in attribute_groups.items():
            detail_rows: list[str] = []
            for attribute in items:
                unit = f" {esc(attribute['unit'])}" if attribute["unit"] else ""
                detail_rows.append(
                    f'<div class="attribute-row"><div class="attribute-label">{esc(attribute["label"])}<div><span class="pill scope">{esc(attribute["scope_level"])}</span></div></div><div class="attribute-value">{esc(attribute["value"])}{unit}{record_actions(attribute["car_id"], "attribute", attribute["id"], "specifications")}</div></div>'
                )
            attribute_cards.append(f'<section class="card attribute-card"><h3>{esc(section)}</h3>{"".join(detail_rows)}</section>')
        attribute_html = "".join(attribute_cards) or '<p class="muted">No detailed attributes added yet.</p>'

        usd_prices = [p for p in prices if p["currency"] == "USD" and p["amount"]]
        max_price = max((p["amount"] for p in usd_prices), default=1)
        price_bars = "".join(
            f'<div class="price-bar-item" title="{esc(p["price_type"])}: {p["amount"]:,.0f} USD"><strong class="small">${p["amount"]/1000:,.0f}k</strong><div class="price-bar" style="height:{max(4, round(p["amount"] / max_price * 140))}px"></div><small>{esc(p["observation_date"])}</small></div>'
            for p in usd_prices
        )
        msrp = next((p for p in prices if p["price_type"] == "Announced MSRP" and p["currency"] == "USD"), None)
        latest_sale = next((p for p in reversed(prices) if p["price_type"] == "Auction sale" and p["currency"] == "USD"), None)

        family_cards = "".join(
            f'''<a class="card family-variant {'current' if item['id'] == car_id else ''}" href="/car/{quote(item['id'])}">
                <span class="pill">{esc(item['model_year_from'] or 'Year unknown')}</span>
                <h3>{esc(item['generation'] or 'Generation unknown')}</h3>
                <div>{esc(item['variant'])}</div>
                <div class="small muted">{value_or_dash(item['display_power_kw'], ' kW')} · {value_or_dash(item['display_production'], ' produced')}</div>
              </a>'''
            for item in related
        )

        color_cards = "".join(
            f'''<article class="card color-card">
                <div class="color-swatch" style="background:{esc(color['swatch_hex'] or '#d8d4cc')}" title="{esc(color['color_name'])}"></div>
                <span class="pill">{esc(color['color_type'])}</span>
                <h3>{esc(color['color_name'])}</h3>
                <p class="small muted">{esc(color['availability_scope'] or 'Availability scope unknown')}</p>
                <p class="small"><strong>{f'{color["production_count"]:,} documented' if color['production_count'] is not None else 'Production count unknown'}</strong>{f' · {color["production_percentage"]:g}%' if color['production_percentage'] is not None else ''}</p>
                <span class="pill confidence">{esc(color['confidence'])}</span> <span class="pill scope">{esc(color['scope_level'])}</span>
                {record_actions(color['car_id'], 'color', color['id'], 'colors')}
              </article>'''
            for color in colors
        ) or '<div class="empty-state">No colors recorded yet. Add factory availability or documented production counts below.</div>'

        geography_groups: dict[str, list[sqlite3.Row]] = defaultdict(list)
        for place in geography:
            geography_groups[place["distribution_type"]].append(place)
        geography_cards: list[str] = []
        for group_name, places in geography_groups.items():
            max_count = max((place["vehicle_count"] or 0 for place in places), default=1) or 1
            rows_html: list[str] = []
            for place in places:
                count_text = f'{place["vehicle_count"]:,}' if place["vehicle_count"] is not None else "Unknown"
                share_text = f' · {place["share_percentage"]:g}%' if place["share_percentage"] is not None else ""
                width = max(3, round((place["vehicle_count"] or 0) / max_count * 100))
                rows_html.append(
                    f'''<div class="distribution-row"><div class="distribution-label"><strong>{esc(place['country'])}</strong><span>{count_text}{share_text}</span></div>
                        <div class="distribution-track"><div class="distribution-fill" style="width:{width}%"></div></div>
                        <div class="small muted">{esc(place['confidence'])} · {esc(place['scope_level'])}{f' · as of {esc(place["as_of_date"])}' if place['as_of_date'] else ''}{f' · denominator {place["denominator"]:,}' if place['denominator'] else ''}</div>
                        {record_actions(place['car_id'], 'geography', place['id'], 'geography')}</div>'''
                )
            notes = next((place["notes"] for place in reversed(places) if place["notes"]), None)
            geography_cards.append(
                f'''<article class="card"><div class="eyebrow">Documented distribution</div><h3>{esc(group_name)}</h3>{''.join(rows_html)}
                    {f'<p class="small muted">{esc(notes)}</p>' if notes else ''}
                    </article>'''
            )
        geography_html = "".join(geography_cards) or '<div class="empty-state">No geographic records yet. Add original delivery, current registration, or listing-location evidence below.</div>'

        body = f"""
        <div class="breadcrumb"><a href="/">All cars</a><span>›</span><strong>{esc(car['manufacturer'])}</strong><span>›</span><strong>{esc(car['model_family'])}</strong><span>›</span>{esc(car['generation'])}<span>›</span>{esc(car['variant'])}</div>
        <div class="eyebrow">{esc(car['category'] or 'Car record')}</div>
        <div class="section-head"><div><h1>{esc(car['manufacturer'])} {esc(car['model_family'])}</h1><p class="muted">{esc(car['generation'])} · {esc(car['variant'])}</p></div><a class="button ghost" href="/car/{quote(car_id)}/edit">Edit car</a></div>
        <nav class="anchor-nav"><a href="#overview">Overview</a><a href="#gallery">Gallery</a><a href="#family">Model family</a><a href="#specifications">Specifications</a><a href="#colors">Colors</a><a href="#geography">Geography</a><a href="#stories">Stories</a><a href="#market">Market</a><a href="#sources">Sources</a></nav>
        <div class="hero" id="overview"><div><div class="hero-image gallery-main">{image}{f'<span class="gallery-count" id="gallery-count" data-total="{len(media)}">1 of {len(media)}</span>' if media else ''}</div><p class="small muted gallery-caption" id="gallery-caption">{esc(primary_caption)}</p></div><div class="card"><div class="eyebrow">At a glance</div><p>{esc(car['summary'] or '')}</p><div class="specs">{spec_html}</div>{evidence_html(car, 'Primary evidence')}</div></div>

        <section class="section" id="gallery"><div class="section-head"><div><div class="eyebrow">Visual record</div><h2>Image gallery</h2></div><span class="muted">{len(media)} documented assets</span></div>
        {f'<div class="gallery-strip">{gallery_thumbs}</div>' if gallery_thumbs else '<div class="empty-state">No images added yet.</div>'}{evidence_html(media, 'Image attribution')}
        <details><summary>Manage gallery entries</summary><div class="card">{gallery_management or '<p class="muted">No images to manage.</p>'}</div></details>
        <details><summary>+ Add another image</summary><form method="post" action="/car/{quote(car_id)}/media" class="form-grid">
          <div class="field"><label>View or type</label><select name="media_type"><option>Exterior image</option><option>Rear image</option><option>Interior image</option><option>Engine image</option><option>Detail image</option><option>Historical image</option></select></div><div class="field"><label>Image URL or local asset path</label><input name="location" required placeholder="https://... or /assets/image.jpg"></div>
          <div class="field full"><label>Caption</label><input name="caption" placeholder="What this image shows"></div><div class="field"><label>Creator</label><input name="creator"></div><div class="field"><label>License</label><input name="license" placeholder="CC BY-SA 4.0"></div>
          <div class="field"><label>Make primary image</label><select name="is_primary"><option value="0">No</option><option value="1">Yes</option></select></div><div class="field"><label>Applies to</label><select name="scope_level"><option>Variant</option><option>Model year</option><option>Generation</option><option>Model family</option></select></div>
          <div class="field full"><label>Attribution source</label><select name="source_id">{source_options}</select></div><div class="form-actions"><button>Add to gallery</button></div>
        </form></details></section>

        <section class="section" id="family"><div class="section-head"><div><div class="eyebrow">Lineage</div><h2>Where this car fits</h2></div><span class="muted">{len(related)} recorded variant{'s' if len(related) != 1 else ''}</span></div>
        <div class="card"><div class="family-flow"><span class="family-node">{esc(car['manufacturer'])}</span><span class="family-arrow">→</span><span class="family-node">{esc(car['model_family'])}</span><span class="family-arrow">→</span><span class="family-node">{esc(car['generation'] or 'Generation unknown')}</span><span class="family-arrow">→</span><span class="family-node">{esc(car['variant'])}</span><span class="family-arrow">→</span><span class="family-node">{esc(car['model_year_from'] or 'Year unknown')}</span></div></div>
        <div class="family-list">{family_cards}</div></section>

        <section class="section" id="specifications"><div class="section-head"><div><div class="eyebrow">Full record</div><h2>Complete specifications</h2></div><span class="muted">{len(attributes)} sourced details</span></div>
        <div class="attribute-sections">{attribute_html}</div>{evidence_html(attributes)}
        <details><summary>+ Add any missing detail</summary><form method="post" action="/car/{quote(car_id)}/attribute" class="form-grid">
          <div class="field"><label>Section</label><select name="section"><option>Identity</option><option>Powertrain</option><option>Performance</option><option>Dimensions</option><option>Chassis & dynamics</option><option>Technology & experience</option><option>Production & rarity</option><option>Ownership & dealer notes</option></select></div>
          <div class="field"><label>Label</label><input name="label" placeholder="Battery capacity, designer, service interval..." required></div>
          <div class="field"><label>Value</label><input name="value" required></div><div class="field"><label>Unit</label><input name="unit" placeholder="kg, mm, rpm..."></div>
          <div class="field"><label>Applies to</label><select name="scope_level"><option>Variant</option><option>Model year</option><option>Generation</option><option>Model family</option></select></div><div class="field"><label>Evidence source</label><select name="source_id">{source_options}</select></div><div class="form-actions"><button>Add detail</button></div>
        </form></details></section>

        <section class="section" id="colors"><div class="section-head"><div><div class="eyebrow">Factory configuration</div><h2>Colors and production evidence</h2></div><span class="muted">Availability and counts are kept separate</span></div>
        <div class="notice">A listed color is not automatically a production count. Cards explicitly show when the number built is unknown.</div>
        <div class="color-grid" style="margin-top:14px">{color_cards}</div>{evidence_html(colors)}
        <details><summary>+ Add a color record</summary><form method="post" action="/car/{quote(car_id)}/color" class="form-grid">
          <div class="field"><label>Official color name</label><input name="color_name" required></div><div class="field"><label>Paint / trim code</label><input name="color_code"></div>
          <div class="field"><label>Type</label><select name="color_type"><option>Exterior</option><option>Interior</option><option>Roof</option><option>Accent</option></select></div><div class="field"><label>Swatch color</label><input name="swatch_hex" placeholder="#ffffff" pattern="#[0-9a-fA-F]{{6}}"></div>
          <div class="field full"><label>Availability scope</label><input name="availability_scope" placeholder="All 2012 cars, Nürburgring Package, US market..."></div>
          <div class="field"><label>Documented production count</label><input name="production_count" type="number" min="0"></div><div class="field"><label>Percentage</label><input name="production_percentage" type="number" step="0.01" min="0" max="100"></div>
          <div class="field"><label>Count scope</label><input name="count_scope" placeholder="500-car global run"></div><div class="field"><label>Evidence quality</label><select name="confidence"><option>Manufacturer reported</option><option>Registry documented</option><option>Documented estimate</option><option>Unknown</option></select></div>
          <div class="field"><label>Applies to</label><select name="scope_level"><option>Variant</option><option>Model year</option><option>Generation</option><option>Model family</option></select></div><div class="field"><label>Evidence source</label><select name="source_id">{source_options}</select></div><div class="field full"><label>Notes</label><textarea name="notes"></textarea></div><div class="form-actions"><button>Add color</button></div>
        </form></details></section>

        <section class="section" id="geography"><div class="section-head"><div><div class="eyebrow">Delivery footprint</div><h2>Country and region distribution</h2></div><span class="muted">Original delivery and current location remain separate</span></div>
        <div class="distribution-groups">{geography_html}</div>{evidence_html(geography)}
        <details><summary>+ Add a geographic record</summary><form method="post" action="/car/{quote(car_id)}/geography" class="form-grid">
          <div class="field"><label>Distribution type</label><select name="distribution_type"><option>Original delivery · global region</option><option>Original delivery · country</option><option>Current registration · country</option><option>Public listing · country</option></select></div><div class="field"><label>Country or region</label><input name="country" required></div>
          <div class="field"><label>Parent region</label><input name="region" placeholder="Europe"></div><div class="field"><label>Vehicle count</label><input name="vehicle_count" type="number" min="0"></div>
          <div class="field"><label>Share percentage</label><input name="share_percentage" type="number" step="0.01" min="0" max="100"></div><div class="field"><label>Denominator</label><input name="denominator" type="number" min="1" placeholder="500"></div>
          <div class="field"><label>As-of date</label><input name="as_of_date" placeholder="2026-08-28"></div><div class="field"><label>Evidence quality</label><select name="confidence"><option>Manufacturer reported</option><option>Registry documented</option><option>Documented estimate</option><option>Unknown</option></select></div>
          <div class="field"><label>Applies to</label><select name="scope_level"><option>Variant</option><option>Model year</option><option>Generation</option><option>Model family</option></select></div><div class="field"><label>Evidence source</label><select name="source_id">{source_options}</select></div><div class="field full"><label>Notes</label><textarea name="notes"></textarea></div><div class="form-actions"><button>Add distribution record</button></div>
        </form></details></section>

        <section class="section" id="stories"><div class="section-head"><div><div class="eyebrow">Beyond the numbers</div><h2>Engineering and stories</h2></div><span class="muted">{len(facts)} verified stories</span></div><div class="fact-grid">{fact_html}</div>{evidence_html(facts)}
        <details><summary>+ Add an engineering fact</summary><form method="post" action="/car/{quote(car_id)}/fact" class="form-grid">
          <div class="field"><label>Title</label><input name="title" required></div><div class="field"><label>Category</label><input name="category" placeholder="Engine, materials, design..."></div>
          <div class="field full"><label>Explanation</label><textarea name="explanation" required></textarea></div><div class="field full"><label>Why it matters</label><textarea name="why_it_matters"></textarea></div>
          <div class="field"><label>Applies to</label><select name="scope_level"><option>Variant</option><option>Model year</option><option>Generation</option><option>Model family</option></select></div><div class="field"><label>Evidence quality</label><select name="confidence"><option>Manufacturer reported</option><option>Registry documented</option><option>Documented estimate</option><option>Unknown</option></select></div>
          <div class="field full"><label>Evidence source</label><select name="source_id">{source_options}</select></div><div class="form-actions"><button>Add fact</button></div>
        </form></details></section>

        <section class="section" id="market"><div class="section-head"><div><div class="eyebrow">Market evidence</div><h2>Price history</h2></div><span class="muted">Individual observations, not a formal index</span></div>
        <div class="market-overview"><div class="card market-number"><span class="muted">Announced US MSRP</span><strong>{f'${msrp["amount"]:,.0f}' if msrp else '—'}</strong><span class="small muted">Base price when new</span></div><div class="card market-number"><span class="muted">Latest recorded public sale</span><strong>{f'${latest_sale["amount"]:,.0f}' if latest_sale else '—'}</strong><span class="small muted">{esc(latest_sale['observation_date']) if latest_sale else 'No sale recorded'}</span></div></div>
        {f'<div class="card"><div class="price-bars">{price_bars}</div><p class="small muted">Published USD observations for different physical cars. Mileage, condition and specification affect comparability.</p></div>' if price_bars else ''}
        <div class="table-wrap"><table><thead><tr><th>Date</th><th>Type</th><th>Amount</th><th>Market</th><th>Venue</th><th>Mileage</th><th>Evidence</th><th>Actions</th></tr></thead><tbody>{price_rows}</tbody></table></div>{evidence_html(prices)}
        <details><summary>+ Add a price observation</summary><form method="post" action="/car/{quote(car_id)}/price" class="form-grid">
          <div class="field"><label>Date or year</label><input name="observation_date" placeholder="2026-08-28"></div><div class="field"><label>Price type</label><select name="price_type"><option>Auction sale</option><option>Announced MSRP</option><option>Listing</option><option>Valuation</option></select></div>
          <div class="field"><label>Amount</label><input name="amount" type="number" step="0.01" required></div><div class="field"><label>Currency</label><input name="currency" value="USD" required></div>
          <div class="field"><label>Market</label><input name="market"></div><div class="field"><label>Venue</label><input name="venue"></div>
          <div class="field"><label>Serial number</label><input name="serial_number"></div><div class="field"><label>Mileage</label><input name="mileage"></div>
          <div class="field full"><label>Evidence source</label><select name="source_id">{source_options}</select></div><div class="field full"><label>Notes</label><textarea name="notes"></textarea></div><div class="form-actions"><button>Add price</button></div>
        </form></details></section>

        <section class="section" id="sources"><div class="eyebrow">Audit trail</div><h2>Source library</h2><p class="muted">Each external reference is stored once and reused throughout this car record.</p><div class="card"><ul>{source_html}</ul></div>
        <details><summary>+ Add a source</summary><form method="post" action="/car/{quote(car_id)}/source" class="form-grid">
          <div class="field"><label>Title</label><input name="title" required></div><div class="field"><label>Publisher</label><input name="publisher"></div><div class="field"><label>Source type</label><input name="source_type"></div><div class="field"><label>URL</label><input type="url" name="url" required></div><div class="field full"><label>Notes</label><textarea name="notes"></textarea></div><div class="form-actions"><button>Add source</button></div>
        </form></details></section>
        """
        self.send_html(page(f"{car['manufacturer']} {car['model_family']}", body))

    def show_edit(self, car_id: str) -> None:
        with connect() as db:
            car = db.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
            attributes = db.execute("SELECT * FROM attributes WHERE car_id = ?", (car_id,)).fetchall()
            primary_source = db.execute(
                """SELECT s.url FROM sources s JOIN cars c ON c.primary_source_id = s.id
                   WHERE c.id = ?""", (car_id,)
            ).fetchone()
        if not car:
            self.send_html(page("Not found", "<h1>Car not found</h1>"), 404); return
        data: dict[str, object] = dict(car)
        for field, (section, label, unit) in TECHNICAL_SPECS.items():
            match = next(
                (item for item in attributes if item["section"] == section and item["label"] == label and (item["unit"] or None) == unit),
                None,
            )
            data[field] = match["value"] if match else ""
        data["primary_source_url"] = primary_source["url"] if primary_source else ""
        self.send_html(page("Edit car", car_form(f"/car/{quote(car_id)}/update", data, f"Edit {car['manufacturer']} {car['model_family']}")))

    def show_child_edit(self, car_id: str, kind: str, record_id: int | None) -> None:
        config = CHILD_CONFIG.get(kind)
        if not config or record_id is None:
            self.send_html(page("Not found", "<h1>Record not found</h1>"), 404); return
        with connect() as db:
            car = db.execute("SELECT * FROM cars WHERE id = ?", (car_id,)).fetchone()
            record = db.execute(
                f"SELECT * FROM {config['table']} WHERE id = ? AND car_id = ?", (record_id, car_id)
            ).fetchone()
            sources = db.execute("SELECT * FROM sources WHERE car_id = ? ORDER BY publisher,title", (car_id,)).fetchall()
        if not car or not record:
            self.send_html(page("Not found", "<h1>Record not found</h1>"), 404); return

        fields: list[str] = []
        for name, label, field_type in config["fields"]:
            value = record[name] if name in record.keys() else ""
            if field_type == "textarea":
                control = f'<textarea id="{name}" name="{name}">{esc(value)}</textarea>'
            elif field_type == "scope":
                options = ["Model family", "Generation", "Variant", "Model year"]
                option_rows = "".join(
                    f'<option {"selected" if value == option else ""}>{esc(option)}</option>' for option in options
                )
                control = f'<select id="{name}" name="{name}">{option_rows}</select>'
            elif field_type == "confidence":
                options = ["Manufacturer reported", "Registry documented", "Documented estimate", "High", "Unknown"]
                option_rows = "".join(
                    f'<option {"selected" if value == option else ""}>{esc(option)}</option>' for option in options
                )
                control = f'<select id="{name}" name="{name}">{option_rows}</select>'
            elif field_type == "source":
                options = ['<option value="">No source selected</option>'] + [
                    f'<option value="{source["id"]}" {"selected" if value == source["id"] else ""}>{esc(source["publisher"] or "Source")} — {esc(source["title"])}</option>'
                    for source in sources
                ]
                control = f'<select id="{name}" name="{name}">{"".join(options)}</select>'
            elif field_type == "boolean":
                control = f'<select id="{name}" name="{name}"><option value="0" {"selected" if not value else ""}>No</option><option value="1" {"selected" if value else ""}>Yes</option></select>'
            else:
                input_type = "number" if field_type in {"int", "float"} else "url" if field_type == "url" else "text"
                step = ' step="0.01"' if field_type == "float" else ""
                control = f'<input id="{name}" name="{name}" type="{input_type}"{step} value="{esc(value)}">'
            full = " full" if field_type == "textarea" or name in {"location", "url", "availability_scope"} else ""
            fields.append(f'<div class="field{full}"><label for="{name}">{esc(label)}</label>{control}</div>')

        body = f'''<div class="eyebrow">Correct an existing record</div>
        <h1>Edit {esc(config['title'])}</h1>
        <p class="muted">{esc(car['manufacturer'])} {esc(car['model_family'])} · changes remain in the same database.</p>
        <form class="card form-grid" method="post" action="/car/{quote(car_id)}/{kind}/{record_id}/update">
          {''.join(fields)}
          <div class="form-actions"><button>Save changes</button><a class="button ghost" href="/car/{quote(car_id)}#{config['anchor']}">Cancel</a></div>
        </form>'''
        self.send_html(page(f"Edit {config['title']}", body))

    def update_child(self, car_id: str, kind: str, record_id: int) -> None:
        config = CHILD_CONFIG[kind]
        form = get_form(self)
        assignments: list[str] = []
        values: list[object | None] = []
        for name, _label, field_type in config["fields"]:
            assignments.append(f"{name} = ?")
            raw = form.get(name)
            if field_type in {"int", "source", "boolean"}:
                values.append(as_int(raw))
            elif field_type == "float":
                values.append(as_float(raw))
            else:
                values.append(raw or None)
        with connect() as db:
            exists = db.execute(
                f"SELECT 1 FROM {config['table']} WHERE id = ? AND car_id = ?", (record_id, car_id)
            ).fetchone()
            if not exists:
                self.send_html(page("Not found", "<h1>Record not found</h1>"), 404); return
            if kind == "media" and form.get("is_primary") == "1":
                db.execute("UPDATE media SET is_primary = 0 WHERE car_id = ?", (car_id,))
            db.execute(
                f"UPDATE {config['table']} SET {', '.join(assignments)} WHERE id = ? AND car_id = ?",
                values + [record_id, car_id],
            )
        self.redirect(f"/car/{quote(car_id)}#{config['anchor']}")

    def delete_child(self, car_id: str, kind: str, record_id: int) -> None:
        config = CHILD_CONFIG[kind]
        with connect() as db:
            record = db.execute(
                f"SELECT * FROM {config['table']} WHERE id = ? AND car_id = ?", (record_id, car_id)
            ).fetchone()
            if not record:
                self.send_html(page("Not found", "<h1>Record not found</h1>"), 404); return
            if kind == "source":
                for table, column in (
                    ("cars", "primary_source_id"), ("facts", "source_id"), ("price_records", "source_id"),
                    ("media", "source_id"), ("attributes", "source_id"), ("color_records", "source_id"),
                    ("country_distribution", "source_id"),
                ):
                    db.execute(f"UPDATE {table} SET {column} = NULL WHERE {column} = ?", (record_id,))
            was_primary = kind == "media" and bool(record["is_primary"])
            db.execute(f"DELETE FROM {config['table']} WHERE id = ? AND car_id = ?", (record_id, car_id))
            if was_primary:
                replacement = db.execute("SELECT id FROM media WHERE car_id = ? ORDER BY id LIMIT 1", (car_id,)).fetchone()
                if replacement:
                    db.execute("UPDATE media SET is_primary = 1 WHERE id = ?", (replacement[0],))
        self.redirect(f"/car/{quote(car_id)}#{config['anchor']}")

    def create_car(self) -> None:
        form = get_form(self)
        if not form.get("manufacturer") or not form.get("model_family"):
            self.send_html(page("Missing information", '<div class="notice">Manufacturer and model family are required.</div>'+car_form("/cars")), 400); return
        car_id = "CAR-" + uuid.uuid4().hex[:12].upper()
        values = self.car_values(form)
        columns = ", ".join(["id"] + CAR_FIELDS + ["road_legal"])
        placeholders = ", ".join("?" for _ in range(len(CAR_FIELDS) + 2))
        with connect() as db:
            db.execute(f"INSERT INTO cars ({columns}) VALUES ({placeholders})", [car_id] + values + [1 if form.get('road_legal','1') == '1' else 0])
            migrate_hierarchy(db)
            migrate_source_references(db)
            sync_technical_attributes(db, car_id, form)
        self.redirect(f"/car/{quote(car_id)}")

    def update_car(self, car_id: str) -> None:
        form = get_form(self)
        values = self.car_values(form)
        assignments = ", ".join(f"{field} = ?" for field in CAR_FIELDS)
        with connect() as db:
            db.execute(f"UPDATE cars SET {assignments}, road_legal = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", values + [1 if form.get('road_legal','1') == '1' else 0, car_id])
            migrate_hierarchy(db)
            migrate_source_references(db)
            sync_technical_attributes(db, car_id, form)
        self.redirect(f"/car/{quote(car_id)}")

    @staticmethod
    def car_values(form: dict[str, str]) -> list[object | None]:
        numeric_int = {"model_year_from", "model_year_to"}
        numeric_float: set[str] = set()
        result: list[object | None] = []
        for field in CAR_FIELDS:
            if field in numeric_int: result.append(as_int(form.get(field)))
            elif field in numeric_float: result.append(as_float(form.get(field)))
            else: result.append(form.get(field) or None)
        return result

    def add_fact(self, car_id: str) -> None:
        f = get_form(self)
        with connect() as db:
            db.execute("INSERT INTO facts(car_id,title,category,explanation,why_it_matters,source_id,confidence,scope_level) VALUES(?,?,?,?,?,?,?,?)", (car_id,f.get('title'),f.get('category'),f.get('explanation'),f.get('why_it_matters'),as_int(f.get('source_id')),f.get('confidence') or 'Unknown',f.get('scope_level') or 'Variant'))
        self.redirect(f"/car/{quote(car_id)}")

    def add_attribute(self, car_id: str) -> None:
        f = get_form(self)
        with connect() as db:
            next_sort = db.execute(
                "SELECT COALESCE(MAX(sort_order), 0) + 10 FROM attributes WHERE car_id = ? AND section = ?",
                (car_id, f.get("section")),
            ).fetchone()[0]
            db.execute(
                """INSERT INTO attributes(car_id,section,label,value,unit,source_id,scope_level,sort_order)
                   VALUES(?,?,?,?,?,?,?,?)""",
                (
                    car_id,
                    f.get("section") or "Other",
                    f.get("label"),
                    f.get("value"),
                    f.get("unit"),
                    as_int(f.get("source_id")),
                    f.get("scope_level") or "Variant",
                    next_sort,
                ),
            )
        self.redirect(f"/car/{quote(car_id)}#specifications")

    def add_price(self, car_id: str) -> None:
        f = get_form(self)
        with connect() as db:
            db.execute("""INSERT INTO price_records(car_id,observation_date,price_type,amount,currency,market,venue,serial_number,mileage,source_id,notes) VALUES(?,?,?,?,?,?,?,?,?,?,?)""", (car_id,f.get('observation_date'),f.get('price_type'),as_float(f.get('amount')),f.get('currency'),f.get('market'),f.get('venue'),f.get('serial_number'),f.get('mileage'),as_int(f.get('source_id')),f.get('notes')))
        self.redirect(f"/car/{quote(car_id)}")

    def add_source(self, car_id: str) -> None:
        f = get_form(self)
        with connect() as db:
            db.execute("INSERT OR IGNORE INTO sources(car_id,publisher,title,source_type,url,notes) VALUES(?,?,?,?,?,?)", (car_id,f.get('publisher'),f.get('title'),f.get('source_type'),f.get('url'),f.get('notes')))
        self.redirect(f"/car/{quote(car_id)}")

    def add_color(self, car_id: str) -> None:
        f = get_form(self)
        with connect() as db:
            db.execute(
                """INSERT INTO color_records(
                       car_id,color_name,color_code,color_type,swatch_hex,availability_scope,
                       production_count,production_percentage,count_scope,source_id,confidence,scope_level,notes
                   ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    car_id, f.get("color_name"), f.get("color_code"), f.get("color_type") or "Exterior",
                    f.get("swatch_hex"), f.get("availability_scope"), as_int(f.get("production_count")),
                    as_float(f.get("production_percentage")), f.get("count_scope"), as_int(f.get("source_id")),
                    f.get("confidence") or "Unknown", f.get("scope_level") or "Variant", f.get("notes"),
                ),
            )
        self.redirect(f"/car/{quote(car_id)}#colors")

    def add_geography(self, car_id: str) -> None:
        f = get_form(self)
        with connect() as db:
            db.execute(
                """INSERT INTO country_distribution(
                       car_id,distribution_type,country,region,vehicle_count,share_percentage,
                       denominator,as_of_date,source_id,confidence,scope_level,notes
                   ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    car_id, f.get("distribution_type"), f.get("country"), f.get("region"),
                    as_int(f.get("vehicle_count")), as_float(f.get("share_percentage")),
                    as_int(f.get("denominator")), f.get("as_of_date"), as_int(f.get("source_id")),
                    f.get("confidence") or "Unknown", f.get("scope_level") or "Variant", f.get("notes"),
                ),
            )
        self.redirect(f"/car/{quote(car_id)}#geography")

    def add_media(self, car_id: str) -> None:
        f = get_form(self)
        with connect() as db:
            current = db.execute("SELECT COUNT(*) FROM media WHERE car_id = ?", (car_id,)).fetchone()[0]
            make_primary = current == 0 or f.get("is_primary") == "1"
            if make_primary:
                db.execute("UPDATE media SET is_primary = 0 WHERE car_id = ?", (car_id,))
            db.execute("INSERT INTO media(car_id,media_type,location,caption,creator,license,source_id,scope_level,is_primary) VALUES(?,?,?,?,?,?,?,?,?)", (car_id,f.get('media_type'),f.get('location'),f.get('caption'),f.get('creator'),f.get('license'),as_int(f.get('source_id')),f.get('scope_level') or 'Variant',1 if make_primary else 0))
        self.redirect(f"/car/{quote(car_id)}#gallery")

    def serve_asset(self, relative: str) -> None:
        target = (ASSET_DIR / relative).resolve()
        if ASSET_DIR.resolve() not in target.parents or not target.is_file():
            self.send_error(404); return
        payload = target.read_bytes()
        content_type = "image/jpeg" if target.suffix.lower() in {".jpg", ".jpeg"} else "image/png" if target.suffix.lower() == ".png" else "application/octet-stream"
        self.send_response(200); self.send_header("Content-Type", content_type); self.send_header("Content-Length", str(len(payload))); self.end_headers(); self.wfile.write(payload)

    def serve_web_file(self, name: str) -> None:
        target = (WEB_DIR / name).resolve()
        if WEB_DIR.resolve() not in target.parents or not target.is_file():
            self.send_error(404)
            return
        payload = target.read_bytes()
        content_type = "text/html; charset=utf-8" if target.suffix == ".html" else "text/css; charset=utf-8" if target.suffix == ".css" else "text/javascript; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def serve_data(self) -> None:
        with connect() as db:
            payload = json.dumps(build_payload(db), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[supercars] {self.address_string()} - {fmt % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local supercar database")
    parser.add_argument("--init-only", action="store_true", help="Create/upgrade the database, then exit")
    parser.add_argument("--port", type=int, default=int(os.environ.get("SUPERCAR_PORT", "8765")))
    args = parser.parse_args()
    initialize_database()
    if args.init_only:
        print(f"Database ready: {DB_PATH}")
        return
    server = ThreadingHTTPServer(("127.0.0.1", args.port), AppHandler)
    print(f"Supercar Archive: http://127.0.0.1:{args.port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
