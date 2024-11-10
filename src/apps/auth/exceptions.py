class JWTException(Exception):
    def __init__(self, message: str = 'Ошибка JWT'):
        super().__init__(message)


class InvalidTokenError(JWTException):
    def __init__(self, message: str = 'Невалидный формат рефреш токена'):
        super().__init__(message)


class TokenExpireError(JWTException):
    def __init__(self, message: str = 'Время токена истекло'):
        super().__init__(message)


class TokenRefreshExpireError(JWTException):
    def __init__(
        self,
        message: str = 'Токен обновления недействителен или срок его действия истек. Пожалуйста, войдите в систему еще раз.',
    ):
        super().__init__(message)
