# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

from enum import Enum
from typing import Union

from .base import GenericModel


class OrderingFilmOption(Enum):

    imdb_rating = "rating"
    title = "title"
    director = "directors_names"


class CombinedSorter(GenericModel):

    desc: bool = False
    order_by: Enum = None

    @property
    def search_params(self):
        return {
            "sort": [*self._search_query_options, "_score"],
        }

    @property
    def _search_query_options(self):
        options = []
        if self.order_by:
            options.append({self.order_by.name: "desc"
                            if self.desc else "asc"})
        return options

    @property
    def cache_key(self):
        return self.json()


class CombinedSorterFilm(CombinedSorter):
    order_by: OrderingFilmOption = OrderingFilmOption.title


class CombinedFilter(GenericModel):

    _match_fields = set()

    _range_fields = set()

    def _get_option_template(self, field_name, variant, value):
        """ """
        raise Exception("Should be implemented.")

    @property
    def cache_key(self):
        return self.json()

    @property
    def _search_query_options(self):
        results = []
        for field_name in self.dict():
            value = self.dict()[field_name]
            if field_name in self._match_fields:
                variant = "match"
            elif field_name in self._range_fields:
                variant = "range"
            else:
                raise Exception("Something wrong happens with field_name.")
            if value is not None:
                results.append(self._get_option_template(field_name,
                                                         variant,
                                                         value))
        return results

    @property
    def search_params(self):
        return self._search_query_options


class CombinedFilterFilm(CombinedFilter):

    min_rating: Union[float, None] = None
    max_rating: Union[float, None] = None
    director_name: Union[str, None] = None
    actor_name: Union[str, None] = None
    writer_name: Union[str, None] = None
    genre: Union[str, None] = None
    title: Union[str, None] = None
    description: Union[str, None] = None

    _match_fields = set(
        [
            "director_name",
            "actor_name",
            "writer_name",
            "genre",
            "title",
            "description",
        ]
    )

    _range_fields = set(
        [
            "min_rating",
            "max_rating",
        ]
    )

    def _get_option_template(self, field_name, variant, value):
        """ """
        return {
            "min_rating": {variant: {"imdb_rating": {"gte": value}}},
            "max_rating": {variant: {"imdb_rating": {"lte": value}}},
            "director": {variant: {"director_names": value}},
            "actor_name": {variant: {"actors_names": value}},
            "writer_name": {variant: {"writers_names": value}},
            "genre": {variant: {"genres": value}},
            "title": {variant: {"title": value}},
            "description": {variant: {"description": value}},
        }[field_name]


class CombinedFilterPerson(CombinedFilter):

    full_name: Union[str, None] = None
    is_actor: Union[bool, None] = None
    is_writer: Union[bool, None] = None
    is_director: Union[bool, None] = None

    _match_fields = set(
        [
            "full_name",
            "is_actor",
            "is_writer",
            "is_director",
        ]
    )

    _range_fields = set()

    def _get_option_template(self, field_name, variant, value):
        """ """
        return {
            "full_name": {variant: {"full_name": value}},
            "is_actor": {variant: {"is_actor": value}},
            "is_writer": {variant: {"is_writer": value}},
            "is_director": {variant: {"is_director": value}},
        }[field_name]


class CombinedFilterGenre(CombinedFilter):

    name: Union[str, None] = None
    description: Union[str, None] = None

    _match_fields = set(
        [
            "name",
            "description",
        ]
    )

    _range_fields = set()

    def _get_option_template(self, field_name, variant, value):
        """ """
        return {
            "name": {variant: {"name": value}},
            "description": {variant: {"description": value}},
        }[field_name]
