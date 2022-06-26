import os
from datetime import timedelta


POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']
POSTGRES_DB = os.environ['POSTGRES_DB']

SECRET_KEY = os.environ['SECRET_KEY']

JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_ACCESS_TOKEN_EXPIRES = timedelta(
    hours=int(os.environ['JWT_ACCESS_TOKEN_EXPIRES_HOURS'])
)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(
    days=int(os.environ['JWT_REFRESH_TOKEN_EXPIRES_DAYS'])
)

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
