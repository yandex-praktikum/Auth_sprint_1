# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from gevent import monkey

monkey.patch_all()

import os

from app import app
from gevent.pywsgi import WSGIServer

http_server = WSGIServer((app.config["HOST"], app.config["PORT"]), app)
http_server.serve_forever()
