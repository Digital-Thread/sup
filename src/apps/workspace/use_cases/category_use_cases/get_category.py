from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.dtos.category_dtos import CategoryAppDTO
from src.apps.workspace.exceptions.category_exceptions import CategoryNotFound
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class GetCategoryByIdUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_id: int) -> CategoryAppDTO:
        try:
            category = await self._category_repository.find_by_id(category_id)
        except CategoryNotFound:
            raise ValueError(f'Тег с id={category_id} не найдена')
        else:
            return CategoryAppDTO.from_entity(category)
