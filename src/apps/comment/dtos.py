import dataclasses
from datetime import datetime


@dataclasses.dataclass
class BaseCommentDto:
    author_id: int
    content: str
    task_id: int | None
    feature_id: int | None


@dataclasses.dataclass
class AddCommentToTaskDto:
    author_id: int
    task_id: int
    content: str
    feature_id: None = None


@dataclasses.dataclass
class AddCommentToFeatureDto:
    author_id: int
    feature_id: int
    content: str
    task_id: None = None


@dataclasses.dataclass
class UpdateCommentDto:
    comment_id: int
    new_content: str


@dataclasses.dataclass
class DeleteCommentDto:
    comment_id: int


@dataclasses.dataclass
class CommentOutDto(BaseCommentDto):
    comment_id: int
    created_at: datetime
    updated_at: datetime
