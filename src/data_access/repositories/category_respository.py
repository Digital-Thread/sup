from logging import warning

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.category import CategoryEntity
from src.apps.workspace.domain.types_ids import CategoryId, WorkspaceId
from src.apps.workspace.exceptions.category_exceptions import (
    CategoryAlreadyExists,
    CategoryNotFound,
    WorkspaceCategoryNotFound,
)
from src.apps.workspace.repositories.category_repository import ICategoryRepository
from src.data_access.mappers.category_mapper import CategoryMapper
from src.data_access.models.workspace_models.category import CategoryModel


class CategoryRepository(ICategoryRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, category: CategoryEntity) -> None:
        stmt = CategoryMapper.entity_to_model(category)
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

    async def get_by_id(
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
            return CategoryMapper.model_to_entity(category_model)

    async def get_by_workspace_id(
        self, workspace_id: WorkspaceId, page: int, page_size: int
    ) -> list[CategoryEntity]:
        query = (
            select(CategoryModel)
            .filter_by(workspace_id=workspace_id)
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        result = await self._session.execute(query)
        categories = [
            CategoryMapper.model_to_entity(category) for category in result.scalars().all()
        ]
        return categories

    async def update(self, category: CategoryEntity) -> None:
        update_data = CategoryMapper.entity_to_dict(category)
        stmt = (
            update(CategoryModel)
            .filter_by(id=category.id, workspace_id=category.workspace_id)
            .values(**update_data)
        )
        await self._session.execute(stmt)

    async def delete(self, category_id: CategoryId, workspace_id: WorkspaceId) -> None:
        stmt = delete(CategoryModel).filter_by(id=category_id, workspace_id=workspace_id)
        result = await self._session.execute(stmt)
        if result.rowcount == 0:
            raise CategoryNotFound(
                f'Категория с id={category_id} не найдена в рабочем пространстве'
            )
