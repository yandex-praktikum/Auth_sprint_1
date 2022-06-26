# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

import json
import logging
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from core.config import settings
from elasticsearch import NotFoundError
from models.filters import CombinedFilter, CombinedSorter


class AsyncDataStorage(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        pass

    @abstractmethod
    async def search(self, *args, **kwargs):
        pass


class PaginatedParams:
    def __init__(self, page: Optional[int] = 0, size: Optional[int] = 10):
        self.page = page
        self.size = size

    @property
    def from_(self):
        return self.page * self.size


class CachableInterface(ABC):

    @abstractmethod
    async def get_from_cache(self, cache_key):
        ...

    @abstractmethod
    async def _put_to_cache(self, cache_key, data: dict):
        ...


class DatastorageInterface(ABC):

    @abstractmethod
    async def get_from_datastore(self):
        ...


class ElasticDatastorageMixIn(DatastorageInterface):

    async def elastic_get(self, elastic, *args, **kwargs):
        try:
            doc = await elastic.get(*args, **kwargs)
            logging.info(doc["_source"])
        except NotFoundError:
            return None
        return doc

    async def elastic_search(self, elastic, *args, **kwargs):

        try:
            docs = await elastic.search(*args, **kwargs)
        except NotFoundError:
            return []
        return docs


class ServiceManagerMixin(ABC):

    def __init__(
        self,
        index_name: str,
        paginated_params: PaginatedParams = PaginatedParams(),
        item_id: UUID = None,
        combined_filter: CombinedFilter = None,
        combined_sorter: CombinedSorter = None,
    ) -> None:
        """Init fields required for filtering"""
        self.paginated_params = paginated_params
        self.index_name = index_name
        if bool(item_id) + bool(combined_filter) != 1:
            raise Exception("Something wrong happens \
that I don't understand (AK)")
        self.item_id = item_id
        self.combined_filter = combined_filter
        self.combined_sorter = combined_sorter

    async def get_from_cache(self, cache_storage, cache_key):
        """Get data from cache or None"""
        data = await cache_storage.get(cache_key)
        if not data:
            return None
        logging.debug(f"cached_data: {data}")
        return json.loads(data)  # TODO: replace it with ORJSONResponse

    async def _put_to_cache(self, cache_storage, cache_key, data: dict):
        """Put serilized data into JSON."""
        result = await cache_storage.set(
            cache_key,
            json.dumps(data),  # TODO: replace it with ORJSONResponse
            expire=settings.redis_cache_expire_min,
        )
        logging.debug(f"{cache_key} cached in cache storage: {result}")

    @property
    def _cache_key(self):
        """Return cache key with some magic."""
        combined_filter = None
        if self.combined_filter:
            combined_filter = self.combined_filter.cache_key
        combined_sorter = None
        if self.combined_sorter:
            combined_sorter = self.combined_sorter.cache_key
        return "::".join([
                self.index_name,
                "combined_filter",
                str(combined_filter),
                "combined_sorter",
                str(combined_sorter),
                "item_id",
                str(self.item_id),
                "from",
                str(self.paginated_params.from_),
                "size",
                str(self.paginated_params.size),
            ])

    async def get_result(self, cache_storage, data_storage):
        """Get data from cache or from Elastic"""
        result = await self.get_from_cache(cache_storage, self._cache_key)
        if not result:
            result = await self.get_from_datastore(data_storage)
            if not result:
                return None
            await self._put_to_cache(cache_storage, self._cache_key, result)
        return result


class SingleServiceManager(ServiceManagerMixin,
                           CachableInterface,
                           ElasticDatastorageMixIn):

    async def get_from_datastore(self,
                                 data_storage: AsyncDataStorage):
        doc = await self.elastic_get(data_storage,
                                     self.index_name,
                                     self.item_id)
        return doc


class MultipleServiceManager(ServiceManagerMixin,
                             CachableInterface,
                             ElasticDatastorageMixIn):

    async def get_from_datastore(self,
                                 data_storage: AsyncDataStorage) -> list:

        search_body = {"query": {"bool": {}}}
        if self.combined_filter:
            search_body["query"]["bool"].update(
                filter=self.combined_filter.search_params
            )
        if self.combined_sorter:
            search_body.update(self.combined_sorter.search_params)

        logging.debug(f"search body: {search_body}")
        logging.debug(f"size: {self.paginated_params.size}")
        logging.debug(f"from_: {self.paginated_params.from_}")
        output = await self.elastic_search(
            data_storage,
            index=self.index_name,
            body=search_body,
            from_=self.paginated_params.from_,
            size=self.paginated_params.size,
        )
        logging.debug(output)
        return output
