# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from flask import request
from flask import jsonify
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from db.refresh import pull_refresh_token, update_refresh_token

from utils.jwt_tokens import get_access_token, get_refresh_token
from utils.jwt_tokens import get_jwt, get_jwt_identity
from pages.auth import auth_blueprint


@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_post():
    # Вытаскиваем содержимое refresh токена
    get_token = get_jwt()
    user_info = get_jwt_identity()
    user_agent = request.user_agent.string

    # Вытаскиваем из БД токен
    token_info = pull_refresh_token(user_info['id'], user_agent)

    # Если машина не та или токена удален из БД
    if not token_info:
        return {}, HTTPStatus.UNAUTHORIZED

    # Если токен не совпал
    if token_info.refresh_token != get_token:
        return {}, HTTPStatus.UNAUTHORIZED

    # Создаем токены
    access_token = get_access_token(user_info)
    refresh_token = get_refresh_token(user_info)

    # Обновляем данные о refresh токене
    update_refresh_token(token_info, refresh_token)

    return jsonify(access_token=access_token, refresh_token=refresh_token), \
        HTTPStatus.OK
