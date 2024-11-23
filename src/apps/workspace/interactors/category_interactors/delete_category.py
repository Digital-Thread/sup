from uuid import UUID

from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.dtos.category_dtos import DeleteCategoryAppDTO
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryException,
    CategoryNotFound,
    WorkspaceCategoryNotFound,
)
from src.apps.workspace.repositories.category_repository import ICategoryRepository


class DeleteCategoryInteractor:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, request_data: DeleteCategoryAppDTO) -> None:
        try:
            await self._category_repository.delete(
                CategoryId(request_data.id), WorkspaceId(request_data.workspace_id)
            )
        except (CategoryNotFound, WorkspaceCategoryNotFound) as error:
            raise CategoryException(f'{str(error)}')
