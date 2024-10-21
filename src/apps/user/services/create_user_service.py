import random
import string
import uuid
from dataclasses import asdict
from datetime import timedelta

import redis.asyncio as redis  # type: ignore
from passlib.context import CryptContext

from src.apps.user.domain.entities import User
from src.apps.user.dtos import UserCreateDTO, UserResponseDTO
from src.apps.user.dtos.dtos import AdminCreateUserDTO
from src.apps.user.exceptions import (
    LengthUserPasswordException,
    TokenActivationExpire,
    UserAlreadyExistsError,
    UserNotFoundByEmailException,
    UserNotFoundError,
    UserPermissionError,
)
from src.apps.user.protocols import JWTServiceProtocol, SendMailServiceProtocol
from src.apps.user.repositories import IUserRepository
from src.config import RedisConfig


class CreateUserService:
    def __init__(
        self,
        pwd_context: CryptContext,
        send_mail_service: SendMailServiceProtocol,
        repository: IUserRepository,
        redis_config: RedisConfig,
        token_service: JWTServiceProtocol,
    ):
        self.repository = repository
        self.pwd_context = pwd_context or CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.send_mail_service = send_mail_service
        dsn = redis_config.construct_redis_dsn
        self.redis_client = redis.StrictRedis.from_url(dsn)
        self.token_service = token_service

    async def create_user(self, dto: UserCreateDTO, token: str) -> User:
        existing_user = await self.repository.find_by_email(dto.email)
        if existing_user:
            raise UserAlreadyExistsError(dto.email)
        invite_token = await self.redis_client.get(f'invite_token:{dto.email}')
        if invite_token is None:
            raise TokenActivationExpire()
        if invite_token is not None:
            invite_token = invite_token.decode('utf-8')
        if invite_token == token:
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
                    email=user.email, password=password, token=activation_token
                )
            else:
                await self.send_mail_service.send_activation_email(
                    email=user.email, token=activation_token
                )
            return user
        else:
            raise UserPermissionError()

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
            await self.send_mail_service.send_login_and_activate_email(
                email=user.email, password=password, token=activation_token
            )
        if user.is_active and dto.send_mail:
            await self.send_mail_service.send_login_email(
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

    async def send_invite_link(self, email: str) -> None:
        user = await self.repository.find_by_email(email)
        if user:
            raise UserAlreadyExistsError(email)
        invite_token = self.generate_uuid_token()
        await self.redis_client.set(f'invite_token:{email}', invite_token, ex=timedelta(days=7))
        return await self.send_mail_service.send_invite_email(email, invite_token)

    @staticmethod
    def generate_password(length: int = 12) -> str:
        characters = string.ascii_letters + string.digits + "!#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        password = ''.join(random.choice(characters) for i in range(length))
        return password
