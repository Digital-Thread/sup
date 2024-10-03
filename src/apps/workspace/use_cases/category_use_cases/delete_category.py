from src.apps.workspace.exceptions.category_exceptions import CategoryNotFound
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class DeleteCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_id: int) -> None:
        try:
            await self._category_repository.delete(category_id)
        except CategoryNotFound:
            ValueError(f'Категории с id={category_id} не существует')
