"""Curated imports must retain evidence and preserve the existing catalogue."""
import json
import hashlib
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from scripts.import_curated import import_curated, ROOT
from test_startup import snapshot


class CuratedImportTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix='.test-curated-', dir=ROOT)
        self.addCleanup(self.folder.cleanup)
        self.db = Path(self.folder.name)/'archive.db'
        self.manifest = Path(self.folder.name)/'batch.json'
        self.data = json.loads((ROOT/'data/icons-road-01.json').read_text(encoding='utf8'))
        with closing(sqlite3.connect(ROOT/'supercars.db')) as original, closing(sqlite3.connect(self.db)) as copy:
            original.backup(copy)
            copy.execute('PRAGMA foreign_keys=ON')
            copy.executemany('DELETE FROM cars WHERE id=?', [(c['id'],) for c in self.data['cars']])
            copy.execute('DELETE FROM meta WHERE key=?', ('import:'+self.data['batch'],))
            copy.commit()
        self.save()

    def save(self):
        self.manifest.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf8')

    def test_additive_preview_apply_and_repeat(self):
        before = snapshot(self.db)
        self.assertEqual(import_curated(self.db, self.manifest), 4)
        self.assertEqual(before, snapshot(self.db))
        self.assertEqual(import_curated(self.db, self.manifest, True), 4)
        after = snapshot(self.db)
        self.assertEqual(len(after['cars']), len(before['cars'])+4)
        for table, rows in before.items():
            self.assertTrue(rows <= after[table], table)
        self.assertEqual(import_curated(self.db, self.manifest, True), 0)
        self.assertEqual(after, snapshot(self.db))

    def test_admission_reason_requires_a_sourced_public_fact(self):
        self.data['cars'][0]['admission_reason'] = 'A different reason, deliberately absent from the sourced public facts.'
        self.save()
        before = snapshot(self.db)
        with self.assertRaisesRegex(ValueError, 'sourced public fact'):
            import_curated(self.db, self.manifest, True)
        self.assertEqual(before, snapshot(self.db))

    def test_line_endings_preserve_legacy_markers_and_all_rows(self):
        lf = json.dumps(self.data, ensure_ascii=False, indent=2).encode('utf8')
        crlf = lf.replace(b'\n', b'\r\n')
        self.manifest.write_bytes(crlf)
        self.assertEqual(import_curated(self.db, self.manifest, True), 4)
        marker = 'import:' + self.data['batch']
        with closing(sqlite3.connect(self.db)) as db:
            self.assertEqual(db.execute('SELECT value FROM meta WHERE key=?',
                                       (marker,)).fetchone()[0], hashlib.sha256(lf).hexdigest())
        for historical, checkout in ((lf, crlf), (crlf, lf)):
            with self.subTest(historical_crlf=b'\r\n' in historical):
                with closing(sqlite3.connect(self.db)) as db, db:
                    db.execute('UPDATE meta SET value=? WHERE key=?',
                               (hashlib.sha256(historical).hexdigest(), marker))
                before = snapshot(self.db)
                self.manifest.write_bytes(checkout)
                self.assertEqual(import_curated(self.db, self.manifest), 0)
                self.assertEqual(import_curated(self.db, self.manifest, True), 0)
                self.assertEqual(before, snapshot(self.db))

    def test_source_edit_still_rejects_previously_applied_manifest(self):
        self.assertEqual(import_curated(self.db, self.manifest, True), 4)
        before = snapshot(self.db)
        self.data['cars'][0]['sources'][0]['notes'] += ' Changed evidence note.'
        self.save()
        with self.assertRaisesRegex(ValueError, 'different manifest'):
            import_curated(self.db, self.manifest, True)
        self.assertEqual(before, snapshot(self.db))

    def test_declared_count_must_match(self):
        self.data['expected_count'] = 5
        self.save()
        with self.assertRaisesRegex(ValueError, 'count'):
            import_curated(self.db, self.manifest, True)

    def test_export_failure_rolls_back(self):
        before = snapshot(self.db)
        with patch('scripts.import_supercars50.build_payload', side_effect=ValueError('export sentinel')):
            with self.assertRaisesRegex(ValueError, 'export sentinel'):
                import_curated(self.db, self.manifest, True)
        self.assertEqual(before, snapshot(self.db))

    def test_all_curated_batches_preserve_baseline_and_do_not_collide(self):
        batches = [(path, json.loads(path.read_text(encoding='utf8')))
                   for path in sorted((ROOT/'data').glob('icons-road-*.json'))]
        with closing(sqlite3.connect(self.db)) as db, db:
            db.execute('PRAGMA foreign_keys=ON')
            for _, data in batches:
                db.executemany('DELETE FROM cars WHERE id=?', [(c['id'],) for c in data['cars']])
                db.execute('DELETE FROM meta WHERE key=?', ('import:'+data['batch'],))
        before = snapshot(self.db)
        expected = len(before['cars'])
        for path, data in batches:
            with self.subTest(batch=data['batch']):
                self.assertEqual(import_curated(self.db, path, True), data['expected_count'])
                expected += data['expected_count']
                self.assertEqual(import_curated(self.db, path, True), 0)
        after = snapshot(self.db)
        self.assertEqual(len(after['cars']), expected)
        for table, rows in before.items():
            self.assertTrue(rows <= after[table], table)


if __name__ == '__main__':
    unittest.main()
