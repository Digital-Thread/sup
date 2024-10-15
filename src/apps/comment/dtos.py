import dataclasses
from datetime import datetime
from uuid import UUID


@dataclasses.dataclass
class BaseCommentDto:
    author_id: UUID
    content: str
    task_id: int | None
    feature_id: int | None


@dataclasses.dataclass
class AddCommentToTaskDto(BaseCommentDto):
    pass


@dataclasses.dataclass
class AddCommentToFeatureDto(BaseCommentDto):
    pass


@dataclasses.dataclass
class UpdateCommentDto(BaseCommentDto):
    comment_id: int | None = None
    new_content: str | None = None


@dataclasses.dataclass
class DeleteCommentDto:
    comment_id: int


@dataclasses.dataclass
class CommentOutDto(BaseCommentDto):
    comment_id: int
    created_at: datetime
    updated_at: datetime
