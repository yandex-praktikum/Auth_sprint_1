# -*- coding: utf-8 -*-
#
# @created: 27.06.2022
# @author: sprint6_team

from typing import Any
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Dataclass for settings."""

    debug: bool = True
    batch_size: int = 100
    
    redis_db: str = Field("movies", env="REDIS_DB")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_min_size: int = 10
    redis_max_size: int = 10
    redis_cache_expire_min: int = 60 * 5

    postgres_user: str = Field("docker", env="POSTGRES_USER")
    postgres_password: str = Field("docker", env="POSTGRES_PASSWORD")
    postgres_host: str = Field("127.0.0.1", env="POSTGRES_HOST")
    postgres_port: int = Field(5432, env="POSTGRES_PORT")
    postgres_db: str = Field("content", env="POSTGRES_DB")

    SECRET_KEY: str = Field("SECRET_KEY", env="SECRET_KEY")
    JWT_SECRET_KEY: str = Field("JWT_SECRET_KEY", env="JWT_SECRET_KEY")
    
    JWT_REFRESH_TOKEN_EXPIRES_DAYS: int = Field(5, env="JWT_REFRESH_TOKEN_EXPIRES_DAYS")
    JWT_ACCESS_TOKEN_EXPIRES_HOURS: int = Field(5, env="JWT_ACCESS_TOKEN_EXPIRES_HOURS")

    auth_app_host: str = Field("127.0.0.1", env="AUTH_APP_HOST")
    auth_app_port: int = Field(5000, env="AUTH_APP_PORT")

    class Config:
        case_sensitive = False


settings = Settings()
