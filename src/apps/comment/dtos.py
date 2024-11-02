import dataclasses
from datetime import datetime
from uuid import UUID


@dataclasses.dataclass
class BaseCommentDto:
    user_id: UUID
    content: str
    task_id: int | None
    feature_id: int | None


@dataclasses.dataclass
class AddCommentDto(BaseCommentDto):
    pass


@dataclasses.dataclass
class FetchCommentDto:
    comment_id: int


@dataclasses.dataclass
class UpdateCommentDto:
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


@dataclasses.dataclass
class CommentPaginationDto:
    page: int
    page_size: int


@dataclasses.dataclass
class FetchTaskCommentDto(CommentPaginationDto):
    task_id: int


@dataclasses.dataclass
class FetchFeatureCommentDto(CommentPaginationDto):
    feature_id: int
