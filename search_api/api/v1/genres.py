# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Query
from models.filters import CombinedFilterGenre, CombinedSorter
from models.genre import FilteredGenreListResponse, GenreResponse
from services.common import Service
from services.genres import get_genre_service
from services.managers import PaginatedParams
from utils.constants import Message

router = APIRouter()


@router.get("/", response_model=FilteredGenreListResponse)
async def genre_list(
    name: Union[str, None] = Query(
        default=None,
        title="Genre",
        description="Genre name",
    ),
    description: Union[str, None] = Query(
        default=None,
        title="Description",
        description="Genre description",
    ),
    page: Union[int, None] = Query(default=0, alias="page[number]"),
    size: Union[int, None] = Query(default=10, alias="page[size]"),
    _service: Service = Depends(get_genre_service),
) -> GenreResponse:

    filter_kwargs = dict(
        name=name,
        description=description,
    )
    filters = CombinedFilterGenre(**filter_kwargs)
    sorter_kwargs = {}
    sorters = CombinedSorter(**sorter_kwargs)
    response = await _service.get_filtered(
        filters,
        sorters,
        paginated_params=PaginatedParams(page, size)
    )
    return response


@router.get("/{genre_id}", response_model=GenreResponse)
async def genre_details(
    genre_id: str, _service: Service = Depends(get_genre_service)
) -> GenreResponse:

    _response = await _service.get_by_id(genre_id)
    if not _response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=Message.genre_not_found)
    return _response
