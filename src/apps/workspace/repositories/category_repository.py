from abc import abstractmethod

from src.apps.workspace.domain.entities.category import CategoryEntity
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.repositories.base_repository import IBaseRepository


class ICategoryRepository(IBaseRepository[CategoryEntity, CategoryId]):
    @abstractmethod
    async def get_by_workspace_id(self) -> list[CategoryEntity]:
        raise NotImplementedError

