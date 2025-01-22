from typing import Any

from src.apps import ApplicationException


class MeetError(ApplicationException):
    DEFAULT_MESSAGE = 'Meet error'

    def __init__(self, context: Exception | None = None, message: str | None = None) -> None:
        self.context = context
        self.message = message or self.DEFAULT_MESSAGE
        self.args: tuple[Any, ...] = (self.context, self.message)

    def __str__(self) -> str:
        if self.context:
            return f'{self.message} {self.context}'

        return self.message


class MeetAccessDeniedError(MeetError):
    DEFAULT_MESSAGE = 'Meet access denied'


class MeetNameLengthError(MeetError):
    DEFAULT_MESSAGE = 'Meet name length error'


class MeetNotFoundError(MeetError):
    DEFAULT_MESSAGE = 'Meet not found'


class MeetCreateError(MeetError):
    DEFAULT_MESSAGE = 'Meet create error'


class MeetInviteError(MeetError):
    DEFAULT_MESSAGE = 'Meet invite error'


class ParticipantCheckError(MeetError):
    DEFAULT_MESSAGE = 'Participant check error'


class ParticipantNotFoundException(MeetError):
    DEFAULT_MESSAGE = 'Participant not found'


class ParticipantCreateError(MeetError):
    DEFAULT_MESSAGE = 'Participant create error'
