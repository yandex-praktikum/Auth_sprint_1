# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from flask import Blueprint

auth_blueprint = Blueprint("auth", __name__, url_prefix="/api/v1/")
