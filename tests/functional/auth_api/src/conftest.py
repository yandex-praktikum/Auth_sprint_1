import sys
sys.path.append("/tests")

import aiohttp
import pytest_asyncio
import json
import asyncio
import aiofiles
import pytest

from typing import Any, Callable
from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

from typing import AsyncGenerator

from aioredis import create_redis_pool, Redis
from elasticsearch.helpers import async_bulk
from elasticsearch.exceptions import RequestError

import logging
import os


from functional.settings import settings

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture()
async def read_json_data():
    async def inner(path: str) -> Any:
        async with aiofiles.open(os.path.dirname(__file__)+path, 'r') as f:
            json_dict = json.loads(await f.read())
            logging.info('File {path} was read'.format(path=path))
            return json_dict
    return inner


@pytest_asyncio.fixture(scope='session')
async def es_client() -> AsyncGenerator[AsyncElasticsearch, None]:
    client = AsyncElasticsearch([f"{settings.es_host}:{settings.es_port}"])
    yield client
    logging.info('ES client closes soon')
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client() -> AsyncGenerator[Redis, None]:
    redis = await create_redis_pool((settings.redis_host, settings.redis_port),
                                    minsize=settings.redis_min_size, maxsize=settings.redis_max_size)
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest_asyncio.fixture(scope='session')
def clear_cache(redis_client: Redis):
    async def inner() -> None:
        await redis_client.flushall(async_op=True)
    return inner


@pytest_asyncio.fixture(scope='function')
async def session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
async def make_request(session):
    async def inner(service: str = '',
                    method: str = '', 
                    path: str = '', 
                    data: dict = None, 
                    params: dict = None,
                    **kwargs
                ) -> HTTPResponse:
        params = params or {}
        url = f'http://{service}/api/v1/{path}'
        if method == "GET":
            async with session.get(url, params=params, **kwargs) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
            )
        elif method == "POST":
            async with session.post(url, data=data, params=params, **kwargs) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
            )
        elif method == "DELETE":
            async with session.delete(url, data=data, params=params, **kwargs) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
            )
        elif method == "PUT":
            async with session.put(url, data=data, params=params, **kwargs) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
            )
    return inner


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
