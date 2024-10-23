from src.apps.workspace.domain.types_ids import CategoryId
from src.apps.workspace.dtos.category_dtos import UpdateCategoryAppDTO
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryNotFound,
    CategoryNotUpdated,
)
from src.apps.workspace.mappers.category_mapper import CategoryMapper
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class UpdateCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    async def execute(self, category_id: CategoryId, update_data: UpdateCategoryAppDTO) -> None:
        try:
            existing_category = await self.category_repository.find_by_id(category_id)
        except CategoryNotFound:
            pass
            # TODO пробросить дальше
        else:
            update_category = CategoryMapper.update_data(existing_category, update_data)

            try:
                await self.category_repository.update(update_category)
            except CategoryNotUpdated:
                pass
                # TODO пробросить дальше
