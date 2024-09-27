class BaseUserError(Exception):
    def __init__(self, message: str = 'Пользователь не найден.'):
        super().__init__(message)


class UserNotFoundError(BaseUserError):
    message = 'Пользователь не найден.'


class UserAlreadyExistsError(Exception):

    def __init__(self, email: str):
        super().__init__(f'Пользователь с email {email} уже существует.')
