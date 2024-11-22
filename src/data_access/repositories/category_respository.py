from logging import warning

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import delete, exists, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.category import CategoryEntity
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryAlreadyExists,
    CategoryNotFound,
    CategoryNotUpdated,
    WorkspaceCategoryNotFound,
)
from src.apps.workspace.repositories.category_repository import ICategoryRepository
from src.data_access.converters.category_converter import CategoryConverter
from src.data_access.models.workspace_models.category import CategoryModel


class CategoryRepository(ICategoryRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, category: CategoryEntity) -> None:
        stmt = CategoryConverter.entity_to_model(category)
        self._session.add(stmt)

        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise CategoryAlreadyExists(
                    'Категория с таким именем в этом рабочем пространстве уже существует.'
                )

            raise WorkspaceCategoryNotFound(
                f'Рабочего пространства с id={category.workspace_id} не существует'
            )

    async def find_by_id(
        self, category_id: CategoryId, workspace_id: WorkspaceId
    ) -> CategoryEntity | None:
        query = select(CategoryModel).filter_by(id=category_id, workspace_id=workspace_id)
        result = await self._session.execute(query)
        try:
            category_model = result.scalar_one()
        except NoResultFound as error:
            warning(error)
            raise CategoryNotFound(
                f'Категория с id={category_id} не найдена в указанном рабочем пространстве.'
            )
        else:
            return CategoryConverter.model_to_entity(category_model)

    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[CategoryEntity]:
        query = select(CategoryModel).filter_by(workspace_id=workspace_id)
        result = await self._session.execute(query)
        categories = [
            CategoryConverter.model_to_entity(category) for category in result.scalars().all()
        ]
        if not categories:
            raise WorkspaceCategoryNotFound(f'Рабочее пространство с id={workspace_id} не найдено')

        return categories

    async def update(self, category: CategoryEntity) -> None:
        update_data = CategoryConverter.entity_to_dict(category)
        stmt = update(CategoryModel).filter_by(id=category.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise CategoryNotUpdated(f'Категория с id={category.id} не обновлена')

    async def delete(self, category_id: CategoryId, workspace_id: WorkspaceId) -> None:
        exists_category = await self._session.execute(
            select(
                exists().where(
                    CategoryModel.id == category_id, CategoryModel.workspace_id == workspace_id
                )
            )
        )

        if not exists_category.scalar():
            raise CategoryNotFound(
                f'Категория с id={category_id} не найдена в рабочем пространстве'
            )

        stmt = delete(CategoryModel).filter_by(id=category_id, workspace_id=workspace_id)
        await self._session.execute(stmt)
