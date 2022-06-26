# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

from typing import Optional
from uuid import UUID

from .base import GenericModel


class GenreResponse(GenericModel):
    id: Optional[UUID] = None
    name: str
    description: Optional[str] = ""


class FilteredGenreListResponse(GenericModel):
    results: list[GenreResponse]
