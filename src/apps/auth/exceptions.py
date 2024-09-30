class JWTException(Exception):
    def __init__(self, message: str = 'Ошибка JWT'):
        super().__init__(message)


class InvalidTokenError(JWTException):
    def __init__(self, message: str = 'Невалидный формат токена'):
        super().__init__(message)

class TokenExpireError(JWTException):
    def __init__(self, message: str = 'Время токена истекло'):
        super().__init__(message)
