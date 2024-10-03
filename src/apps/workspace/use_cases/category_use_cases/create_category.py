from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.exceptions.category_exceptions import CategoryAlreadyExists
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class CreateCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category: Category) -> None:
        try:
            await self._category_repository.save(category)
        except CategoryAlreadyExists:
            raise ValueError(f'Категория {category.name} уже существует')
