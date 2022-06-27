# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from db.db_models import AuthRecord
from db.db import db


def get_auth_records(user_id):
    auth_records = AuthRecord.query.filter_by(user_id=user_id).all()
    return auth_records


def post_auth_record(auth_record: dict):
    auth_record = AuthRecord(**auth_record)
    db.session.add(auth_record)
    db.session.commit()
