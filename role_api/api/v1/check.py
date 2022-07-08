# -*- coding: utf-8 -*-
#
# @created: 25.06.2022
# @author: Aleksey Komissarov & Lyubov Antyufrieva
# @contact: ad3002@gmail.com

from http import HTTPStatus

from sqlalchemy import and_

from db import db
from db_models import Role, UserRole
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from views.role import role_blueprint


@role_blueprint.route("/check", methods=["GET"])
@jwt_required()
def check_role():
    user = get_jwt_identity()
    role_id = request.form.get("role")
    hit = UserRole.query.filter(and_(UserRole.role_id==role_id, UserRole.user_id==user["id"])).one_or_none()
    if hit:
        return {}, HTTPStatus.OK
    return {}, HTTPStatus.UNAUTHORIZED


@role_blueprint.route("/check/<userid>/<role>", methods=["GET"])
@jwt_required()
def check_user_and_role(userid, role):
    user = get_jwt_identity()
    if not user["role"] in ["admin"]:
        return {}, HTTPStatus.UNAUTHORIZED
    hit = UserRole.query.filter(and_(UserRole.role_id==role, UserRole.user_id==userid)).one_or_none()
    if hit:
        return {}, HTTPStatus.OK
    return {}, HTTPStatus.UNAUTHORIZED
