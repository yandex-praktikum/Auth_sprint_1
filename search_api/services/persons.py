# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

from functools import lru_cache

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.person import FilteredPersonListResponse, PersonResponse
from services.common import AsyncCacheStorage, Service
from services.managers import AsyncDataStorage

INDEX_NAME = settings.elastic_scheme_persons


def transform_single_response(data):
    """ """
    return PersonResponse(**data["_source"])


@lru_cache()
def get_person_service(
    cache_storage: AsyncCacheStorage = Depends(get_redis),
    data_storage: AsyncDataStorage = Depends(get_elastic),
) -> Service:
    return Service(
        cache_storage,
        data_storage,
        index_name=INDEX_NAME,
        single_response_func=transform_single_response,
        filtered_response_func=FilteredPersonListResponse,
    )
