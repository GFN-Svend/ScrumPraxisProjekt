from flask import Blueprint, jsonify, request, url_for

from ..database.flask import get_database


blueprint = Blueprint("anliegen", __name__, url_prefix="/api/anliegen")
REQUIRED_FIELDS = ("titel", "beschreibung", "kategorie", "ort")


@blueprint.get("")
def list_anliegen():
    rows = get_database().execute(
        """
        SELECT id, titel, beschreibung, kategorie, ort, foto_pfad, datum, status
        FROM anliegen
        ORDER BY id DESC
        """
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@blueprint.post("")
def create_anliegen():
    data = request.get_json(silent=True) or {}
    missing_fields = [field for field in REQUIRED_FIELDS if not data.get(field)]

    if missing_fields:
        return {
            "error": "Pflichtfelder fehlen.",
            "fields": missing_fields,
        }, 400

    database = get_database()
    with database.transaction():
        cursor = database.execute(
            """
            INSERT INTO anliegen
                (titel, beschreibung, kategorie, ort, foto_pfad, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["titel"],
                data["beschreibung"],
                data["kategorie"],
                data["ort"],
                data.get("foto_pfad"),
                data.get("status", "offen"),
            ),
        )

    anliegen_id = cursor.lastrowid
    response = jsonify({"id": anliegen_id, "status": "erstellt"})
    response.status_code = 201
    response.headers["Location"] = url_for(
        "anliegen.get_anliegen", anliegen_id=anliegen_id
    )
    return response


@blueprint.get("/<int:anliegen_id>")
def get_anliegen(anliegen_id: int):
    row = get_database().execute(
        """
        SELECT id, titel, beschreibung, kategorie, ort, foto_pfad, datum, status
        FROM anliegen
        WHERE id = ?
        """,
        (anliegen_id,),
    ).fetchone()

    if row is None:
        return {"error": "Anliegen nicht gefunden."}, 404

    return jsonify(dict(row))
