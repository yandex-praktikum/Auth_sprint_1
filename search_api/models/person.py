# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

from uuid import UUID

from pydantic.schema import Optional

from .base import GenericModel


class PersonResponse(GenericModel):
    id: Optional[UUID] = None
    full_name: str
    is_actor: Optional[bool] = False
    is_director: Optional[bool] = False
    is_writer: Optional[bool] = False


class FilteredPersonListResponse(GenericModel):
    results: list[PersonResponse]
