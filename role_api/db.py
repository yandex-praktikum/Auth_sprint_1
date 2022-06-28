# -*- coding: utf-8 -*-
#
# @created: 25.06.2022
# @author: Aleksey Komissarov & Lyubov Antyufrieva
# @contact: ad3002@gmail.com


from typing import Any
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import settings
import redis

db = SQLAlchemy()

redis_db = redis.Redis(
                host=settings.redis_host, 
                port=settings.redis_port, 
                db=settings.redis_db)

def blocklist_check(jwt: Any):
    return redis_db.get(jwt)

def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}'
    db.init_app(app) 
    db.create_all()
