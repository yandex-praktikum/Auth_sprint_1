import redis

from config import REDIS_HOST, REDIS_PORT
from config import JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES


redis_blocklist = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True
)


def push_blocklist(jwt):
    redis_blocklist.set(jwt, "", ex=JWT_ACCESS_TOKEN_EXPIRES)
    

def push_blocklist(jwt):
    redis_blocklist.set(jwt, "", ex=JWT_ACCESS_TOKEN_EXPIRES)


def check_blocklist(jwt):
    return redis_blocklist.get(jwt)