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


class UserNotFoundByEmailException(BaseUserError):
    def __init__(self, email: str):
        super().__init__(f'Пользователь с email {email} не найден')


class PermissionDeniedException(BaseUserError):
    def __init__(self, message: str = 'Вы можете редактировать только свою учетную запись'):
        super().__init__(message)


class LengthUserPasswordException(BaseUserError):
    def __init__(self, message: str = 'Пароль не может быть длиннее 50 символов'):
        super().__init__(message)


class UserPasswordException(BaseUserError):
    def __init__(self, message: str = 'Неверный пароль'):
        self.message = message
        super().__init__(message)


class TokenExpiredError(Exception):
    def __init__(self, message: str = 'Зайдите в систему'):
        super().__init__(message)


class UserNotAdminError(BaseUserError):
    def __init__(self, message: str = 'Вы можете смотреть информацию только о себе'):
        super().__init__(message)


class UserPermissionError(BaseUserError):
    def __init__(self, message: str = 'У вас нет прав для доступа к этому ресурсу'):
        super().__init__(message)
