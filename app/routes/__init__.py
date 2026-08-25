from flask import Flask

from .anliegen import blueprint as anliegen_blueprint
from .main import blueprint as main_blueprint


def register_routes(app: Flask) -> None:
    """Registriert alle HTTP-Routen der Anwendung an einer Stelle."""
    app.register_blueprint(main_blueprint)
    app.register_blueprint(anliegen_blueprint)
