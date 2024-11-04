import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseCommentDto(BaseModel):
    user_id: UUID
    content: str


class CreateCommentForTaskDto(BaseCommentDto):
    task_id: int


class CreateCommentForFeatureDto(BaseCommentDto):
    feature_id: int


class UpdateCommentRequestDto(BaseModel):
    new_content: str


class CommentResponseDto(BaseCommentDto):
    id: int
    task_id: int | None
    feature_id: int | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    model_config = ConfigDict(
        from_attributes=True,
    )
