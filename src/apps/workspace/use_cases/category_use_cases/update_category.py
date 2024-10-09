from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.dtos.category_dtos import CategoryAppDTO
from src.apps.workspace.exceptions.category_exceptions import CategoryNotUpdated
from src.apps.workspace.mappers.category_mapper import CategoryMapper
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class UpdateCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    async def execute(
        self, category_id: CategoryId, workspace_id: WorkspaceId, update_data: CategoryAppDTO
    ) -> None:
        category = CategoryMapper.dto_to_entity(
            update_data, {'category_id': category_id, 'workspace_id': workspace_id}
        )
        try:
            await self.category_repository.update(category)
        except CategoryNotUpdated:
            pass
            # TODO пробросить дальше
