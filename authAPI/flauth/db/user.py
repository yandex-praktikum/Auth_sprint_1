from sqlalchemy.exc import IntegrityError

from db.db_models import User
from db.db import db


def get_user(login: str):
    user = User.query.filter_by(login=login).first()
    return user


def post_user(user: dict):
    try:
        user = User(**user)
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return None
    return 'OK'
