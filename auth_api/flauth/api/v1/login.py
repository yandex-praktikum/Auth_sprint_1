# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from http import HTTPStatus

from db.auth import get_auth_records, post_auth_record
from db.refresh import (pull_refresh_token, push_refresh_token,
                        update_refresh_token)
from db.user import get_user
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from pages.auth import auth_blueprint
from utils.jwt_tokens import get_access_token, get_jti, get_refresh_token
from utils.passwords import verify_password


@auth_blueprint.route("/login", methods=["POST"])
def login_post():
    login = request.form.get("login")
    password = request.form.get("password")

    # Проверяем парроль
    user = get_user(login)
    if not user:
        return {}, HTTPStatus.BAD_REQUEST

    if not verify_password(password, user.hash_password):
        return {}, HTTPStatus.UNAUTHORIZED

    # Проверяем есть ли regresh токен с этого устройства
    user_agent = request.user_agent.string
    token_info = pull_refresh_token(user.id, user_agent)

    # Создаем новый токены
    access_token = get_access_token(user)
    refresh_token = get_refresh_token(user)

    # Есть regresh токен - меняем, нет - создаем
    jti = get_jti(refresh_token)

    if token_info:
        update_refresh_token(token_info, jti)
    else:
        push_refresh_token(user.id, user_agent, jti)

    # Создаем запись о входе в акаунт
    auth_dict = {"user_id": user.id, "user_agent": request.user_agent.string}
    post_auth_record(auth_dict)

    return (
        jsonify(access_token=access_token, refresh_token=refresh_token),
        HTTPStatus.OK,
    )


@auth_blueprint.route("/login/<page>", methods=["GET"])
@jwt_required()
def info_get(page: int):
    user_info = get_jwt_identity()
    if not page.isnumeric():
        return {}, HTTPStatus.BAD_REQUEST
    page = int(page)
    auth_records = get_auth_records(user_info["id"], page=page)
    auth_records = [
        {"user_agent": item.user_agent, "date_time": item.date_time}
        for item in auth_records
    ]
    return jsonify(auth_records), HTTPStatus.OK
