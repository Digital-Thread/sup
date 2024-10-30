from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.category_dtos import CategoryAppDTO
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryException,
    WorkspaceCategoryNotFound,
)
from src.apps.workspace.mappers.category_mapper import CategoryMapper
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class GetCategoryByWorkspaceUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, workspace_id: WorkspaceId) -> list[CategoryAppDTO]:
        try:
            categories = await self._category_repository.find_by_workspace_id(workspace_id)
        except WorkspaceCategoryNotFound as error:
            raise CategoryException(f'{str(error)}')
        else:
            return [
                CategoryMapper.entity_to_dto(category, CategoryAppDTO) for category in categories
            ]
