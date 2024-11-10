from abc import ABC, abstractmethod

from src.apps.workspace.domain.types_ids import WorkspaceId


class IBaseRepository[T, ID](ABC):
    """
    param:
    T - это экземпляр сущности,
    ID - это id экземпляра сущности
    """

    @abstractmethod
    async def save(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, entity_id: ID, workspace_id: WorkspaceId) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: ID, workspace_id: WorkspaceId) -> None:
        raise NotImplementedError
