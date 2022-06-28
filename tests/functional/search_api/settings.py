from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    SERVICE_URL: str = Field('http://nginx:8000', env='SERVICE_URL')
    ES_HOST_PORT: str = Field('es:9200', env='ES_HOST_PORT')
    REDIS_HOST: str = Field('redis', env='REDIS_HOST')
    REDIS_PORT: int = Field(6379, env='REDIS_PORT')
