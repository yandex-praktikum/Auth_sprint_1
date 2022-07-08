#!/bin/sh

echo "Waiting for AUTH_APP..."
while ! nc -z $AUTH_APP_HOST $AUTH_APP_PORT; do
  sleep 0.1
done
echo "AUTH_APP started"

cd /app/

### impossible to run two apps with open migration db
# flask db init &&
# flask db migrate -x include_schemas=True && 
# flask db upgrade -x include_schemas=True &&

export PGPASSWORD=$POSTGRES_PASSWORD
psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -f /app/init.sql


python3 /app/wsgi_app.py

exec "$@"