# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

import logging
from abc import ABC, abstractmethod
from typing import Any

from services.managers import (AsyncDataStorage, MultipleServiceManager,
                               SingleServiceManager)


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int, **kwargs):
        pass


class Service:
    def __init__(
        self,
        cache_storage: AsyncCacheStorage,
        data_storage: AsyncDataStorage,
        index_name=None,
        single_response_func=None,
        filtered_response_func=None,
    ):
        """ """
        self.index_name = index_name
        self.single_response_func = single_response_func
        self.filtered_response_func = filtered_response_func
        self.cache_storage = cache_storage
        self.data_storage = data_storage

    def get_response(self, data):
        """ """
        return self.single_response_func(data)

    async def get_by_id(self, _id: str) -> Any:
        """ """
        logging.info(f"Getting {self.index_name} _id: {_id}")
        manager = SingleServiceManager(
            self.index_name,
            item_id=_id,
        )
        _data = await manager.get_result(self.cache_storage, self.data_storage)
        if not _data:
            return None
        return self.get_response(_data)

    async def get_filtered(
        self, combined_filter, combined_sorter, paginated_params
    ) -> Any:
        """ """
        manager = MultipleServiceManager(
            self.index_name,
            combined_filter=combined_filter,
            combined_sorter=combined_sorter,
            paginated_params=paginated_params
        )
        results = await manager.get_result(self.cache_storage,
                                           self.data_storage)
        response = self.filtered_response_func(
            results=list(
                map(
                    self.get_response,
                    results["hits"]["hits"],
                )
            ),
        )
        return response
