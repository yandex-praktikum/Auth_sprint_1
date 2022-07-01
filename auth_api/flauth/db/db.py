from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import settings

db = SQLAlchemy()

def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}'
    print(f'postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}')
    db.init_app(app) 