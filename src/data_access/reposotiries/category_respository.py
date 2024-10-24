from logging import warning

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryCreatedException,
    CategoryNotDeleted,
    CategoryNotUpdated,
)
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository
from src.data_access.converters.category_converter import CategoryConverter
from src.data_access.models.workspace_models.category import CategoryModel


class CategoryRepository(ICategoryRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, category: Category) -> None:
        stmt = CategoryConverter.entity_to_model(category)
        self._session.add(stmt)

        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            raise CategoryCreatedException

    async def find_by_id(self, category_id: CategoryId) -> Category | None:
        query: CategoryModel | None = await self._session.get(CategoryModel, category_id)
        category = CategoryConverter.model_to_entity(query) if query else None
        return category

    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[Category]:
        query = select(CategoryModel).filter_by(workspace_id=workspace_id)
        result = await self._session.execute(query)
        categories = [
            CategoryConverter.model_to_entity(category) for category in result.scalars().all()
        ]
        return categories

    async def update(self, category: Category) -> None:
        update_data = CategoryConverter.entity_to_dict(category)
        stmt = update(CategoryModel).filter_by(id=category.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise CategoryNotUpdated(f'Категория с id={category.id} не обновлена')

    async def delete(self, category_id: CategoryId) -> None:
        stmt = delete(CategoryModel).filter_by(id=category_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise CategoryNotDeleted(f'Категория с id={category_id} не удалена')
