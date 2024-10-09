from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional


class IBaseRepository[T, ID](ABC):
    """
    Параметры:
    T - это экземпляр сущности,
    ID - это id экземпляра сущности
    """

    @abstractmethod
    async def save(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, entity_id: ID) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_partial(self, entity_id: ID, update_data: Mapping[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: ID) -> None:
        raise NotImplementedError
