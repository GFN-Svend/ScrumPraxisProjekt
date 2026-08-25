# ScrumPraxisProjekt

Kleine Flask-Webanwendung mit einer austauschbaren Datenbankschicht und SQLite
als lokaler Standarddatenbank.

## Lokal starten

Voraussetzung ist Python 3.10 oder neuer. Beim ersten Start:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python start.py
```

Unter macOS oder Linux wird die Umgebung mit `source .venv/bin/activate`
aktiviert. Danach ist die Website unter <http://127.0.0.1:5000> erreichbar.
Die SQLite-Datei wird automatisch unter `instance/scrum_praxis.sqlite3`
angelegt. Der Ordner `instance/` ist absichtlich nicht Teil des Repositories.

Optionale Umgebungsvariablen:

- `HOST` legt die Netzwerkadresse fest (Standard: `127.0.0.1`).
- `PORT` legt den Port fest (Standard: `5000`).
- `FLASK_DEBUG=0` deaktiviert den Debug-Modus.

## Datenbankschicht

`app/database/base.py` definiert den allgemeinen `Database`-Vertrag.
`app/database/sqlite.py` implementiert ihn für SQLite. Flask öffnet in
`app/database/flask.py` pro Anwendungskontext eine Verbindung und schließt sie
anschließend automatisch. Das Schema in `app/database/schema.sql` wird beim
Start idempotent initialisiert. Die Tabelle `anliegen` enthält `id`, `titel`,
`beschreibung`, `kategorie`, `ort`, `foto_pfad`, `datum` und `status`.

Für einen späteren Wechsel, beispielsweise zu PostgreSQL, wird eine neue
Unterklasse von `Database` implementiert. Über `DATABASE_FACTORY` wird dann
eine parameterlose Factory-Funktion in der Flask-Konfiguration gesetzt, die
den neuen Adapter samt seiner Verbindungsparameter erzeugt. Routen greifen
ausschließlich über `get_database()` auf die Datenbank zu.

## Nützliche Endpunkte

- `/` zeigt die Startseite.
- `/health` prüft Anwendung und Datenbankverbindung.
- `GET /api/anliegen` listet alle Anliegen.
- `GET /api/anliegen/<id>` liefert ein einzelnes Anliegen.
- `POST /api/anliegen` legt ein Anliegen aus JSON-Daten an.

## Tests ausführen

```powershell
python -m unittest discover -s tests
```

## Automatischer Test-Workflow

Der GitHub-Actions-Workflow `.github/workflows/tests.yml` läuft bei jedem Push,
bei jedem Pull Request und bei manueller Ausführung. Er prüft die Anwendung mit
Python 3.10 und 3.14 nach folgenden Kriterien:

- Alle Abhängigkeiten aus `requirements.txt` lassen sich installieren.
- Alle Python-Dateien lassen sich ohne Syntaxfehler kompilieren.
- Alle automatisierten Tests unter `tests/` sind erfolgreich.

Schlägt eines der Kriterien fehl, wird der Workflow rot markiert. Damit ein
fehlerhafter Pull Request nicht nach `main` übernommen werden kann, sollte in
GitHub zusätzlich eine Branch-Protection-Regel für `main` aktiviert und der
Statuscheck `Python 3.10` als verpflichtend ausgewählt werden.
