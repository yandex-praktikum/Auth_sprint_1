# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import jwt_required

from db.redis import blocklist_push
from db.refresh import delete_refresh_token
from pages.auth import auth_blueprint
from utils.jwt_tokens import get_jwt, get_jwt_identity


@auth_blueprint.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    # Вытаскиваем данные о пользователе и устройсве
    user_info = get_jwt_identity()
    user_agent = request.user_agent.string

    # Добавляем access токен в blocklist
    jti = get_jwt()
    blocklist_push(jti)

    # Удаляем refrech токен
    delete_refresh_token(user_info["id"], user_agent)

    return {}, HTTPStatus.OK
