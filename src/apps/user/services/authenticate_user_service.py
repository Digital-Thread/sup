from passlib.context import CryptContext

from src.apps.user.domain.entities import User
from src.apps.user.dtos import AuthDTO
from src.apps.user.exceptions import NotActivationExpire, UserPasswordException
from src.apps.user.repositories import IUserRepository
from src.apps.user.services import GetUserService


class AuthenticateUserService:

    def __init__(
        self,
        repository: IUserRepository,
        pwd_context: CryptContext,
        get_user_service: GetUserService,
    ):
        self.repository = repository
        self.pwd_context = pwd_context or CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.get_user_service = get_user_service

    async def authenticate_user(self, dto: AuthDTO) -> User:
        user = await self.get_user_service.get_user_by_email(email=dto.email)

        if not user or not self.verify_password(dto.password, user.password):
            raise UserPasswordException()
        if not user.is_active:
            raise NotActivationExpire()
        return user

    def verify_password(self, plain_password: str, user_password: str) -> bool:
        return self.pwd_context.verify(plain_password, user_password)
