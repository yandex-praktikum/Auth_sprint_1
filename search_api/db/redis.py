# -*- coding: utf-8 -*-
#
# @created: 20.05.2022
# @author: sprint4_team

from typing import Optional

from aioredis import Redis

redis: Optional[Redis] = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return redis
