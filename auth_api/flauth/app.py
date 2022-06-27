# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from flask import Flask
from db.db import init_db
from config import settings
from pages import auth
from pages import main
from utils.jwt_tokens import jwt

from api.v1 import login
from api.v1 import signup
from api.v1 import logout
from api.v1 import user
from api.v1 import refresh

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
app.config['HOST'] = settings.auth_app_host
app.config['PORT'] = settings.auth_app_port
app.config['DEBUG'] = settings.debug


app.app_context().push()

init_db(app)

jwt.init_app(app)

app.register_blueprint(auth.auth_blueprint)
app.register_blueprint(main.main_blueprint)



if __name__ == '__main__':
    app.run(host=settings.auth_app_host, port=settings.auth_app_port, debug=settings.debug)





