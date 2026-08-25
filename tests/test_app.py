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

    def test_index_is_available(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Willkommen im Bürgerportal", response.get_data(as_text=True))

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
        create_response = self.client.post(
            "/api/anliegen",
            json={
                "titel": "Defekte Straßenlaterne",
                "beschreibung": "Die Laterne flackert seit zwei Tagen.",
                "kategorie": "Beleuchtung",
                "ort": "Marktplatz 1",
            },
        )

        self.assertEqual(create_response.status_code, 201)
        detail_response = self.client.get(create_response.headers["Location"])
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.get_json()["status"], "offen")

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
