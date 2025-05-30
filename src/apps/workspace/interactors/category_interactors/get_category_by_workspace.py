from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.category_dtos import CategoryOutDTO, GetCategoryDTO
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryException,
    WorkspaceCategoryNotFound,
)
from src.apps.workspace.mappers.category_mapper import CategoryMapper
from src.apps.workspace.repositories.category_repository import ICategoryRepository


class GetCategoryByWorkspaceInteractor:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, request_data: GetCategoryDTO) -> list[CategoryOutDTO]:
        try:
            categories = await self._category_repository.get_by_workspace_id(
                workspace_id=WorkspaceId(request_data.workspace_id),
                page=request_data.page,
                page_size=request_data.page_size,
            )
        except WorkspaceCategoryNotFound as error:
            raise CategoryException(f'{str(error)}')
        else:
            return [
                CategoryMapper.entity_to_dto(category, CategoryOutDTO) for category in categories
            ]
