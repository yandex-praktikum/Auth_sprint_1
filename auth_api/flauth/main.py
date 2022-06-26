from app import create_app
from db.db import init_db
from utils.jwt_token import init_jwt

from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST
from config import POSTGRES_PORT, POSTGRES_DB, SECRET_KEY
from config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES
from config import JWT_REFRESH_TOKEN_EXPIRES

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
