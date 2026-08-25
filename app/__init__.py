from pathlib import Path

from flask import Flask

from .database.flask import init_database
from .routes import register_routes


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE_FACTORY=None,
        DATABASE_PATH=Path(app.instance_path) / "scrum_praxis.sqlite3",
    )

    if test_config:
        app.config.update(test_config)

    init_database(app)
    register_routes(app)

    return app
