from datetime import timedelta
from typing import AsyncIterator

import redis.asyncio as redis

from src.apps.auth.repositories import IAuthRedisRepository
from src.apps.user.repositories import IUserRedisRepository
from src.config import RedisConfig


class RedisRepository(IUserRedisRepository, IAuthRedisRepository):
    def __init__(self, redis_config: RedisConfig):
        dsn = redis_config.construct_redis_dsn
        self.redis_client = redis.StrictRedis.from_url(dsn)

    async def set(self, name: str, value: str, ex: timedelta | None) -> None:
        await self.redis_client.set(name, value, ex=ex)

    async def get(self, name: str) -> str | None:
        result: bytes | None = await self.redis_client.get(name)
        return result.decode('utf-8') if result else None

    async def delete(self, email: str) -> None:
        await self.redis_client.delete(email)

    async def delete_all_tokens(self, pattern: str) -> None:
        async for key in self.redis_client.scan_iter(pattern):
            await self.redis_client.delete(key)
