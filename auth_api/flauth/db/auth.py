# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from db.db import db
from db.db_models import AuthRecord


def get_auth_records(user_id, page=1, per_page=20):
    auth_records = AuthRecord.query.filter_by(user_id=user_id).paginate(
        page, per_page, False
    )
    return auth_records


def post_auth_record(auth_record: dict):
    auth_record = AuthRecord(**auth_record)
    db.session.add(auth_record)
    db.session.commit()
