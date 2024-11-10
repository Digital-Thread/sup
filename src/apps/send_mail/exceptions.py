class SendMailException(Exception):
    def __init__(self, message: str = 'Ошибка отправки'):
        super().__init__(message)


class SendMailActivationException(SendMailException):
    def __init__(self, message: str = 'Ошибка отправки письма с активацией'):
        super().__init__(message)
