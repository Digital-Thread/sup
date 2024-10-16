from abc import ABC
from dataclasses import dataclass

from .value_objects import AuthorId, CommentId, Content, CreatedAt, FeatureId, TaskId


@dataclass
class Event(ABC):
    pass


@dataclass
class CommentCreatedEvent(Event):
    comment_id: CommentId | None
    task_id: TaskId | None
    feature_id: FeatureId | None
    author_id: AuthorId
    content: Content
    created_at: CreatedAt


@dataclass
class CommentUpdatedEvent(Event):
    comment_id: CommentId
    new_content: Content


@dataclass
class CommentDeletedEvent(Event):
    comment_id: CommentId
    task_id: TaskId | None
    feature_id: FeatureId | None
