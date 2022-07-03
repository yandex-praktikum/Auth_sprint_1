# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

import logging

import aioredis
import uvicorn
from api.v1 import films, genres, persons
from core.config import settings
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=settings.project_name,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
    default_response_class=ORJSONResponse,
)


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


@app.on_event("startup")
async def startup():
    """Startap preparation with database connection."""
    logging.info("On startup database connection")
    redis.redis = await aioredis.create_redis_pool(
        (settings.redis_host, settings.redis_port),
        minsize=settings.redis_min_size,
        maxsize=settings.redis_max_size,
    )
    logging.info("Redis connected")
    elastic.es = AsyncElasticsearch(
        hosts=[f"{settings.elastic_host}:{settings.elastic_port}"]
    )
    logging.info("Elastic connected")


@app.on_event("shutdown")
async def shutdown():
    """Shutdown action with database closing connection."""
    redis.redis.close()
    await redis.redis.wait_closed()
    logging.info("Redis disconnected")
    await elastic.es.close()
    logging.info("Elastic disconnected")


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])

if __name__ == "__main__":
    logging.info("Running the main app")
    uvicorn.run(
        "main:app",
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        debug=settings.debug,
        log_level="trace",
    )
