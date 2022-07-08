# -*- coding: utf-8 -*-
#
# @created: 25.06.2022
# @author: Aleksey Komissarov & Lyubov Antyufrieva
# @contact: ad3002@gmail.com

from http import HTTPStatus

from db_models import Role
from flask import jsonify
from flask_jwt_extended import jwt_required
from views.role import role_blueprint


@role_blueprint.route("/roles", methods=["GET"])
@jwt_required()
def get_roles():
    roles = Role.query.all()
    roles = [{"id": role.id,
              "role": role.role,
              "description": role.description,
              "rule": role.rule,
             } for role in roles]
    return jsonify(roles), HTTPStatus.OK
