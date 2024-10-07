from typing import TYPE_CHECKING

from passlib.context import CryptContext
from pydantic import EmailStr

from src.apps.user.dtos import UserResponseDTO
from src.apps.user.repositories import IUserRepository
from src.apps.user.services import GetUserService

if TYPE_CHECKING:
    from src.apps.user.protocols import JWTServiceProtocol


class AuthenticateUserService:

    def __init__(
        self,
        jwt_service: JWTServiceProtocol,
        repository: IUserRepository,
        pwd_context: CryptContext,
    ):
        self.repository = repository
        self.jwt_service = jwt_service
        self.pwd_context = pwd_context or CryptContext(schemes=['bcrypt'], deprecated='auto')

    async def authenticate_user(self, email: EmailStr, password: str) -> UserResponseDTO:
        get_user_service = GetUserService(self.repository)
        user = await get_user_service.get_user_by_email(email=email)
        if not user or not self.verify_password(password, user.password):
            return None
        await self.jwt_service.creating_tokens(user.email)
        return user

    def verify_password(self, plain_password: str, user_password: str) -> bool:
        return self.pwd_context.verify(plain_password, user_password)
