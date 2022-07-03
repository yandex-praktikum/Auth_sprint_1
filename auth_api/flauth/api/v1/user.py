# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from http import HTTPStatus

from db.user import get_user, post_user
from flask import request
from flask_jwt_extended import jwt_required
from pages.auth import auth_blueprint
from utils.passwords import hash_password, verify_password


@auth_blueprint.route("/user", methods=["PUT"])
@jwt_required()
def update_user():
    login = request.form.get("login")
    password = request.form.get("password")
    new_login = request.form.get("new_login")
    new_password = request.form.get("new_password")

    # Пороверяем, что ползователь есть
    user = get_user(login)
    if not user:
        return {}, HTTPStatus.NOT_FOUND

    # Проверяем пароль
    if not verify_password(password, user.hash_password):
        return {}, HTTPStatus.UNAUTHORIZED

    # Если все хорошо, подменяем и постим
    if new_password:
        user.hash_password = hash_password(new_password)
    user.login = new_login
    if post_user(user):
        return {}, HTTPStatus.OK
    else:
        return {}, HTTPStatus.CONFLICT
