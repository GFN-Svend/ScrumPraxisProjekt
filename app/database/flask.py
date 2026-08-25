from pathlib import Path

from flask import Flask, current_app, g

from .base import Database
from .sqlite import SQLiteDatabase


def get_database() -> Database:
    """Liefert pro Flask-Kontext genau eine Datenbankverbindung."""
    if "database" not in g:
        database_factory = current_app.config.get("DATABASE_FACTORY")
        database = (
            database_factory()
            if database_factory is not None
            else SQLiteDatabase(current_app.config["DATABASE_PATH"])
        )

        if not isinstance(database, Database):
            raise TypeError("DATABASE_FACTORY muss eine Database-Instanz liefern.")

        database.connect()
        g.database = database

    return g.database


def close_database(_exception: BaseException | None = None) -> None:
    database = g.pop("database", None)
    if database is not None:
        database.close()


def init_database(app: Flask) -> None:
    """Registriert den Adapter und legt das Schema bei Bedarf an."""
    app.teardown_appcontext(close_database)

    schema_path = Path(__file__).with_name("schema.sql")
    with app.app_context():
        database = get_database()
        database.execute_script(schema_path.read_text(encoding="utf-8"))
