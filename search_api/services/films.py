# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

from functools import lru_cache

from core.config import settings
from db.elastic import get_elastic
from db.redis import get_redis
from fastapi import Depends
from models.film import FilmResponse, FilteredFilmListResponse
from models.genre import GenreResponse
from models.person import PersonResponse
from services.common import AsyncCacheStorage, Service
from services.managers import AsyncDataStorage

INDEX_NAME = settings.elastic_scheme_films


def transform_single_response(data):
    """ """
    actors_names = data["_source"].pop("actors_names")
    writers_names = data["_source"].pop("writers_names")
    directors_names = data["_source"].pop("directors_names")
    genres = data["_source"].pop("genres")
    data["_source"]["actors"] = [
        PersonResponse(full_name=name, is_actor=True)
        for name in actors_names
    ]
    data["_source"]["writers"] = [
        PersonResponse(full_name=name, is_writer=True)
        for name in writers_names
    ]
    if genres:
        data["_source"]["genres"] = [
            GenreResponse(name=genre, description="")
            for genre in genres
        ]
    data["_source"]["directors"] = [
        PersonResponse(full_name=name, is_director=True)
        for name in directors_names
    ]

    return FilmResponse(**data["_source"])


@lru_cache()
def get_film_service(
    cache_storage: AsyncCacheStorage = Depends(get_redis),
    data_storage: AsyncDataStorage = Depends(get_elastic),
) -> Service:
    return Service(
        cache_storage,
        data_storage,
        index_name=INDEX_NAME,
        single_response_func=transform_single_response,
        filtered_response_func=FilteredFilmListResponse,
    )
