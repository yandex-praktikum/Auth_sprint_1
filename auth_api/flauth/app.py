# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

import sys


sys.path.append(".")

from asyncio.log import logger
from flask import Flask
from db.user import post_user
from db.user import get_user
from utils.passwords import hash_password
from db.db import init_db
from config import settings, logger
from pages import auth
from pages import main
from utils.jwt_tokens import jwt

from api.v1 import login
from api.v1 import signup
from api.v1 import logout
from api.v1 import user
from api.v1 import refresh

import click
from flask import Flask
from flask.cli import AppGroup


app = Flask(__name__, template_folder="templates")

app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
app.config["HOST"] = settings.auth_app_host
app.config["PORT"] = settings.auth_app_port
app.config["DEBUG"] = settings.debug

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.app_context().push()

init_db(app)

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
        logger.info("Admin user created with status", status)
    else:
        logger.info("Admin user exists", status)


app.cli.add_command(user_cli)


if __name__ == "__main__":
    app.run(
        host=settings.auth_app_host, port=settings.auth_app_port, debug=settings.debug
    )
