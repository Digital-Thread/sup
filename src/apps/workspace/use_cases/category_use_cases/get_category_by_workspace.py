from uuid import UUID

from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.exceptions.category_exceptions import WorkspaceCategoryNotFound
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class GetCategoryByWorkspaceUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, workspace_id: UUID) -> list[Category]:
        try:
            categories = await self._category_repository.find_by_workspace_id(workspace_id)
        except WorkspaceCategoryNotFound:
            raise ValueError(f'Рабочее пространство с id={workspace_id} для категории не найдено')

        return categories
