#!/bin/sh

echo "Waiting for elasticsearch connection"

while ! nc -z elasticsearch 9200; do
    sleep 0.1
done

echo "Waiting for redis connection"

while ! nc -z redis 6379; do
    sleep 0.1
done

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

exec "$@"
