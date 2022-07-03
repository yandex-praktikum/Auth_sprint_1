# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class Settings(BaseSettings):
    """Dataclass for settings."""

    debug: bool = Field(False, env="DEBUG")
    batch_size: int = 100

    redis_db: str = Field("movies", env="REDIS_DB")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_min_size: int = 10
    redis_max_size: int = 10
    redis_cache_expire_min: int = 60 * 5

    search_api_host: str = Field("127.0.0.1", env="SEARCH_APP_HOST")
    search_api_port: int = Field(5003, env="SEARCH_APP_PORT")

    es_host: str = Field("127.0.0.1", env="ELASTIC_HOST")
    es_port: int = Field(5003, env="ELASTIC_PORT")

    postgres_user: str = Field("docker", env="POSTGRES_USER")
    postgres_password: str = Field("docker", env="POSTGRES_PASSWORD")
    postgres_host: str = Field("127.0.0.1", env="POSTGRES_HOST")
    postgres_port: int = Field(10, env="POSTGRES_PORT")
    postgres_db: str = Field("content", env="POSTGRES_DB")

    role_api_host: str = Field("127.0.0.1", env="ROLE_APP_HOST")
    role_api_port: int = Field(5002, env="ROLE_APP_PORT")

    auth_api_host: str = Field("127.0.0.1", env="AUTH_APP_HOST")
    auth_api_port: int = Field(5001, env="AUTH_APP_PORT")

    JWT_SECRET_KEY: str = Field("JWT_SECRET_KEY", env="JWT_SECRET_KEY")

    class Config:
        case_sensitive = False


settings = Settings()
