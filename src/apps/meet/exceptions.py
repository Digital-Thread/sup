from apps import ApplicationError


class BaseMeetException(ApplicationError):
    def __init__(self, message: str = 'Meet error'):
        self.message = message
        super().__init__(self.message)


class MeetNotFoundException(BaseMeetException):
    def __init__(self):
        super().__init__(message='Meet not found')


class MeetCreateException(BaseMeetException):
    def __init__(self):
        super().__init__(message='Meet create error')


class MeetInviteException(BaseMeetException):
    def __init__(self):
        super().__init__(message='Meet invite error')


class ParticipantCheckException(ApplicationError):
    def __init__(self):
        super().__init__(status_code=400, message='Participant check error')


class ParticipantCheckException(ApplicationError):
    def __init__(self):
        super().__init__(status_code=400, message='Participant check error')


class ParticipantNotFoundException(ApplicationError):
    def __init__(self):
        super().__init__(message='Participant not found')
