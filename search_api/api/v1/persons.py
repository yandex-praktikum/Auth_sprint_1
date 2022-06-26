# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Query
from models.filters import CombinedFilterPerson, CombinedSorter
from models.person import FilteredPersonListResponse, PersonResponse
from services.common import Service
from services.managers import PaginatedParams
from services.persons import get_person_service
from utils.constants import Message

router = APIRouter()


@router.get("/", response_model=FilteredPersonListResponse)
async def person_list(
    full_name: Union[str, None] = Query(
        default=None,
        title="Full name",
        description="Full name",
    ),
    is_actor: Union[bool, None] = Query(
        default=None,
        title="Is actor",
        description="Is actor?",
    ),
    is_writer: Union[bool, None] = Query(
        default=None,
        title="Is writer",
        description="Is writer?",
    ),
    is_director: Union[bool, None] = Query(
        default=None,
        title="Is director",
        description="Is director",
    ),
    page: Union[int, None] = Query(default=0, alias="page[number]"),
    size: Union[int, None] = Query(default=10, alias="page[size]"),
    _service: Service = Depends(get_person_service),
) -> PersonResponse:

    filter_kwargs = dict(
        full_name=full_name,
        is_actor=is_actor,
        is_writer=is_writer,
        is_director=is_director,
    )
    filters = CombinedFilterPerson(**filter_kwargs)
    sorter_kwargs = {}
    sorters = CombinedSorter(**sorter_kwargs)
    response = await _service.get_filtered(
        filters,
        sorters,
        PaginatedParams(page, size)
    )
    return response


@router.get("/{person_id}", response_model=PersonResponse)
async def person_details(
    person_id: str, _service: Service = Depends(get_person_service)
) -> PersonResponse:

    _response = await _service.get_by_id(person_id)
    if not _response:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=Message.person_not_found)
    return _response
