"""The supercar import must be additive, repeat-safe, and transactional."""
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from scripts.import_supercars50 import apply_batch, load_manifest, MANIFEST, ROOT
from test_startup import snapshot


class SupercarImportTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix='.test-supercars-', dir=ROOT)
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name)/'archive.db'
        with closing(sqlite3.connect(ROOT/'supercars.db')) as original, closing(sqlite3.connect(self.path)) as copy:
            original.backup(copy)
            data,_ = load_manifest(MANIFEST)
            marker = 'import:' + data['batch']
            if copy.execute('SELECT 1 FROM meta WHERE key=?',(marker,)).fetchone():
                copy.execute('PRAGMA foreign_keys=ON')
                copy.executemany('DELETE FROM cars WHERE id=?',[(c['id'],) for c in data['cars']])
                copy.execute('DELETE FROM meta WHERE key=?',(marker,))
                copy.commit()

    def test_adds_exactly_50_preserves_existing_rows_and_is_repeat_safe(self):
        before = snapshot(self.path)
        self.assertEqual(apply_batch(self.path, apply=True), 50)
        after = snapshot(self.path)
        self.assertEqual(len(after['cars']), len(before['cars'])+50)
        for table, rows in before.items():
            self.assertTrue(rows <= after[table], f'Existing {table} records changed')
        self.assertEqual(apply_batch(self.path, apply=True), 0)
        self.assertEqual(after, snapshot(self.path))

    def test_existing_id_collision_rejects_entire_import(self):
        data,_ = load_manifest(MANIFEST)
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute("INSERT INTO cars(id,manufacturer,model_family) VALUES(?,?,?)",
                       (data['cars'][0]['id'], 'Ferrari', 'Collision sentinel'))
        before = snapshot(self.path)
        with self.assertRaisesRegex(ValueError, 'collision'):
            apply_batch(self.path, apply=True)
        self.assertEqual(before, snapshot(self.path))

    def test_failed_export_validation_rolls_back_all_writes(self):
        before = snapshot(self.path)
        with patch('scripts.import_supercars50.build_payload', side_effect=ValueError('sentinel validation failure')):
            with self.assertRaisesRegex(ValueError, 'sentinel'):
                apply_batch(self.path, apply=True)
        self.assertEqual(before, snapshot(self.path))

    def test_renamed_generation_or_year_is_not_a_new_variant(self):
        data,_ = load_manifest(MANIFEST)
        car = data['cars'][0]
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute('INSERT INTO cars(id,manufacturer,model_family,generation,variant,model_year_from) VALUES(?,?,?,?,?,?)',
                       ('COLLISION-SENTINEL', car['manufacturer'], car['model_family'],
                        'Different generation wording', car['variant'].upper(), 1900))
        before = snapshot(self.path)
        with self.assertRaisesRegex(ValueError, 'collision'):
            apply_batch(self.path, apply=True)
        self.assertEqual(before, snapshot(self.path))

    def test_preview_is_read_only(self):
        before = snapshot(self.path)
        self.assertEqual(apply_batch(self.path), 50)
        self.assertEqual(before, snapshot(self.path))


if __name__ == '__main__':
    unittest.main()

