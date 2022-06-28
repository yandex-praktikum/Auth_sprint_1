# -*- coding: utf-8 -*-
#
# @created: 25.06.2022
# @author: Aleksey Komissarov & Lyubov Antyufrieva
# @contact: ad3002@gmail.com

from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from app import app

http_server = WSGIServer(('', 5001), app)
http_server.serve_forever() 