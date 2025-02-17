from datetime import datetime, timezone
from typing import Self

from src.apps.comment import CommentAssociatedWithBothError, CommentNotAssociatedError, InvalidContentError

from .types_ids import (
    AuthorId,
    CommentId,
    FeatureId,
    TaskId,
)


class CommentEntity:

    def __init__(
            self,
            user_id: AuthorId,
            task_id: TaskId | None,
            feature_id: FeatureId | None,
            content: str,
    ) -> None:
        if not task_id and not feature_id:
            raise CommentNotAssociatedError()
        if task_id and feature_id:
            raise CommentAssociatedWithBothError()

        self._id: CommentId | None = None
        self.user_id = user_id
        self.task_id = task_id
        self.feature_id = feature_id
        self.content = content
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
    
    @property
    def id(self) -> CommentId:
        return self._id

    @id.setter
    def id(self, _id: CommentId) -> None:
        if self._id is not None:
            raise AttributeError('Идентификатор комментария уже установлен')
        self._id = _id
    
    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, new_content: str) -> None:
        max_len = 1000
        if not isinstance(new_content, str) or not new_content.strip() or len(new_content) > max_len:
            raise InvalidContentError()

        self._content = new_content

    def update_content(self: Self, new_content: str) -> None:
        self.content = new_content
        self.updated_at = datetime.now(timezone.utc)
