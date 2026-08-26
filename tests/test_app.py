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

    def test_index_shows_empty_news_state(self) -> None:
        response = self.client.get("/")

        self.assertIn(
            "Aktuell liegen keine Meldungen vor.", response.get_data(as_text=True)
        )

    def test_index_shows_three_newest_anliegen_with_details(self) -> None:
        entries = [
            ("Älteste Katze", "2026-08-20 10:00:00"),
            ("Drittneueste Katze", "2026-08-21 10:00:00"),
            ("Zweitneueste Katze", "2026-08-22 10:00:00"),
            ("Neueste Katze", "2026-08-23 10:00:00"),
        ]
        with SQLiteDatabase(self.database_path) as database:
            with database.transaction():
                for title, date in entries:
                    database.execute(
                        """
                        INSERT INTO anliegen
                            (titel, beschreibung, kategorie, ort, datum)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (title, "Katzenbeschreibung", "Katzennews", "Musterstadt", date),
                    )

        page = self.client.get("/").get_data(as_text=True)

        self.assertNotIn("Älteste Katze", page)
        self.assertLess(page.index("Neueste Katze"), page.index("Zweitneueste Katze"))
        self.assertLess(
            page.index("Zweitneueste Katze"), page.index("Drittneueste Katze")
        )
        self.assertIn("Katzenbeschreibung", page)
        self.assertIn("Katzennews", page)
        self.assertIn("Musterstadt", page)
        self.assertIn("23.08.2026", page)
        self.assertIn('href="/aktuelles"', page)

    def test_aktuelles_shows_all_anliegen_newest_first(self) -> None:
        entries = [
            ("Älteste Meldung", "2026-08-20 10:00:00"),
            ("Neueste Meldung", "2026-08-23 10:00:00"),
            ("Mittlere Meldung", "2026-08-22 10:00:00"),
        ]
        with SQLiteDatabase(self.database_path) as database:
            with database.transaction():
                for title, date in entries:
                    database.execute(
                        """
                        INSERT INTO anliegen
                            (titel, beschreibung, kategorie, ort, datum)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (title, "Beschreibung", "Kategorie", "Musterstadt", date),
                    )

        response = self.client.get("/aktuelles")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Älteste Meldung", page)
        self.assertLess(page.index("Neueste Meldung"), page.index("Mittlere Meldung"))
        self.assertLess(page.index("Mittlere Meldung"), page.index("Älteste Meldung"))

    def test_aktuelles_shows_empty_state(self) -> None:
        response = self.client.get("/aktuelles")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Aktuell liegen keine Meldungen vor.", response.get_data(as_text=True)
        )

    def test_seed_data_is_loaded_idempotently_and_restores_missing_entries(self) -> None:
        seeded_database_path = Path(self.temporary_directory.name) / "seeded.sqlite3"
        config = {
            "TESTING": True,
            "DATABASE_PATH": seeded_database_path,
            "SEED_DATABASE": True,
        }

        create_app(config)

        with SQLiteDatabase(seeded_database_path) as database:
            database.execute(
                "DELETE FROM anliegen WHERE titel = ?",
                ("Betrunkene Katze fährt in ein KFC",),
            )
            database.commit()

        create_app(config)

        with SQLiteDatabase(seeded_database_path) as database:
            count = database.execute("SELECT COUNT(*) FROM anliegen").fetchone()[0]
            missing_image_count = database.execute(
                "SELECT COUNT(*) FROM anliegen WHERE foto_pfad IS NULL"
            ).fetchone()[0]
            image_paths = database.execute(
                """
                SELECT titel, foto_pfad
                FROM anliegen
                WHERE foto_pfad IS NOT NULL
                ORDER BY datum, id
                """
            ).fetchall()

        self.assertEqual(count, 66)
        self.assertEqual(missing_image_count, 0)
        self.assertEqual(
            [row[1] for row in image_paths[:6]],
            [
                "img/news/01-kfc-unfall.png",
                "img/news/02-katzenminze-ermittlung.png",
                "img/news/03-katzenschalter.png",
                "img/news/04-karlo-entschuldigung.png",
                "img/news/05-kfc-wiedereroeffnung.png",
                "img/news/06-minka-vermisst.png",
            ],
        )
        self.assertEqual(len(image_paths), 66)
        paths_by_title = {row[0]: row[1] for row in image_paths}
        expected_codex_images = {
            "Pfotenabdrücke führen zum alten Glockenturm": "codex-clipboard-78030a55-1409-49dd-97a3-b78b9ba2a12c.png",
            "Feuerwehr rettet Minka aus dem Glockenturm": "codex-clipboard-924843c7-ec03-4588-b9bc-fa389a320967.png",
            "Minka dankt ihren Retterkatzen mit Rathausfest": "codex-clipboard-6324df55-0983-436b-8ec9-09f06c502d9f.png",
            "Kätzchen entdeckt geheimen Tunnel unter dem Marktplatz": "codex-clipboard-a8e23707-52d0-417c-beb5-73bd05e411d7.png",
            "Katzenarchäologen untersuchen Marktplatztunnel": "codex-clipboard-ac82dcb2-d42f-4730-b030-b90e8124c24e.png",
            "Tunnel war historische Katzenpost-Route": "codex-clipboard-94478d2f-d0fc-4aea-8430-82b726283ed0.png",
            "Historischer Katzentunnel wird sonntags geöffnet": "codex-clipboard-08f2ced3-7424-4549-a6ac-0333245d9caf.png",
            "Seltenes Katzenkochbuch aus Bibliothek verschwunden": "codex-clipboard-0cbb3681-c956-4d8e-a081-cb54bcb666d3.png",
            "Bibliothekskater Goethe entdeckt verdächtige Krümelspur": "codex-clipboard-7f4b0fd2-d8a5-41c0-b70a-cd0c4e6badf7.png",
            "Katzenkochbuch hinter Sitzkissen wiedergefunden": "codex-clipboard-2c69eb82-9365-4647-a8af-e141455d052f.png",
            "Kater meldet verdächtig leeren Futternapf": "codex-clipboard-111e8683-1e99-494b-937d-4b8837082db3.png",
        }
        for title, filename in expected_codex_images.items():
            self.assertEqual(paths_by_title[title], f"img/news/{filename}")

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

    def test_easter_egg_is_linked_from_the_portal(self) -> None:
        page = self.client.get("/").get_data(as_text=True)

        self.assertIn('href="/katzenklo"', page)
        self.assertIn("Nicht streicheln", page)
        self.assertIn("/static/footer_easter_egg.js", page)
        for filename in (
            "minka-calm.webp",
            "minka-annoyed.webp",
            "minka-angry.webp",
            "minka-furious.webp",
        ):
            self.assertIn(f"/static/img/{filename}", page)
            with self.client.get(f"/static/img/{filename}") as response:
                self.assertEqual(response.status_code, 200)

    def test_pic_pac_paw_page_is_available(self) -> None:
        response = self.client.get("/katzenklo")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Pic Pac Paw", page)
        self.assertIn(
            "Da du Minka gestreichelt hast, fordert sie dich zu einem Pic Pac Paw Duell heraus.",
            page,
        )
        self.assertEqual(page.count('data-cell="'), 9)
        self.assertIn('/static/tic_tac_toe.js', page)
        self.assertIn('/static/img/paw-light.png', page)
        self.assertIn('/static/img/paw-dark.png', page)
        for emote in ("neutral", "angry", "laughing", "defeated"):
            asset_path = f"/static/img/minka-game-{emote}.webp"
            self.assertIn(asset_path, page)
            with self.client.get(asset_path) as emote_response:
                self.assertEqual(emote_response.status_code, 200)
        self.assertIn('href="/"', page)

        for asset_path in (
            "/static/img/paw-light.png",
            "/static/img/paw-dark.png",
            "/static/tic_tac_toe.js",
        ):
            with self.subTest(asset_path=asset_path):
                with self.client.get(asset_path) as asset_response:
                    self.assertEqual(asset_response.status_code, 200)

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
