class BaseUserError(Exception):
    def __init__(self, message: str = 'Ошибка'):
        super().__init__(message)


class UserNotFoundError(BaseUserError):
    def __init__(self, message: str = 'Пользователь не найден.'):
        super().__init__(message)


class UserAlreadyExistsError(Exception):

    def __init__(self, email: str):
        super().__init__(f'Пользователь с email {email} уже существует.')


class TokenActivationExpire(BaseUserError):
    def __init__(self, message: str = 'Время действия токена истекло'):
        super().__init__(message)


class UserNotFoundException(BaseUserError):
    def __init__(self, email: str):
        super().__init__(f'Пользователь с email {email} не найден')


class PermissionDeniedException(BaseUserError):
    def __init__(self, message: str = 'Вы можете редактировать только свою учетную запись'):
        super().__init__(message)
