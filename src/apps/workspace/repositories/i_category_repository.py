from abc import abstractmethod
from uuid import UUID

from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.repositories.base_repository import IBaseRepository


class ICategoryRepository(IBaseRepository[Category, int]):
    @abstractmethod
    async def find_by_workspace_id(self, workspace_id: UUID) -> list[Category]:
        raise NotImplementedError
