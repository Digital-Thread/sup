from src.apps.user.domain.entities import User
from src.apps.user.dtos import AdminPasswordUpdateDTO
from src.apps.user.dtos.dtos import UserPasswordUpdateDTO
from src.apps.user.exceptions import UserNotFoundByEmailException, UserPasswordException
from src.apps.user.repositories import IUserRepository
from src.apps.user.services import AuthenticateUserService, CreateUserService


class PasswordResetUserService:
    def __init__(
        self,
        repository: IUserRepository,
        authenticate_service: AuthenticateUserService,
        create_service: CreateUserService,
    ):
        self.repository = repository
        self.authenticate_service = authenticate_service
        self.create_service = create_service

    async def password_reset_user(self, email: str, dto: UserPasswordUpdateDTO) -> User:
        user = await self.repository.find_by_email(email)
        if not user:
            raise UserNotFoundByEmailException(email)
        verify = self.authenticate_service.verify_password(dto.plain_password, user.password)
        if not verify:
            raise UserPasswordException()
        else:
            User.validate_new_password(password=dto.new_password)
            user.password = self.create_service.get_password_hash(dto.new_password)
            await self.repository.update(user)
        return user

    async def password_reset_user_by_admin(self, email: str, dto: AdminPasswordUpdateDTO) -> User:
        user = await self.repository.find_by_email(email)
        if not user:
            raise UserNotFoundByEmailException(email)
        else:
            if dto.new_password is None:
                dto.new_password = self.create_service.generate_password()
                password_sent = True
            else:
                password_sent = False
                User.validate_new_password(password=dto.new_password)
            password = dto.new_password
            user.password = self.create_service.get_password_hash(dto.new_password)
            await self.repository.update(user)
            if password_sent:
                await self.create_service.send_mail_service.send_login_email(
                    email=user.email,
                    password=password,
                )
        return user
