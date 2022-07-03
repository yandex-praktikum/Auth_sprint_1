# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

import sys

sys.path.append(".")

from asyncio.log import logger

import click
from flask import Flask
from flask.cli import AppGroup
from flask_migrate import Migrate

from api.v1 import login, logout, refresh, signup, user
from config import logger, settings
from db.db import db, init_db
from db.user import get_user, post_user
from pages import auth, main
from utils.jwt_tokens import jwt
from utils.passwords import hash_password

app = Flask(__name__, template_folder="templates")

app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
app.config["HOST"] = settings.auth_app_host
app.config["PORT"] = settings.auth_app_port
app.config["DEBUG"] = settings.debug

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.app_context().push()

init_db(app)

migrage = Migrate(app, db)

jwt.init_app(app)

app.register_blueprint(auth.auth_blueprint)
app.register_blueprint(main.main_blueprint)


user_cli = AppGroup("user")


@user_cli.command("add_admin")
@click.argument("login")
@click.argument("email")
@click.argument("name")
@click.argument("password")
def create_user(login, email, name, password):
    user_dict = {}
    user_dict["login"] = login
    user_dict["email"] = email
    user_dict["name"] = name
    user_dict["role"] = "admin"
    user_dict["hash_password"] = hash_password(password)
    user = get_user(login)
    if not user:
        status = post_user(user_dict)
        logger.info(f"Admin user created with status {status}")
    else:
        logger.info(f"Admin user exists {status}")


app.cli.add_command(user_cli)


if __name__ == "__main__":
    app.run(
        host=settings.auth_app_host, port=settings.auth_app_port, debug=settings.debug
    )
