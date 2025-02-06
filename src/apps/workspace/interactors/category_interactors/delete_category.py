from uuid import UUID

from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryNotFound,
    CategoryNotDeleted,
)
from src.apps.workspace.repositories.category_repository import ICategoryRepository


class DeleteCategoryInteractor:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_id: int, workspace_id: UUID) -> None:
        try:
            await self._category_repository.delete(
                CategoryId(category_id), WorkspaceId(workspace_id)
            )
        except CategoryNotFound as error:
            if isinstance(error, CategoryNotFound):
                raise
            raise CategoryNotDeleted(f'Тег с id={category_id} не удален')
