from uuid import UUID

from src.apps.workspace.domain.entities.category import CategoryEntity
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryException,
    CategoryNotFound,
    CategoryNotUpdated,
)
from src.apps.workspace.repositories.category_repository import ICategoryRepository


class UpdateCategoryInteractor:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_id: int, category_name: str, workspace_id: UUID) -> None:
        existing_category = await self._get_existing_category_in_workspace(
            CategoryId(category_id), WorkspaceId(workspace_id)
        )
        existing_category.name = category_name

        try:
            await self._category_repository.update(existing_category)
        except CategoryNotUpdated as error:
            raise CategoryException(f'{str(error)}')

    async def _get_existing_category_in_workspace(
        self, category_id: CategoryId, workspace_id: WorkspaceId
    ) -> CategoryEntity:
        try:
            existing_category = await self._category_repository.get_by_id(category_id, workspace_id)
        except CategoryNotFound as error:
            raise CategoryException(f'{str(error)}')
        else:
            return existing_category
