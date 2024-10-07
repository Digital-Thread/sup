from typing import Callable, Any
from uuid import UUID

from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository
from src.apps.workspace.services.base_service import BaseService


class CategoryService(BaseService[Category, int, ICategoryRepository]):
    async def retrieve_by_workspace_id(
        self, workspace_id: UUID, use_case: Callable[[ICategoryRepository], Any]
    ) -> list[Category]:
        return await self.retrieve_by_workspace_id(workspace_id, use_case)
