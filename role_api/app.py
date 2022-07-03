# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

import sys

sys.path.append(".")

from api.v1 import check, role, roles, user
from db import db, init_db
from flask import Flask
from flask_migrate import Migrate
from settings import settings
from utils.jwt_tokens import jwt
from views import main, role

app = Flask(__name__, template_folder="templates")

app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
app.config["HOST"] = settings.role_app_host
app.config["PORT"] = settings.role_app_port
app.config["DEBUG"] = settings.debug

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.app_context().push()

init_db(app)

migrage = Migrate(app, db)

jwt.init_app(app)

app.register_blueprint(role.role_blueprint)
app.register_blueprint(main.main_blueprint)


if __name__ == "__main__":
    app.run(
        host=settings.role_app_host, port=settings.role_app_port, debug=settings.debug
    )
