from abc import ABC, abstractmethod


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
    async def find_by_id(self, entity_id: ID) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: ID) -> None:
        raise NotImplementedError
