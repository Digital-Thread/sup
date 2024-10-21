import logging

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.comment import CommentNotFoundError
from src.apps.comment.domain import (
    CommentEntity,
    CommentId,
    Content,
    ICommentRepository,
)
from src.data_access import CommentConverter
from src.data_access.models import CommentModel


class CommentRepository(ICommentRepository[Content, CommentId, CommentEntity]):

    def __init__(self, session_factory: AsyncSession) -> None:
        self._session = session_factory
        # self._event = event_handler

    async def save(self, entity: CommentEntity) -> CommentEntity | None:
        comment = CommentConverter.convert_comment_entity_to_db_model(entity)
        self._session.add(comment)
        try:
            await self._session.flush()
            entity.comment_id = CommentId(comment.id)
            entity.register_creation_event()
            # await self._event.handle(entity.pull_events())
            return entity
        except IntegrityError as err:
            logging.warning(err)
            raise ValueError('User does not exist')

    async def fetch_by_id(self, comment_id: CommentId) -> CommentEntity | None:
        stmt = select(CommentModel).where(CommentModel.id == comment_id.to_raw())
        result = await self._session.execute(stmt)
        comment: CommentModel = result.scalar_one_or_none()
        if comment is None:
            raise CommentNotFoundError()
        return CommentConverter.convert_db_model_to_comment_entity(comment)

    async def fetch_all(self, page: int, page_size: int) -> list[CommentEntity]:
        offset = (page - 1) * page_size
        result = await self._session.execute(select(CommentModel).offset(offset).limit(page_size))
        comments = result.scalars().all()
        return [
            CommentConverter.convert_db_model_to_comment_entity(comment) for comment in comments
        ]

    async def update_comment(
        self, comment_id: CommentId, new_content: Content
    ) -> CommentEntity | None:
        comment = await self.fetch_by_id(comment_id)
        if comment is None:
            raise CommentNotFoundError()
        comment.update_content(new_content)
        stmt = (
            update(CommentModel)
            .where(CommentModel.id == comment_id.to_raw())
            .values(content=new_content.to_raw())
        )
        await self._session.execute(stmt)

        return comment

    async def delete_comment(self, comment_id: CommentId) -> None:
        result = await self._session.execute(
            select(CommentModel).where(CommentModel.id == comment_id.to_raw())
        )
        comment = result.scalar_one_or_none()
        if comment is None:
            raise CommentNotFoundError()
        await self._session.delete(comment)
        return None
