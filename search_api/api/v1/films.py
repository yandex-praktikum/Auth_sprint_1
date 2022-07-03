# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team


import logging
from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Query
from models.film import FilmResponse, FilteredFilmListResponse
from models.filters import CombinedFilterFilm, CombinedSorterFilm
from services.common import Service
from services.films import get_film_service
from services.managers import PaginatedParams
from utils.constants import Message

router = APIRouter()


@router.get("/", response_model=FilteredFilmListResponse)
async def film_list(
    min_rating: Union[float, None] = Query(
        default=None,
        title="Min IMDB",
        description="Mininal IMDB rating",
    ),
    max_rating: Union[float, None] = Query(
        default=None,
        title="Max IMDB",
        description="Maximal IMDB rating",
    ),
    genre: Union[str, None] = Query(
        default=None,
        title="Genre",
        description="Genre, for the possible values see genre API",
    ),
    actor_name: Union[str, None] = Query(
        default=None,
        title="Actor name",
        description="Actor name",
    ),
    writer_name: Union[str, None] = Query(
        default=None,
        title="Writer name",
        description="Writer name",
    ),
    director_name: Union[str, None] = Query(
        default=None,
        title="Director name",
        description="Director name",
    ),
    title: Union[str, None] = Query(
        default=None,
        title="Movie title",
        description="Movie title",
    ),
    description: Union[str, None] = Query(
        default=None,
        title="Movie description",
        description="Movie description",
    ),
    order_by: Union[str, None] = Query(
        default=None,
        title="Order by",
        description="Order by",
    ),
    show_description: Union[bool, None] = Query(
        default=None,
        title="Show description",
        description="Show description",
    ),
    page: Union[int, None] = Query(default=0, alias="page[number]"),
    size: Union[int, None] = Query(default=10, alias="page[size]"),
    _service: Service = Depends(get_film_service),
) -> FilmResponse:
    """Film API."""

    filter_kwargs = dict(
        max_rating=max_rating,
        min_rating=min_rating,
        genre=genre,
        actor_name=actor_name,
        writer_name=writer_name,
        title=title,
        description=description,
        directors_names=director_name,
    )
    logging.info(filter_kwargs)
    sorter_kwargs = {}
    if order_by:
        sorter_kwargs.update(order_by=order_by)
    response = await _service.get_filtered(
        CombinedFilterFilm(**filter_kwargs),
        CombinedSorterFilm(**sorter_kwargs),
        PaginatedParams(page, size),
    )

    if not show_description:
        response.remove_description()

    return response


@router.get("/{film_id}", response_model=FilmResponse)
async def film_details(
    film_id: str, _service: Service = Depends(get_film_service)
) -> FilmResponse:

    logging.info("Get film by id")
    _response = await _service.get_by_id(film_id)
    if not _response:
        # Если фильм не найден, отдаём 404 статус
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=Message.film_not_found
        )

    return _response
