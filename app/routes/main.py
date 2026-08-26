from flask import Blueprint, render_template

from ..database.flask import get_database

blueprint = Blueprint("main", __name__)


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


@blueprint.get("/health")
def health():
    database = get_database()
    database.execute("SELECT 1").fetchone()
    return {"status": "ok", "database": "connected"}
