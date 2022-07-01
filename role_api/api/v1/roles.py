# -*- coding: utf-8 -*-
#
# @created: 25.06.2022
# @author: Aleksey Komissarov & Lyubov Antyufrieva
# @contact: ad3002@gmail.com

from http import HTTPStatus

from flask import jsonify
from views.role import role_blueprint
from db_models import Role
from flask_jwt_extended import jwt_required

@role_blueprint.route("/roles", methods=["GET"])
@jwt_required()
def get_roles():
    roles = Role.query().all()
    return jsonify(roles), HTTPStatus.OK