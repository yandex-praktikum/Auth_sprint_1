# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from sqlalchemy.exc import IntegrityError

from db.db_models import User
from db.db import db


def get_user(login: str):
    user = User.query.filter_by(login=login).one_or_none()
    return user

def post_user(user):
    try:
        if type(user) == dict:
            user = User(**user)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return None
    return 'OK'
