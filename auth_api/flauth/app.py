from flask import Flask

from pages.auth import auth
from pages.main import main


def create_app():
    app = Flask(__name__, template_folder='templates')

    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
