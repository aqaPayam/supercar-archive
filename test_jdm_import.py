"""The JDM import must be additive, repeat-safe, and transactional."""
import sqlite3
import hashlib
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from scripts.import_jdm50 import apply_batch, load_manifest, MANIFEST, ROOT
from test_startup import snapshot


class JdmImportTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix='.test-jdm-', dir=ROOT)
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
                       (data['cars'][0]['id'], 'Nissan', 'Collision sentinel'))
        before = snapshot(self.path)
        with self.assertRaisesRegex(ValueError, 'collision'):
            apply_batch(self.path, apply=True)
        self.assertEqual(before, snapshot(self.path))

    def test_line_endings_preserve_legacy_markers_and_all_rows(self):
        lf = MANIFEST.read_bytes().replace(b'\r\n', b'\n')
        crlf = lf.replace(b'\n', b'\r\n')
        manifest = Path(self.folder.name)/'batch.json'
        manifest.write_bytes(crlf)
        self.assertEqual(apply_batch(self.path, manifest, True), 50)
        data, digest = load_manifest(manifest)
        self.assertEqual(digest, hashlib.sha256(lf).hexdigest())
        marker = 'import:' + data['batch']
        with closing(sqlite3.connect(self.path)) as db:
            self.assertEqual(db.execute('SELECT value FROM meta WHERE key=?',
                                       (marker,)).fetchone()[0], digest)
        for historical, checkout in ((lf, crlf), (crlf, lf)):
            with self.subTest(historical_crlf=b'\r\n' in historical):
                with closing(sqlite3.connect(self.path)) as db, db:
                    db.execute('UPDATE meta SET value=? WHERE key=?',
                               (hashlib.sha256(historical).hexdigest(), marker))
                before = snapshot(self.path)
                manifest.write_bytes(checkout)
                self.assertEqual(apply_batch(self.path, manifest), 0)
                self.assertEqual(apply_batch(self.path, manifest, True), 0)
                self.assertEqual(before, snapshot(self.path))

    def test_failed_export_validation_rolls_back_all_writes(self):
        before = snapshot(self.path)
        with patch('scripts.import_jdm50.build_payload', side_effect=ValueError('sentinel validation failure')):
            with self.assertRaisesRegex(ValueError, 'sentinel'):
                apply_batch(self.path, apply=True)
        self.assertEqual(before, snapshot(self.path))


if __name__ == '__main__':
    unittest.main()
