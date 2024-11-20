import random
import string
import uuid
from dataclasses import asdict
from datetime import timedelta
from typing import Optional

from src.apps.user.domain.entities import User
from src.apps.user.dtos import UserCreateDTO
from src.apps.user.dtos.dtos import AdminCreateUserDTO
from src.apps.user.exceptions import (
    LengthUserPasswordException,
    TokenActivationExpire,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserPermissionError,
)
from src.apps.user.protocols import PasswordServiceProtocol
from src.apps.user.repositories import IUserRepository
from src.apps.user.repositories.redis_repository import IUserRedisRepository
from src.apps.user.tasks import (
    send_activation_email_task,
    send_invite_email_task,
    send_login_and_activate_email_task,
    send_login_email_task,
)
from src.config import SMTPConfig


class CreateUserService:
    def __init__(
        self,
        repository: IUserRepository,
        redis_client: IUserRedisRepository,
        smtp_config: SMTPConfig,
        password_service: PasswordServiceProtocol,
    ):
        self.repository = repository
        self.redis_client = redis_client
        self.password_service = password_service
        self.smtp_config = smtp_config

    async def create_user(self, dto: UserCreateDTO) -> User:
        existing_user = await self.repository.find_by_email(dto.email)
        if existing_user:
            raise UserAlreadyExistsError(dto.email)
        if dto.password is None:
            dto.password = self.generate_password()
            password_sent = True
        else:
            password_sent = False
        user_data = {k: v for k, v in asdict(dto).items() if k != 'password'}
        user_data['password'] = dto.password
        user = User(**user_data)
        if len(user.password) > 51:
            raise LengthUserPasswordException()
        password = user.password
        user.password = self.get_password_hash(dto.password)
        await self.repository.save(user)
        await self.redis_client.delete(f'invite_token:{dto.email}')
        activation_token = self.generate_uuid_token()
        await self.redis_client.set(
            f'activation_token:{activation_token}', user.email, ex=timedelta(days=7)
        )
        if password_sent:
            await send_login_and_activate_email_task.kiq(
                smtp_config=self.smtp_config,
                email=user.email,
                password=password,
                token=activation_token,
            )
        else:
            await send_activation_email_task.kiq(
                smtp_config=self.smtp_config, email=user.email, token=activation_token
            )
        return user

    async def create_user_by_invite(self, dto: UserCreateDTO, token: str) -> tuple[User, uuid.UUID]:
        invite_token = await self.redis_client.get(f'invite_token:{dto.email}')
        if invite_token is None:
            raise TokenActivationExpire()
        comparison_token = invite_token.split('_')[0]

        if comparison_token != token:
            raise UserPermissionError()

        inviter_email = invite_token.split('_')[1]

        inviter_user = await self.repository.find_by_email(inviter_email)
        inviter_user_id = inviter_user.id

        new_user = await self.create_user(dto)

        return new_user, inviter_user_id

    async def create_user_by_admin(self, dto: AdminCreateUserDTO) -> tuple[str, str]:
        existing_user = await self.repository.find_by_email(dto.email)
        if existing_user:
            raise UserAlreadyExistsError(dto.email)
        if dto.password is None:
            dto.password = self.generate_password()
        user_data = {k: v for k, v in asdict(dto).items() if k != 'send_mail'}
        user = User(**user_data)
        if len(user.password) > 51:
            raise LengthUserPasswordException
        password = user.password
        user.password = self.get_password_hash(dto.password)
        await self.repository.save(user)
        if not user.is_active and dto.send_mail:
            activation_token = self.generate_uuid_token()
            await self.redis_client.set(
                f'activation_token:{activation_token}', user.email, ex=timedelta(days=7)
            )
            await send_login_and_activate_email_task.kiq(
                smtp_config=self.smtp_config,
                email=user.email,
                password=password,
                token=activation_token,
            )
        if user.is_active and dto.send_mail:
            await send_login_email_task.kiq(
                smtp_config=self.smtp_config,
                email=user.email,
                password=password,
            )

        return user.email, password

    async def activate_user_by_admin(self, user: User) -> User:
        current_user = await self.repository.find_by_email(user.email)
        if current_user is None:
            raise UserNotFoundError()
        return await self.activate_user(user=current_user)

    async def activate_user(self, user: User) -> User:
        user.is_active = True
        await self.repository.update(user)
        return user

    async def activate_user_by_token(self, token: str) -> User:
        email = await self.redis_client.get(f'activation_token:{token}')
        if email is None:
            raise TokenActivationExpire()
        current_user = await self.repository.find_by_email(email)
        user = await self.activate_user(user=current_user)
        await self.redis_client.delete(f'activation_token:{token}')
        return user

    def get_password_hash(self, password: str) -> str:
        return self.password_service.hash_password(password)

    @staticmethod
    def generate_uuid_token() -> str:
        return str(uuid.uuid4())

    async def send_invite_link(self, from_email: str, to_email: str) -> None:
        user = await self.repository.find_by_email(to_email)
        if user:
            raise UserAlreadyExistsError(to_email)
        invite_token = self.generate_uuid_token() + '_' + from_email
        await self.redis_client.set(f'invite_token:{to_email}', invite_token, ex=timedelta(days=7))
        await send_invite_email_task.kiq(
            smtp_config=self.smtp_config, email=to_email, token=invite_token
        )

    @staticmethod
    def generate_password(length: int = 12) -> str:
        characters = string.ascii_letters + string.digits + "!#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        password = ''.join(random.choice(characters) for i in range(length))
        return password
