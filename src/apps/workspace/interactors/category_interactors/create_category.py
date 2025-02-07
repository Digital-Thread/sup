from uuid import UUID

from src.apps.workspace.domain.entities.category import CategoryEntity
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryAlreadyExists,
    CategoryException,
    WorkspaceCategoryNotFound,
)
from src.apps.workspace.repositories.category_repository import ICategoryRepository


class CreateCategoryInteractor:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_name: str, workspace_id: UUID) -> None:
        try:
            await self._category_repository.save(
                CategoryEntity(_name=category_name, _workspace_id=WorkspaceId(workspace_id))
            )
        except (ValueError, WorkspaceCategoryNotFound, CategoryAlreadyExists) as error:
            raise CategoryException(f'{str(error)}')
