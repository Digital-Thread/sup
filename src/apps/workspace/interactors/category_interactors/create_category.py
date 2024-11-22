from src.apps.workspace.domain.entities.category import CategoryEntity
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.category_dtos import CreateCategoryAppDTO
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryAlreadyExists,
    CategoryException,
    WorkspaceCategoryNotFound,
)
from src.apps.workspace.repositories.category_repository import ICategoryRepository


class CreateCategoryInteractor:
    def __init__(self, category_repository: ICategoryRepository):
        self._category_repository = category_repository

    async def execute(self, request_data: CreateCategoryAppDTO) -> None:
        try:
            await self._category_repository.save(
                CategoryEntity(
                    _name=request_data.name,
                    _workspace_id=WorkspaceId(request_data.workspace_id),
                )
            )
        except (ValueError, WorkspaceCategoryNotFound, CategoryAlreadyExists) as error:
            raise CategoryException(f'{str(error)}')
