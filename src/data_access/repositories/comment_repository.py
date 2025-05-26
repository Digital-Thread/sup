import logging
from typing import Any

from sqlalchemy import exists, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.apps.comment import CommentOutDto, CommentRepositoryError
from src.apps.comment.domain import CommentEntity, CommentId, FeatureId, TaskId
from src.apps.comment.repository import ICommentRepository
from src.data_access.mappers import CommentMapper
from src.data_access.models import CommentModel, FeatureModel, TaskModel


class CommentRepository(ICommentRepository):

    def __init__(self, session_factory: AsyncSession) -> None:
        self._session = session_factory

    async def save(self, entity: CommentEntity) -> None:
        comment = CommentMapper.convert_comment_entity_to_db_model(entity)
        self._session.add(comment)
        try:
            await self._session.flush()
        except IntegrityError as err:
            logging.warning(err)
            raise CommentRepositoryError(message='User does not exist')

    async def get_by_id(self, comment_id: CommentId) -> CommentEntity | None:
        stmt = select(CommentModel).where(CommentModel.id == comment_id)
        result = await self._session.execute(stmt)
        comment: CommentModel = result.scalar_one_or_none()
        if comment:
            return CommentMapper.convert_db_model_to_comment_entity(comment)

        return None

    async def _fetch_comments(self, query: Any, page: int, page_size: int) -> list[CommentOutDto]:
        offset = (page - 1) * page_size
        stmt = query.offset(offset).limit(page_size)
        result = await self._session.execute(stmt)
        comments = result.scalars().all()
        return [CommentMapper.convert_db_model_to_output_dto(comment) for comment in comments]

    async def get_by_task_id(
        self, task_id: TaskId, page: int, page_size: int
    ) -> list[CommentOutDto]:
        query = (
            select(CommentModel)
            .where(CommentModel.task_id == task_id)
            .options(selectinload(CommentModel.user))
        )
        return await self._fetch_comments(query, page, page_size)

    async def get_by_feature_id(
        self, feature_id: FeatureId, page: int, page_size: int
    ) -> list[CommentOutDto]:
        query = (
            select(CommentModel)
            .where(CommentModel.feature_id == feature_id)
            .options(selectinload(CommentModel.user))
        )
        return await self._fetch_comments(query, page, page_size)

    async def update_comment(self, comment: CommentEntity) -> None:
        stmt = (
            update(CommentModel)
            .where(CommentModel.id == comment.id)
            .values(content=comment.content, updated_at=comment.updated_at)
        )
        await self._session.execute(stmt)

    async def delete_comment(self, comment_id: CommentId) -> None:
        result = await self._session.execute(
            select(CommentModel).where(CommentModel.id == comment_id)
        )
        comment = result.scalar_one_or_none()
        if comment is None:
            raise CommentRepositoryError()
        await self._session.delete(comment)

    async def is_task_or_feature_exists(self, comment_entity: CommentEntity) -> bool:
        parent_id, model = (
            (comment_entity.task_id, TaskModel)
            if comment_entity.task_id
            else (comment_entity.feature_id, FeatureModel)
        )
        stmt = select(exists().where(model.id == parent_id))  # type: ignore[attr-defined]
        result = await self._session.execute(stmt)

        exists_ = result.scalar()
        return exists_
