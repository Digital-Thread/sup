from logging import warning

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.tag import Tag
from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.apps.workspace.exceptions.tag_exceptions import (
    TagCreatedException,
    TagNotDeleted,
    TagNotUpdated,
)
from src.apps.workspace.repositories.i_tag_repository import ITagRepository
from src.data_access.converters.tag_converter import TagConverter
from src.data_access.models.workspace_models.tag import TagModel


class TagRepository(ITagRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, tag: Tag) -> None:
        stmt = TagConverter.entity_to_model(tag)
        self._session.add(stmt)

        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            raise TagCreatedException('Ошибка создания тега')

    async def find_by_id(self, tag_id: TagId) -> Tag | None:
        query: TagModel | None = await self._session.get(TagModel, tag_id)
        tag = TagConverter.model_to_entity(query) if query else None
        return tag

    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[Tag]:
        query = select(TagModel).filter_by(workspace_id=workspace_id)
        result = await self._session.execute(query)
        tags = [TagConverter.model_to_entity(tag) for tag in result.scalars().all()]
        return tags

    async def update(self, tag: Tag) -> None:
        update_data = TagConverter.entity_to_dict(tag)
        stmt = update(TagModel).filter_by(id=tag.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise TagNotUpdated(f'Тег с id={tag.id} не обновлен')

    async def delete(self, tag_id: TagId) -> None:
        stmt = delete(TagModel).filter_by(id=tag_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise TagNotDeleted(f'Тег с id={tag_id} не удален')
