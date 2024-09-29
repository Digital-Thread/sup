class MeetException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.message


class MeetNotFoundException(MeetException):
    def __init__(self):
        self.message = 'Meet not found'
        super().__init__(self.message)


class MeetCreateException(MeetException):
    def __init__(self):
        self.message = 'Meet create error'
        super().__init__(self.message)


class MeetInviteException(MeetException):
    def __init__(self):
        self.message = 'Meet invite error'
        super().__init__(self.message)


class ParticipantCheckException(MeetException):
    def __init__(self):
        self.message = 'Participant check error'
        super().__init__(self.message)


class ParticipantNotFoundException(MeetException):
    def __init__(self):
        self.message = 'Participant not found'
        super().__init__(self.message)
