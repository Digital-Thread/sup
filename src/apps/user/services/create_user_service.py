import random
import string
import uuid
from dataclasses import asdict
from datetime import timedelta
from typing import Optional

import redis.asyncio as redis
from passlib.context import CryptContext

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
from src.apps.user.protocols import SendMailServiceProtocol
from src.apps.user.repositories import IUserRepository
from src.config import RedisConfig, SMTPConfig


class CreateUserService:
    def __init__(
        self,
        pwd_context: CryptContext,
        send_mail_service: SendMailServiceProtocol,
        repository: IUserRepository,
        redis_config: RedisConfig,
        smtp_config: SMTPConfig,
    ):
        self.repository = repository
        self.pwd_context = pwd_context or CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.send_mail_service = send_mail_service
        dsn = redis_config.construct_redis_dsn
        self.redis_client = redis.StrictRedis.from_url(dsn)
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
            await self.send_mail_service.send_login_and_activate_email(
                smtp_config=self.smtp_config,
                email=user.email,
                password=password,
                token=activation_token,
            )
        else:
            await self.send_mail_service.send_activation_email(
                smtp_config=self.smtp_config, email=user.email, token=activation_token
            )
        return user

    async def create_user_by_invite(self, dto: UserCreateDTO, token: str) -> tuple[User, uuid.UUID]:
        invite_token: Optional[bytes] = await self.redis_client.get(f'invite_token:{dto.email}')
        if invite_token is None:
            raise TokenActivationExpire()
        invite_token_str: str = invite_token.decode('utf-8')
        comparison_token = invite_token_str.split('_')[0]

        if comparison_token != token:
            raise UserPermissionError()

        inviter_email = invite_token_str.split('_')[1]

        inviter_user = await self.repository.find_by_email(inviter_email)
        inviter_user_id = inviter_user.id

        new_user = await self.create_user(dto)

        return new_user, inviter_user_id

    async def create_user_by_admin(self, dto: AdminCreateUserDTO) -> tuple[uuid.UUID, str, str, str]:
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
            await self.send_mail_service.send_login_and_activate_email(
                smtp_config=self.smtp_config,
                email=user.email,
                password=password,
                token=activation_token,
            )
        if user.is_active and dto.send_mail:
            await self.send_mail_service.send_login_email(
                smtp_config=self.smtp_config,
                email=user.email,
                password=password,
                token=activation_token,
            )

        return user.id, user.first_name + '' + user.last_name, user.email, password

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
        email_bytes = await self.redis_client.get(f'activation_token:{token}')
        print(email_bytes)
        if email_bytes is None:
            raise TokenActivationExpire()
        email = email_bytes.decode()
        print(email)
        current_user = await self.repository.find_by_email(email)
        user = await self.activate_user(user=current_user)
        await self.redis_client.delete(f'activation_token:{token}')
        return user

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    @staticmethod
    def generate_uuid_token() -> str:
        return str(uuid.uuid4())

    async def send_invite_link(self, from_email: str, to_email: str) -> None:
        user = await self.repository.find_by_email(to_email)
        if user:
            raise UserAlreadyExistsError(to_email)
        invite_token = self.generate_uuid_token() + '_' + from_email
        await self.redis_client.set(f'invite_token:{to_email}', invite_token, ex=timedelta(days=7))
        return await self.send_mail_service.send_invite_email(
            smtp_config=self.smtp_config, email=to_email, token=invite_token
        )

    @staticmethod
    def generate_password(length: int = 12) -> str:
        characters = string.ascii_letters + string.digits + "!#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        password = ''.join(random.choice(characters) for i in range(length))
        return password
