from flask import Blueprint, render_template

from ..database.flask import get_database


blueprint = Blueprint("main", __name__)


@blueprint.get("/")
def index():
    return render_template("index.html")


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
