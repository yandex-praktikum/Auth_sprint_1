# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

from typing import Optional
from uuid import UUID

from .base import GenericModel
from .genre import GenreResponse
from .person import PersonResponse


class FilmResponse(GenericModel):
    id: UUID
    title: str
    description: Optional[str] = None
    imdb_rating: float
    genres: list[GenreResponse] = []
    actors: list[PersonResponse] = []
    writers: list[PersonResponse] = []
    directors: list[PersonResponse] = []


class FilteredFilmListResponse(GenericModel):
    results: list[FilmResponse]

    def remove_description(self):
        for film in self.results:
            film.description = None
