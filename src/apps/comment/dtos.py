import dataclasses
from datetime import datetime
from typing import TypedDict
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
    comment_id: int
    new_content: str


@dataclasses.dataclass
class DeleteCommentDto:
    comment_id: int


class UserInfo(TypedDict):
    user_id: UUID
    avatar: str
    fullname: str


@dataclasses.dataclass
class CommentOutDto:
    comment_id: int
    user: UserInfo
    content: str
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
