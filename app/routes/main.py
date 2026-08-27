import json
import os
from flask import Blueprint, render_template, session

from ..database.flask import get_database

blueprint = Blueprint("main", __name__)

COUNTER_FILE = "counter.json"


def get_counter():
    """Liest den aktuellen Zählerstand aus."""
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r") as f:
                data = json.load(f)
                return data.get("views", 0)
        except Exception:
            return 0
    return 0


def increment_counter():
    """Erhöht den Zähler um 1 und speichert ihn."""
    count = get_counter() + 1
    with open(COUNTER_FILE, "w") as f:
        json.dump({"views": count}, f)
    return count


@blueprint.get("/")
def index():
    aktuelle_meldungen = get_database().execute(
        """
        SELECT id, titel, beschreibung, kategorie, ort, foto_pfad, datum, status
        FROM anliegen
        ORDER BY datum DESC, id DESC
        LIMIT 3
        """
    ).fetchall()
    return render_template("index.html", aktuelle_meldungen=aktuelle_meldungen)


@blueprint.get("/aktuelles")
def aktuelles():
    meldungen = get_database().execute(
        """
        SELECT id, titel, beschreibung, kategorie, ort, foto_pfad, datum, status
        FROM anliegen
        ORDER BY datum DESC, id DESC
        """
    ).fetchall()
    return render_template("aktuelles.html", meldungen=meldungen)


@blueprint.get("/impressum")
def impressum():
    return render_template("impressum.html")


@blueprint.get("/datenschutz")
def datenschutz():
    return render_template("datenschutz.html")


@blueprint.get("/katzenklo")
def tic_tac_toe():
    return render_template("tic_tac_toe.html")


@blueprint.get("/health")
def health():
    database = get_database()
    database.execute("SELECT 1").fetchone()
    return {"status": "ok", "database": "connected"}


@blueprint.app_template_global()
def total_views():
    # Prüft, ob der Besucher in dieser Browser-Sitzung schon gezählt wurde
    if not session.get("has_visited"):
        session["has_visited"] = True
        return increment_counter()

    # Bereits gezählt -> nur den alten Stand anzeigen
    return get_counter()