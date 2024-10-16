from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Self

from src.apps.comment import CommentAssociatedWithBothError, CommentNotAssociatedError

from .event import CommentCreatedEvent, CommentDeletedEvent, CommentUpdatedEvent, Event
from .value_objects import (
    AuthorId,
    CommentId,
    Content,
    CreatedAt,
    FeatureId,
    TaskId,
    UpdatedAt,
)


class Entity(ABC):
    pass


@dataclass
class AggregateRoot(Entity, ABC):
    _events: list[Event] = field(
        default_factory=list, init=False, repr=False, hash=False, compare=False
    )

    def record_event(self: Self, event: Event) -> None:
        self._events.append(event)

    def get_events(self: Self) -> list[Event]:
        return self._events

    def clear_events(self: Self) -> None:
        self._events = []

    def pull_events(self: Self) -> list[Event]:
        events = self.get_events().copy()
        self.clear_events()
        return events


@dataclass
class CommentEntity(AggregateRoot):
    comment_id: CommentId | None
    author_id: AuthorId
    task_id: TaskId | None
    feature_id: FeatureId | None
    content: Content
    created_at: CreatedAt
    updated_at: UpdatedAt

    @classmethod
    def create_for_entity(
        cls,
        task_id: TaskId | None,
        feature_id: FeatureId | None,
        author_id: AuthorId,
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
            author_id=author_id,
            created_at=CreatedAt(datetime.now()),
            updated_at=UpdatedAt(datetime.now()),
        )

        return instance

    def register_creation_event(self: Self) -> None:
        if self.comment_id is not None:
            self.record_event(
                CommentCreatedEvent(
                    comment_id=self.comment_id,
                    task_id=self.task_id,
                    feature_id=self.feature_id,
                    author_id=self.author_id,
                    content=self.content,
                    created_at=self.created_at,
                )
            )

    def update_content(self: Self, new_content: Content) -> None:
        self.content = new_content
        self.updated_at = UpdatedAt(datetime.now())
        self.record_event(CommentUpdatedEvent(self.comment_id, new_content))

    def delete(self: Self) -> None:
        self.record_event(
            CommentDeletedEvent(
                comment_id=self.comment_id, task_id=self.task_id, feature_id=self.feature_id
            )
        )
