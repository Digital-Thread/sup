from apps import ApplicationException


class BaseMeetException(ApplicationException):
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


class ParticipantCheckException(BaseMeetException):
    def __init__(self):
        super().__init__(message='Participant check error')


class ParticipantNotFoundException(BaseMeetException):
    def __init__(self):
        super().__init__(message='Participant not found')
