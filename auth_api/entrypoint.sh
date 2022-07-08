#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

export PGPASSWORD=$POSTGRES_PASSWORD
psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -f /app/drop.sql

cd /app/flauth
flask db init &&
flask db migrate -x include_schemas=True &&
flask db upgrade  -x include_schemas=True &&
flask user add_admin $ADMIN_LOGIN $ADMIN_EMAIL $ADMIN_NAME $ADMIN_PASSWORD &&
python3 /app/flauth/wsgi_app.py

exec "$@"