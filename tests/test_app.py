import re
import tempfile
import unittest
from pathlib import Path

from app import create_app
from app.database.sqlite import SQLiteDatabase


class ApplicationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temporary_directory.name) / "test.sqlite3"
        self.app = create_app(
            {"TESTING": True, "DATABASE_PATH": self.database_path}
        )
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def create_anliegen(self, **overrides):
        payload = {
            "titel": "Defekte Straßenlaterne",
            "beschreibung": "Die Laterne flackert seit zwei Tagen.",
            "kategorie": "Beleuchtung",
            "ort": "Marktplatz 1",
        }
        payload.update(overrides)
        return self.client.post("/api/anliegen", json=payload)

    def test_index_is_available(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Willkommen im Bürgerportal", response.get_data(as_text=True))

    def test_index_links_to_legal_pages(self) -> None:
        response = self.client.get("/")
        page = response.get_data(as_text=True)

        self.assertIn('href="/impressum"', page)
        self.assertIn('href="/datenschutz"', page)

    def test_legal_pages_are_available(self) -> None:
        pages = {
            "/impressum": "<h1>Impressum</h1>",
            "/datenschutz": "<h1>Datenschutzerklärung</h1>",
        }

        for path, expected_heading in pages.items():
            with self.subTest(path=path):
                response = self.client.get(path)
                page = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)
                self.assertIn(expected_heading, page)
                self.assertIn('lang="de"', page)
                self.assertIn('href="/"', page)

    def test_static_assets_referenced_on_index_are_available(self) -> None:
        index_response = self.client.get("/")
        asset_paths = set(
            re.findall(
                r'(?:href|src)="(/static/[^"]+)"',
                index_response.get_data(as_text=True),
            )
        )

        self.assertTrue(asset_paths)
        for asset_path in asset_paths:
            with self.subTest(asset_path=asset_path):
                with self.client.get(asset_path) as response:
                    self.assertEqual(response.status_code, 200)

    def test_anliegen_schema_contains_expected_fields(self) -> None:
        expected_fields = {
            "id",
            "titel",
            "beschreibung",
            "kategorie",
            "ort",
            "foto_pfad",
            "datum",
            "status",
        }

        with SQLiteDatabase(self.database_path) as database:
            rows = database.execute("PRAGMA table_info(anliegen)").fetchall()

        self.assertEqual({row["name"] for row in rows}, expected_fields)

    def test_anliegen_can_be_created_and_loaded(self) -> None:
        create_response = self.create_anliegen()

        self.assertEqual(create_response.status_code, 201)
        detail_response = self.client.get(create_response.headers["Location"])
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.get_json()["status"], "offen")

    def test_anliegen_list_is_initially_empty(self) -> None:
        response = self.client.get("/api/anliegen")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_anliegen_list_is_sorted_by_newest_first(self) -> None:
        first_response = self.create_anliegen(titel="Erstes Anliegen")
        second_response = self.create_anliegen(titel="Zweites Anliegen")

        response = self.client.get("/api/anliegen")
        entries = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [entry["id"] for entry in entries],
            [second_response.get_json()["id"], first_response.get_json()["id"]],
        )

    def test_optional_fields_are_stored(self) -> None:
        create_response = self.create_anliegen(
            foto_pfad="uploads/laterne.jpg", status="in_bearbeitung"
        )

        detail_response = self.client.get(create_response.headers["Location"])
        anliegen = detail_response.get_json()

        self.assertEqual(anliegen["foto_pfad"], "uploads/laterne.jpg")
        self.assertEqual(anliegen["status"], "in_bearbeitung")

    def test_each_required_field_is_validated(self) -> None:
        valid_payload = {
            "titel": "Defekte Straßenlaterne",
            "beschreibung": "Die Laterne flackert seit zwei Tagen.",
            "kategorie": "Beleuchtung",
            "ort": "Marktplatz 1",
        }

        for required_field in valid_payload:
            with self.subTest(required_field=required_field):
                payload = valid_payload.copy()
                payload.pop(required_field)

                response = self.client.post("/api/anliegen", json=payload)

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.get_json(),
                    {
                        "error": "Pflichtfelder fehlen.",
                        "fields": [required_field],
                    },
                )

    def test_empty_json_reports_all_required_fields(self) -> None:
        response = self.client.post("/api/anliegen", json={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["fields"],
            ["titel", "beschreibung", "kategorie", "ort"],
        )

    def test_unknown_anliegen_returns_not_found(self) -> None:
        response = self.client.get("/api/anliegen/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Anliegen nicht gefunden."})

    def test_health_checks_database_connection(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(), {"status": "ok", "database": "connected"}
        )

    def test_database_transaction_rolls_back_on_error(self) -> None:
        database_path = Path(self.temporary_directory.name) / "transaction.sqlite3"

        with SQLiteDatabase(database_path) as database:
            database.execute("CREATE TABLE example (value TEXT NOT NULL)")

            with self.assertRaises(RuntimeError):
                with database.transaction():
                    database.execute("INSERT INTO example VALUES (?)", ("test",))
                    raise RuntimeError("rollback")

            count = database.execute("SELECT COUNT(*) FROM example").fetchone()[0]

        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
