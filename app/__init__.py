from flask import Flask

from .config import get_secret_key, debug_enabled
from .routes import blueprint
from .db import init_db


DEBUG = debug_enabled()


def init() -> Flask:
    init_db()

    app = Flask(__name__)
    app.secret_key = get_secret_key()
    app.register_blueprint(blueprint)

    return app
