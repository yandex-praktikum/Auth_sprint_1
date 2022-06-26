import os
from datetime import timedelta

from app import create_app
from db.db import init_db
from utils.jwt_tocken import init_jwt


POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']
POSTGRES_DB = os.environ['POSTGRES_DB']

SECRET_KEY = os.environ['SECRET_KEY']

JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

JWT_ACCESS_TOKEN_EXPIRES = timedelta(
    hours=int(os.environ['JWT_ACCESS_TOKEN_EXPIRES_HOURS'])
)

JWT_REFRESH_TOKEN_EXPIRES = timedelta(
    days=int(os.environ['JWT_REFRESH_TOKEN_EXPIRES_DAYS'])
)


if __name__ == '__main__':
    db_url = 'postgresql://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + \
        '@' + POSTGRES_HOST + ':' + POSTGRES_PORT + '/' + POSTGRES_DB

    app = create_app()

    app.config['SECRET_KEY'] = SECRET_KEY

    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = JWT_REFRESH_TOKEN_EXPIRES


    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.app_context().push()

    init_db(app)
    init_jwt(app)

    app.run(host="0.0.0.0", debug=True)
