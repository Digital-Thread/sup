from src.apps.user.domain.entities import User
from src.apps.user.dtos import AuthDTO
from src.apps.user.exceptions import NotActivationExpire, UserPasswordException
from src.apps.user.protocols import PasswordServiceProtocol
from src.apps.user.repositories import IUserRepository
from src.apps.user.services import GetUserService


class AuthenticateUserService:

    def __init__(
        self,
        repository: IUserRepository,
        get_user_service: GetUserService,
        password_service: PasswordServiceProtocol,
    ):
        self.repository = repository
        self.get_user_service = get_user_service
        self.password_service = password_service

    async def authenticate_user(self, dto: AuthDTO) -> User:
        user = await self.get_user_service.get_user_by_email(email=dto.email)

        if not user or not self.verify_password(dto.password, user.password):
            raise UserPasswordException()
        if not user.is_active:
            raise NotActivationExpire()
        return user

    def verify_password(self, hashed_password: str, password: str) -> bool:
        return self.password_service.verify_password(hashed_password, password)
