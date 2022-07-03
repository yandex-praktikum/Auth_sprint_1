#!/bin/sh

# run tests
cd /app/flauth
flask user add_admin $ADMIN_LOGIN $ADMIN_EMAIL $ADMIN_NAME $ADMIN_PASSWORD
python3 /app/flauth/wsgi_app.py

exec "$@"