from typing import TYPE_CHECKING

from pydantic import EmailStr

from src.apps.user.dtos import UserResponseDTO
from src.apps.user.repositories import UserRepository
from src.apps.user.services import CreateUserService, GetUserService

if TYPE_CHECKING:
    from src.apps.user.protocols import JWTServiceProtocol


class AuthenticateUserService(CreateUserService):

    def __init__(self, jwt_service: JWTServiceProtocol, repository: UserRepository):
        super().__init__(repository=repository)
        self.jwt_service = jwt_service

    def authenticate_user(self, email: EmailStr, password: str) -> UserResponseDTO:
        """Аутентификация пользователя"""
        get_user_service = GetUserService(self.repository)
        user = get_user_service.get_user_by_email(email=email)
        if not user or not self.verify_password(password, user.password):
            return None
        self.jwt_service.creating_tokens(user.email)
        return user

    def verify_password(self, plain_password: str, user_password: str) -> bool:
        """Проврка совпадения пароля"""
        return self.pwd_context.verify(plain_password, user_password)
