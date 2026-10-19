"""Regression coverage: opening the local viewer must preserve catalogue data."""
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import supercar_app as app
from export_public import build_payload


def snapshot(path):
    with closing(sqlite3.connect(path)) as db:
        return {
            table: set(db.execute('SELECT * FROM "' + table + '"'))
            for (table,) in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
        }


class StartupPreservationTests(unittest.TestCase):
    def test_current_catalogue_is_unchanged_after_repeated_startup(self):
        with tempfile.TemporaryDirectory(prefix=".test-startup-", dir=app.ROOT) as folder:
            path = Path(folder) / "catalogue.db"
            with closing(sqlite3.connect(app.DB_PATH)) as original, closing(sqlite3.connect(path)) as copy:
                original.backup(copy)
            before = snapshot(path)
            with closing(sqlite3.connect(path)) as db:
                db.row_factory = sqlite3.Row
                payload = build_payload(db)
            with patch.object(app, "DB_PATH", path):
                app.initialize_database()
                app.initialize_database()
            self.assertEqual(before, snapshot(path))
            with closing(sqlite3.connect(path)) as db:
                db.row_factory = sqlite3.Row
                self.assertEqual(payload, build_payload(db))
                self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
                self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_fresh_database_is_seeded_once(self):
        with tempfile.TemporaryDirectory(prefix=".test-fresh-", dir=app.ROOT) as folder:
            path = Path(folder) / "catalogue.db"
            with patch.object(app, "DB_PATH", path):
                app.initialize_database()
                before = snapshot(path)
                self.assertEqual(len(before['cars']), 1)
                self.assertIn(('schema_version', '3'), before['meta'])
                app.initialize_database()
            self.assertEqual(before, snapshot(path))


if __name__ == '__main__':
    unittest.main()
