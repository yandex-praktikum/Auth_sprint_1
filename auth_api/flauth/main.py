import os
from app import create_app
from db.db import init_db


POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']

POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']

POSTGRES_DB = os.environ['POSTGRES_DB']


if __name__ == '__main__':
    db_url = 'postgresql://' + POSTGRES_USER + ':' + POSTGRES_PASSWORD + \
        '@' + POSTGRES_HOST + ':' + POSTGRES_PORT + '/' + POSTGRES_DB

    app = create_app()

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.app_context().push()

    init_db(app)

    app.run(host="0.0.0.0", debug=True)
