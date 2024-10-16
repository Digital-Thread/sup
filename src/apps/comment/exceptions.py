from dataclasses import dataclass

from src.apps import ApplicationException


@dataclass
class BaseCommentException(ApplicationException):
    """Base Domain Error"""

    message: str = 'A domain error occurred'


@dataclass
class CommentNotAssociatedError(BaseCommentException):
    """Выбрасывается, когда комментарий не ассоциирован ни с задачей, ни с фичей"""

    message: str = 'Comment must be associated with either a Task or a Feature.'


@dataclass
class CommentAssociatedWithBothError(BaseCommentException):
    """Выбрасывается, когда комментарий ассоциирован и с задачей, и с фичей одновременно"""

    message: str = 'Comment cannot be associated with both a Task and a Feature.'


@dataclass
class InvalidCommentIdError(BaseCommentException):
    """Выбрасывается, когда идентификатор комментария некорректный"""

    message: str = 'CommentId must be a positive integer.'


@dataclass
class InvalidAuthorIdError(BaseCommentException):
    """Выбрасывается, когда идентификатор автора некорректный"""

    message: str = 'AuthorId must be a uuid object.'


@dataclass
class InvalidTaskIdError(BaseCommentException):
    """Выбрасывается, когда идентификатор задачи некорректный"""

    message: str = 'TaskId must be a positive integer.'


@dataclass
class InvalidFeatureIdError(BaseCommentException):
    """Выбрасывается, когда идентификатор фичи некорректный"""

    message: str = 'FeatureId must be a positive integer.'


@dataclass
class InvalidContentError(BaseCommentException):
    """Выбрасывается, когда контент комментария некорректный"""

    message: str = 'Content must be a non-empty string.'
