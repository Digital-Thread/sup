class BaseUserError(Exception):
    def __init__(self, message: str = 'Ошибка'):
        super().__init__(message)


class UserNotFoundError(BaseUserError):
    def __init__(self, message: str = 'Пользователь не найден.'):
        super().__init__(message)


class UserAlreadyExistsError(Exception):

    def __init__(self, email: str):
        super().__init__(f'Пользователь с email: {email} уже существует.')


class TokenActivationExpire(BaseUserError):
    def __init__(self, message: str = 'Время действия токена истекло'):
        super().__init__(message)


class UserNotFoundByEmailException(BaseUserError):
    def __init__(self, email: str):
        super().__init__(f'Пользователь с email: {email} не найден')


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


class InviteTokenExpiredError(Exception):
    def __init__(self, email: str):
        super().__init__(f'Для пользователя {email} нет инвайт ссылки на регистрацию')


class NotActivationExpire(BaseUserError):
    def __init__(self, message: str = 'Ваш аккаунт не активирован'):
        super().__init__(message)


class ValidateLengthError(Exception):
    def __init__(self, field_name: str, max_length: int):
        super().__init__(f'Длина {field_name} не должна превышать {max_length} символов.')


class ValidateEmptyLengthError(Exception):
    def __init__(self, field_name: str):
        super().__init__(f'{field_name} не может быть пустым.')


class OneOfTheExpire(BaseUserError):
    def __init__(
        self, message: str = 'Необходимо указать хотя бы один ник: nick_gitlab или nick_github.'
    ):
        super().__init__(message)


class InvalidNameError(BaseUserError):
    def __init__(
        self,
        message: str = 'В названии допускается использование только букв '
        'латинского и кириллического алфавитов.',
    ):
        super().__init__(message)


class InvalidEmailFormatError(BaseUserError):
    def __init__(self, message: str = 'Некорректный формат электронной почты.'):
        super().__init__(message)


class MissingUppercaseLetterError(BaseUserError):
    def __init__(self, message: str = 'Пароль должен содержать хотя бы одну заглавную букву.'):
        super().__init__(message)


class MissingDigitError(BaseUserError):
    def __init__(self, message: str = 'Пароль должен содержать хотя бы одну цифру.'):
        super().__init__(message)


class MissingSpecialCharacterError(BaseUserError):
    def __init__(self, message: str = 'Пароль должен содержать хотя бы один специальный символ.'):
        super().__init__(message)
