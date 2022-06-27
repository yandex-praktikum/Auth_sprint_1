# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from db.db_models import RefreshToken
from db.db import db


def pull_refresh_token(user_id, user_agent):
    tocken_info = RefreshToken.query.filter_by(
        user_id=user_id,
        user_agent=user_agent).one_or_none()
    return tocken_info


def update_refresh_token(token_info, new_token):
    token_info.refresh_token = new_token
    db.session.add(token_info)
    db.session.commit()


def delete_refresh_token(user_id, user_agent):
    token_info = RefreshToken.query.filter_by(
        user_id=user_id,
        user_agent=user_agent).one_or_none()
    db.session.delete(token_info)
    db.session.commit()


def push_refresh_token(user_id, user_agent, refresh_token):
    token_dict = {
        'user_id': user_id,
        'user_agent': user_agent,
        'refresh_token': refresh_token
    }
    token_info = RefreshToken(**token_dict)
    db.session.add(token_info)
    db.session.commit()
