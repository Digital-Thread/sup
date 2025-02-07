from src.apps.workspace.domain.types_ids import CategoryId
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryException,
    CategoryNotFound,
    WorkspaceCategoryNotFound,
)
from src.apps.workspace.repositories.category_repository import ICategoryRepository


class DeleteCategoryInteractor:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_id: int) -> None:
        try:
            await self._category_repository.delete(CategoryId(category_id))
        except (CategoryNotFound, WorkspaceCategoryNotFound) as error:
            raise CategoryException(f'{str(error)}')
