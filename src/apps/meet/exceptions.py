class MeetException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.message


class MeetNotFoundException(ApplicationError):
    def __init__(self):
        super().__init__(status_code=404, message='Meet not found')


class MeetCreateException(ApplicationError):
    def __init__(self):
        super().__init__(status_code=400, message='Meet create error')


class MeetInviteException(ApplicationError):
    def __init__(self):
        super().__init__(status_code=400, message='Meet invite error')


class ParticipantCheckException(ApplicationError):
    def __init__(self):
        super().__init__(status_code=400, message='Participant check error')


class ParticipantCheckException(MeetException):
    def __init__(self):
        self.message = 'Participant check error'
        super().__init__(self.message)


class ParticipantNotFoundException(MeetException):
    def __init__(self):
        self.message = 'Participant not found'
        super().__init__(self.message)
