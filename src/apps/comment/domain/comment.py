from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Self

from src.apps.comment import CommentAssociatedWithBothError, CommentNotAssociatedError

from .types_ids import (
    AuthorId,
    CommentId,
    Content,
    FeatureId,
    TaskId,
)


@dataclass
class CommentEntity:
    comment_id: CommentId | None
    user_id: AuthorId
    task_id: TaskId | None
    feature_id: FeatureId | None
    content: Content
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create_for_entity(
            cls,
            task_id: TaskId | None,
            feature_id: FeatureId | None,
            user_id: AuthorId,
            content: Content,
    ) -> 'Self':
        if not task_id and not feature_id:
            raise CommentNotAssociatedError()
        if task_id and feature_id:
            raise CommentAssociatedWithBothError()
        instance = cls(
            comment_id=None,
            task_id=task_id,
            feature_id=feature_id,
            content=content,
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        return instance

    def update_content(self: Self, new_content: Content) -> None:
        self.content = new_content
        self.updated_at = datetime.now(timezone.utc)
