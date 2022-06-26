# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    """Dataclass for settings."""

    debug: bool = True

    batch_size: int = 100

    fastapi_host: str = "127.0.0.1"
    fastapi_port: int = 80

    elastic_host: str = Field("127.0.0.1", env="ELASTIC_HOST")
    elastic_port: int = Field(9200, env="ELASTIC_PORT")
    elastic_scheme_films: str = Field("movies",
                                      env="ELASTIC_SCHEME_FILMS")
    elastic_scheme_persons: str = Field("persons",
                                        env="ELASTIC_SCHEME_PERSONS")
    elastic_scheme_genres: str = Field("genres", env="ELASTIC_SCHEME_GENRES")

    redis_db: str = "movies"
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_min_size: int = 10
    redis_max_size: int = 10
    redis_cache_expire_min: int = 60 * 5

    project_name: str = "movies"
    docs_url: str = "/api/openapi"
    openapi_url: str = "/api/openapi.json"

    class Config:
        case_sensitive = False


settings = Settings()
