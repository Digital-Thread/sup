class MeetException(Exception):
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


class MeetCheckException(MeetException):
    def __init__(self):
        self.message = 'Meet check error'
        super().__init__(self.message)
