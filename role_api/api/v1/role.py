# -*- coding: utf-8 -*-
#
# @created: 25.06.2022
# @author: Aleksey Komissarov & Lyubov Antyufrieva
# @contact: ad3002@gmail.com

from http import HTTPStatus

from db import db
from db_models import Role, UserRole
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from views.role import role_blueprint


@role_blueprint.route("/role/<role_id>", methods=["GET"])
@jwt_required()
def get_role(role_id):
    role = Role.query.filter_by(id=role_id).one()
    return jsonify({"id": role.id,
              "role": role.role,
              "description": role.description,
              "rule": role.rule,
             }), HTTPStatus.OK


@role_blueprint.route("/role/<role_id>", methods=["PUT"])
@jwt_required()
def put_role(role_id):
    user = get_jwt_identity()
    if not user["role"] in ["admin"]:
        return {}, HTTPStatus.UNAUTHORIZED
    role_dict = {}
    role_id = request.form.get("role_id")
    role_dict["role"] = request.form.get("role")
    role_dict["description"] = request.form.get("description")
    role_dict["rule"] = request.form.get("rule")

    existing_role = Role.query.filter_by(role=role_dict["role"]).one_or_none()
    if not existing_role:
        role = Role(**role_dict)
        db.session.add(role)
        db.session.commit()
        return {}, HTTPStatus.OK
    existing_role.role = role_dict["role"]
    existing_role.description = role_dict["description"]
    existing_role.rule = role_dict["rule"]
    db.session.commit()
    return {}, HTTPStatus.OK


@role_blueprint.route("/role/<role_id>", methods=["DELETE"])
@jwt_required()
def delete_role(role_id):
    user = get_jwt_identity()
    if not user["role"] in ["admin"]:
        return {}, HTTPStatus.UNAUTHORIZED
    Role.query.filter_by(id=role_id).delete()
    return {}, HTTPStatus.OK
