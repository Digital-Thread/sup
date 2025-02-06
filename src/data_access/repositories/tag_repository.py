from logging import warning

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.tag import TagEntity
from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.apps.workspace.exceptions.tag_exceptions import (
    TagAlreadyExists,
    TagNotFound,
    WorkspaceTagNotFound,
)
from src.apps.workspace.repositories.tag_repository import ITagRepository
from src.data_access.mappers.tag_mapper import TagMapper
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
        tag_model = result.scalar_one_or_none()
        return TagMapper.model_to_entity(tag_model) if tag_model else None

    async def get_by_workspace_id(self, workspace_id: WorkspaceId, page: int, page_size: int) -> list[TagEntity]:
        offset = (page - 1) * page_size
        query = select(TagModel).filter_by(workspace_id=workspace_id).offset(offset).limit(page_size)
        result = await self._session.execute(query)
        tags = [TagMapper.model_to_entity(tag) for tag in result.scalars().all()]
        return tags

    async def update(self, tag: TagEntity) -> None:
        update_data = TagMapper.entity_to_dict(tag)
        stmt = update(TagModel).filter_by(id=tag.id, workspace_id=tag.workspace_id).values(**update_data)
        await self._session.execute(stmt)

    async def delete(self, tag_id: TagId, workspace_id: WorkspaceId) -> None:
        stmt = delete(TagModel).filter_by(id=tag_id, workspace_id=workspace_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise TagNotFound(
                f'Тег с id={tag_id} не найден в рабочем пространстве с id={workspace_id}'
            )
