import sqlite3
from pathlib import Path
from typing import Any, Sequence

from .base import Database


class SQLiteDatabase(Database):
    """SQLite-Adapter hinter dem allgemeinen Database-Interface."""

    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)
        self._connection: sqlite3.Connection | None = None

    @property
    def connection(self) -> sqlite3.Connection:
        if self._connection is None:
            raise RuntimeError("Die Datenbank ist nicht verbunden. connect() zuerst aufrufen.")
        return self._connection

    def connect(self) -> None:
        if self._connection is not None:
            return

        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def execute(
        self, query: str, parameters: Sequence[Any] = ()
    ) -> sqlite3.Cursor:
        return self.connection.execute(query, parameters)

    def execute_script(self, script: str) -> None:
        self.connection.executescript(script)

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()
