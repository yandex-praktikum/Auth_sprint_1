# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from datetime import timedelta
from typing import Any
from config import settings
import redis


redis_db = redis.StrictRedis(
    host=settings.redis_host, port=settings.redis_port, db=settings.redis_db, decode_responses=True
)

JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=int(settings.JWT_ACCESS_TOKEN_EXPIRES_HOURS)) 
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(settings.JWT_REFRESH_TOKEN_EXPIRES_DAYS))

def blocklist_push(jwt: Any):
    redis_db.set(jwt, "", ex=JWT_ACCESS_TOKEN_EXPIRES)

def blocklist_delete(jwt: Any):
    redis_db.delete(jwt)

def blocklist_check(jwt: Any):
    return redis_db.get(jwt)