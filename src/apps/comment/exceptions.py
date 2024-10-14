from src.apps import ApplicationException


class BaseCommentException(ApplicationException):
    """Base Domain Error"""

    @property
    def message(self) -> str:
        return 'A domain error occurred'


class CommentNotAssociatedError(BaseCommentException):
    """Выбрасывается, когда комментарий не ассоциирован ни с задачей, ни с фичей"""

    @property
    def message(self) -> str:
        return 'Comment must be associated with either a Task or a Feature.'


class CommentAssociatedWithBothError(BaseCommentException):
    """Выбрасывается, когда комментарий ассоциирован и с задачей, и с фичей одновременно"""

    @property
    def message(self) -> str:
        return 'Comment cannot be associated with both a Task and a Feature.'


class InvalidCommentIdError(BaseCommentException):
    """Выбрасывается, когда идентификатор комментария некорректный"""

    @property
    def message(self) -> str:
        return 'CommentId must be a positive integer.'


class InvalidAuthorIdError(BaseCommentException):
    """Выбрасывается, когда идентификатор автора некорректный"""

    @property
    def message(self) -> str:
        return 'AuthorId must be a positive integer.'


class InvalidTaskIdError(BaseCommentException):
    """Выбрасывается, когда идентификатор задачи некорректный"""

    @property
    def message(self) -> str:
        return 'TaskId must be a positive integer.'


class InvalidFeatureIdError(BaseCommentException):
    """Выбрасывается, когда идентификатор фичи некорректный"""

    @property
    def message(self) -> str:
        return 'FeatureId must be a positive integer.'


class InvalidContentError(BaseCommentException):
    """Выбрасывается, когда контент комментария некорректный"""

    @property
    def message(self) -> str:
        return 'Content must be a non-empty string.'
