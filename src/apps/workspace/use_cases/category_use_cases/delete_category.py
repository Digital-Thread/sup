from uuid import UUID

from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryException,
    CategoryNotFound,
    WorkspaceCategoryNotFound,
)
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class DeleteCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_id: int, workspace_id: UUID) -> None:
        try:
            await self._category_repository.delete(
                CategoryId(category_id), WorkspaceId(workspace_id)
            )
        except (CategoryNotFound, WorkspaceCategoryNotFound) as error:
            raise CategoryException(f'{str(error)}')
