# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from http import HTTPStatus

from flask import request

from db.user import get_user, post_user
from pages.auth import auth_blueprint
from utils.passwords import hash_password


@auth_blueprint.route("/signup", methods=["POST"])
def signup_post():
    user_dict = {}
    user_dict["login"] = request.form.get("login")
    user_dict["email"] = request.form.get("email")
    user_dict["name"] = request.form.get("name")
    password = request.form.get("password")
    user_dict["hash_password"] = hash_password(password)

    # Проверка, что юзера не сущетвует
    user = get_user(user_dict["login"])

    if user:
        return {}, HTTPStatus.CONFLICT

    # Запись с проверкой уникальности e-mail
    post = post_user(user_dict)
    if not post:
        return {}, HTTPStatus.CONFLICT

    return {}, HTTPStatus.CREATED
