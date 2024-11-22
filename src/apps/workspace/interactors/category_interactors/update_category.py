from uuid import UUID

from src.apps.workspace.domain.entities.category import CategoryEntity
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.dtos.category_dtos import UpdateCategoryAppDTO
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryException,
    CategoryNotFound,
    CategoryNotUpdated,
)
from src.apps.workspace.mappers.category_mapper import CategoryMapper
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class UpdateCategoryInteractor:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(
        self, category_id: int, workspace_id: UUID, update_data: UpdateCategoryAppDTO
    ) -> None:
        existing_category = await self._get_existing_category_in_workspace(
            CategoryId(category_id), WorkspaceId(workspace_id)
        )
        updated_category = self._map_to_update_data(existing_category, update_data)
        try:
            await self._category_repository.update(updated_category)
        except CategoryNotUpdated as error:
            raise CategoryException(f'{str(error)}')

    async def _get_existing_category_in_workspace(
        self, category_id: CategoryId, workspace_id: WorkspaceId
    ) -> CategoryEntity:
        try:
            existing_category = await self._category_repository.find_by_id(category_id, workspace_id)
        except CategoryNotFound as error:
            raise CategoryException(f'{str(error)}')
        else:
            return existing_category

    @staticmethod
    def _map_to_update_data(category: CategoryEntity, update_data: UpdateCategoryAppDTO) -> CategoryEntity:
        try:
            updated_category = CategoryMapper.update_data(category, update_data)
        except ValueError as error:
            raise CategoryException(f'{str(error)}')
        else:
            return updated_category
