#!/bin/sh

cd /app/
flask db init
flask db migrate
flask db upgrade
python3 /app/wsgi_app.py

exec "$@"