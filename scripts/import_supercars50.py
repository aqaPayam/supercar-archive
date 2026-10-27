"""Validate and atomically import the reviewed 50-car supercar batch.

No network or package installation is required. By default this only previews
the import; pass --apply to change the selected database.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import unicodedata
from contextlib import closing
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from export_public import build_payload

MANIFEST = ROOT / 'data' / 'supercars50.json'
CAR_COLUMNS = ('id', 'manufacturer', 'model_family', 'generation', 'variant',
 'model_year_from', 'model_year_to', 'origin_country', 'category', 'body_style',
 'road_legal', 'specification_market', 'summary')


def normalized(value):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', str(value)).casefold())


def identity(car):
    # Changing a reference year or generation label cannot create a new variant.
    return tuple(normalized(car[field]) for field in
                 ('manufacturer', 'model_family', 'variant'))


def insert(db, table, values):
    names = ','.join(values)
    placeholders = ','.join('?' for _ in values)
    return db.execute(f'INSERT INTO {table} ({names}) VALUES ({placeholders})',
                      tuple(values.values())).lastrowid


def load_manifest(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    cars = data['cars']
    if len(cars) != 50 or len({car['id'] for car in cars}) != 50:
        raise ValueError('The batch must contain exactly 50 distinct car IDs')
    if len({identity(car) for car in cars}) != 50:
        raise ValueError('Duplicate normalized vehicle identities in the batch')
    for car in cars:
        if not car['origin_country'] or not car['sources']:
            raise ValueError(f"Missing origin or sources: {car['id']}")
        if len(car['attributes']) < 6 or not car['facts'] or not car['media']:
            raise ValueError(f"Incomplete reviewed profile: {car['id']}")
        for source in car['sources']:
            if not source['url'].startswith('https://'):
                raise ValueError('Sources must have HTTPS URLs')
        for table in ('attributes', 'facts', 'media', 'price_records', 'color_records'):
            for row in car.get(table, []):
                if not 0 <= row['source'] < len(car['sources']):
                    raise ValueError(f"Unresolved {table} evidence: {car['id']}")
        for media in car['media']:
            relative = Path(media['location'].removeprefix('/'))
            target = (ROOT / relative).resolve()
            if ROOT / 'assets' not in target.parents or not target.is_file():
                raise ValueError(f'Missing or unsafe image: {target}')
            if hashlib.sha256(target.read_bytes()).hexdigest() != media['sha256']:
                raise ValueError(f'Image checksum differs: {target}')
            if not media['creator'] or not media['license']:
                raise ValueError('Every image must have creator and license attribution')
    return data, hashlib.sha256(raw).hexdigest()


def apply_batch(path, manifest_path=MANIFEST, apply=False):
    data, digest = load_manifest(manifest_path)
    cars = data['cars']
    marker = 'import:' + data['batch']
    with closing(sqlite3.connect(f'file:{path.resolve().as_posix()}?mode={"rw" if apply else "ro"}', uri=True)) as db:
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        if apply:
            db.execute('BEGIN IMMEDIATE')
        try:
            previous = db.execute('SELECT value FROM meta WHERE key=?', (marker,)).fetchone()
            if previous:
                if previous[0] != digest:
                    raise ValueError('This batch was already applied with a different manifest')
                for car in cars:
                    existing = db.execute('SELECT * FROM cars WHERE id=?', (car['id'],)).fetchone()
                    if existing is None or any(existing[k] != car[k] for k in CAR_COLUMNS):
                        raise ValueError(f"Previously imported car was changed or removed: {car['id']}")
                print('Already applied: 50 matching profiles; no changes made.')
                return 0

            existing = list(db.execute('SELECT * FROM cars'))
            ids = {r['id'] for r in existing}
            identities = {identity(r) for r in existing}
            for car in cars:
                if car['id'] in ids or identity(car) in identities:
                    raise ValueError(f"Existing variant collision: {car['id']}")
            print(f"Validated 50 new profiles against {len(existing)} existing cars.")
            if not apply:
                print('Preview only; use --apply to import.')
                return 50

            for car in cars:
                family = db.execute('SELECT id FROM model_families WHERE manufacturer=? AND name=?',
                                    (car['manufacturer'], car['model_family'])).fetchone()
                family_id = family[0] if family else insert(db, 'model_families', dict(
                    manufacturer=car['manufacturer'], name=car['model_family'], origin_country=car['origin_country']))
                generation = db.execute('SELECT id FROM generations WHERE family_id=? AND name=?',
                                        (family_id, car['generation'])).fetchone()
                generation_id = generation[0] if generation else insert(db, 'generations', dict(
                    family_id=family_id, name=car['generation'],
                    year_from=car['model_year_from'], year_to=None))
                values = {key: car[key] for key in CAR_COLUMNS}
                values.update(family_id=family_id, generation_id=generation_id)
                insert(db, 'cars', values)
                sources = [insert(db, 'sources', dict(car_id=car['id'], **source))
                           for source in car['sources']]
                db.execute('UPDATE cars SET primary_source_id=? WHERE id=?', (sources[0], car['id']))
                for table in ('attributes', 'facts', 'media', 'price_records', 'color_records'):
                    for order, row in enumerate(car.get(table, [])):
                        values = {k: v for k,v in row.items() if k not in ('source', 'sha256')}
                        values.update(car_id=car['id'], source_id=sources[row['source']])
                        if table in ('attributes', 'facts', 'media', 'color_records'):
                            values['scope_level'] = 'Variant'
                        if table == 'attributes':
                            values['sort_order'] = (order + 1) * 10
                        insert(db, table, values)
            insert(db, 'meta', dict(key=marker, value=digest))
            if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise ValueError('Database integrity check failed')
            if db.execute('PRAGMA foreign_key_check').fetchall():
                raise ValueError('Foreign-key validation failed')
            payload = build_payload(db)
            if len(payload['cars']) != len(existing) + 50:
                raise ValueError('Unexpected catalogue count after import')
            db.commit()
            print(f"Imported 50 cars; catalogue now contains {len(payload['cars'])} cars.")
            return 50
        except BaseException:
            db.rollback()
            raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, default=ROOT/'supercars.db')
    parser.add_argument('--manifest', type=Path, default=MANIFEST)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    apply_batch(args.db, args.manifest, args.apply)
