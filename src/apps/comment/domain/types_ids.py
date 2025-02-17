from abc import ABC
from dataclasses import dataclass

__all__ = (
    'CommentId',
    'AuthorId',
    'FeatureId',
    'TaskId',
    'Content',
    'CreatedAt',
    'UpdatedAt',
    'ValueObject',
)

from datetime import datetime
from uuid import UUID

from src.apps.comment import (
    InvalidAuthorIdError,
    InvalidCommentIdError,
    InvalidContentError,
    InvalidFeatureIdError,
    InvalidTaskIdError,
)


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """
        Validate that a value is a valid to create this value object
        :return: None
        """


@dataclass(frozen=True)
class ValueObject[V](BaseValueObject, ABC):
    value: V

    def to_raw(self) -> V:
        return self.value


@dataclass(frozen=True)
class CommentId(ValueObject[int]):

    def _validate(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise InvalidCommentIdError()


@dataclass(frozen=True)
class AuthorId(ValueObject[UUID]):

    def _validate(self) -> None:
        if not isinstance(self.value, UUID):
            raise InvalidAuthorIdError()


@dataclass(frozen=True)
class TaskId(ValueObject[int]):

    def _validate(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise InvalidTaskIdError()


class FeatureId(ValueObject[int]):
    def _validate(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise InvalidFeatureIdError()


@dataclass(frozen=True)
class Content(ValueObject[str]):

    def _validate(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise InvalidContentError()


@dataclass(frozen=True)
class CreatedAt(ValueObject[datetime]):
    def _validate(self) -> None:
        if not isinstance(self.value, datetime):
            raise ValueError('CreatedAt must be a datetime object')


@dataclass(frozen=True)
class UpdatedAt(ValueObject[datetime]):
    def _validate(self) -> None:
        if not isinstance(self.value, datetime):
            raise ValueError('UpdatedAt must be a datetime object')
