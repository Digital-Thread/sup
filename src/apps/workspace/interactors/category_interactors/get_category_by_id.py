from uuid import UUID

from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.dtos.category_dtos import CategoryOutDTO
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryException,
    CategoryNotFound,
)
from src.apps.workspace.mappers.category_mapper import CategoryMapper
from src.apps.workspace.repositories import ICategoryRepository


class GetCategoryByIdInteractor:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_id: int, workspace_id: UUID) -> CategoryOutDTO:
        try:
            category = await self._category_repository.get_by_id(
                CategoryId(category_id), WorkspaceId(workspace_id)
            )
        except CategoryNotFound as error:
            raise CategoryException(str(error))
        else:
            return CategoryMapper.entity_to_dto(category, CategoryOutDTO)
