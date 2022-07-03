# -*- coding: utf-8 -*-
#
# @created: 25.06.2022
# @author: Aleksey Komissarov & Lyubov Antyufrieva
# @contact: ad3002@gmail.com

from http import HTTPStatus

from flask import jsonify, request
from db import db
from db_models import Role, UserRole
from flask_jwt_extended import get_jwt_identity, jwt_required
from views.role import role_blueprint


@role_blueprint.route("/user/{user_id}", methods=["GET"])
@jwt_required()
def get_user_roles(user_id):
    user = get_jwt_identity()
    roles = UserRole.query(user_id=user["id"]).all()
    user_roles = [role.role_id for role in roles]
    return jsonify(user_roles), HTTPStatus.OK


@role_blueprint.route("/user/{user_id}/{role_id}", methods=["PUT"])
@jwt_required()
def add_role_to_user(user_id, role_id):
    user = get_jwt_identity()
    if not user["role"] in ["admin"]:
        return {}, HTTPStatus.UNAUTHORIZED
    role = UserRole(user_id=user_id, role_id=role_id)
    db.session.add(role)
    db.session.commit()
    return {}, HTTPStatus.OK


@role_blueprint.route("/user/{user_id}/{role_id}", methods=["DELETE"])
@jwt_required()
def delete_role_from_user(user_id, role_id):
    user = get_jwt_identity()
    if not user["role"] in ["admin"]:
        return {}, HTTPStatus.UNAUTHORIZED
    Role.query.filter_by(user_id=user_id, role_id=role_id).delete()
    return {}, HTTPStatus.OK
