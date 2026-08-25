from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Iterator, Sequence


class Database(ABC):
    """Gemeinsamer Vertrag fuer austauschbare Datenbank-Adapter."""

    @abstractmethod
    def connect(self) -> None:
        """Stellt die Datenbankverbindung her."""

    @abstractmethod
    def close(self) -> None:
        """Schliesst die Datenbankverbindung."""

    @abstractmethod
    def execute(self, query: str, parameters: Sequence[Any] = ()) -> Any:
        """Fuehrt ein parametrisiertes Statement aus."""

    @abstractmethod
    def execute_script(self, script: str) -> None:
        """Fuehrt mehrere Statements aus, z. B. fuer die Initialisierung."""

    @abstractmethod
    def commit(self) -> None:
        """Bestaetigt die aktuelle Transaktion."""

    @abstractmethod
    def rollback(self) -> None:
        """Verwirft die aktuelle Transaktion."""

    @contextmanager
    def transaction(self) -> Iterator["Database"]:
        """Bestaetigt erfolgreiche Arbeit und rollt bei Fehlern zurueck."""
        try:
            yield self
            self.commit()
        except Exception:
            self.rollback()
            raise

    def __enter__(self) -> "Database":
        self.connect()
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        self.close()
