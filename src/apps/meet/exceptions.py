from apps import ApplicationError


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


class ParticipantCheckException(ApplicationError):
    def __init__(self):
        super().__init__(status_code=400, message='Participant check error')


class ParticipantNotFoundException(ApplicationError):
    def __init__(self):
        super().__init__(status_code=404, message='Participant not found')
