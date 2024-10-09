from src.apps.workspace.dtos.category_dtos import UpdateCategoryAppDTO
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class UpdateCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    async def execute(self, category_id: int, update_data: UpdateCategoryAppDTO) -> None:
        """
        Используем метод с полной загрузкой объекта из БД, т.к. есть поля с валидацией
        """
        category = await self.category_repository.find_by_id(category_id)

        if update_data.get('name'):
            category.name = update_data['name']

        for key, value in update_data.items():
            if key != 'name':
                setattr(category, key, value)

        await self.category_repository.update(category)
