from logging import warning

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import delete, exists, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.tag import TagEntity
from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.apps.workspace.exceptions.tag_exceptions import (
    TagAlreadyExists,
    TagNotFound,
    TagNotUpdated,
    WorkspaceTagNotFound,
)
from src.apps.workspace.repositories.tag_repository import ITagRepository
from src.data_access.mappers.tag_mapper import TagMapper
from src.data_access.models import WorkspaceModel
from src.data_access.models.workspace_models.tag import TagModel


class TagRepository(ITagRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, tag: TagEntity) -> None:
        stmt = TagMapper.entity_to_model(tag)
        self._session.add(stmt)

        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            if isinstance(error.orig.__cause__, UniqueViolationError):
                raise TagAlreadyExists(
                    'Тег с таким именем в этом рабочем пространстве уже существует.'
                )

            raise WorkspaceTagNotFound(
                f'Рабочего пространства с id={tag.workspace_id} не существует'
            )

    async def get_by_id(self, tag_id: TagId, workspace_id: WorkspaceId) -> TagEntity | None:
        query = select(TagModel).filter_by(id=tag_id, workspace_id=workspace_id)
        result = await self._session.execute(query)
        try:
            tag_model = result.scalar_one()
        except NoResultFound as error:
            warning(error)
            raise TagNotFound(f'Тег с id={tag_id} не найден')
        else:
            return TagMapper.model_to_entity(tag_model)

    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[TagEntity]:
        query = select(TagModel).filter_by(workspace_id=workspace_id)
        result = await self._session.execute(query)
        tags = [TagMapper.model_to_entity(tag) for tag in result.scalars().all()]
        if not tags:
            if not await self._session.get(WorkspaceModel, workspace_id):
                raise WorkspaceTagNotFound(f'Рабочее пространство с id={workspace_id} не найдено')

        return tags

    async def update(self, tag: TagEntity) -> None:
        update_data = TagMapper.entity_to_dict(tag)
        stmt = update(TagModel).filter_by(id=tag.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise TagNotUpdated(f'Тег с id={tag.id} не обновлен')

    async def delete(self, tag_id: TagId, workspace_id: WorkspaceId) -> None:
        exists_tag = await self._session.execute(
            select(exists().where(TagModel.id == tag_id, TagModel.workspace_id == workspace_id))
        )

        if not exists_tag.scalar():
            raise TagNotFound(
                f'Тег с id={tag_id} не найден в указанном рабочем пространстве при удалении.'
            )

        stmt = delete(TagModel).filter_by(id=tag_id, workspace_id=workspace_id)
        await self._session.execute(stmt)
