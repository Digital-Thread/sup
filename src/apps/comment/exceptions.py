from dataclasses import dataclass

from src.apps import ApplicationException


@dataclass
class BaseCommentException(ApplicationException):
    """Base Domain Error"""

    message: str = 'A domain error occurred'

    def __str__(self) -> str:
        return self.message


@dataclass
class CommentNotAssociatedError(BaseCommentException):
    """Выбрасывается, когда комментарий не ассоциирован ни с задачей, ни с фичей"""

    message: str = 'Comment must be associated with either a Task or a Feature.'


@dataclass
class CommentAssociatedWithBothError(BaseCommentException):
    """Выбрасывается, когда комментарий ассоциирован и с задачей, и с фичей одновременно"""

    message: str = 'Comment cannot be associated with both a Task and a Feature.'


@dataclass
class CommentNotFoundError(BaseCommentException):
    message: str = 'Comment cannot be found.'


@dataclass
class InvalidContentError(BaseCommentException):
    """Выбрасывается, когда контент комментария некорректный"""

    message: str = 'Content must be a non-empty string.'


@dataclass
class IDAlreadyExistsError(BaseCommentException):
    """Выбрасывается, когда id комментария пытаются установить повторно"""

    message: str = 'The comment ID has already been set.'


@dataclass
class CommentRepositoryError(BaseCommentException):
    """Выбрасывается, когда возникла ошибка при работе с БД"""

    message: str = 'An error occurred while working with the database'
