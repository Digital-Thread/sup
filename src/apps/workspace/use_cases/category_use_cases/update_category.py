from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class UpdateCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    async def execute(self, category_id: int, update_data: dict[str, str]) -> None:
        """
        Используем метод с полной загрузкой объекта из БД, т.к. есть поля с валидацией
        """
        category = await self.category_repository.find_by_id(category_id)

        if update_data.get('name'):
            category.name = update_data['name']

        await self.category_repository.update(category, update_data)
