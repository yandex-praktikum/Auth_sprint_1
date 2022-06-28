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
import os.path
from typing import AsyncGenerator

from aioredis import create_redis_pool, Redis
from elasticsearch.helpers import async_bulk
from elasticsearch.exceptions import RequestError

import logging
import os


from settings import TestSettings


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

settings = TestSettings()
SERVICE_URL = settings.SERVICE_URL
ES_HOST_PORT = settings.ES_HOST_PORT
REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT


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
    client = AsyncElasticsearch([ES_HOST_PORT])
    yield client
    logging.info('ES client closes soon')
    await client.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client() -> AsyncGenerator[Redis, None]:
    redis = await create_redis_pool((REDIS_HOST, REDIS_PORT),
                                    minsize=10, maxsize=20)
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
async def make_get_request(session):
    async def inner(method: str = '', params: dict = None) -> HTTPResponse:
        params = params or {}
        url = '{service}/api/v1/{method}'.format(
            service=SERVICE_URL,
            method=method,
        )
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner


@pytest_asyncio.fixture(scope='session', autouse=True)
async def fill_elastic_data(es_client: AsyncElasticsearch,
                            clear_cache: Callable):
    # создаем все схемы
    index_dict = {
            'movies': '/../testdata/indexes/films.json',
            'genres': '/../testdata/indexes/genres.json',
            'persons': '/../testdata/indexes/persons.json'
        }
    for index, schema_path in index_dict.items():
        async with aiofiles.open(os.path.dirname(__file__)+schema_path,
                                 'r') as f:
            schema = json.loads(await f.read())
        try:
            await es_client.indices.create(
                index=index,
                body=schema
            )
        except RequestError:
            pass
    logging.info("Indexes was created")
    # выгружаем данные
    data_dict = {
        'movies': '/../testdata/data/films.json',
        'genres': '/../testdata/data/genres.json',
        'persons': '/../testdata/data/persons.json'
    }
    for index_name, data_path in data_dict.items():
        async with aiofiles.open(os.path.dirname(__file__)+data_path,
                                 'r') as f:
            data = json.loads(await f.read())
        actions = [
            {
                "_index": index_name,
                "_id": doc['uuid'],
                '_type': '_doc',
                **doc
            }
            for doc in data
        ]
        logging.info(es_client)
        await async_bulk(es_client, actions)
        data_dict[index_name] = data
    logging.info("Data was bulk")
    try:
        yield
    finally:
        for index_name, data in data_dict.items():
            delete_data = [
                {
                    '_op_type': 'delete',
                    '_index': index_name,
                    '_type': '_doc',
                    '_id': doc['uuid'],
                    **doc
                }
                for doc in data]
            await async_bulk(es_client, delete_data)
            logging.info("Data was deleted")
        await clear_cache()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
