import aioredis
import time
import asyncio

from settings import TestSettings


settings = TestSettings()
REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT


async def main():
    redis = await aioredis.create_redis((REDIS_HOST, REDIS_PORT))
    await redis.ping()
    redis.close()
    await redis.wait_closed()


if __name__ == "__main__":
    connection = False
    asyncio.run(main())
    while not connection:
        try:
            asyncio.run(main())
        except Exception:
            logging.info("REDIS: wait for connection")
        else:
            connection = True
            logging.info("REDIS: successful сonnection")
        time.sleep(1)
