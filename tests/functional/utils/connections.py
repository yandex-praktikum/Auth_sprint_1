import sys

sys.path.append("..")
sys.path.append("../..")

import logging
import socket
from contextlib import closing

from elasticsearch import Elasticsearch
from backoff import backoff
from functional.settings import settings
from redis import Redis

logging.basicConfig(level="INFO")


@backoff
def get_es_client() -> Elasticsearch:
    return Elasticsearch(
        hosts=[
            {
                "host": settings.es_host,
                "port": settings.es_port,
            }
        ],
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )


@backoff
def get_redis_client() -> Redis:
    return Redis(host=settings.redis_host, port=settings.redis_port)


@backoff
def check_connection(service):
    server_address = tuple(
        [getattr(settings, f"{service}_{attr}") for attr in ("host", "port")]
    )
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        try:
            if sock.connect_ex(server_address) == 0:
                logging.info(f"{service} is connected {server_address}")
            else:
                logging.info(f"{service} is not connected {server_address}")
                raise ConnectionError(
                    f"{service} could not be connected {server_address}"
                )
        except Exception as e:
            raise e
