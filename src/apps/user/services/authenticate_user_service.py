from passlib.context import CryptContext
from pydantic import EmailStr

from src.apps.user.dtos import UserResponseDTO
from src.apps.user.exceptions import NotActivationExpire, UserPasswordException
from src.apps.user.protocols import JWTServiceProtocol
from src.apps.user.repositories import IUserRepository
from src.apps.user.services import GetUserService


class AuthenticateUserService:

    def __init__(
        self,
        repository: IUserRepository,
        pwd_context: CryptContext,
        token_service: JWTServiceProtocol,
    ):
        self.repository = repository
        self.pwd_context = pwd_context or CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.token_service = token_service

    async def authenticate_user(self, email: EmailStr, password: str) -> UserResponseDTO:
        get_user_service = GetUserService(self.repository, self.token_service)
        user = await get_user_service.get_user_by_email(email=email)
        if not user or not self.verify_password(password, user.password):
            raise UserPasswordException()
        if not user.is_active:
            raise NotActivationExpire()
        return user

    def verify_password(self, plain_password: str, user_password: str) -> bool:
        return self.pwd_context.verify(plain_password, user_password)
