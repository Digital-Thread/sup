from abc import ABC, abstractmethod
from datetime import timedelta


class IUserRedisRepository(ABC):

    @abstractmethod
    async def set(self, name: str, value: str, ex: timedelta | None) -> None:
        pass

    @abstractmethod
    async def get(self, name: str) -> str | None:
        pass

    @abstractmethod
    async def delete(self, email: str) -> None:
        pass
