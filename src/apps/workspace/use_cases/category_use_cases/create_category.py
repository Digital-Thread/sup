from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.category_dtos import CreateCategoryAppDTO
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryAlreadyExists,
    CategoryException,
    WorkspaceCategoryNotFound,
)
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository


class CreateCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, category_data: CreateCategoryAppDTO) -> None:
        try:
            await self._category_repository.save(
                Category(
                    _name=category_data.get('name'),
                    _workspace_id=WorkspaceId(category_data.get('workspace_id')),
                )
            )
        except (ValueError, WorkspaceCategoryNotFound, CategoryAlreadyExists) as error:
            raise CategoryException(f'{str(error)}')
