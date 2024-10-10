from src.apps import ApplicationException


class BaseMeetException(ApplicationException):
    def __init__(self, message: str = 'Meet error'):
        self.message = message
        super().__init__(self.message)


class AccessDeniedException(BaseMeetException):
    def __init__(self, message: str = 'Access denied'):
        super().__init__(message)


class MeetNameLengthException(BaseMeetException):
    def __init__(self, message: str = 'Meet name length error'):
        super().__init__(message)


class MeetNotFoundException(BaseMeetException):
    def __init__(self, message: str = 'Meet not found'):
        super().__init__(message)


class MeetCreateException(BaseMeetException):
    def __init__(self, message: str = 'Meet create error'):
        super().__init__(message)


class MeetInviteException(BaseMeetException):
    def __init__(self, message: str = 'Meet invite error'):
        super().__init__(message)


class ParticipantCheckException(BaseMeetException):
    def __init__(self, message: str = 'Participant check error'):
        super().__init__(message)


class ParticipantNotFoundException(BaseMeetException):
    def __init__(self, message: str = 'Participant not found'):
        super().__init__(message)


class ParticipantCreateException(BaseMeetException):
    def __init__(self, message: str = 'Participant create error'):
        super().__init__(message)
