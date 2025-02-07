import time
from datetime import datetime, timezone
from typing import Optional, Union

import jwt
import redis.asyncio as redis

from src.apps.auth.dto import AccessTokenDTO, RefreshTokenDTO
from src.apps.auth.exceptions import (
    InvalidTokenError,
    TokenExpireError,
    TokenRefreshExpireError,
)
from src.config import JWTConfig, RedisConfig


class JWTService:

    def __init__(self, jwt_config: JWTConfig, redis_config: RedisConfig):
        self.secret_key = jwt_config.secret_key
        self.algorithm = jwt_config.algorithm
        self.access_token_lifetime = jwt_config.access_token_lifetime
        self.refresh_token_lifetime = jwt_config.refresh_token_lifetime

        dsn = redis_config.construct_redis_dsn
        self.redis_client = redis.StrictRedis.from_url(dsn)

    async def create_access_token(self, email: str) -> tuple[str, int]:
        expiration_access = datetime.now(timezone.utc) + self.access_token_lifetime
        max_age_access = int(expiration_access.timestamp()) - int(time.time())
        access_token = jwt.encode(
            {'email': email, 'exp': expiration_access}, self.secret_key, algorithm=self.algorithm
        )
        return access_token, max_age_access

    async def create_refresh_token(self, email: str) -> tuple[str, int]:
        expiration_refresh = datetime.now(timezone.utc) + self.refresh_token_lifetime
        max_age_refresh = int(expiration_refresh.timestamp()) - int(time.time())
        refresh_token = jwt.encode(
            {'email': email, 'exp': expiration_refresh}, self.secret_key, algorithm=self.algorithm
        )
        return refresh_token, max_age_refresh

    async def decode_access_token(self, token: str) -> str | bytes:
        try:
            algorithms = [self.algorithm] if isinstance(self.algorithm, str) else self.algorithm
            payload = jwt.decode(token, self.secret_key, algorithms=algorithms)
            email = payload['email']
            return email
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def decode_refresh_token(self, token: str) -> str | bytes:
        try:
            algorithms = [self.algorithm] if isinstance(self.algorithm, str) else self.algorithm
            payload = jwt.decode(token, self.secret_key, algorithms=algorithms)
            email = payload['email']
            return email
        except jwt.ExpiredSignatureError:
            raise TokenExpireError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    async def creating_tokens(self, email: str, user_agent: str) -> tuple[str, int, str, int]:
        access_token, access_max_age = await self.create_access_token(email)
        refresh_token, refresh_max_age = await self.create_refresh_token(email)

        await self.redis_client.set(
            f'access_token:{email}/{user_agent}', access_token, ex=self.access_token_lifetime
        )
        await self.redis_client.set(
            f'refresh_token:{email}/{user_agent}', refresh_token, ex=self.refresh_token_lifetime
        )
        return access_token, access_max_age, refresh_token, refresh_max_age

    async def removing_tokens(self, email: str, user_agent: str) -> None:
        await self.redis_client.delete(f'access_token:{email}/{user_agent}')
        await self.redis_client.delete(f'refresh_token:{email}/{user_agent}')
        return

    async def access_token_protected_resource(
        self, email: str, access_token_client: str, user_agent: str
    ) -> Union[bool, RefreshTokenDTO]:
        access_token: Optional[bytes] = await self.redis_client.get(
            f'access_token:{email}/{user_agent}'
        )
        if access_token is not None and isinstance(access_token, bytes):
            access_token_str: str = access_token.decode('utf-8')
            if access_token_str == access_token_client:
                decoded = await self.decode_access_token(access_token_str)
                if decoded:
                    return True
        return False

    async def refresh_token_protected_resource(
        self, email: str, refresh_token_client: str, user_agent: str
    ) -> bool:
        refresh_token = await self.redis_client.get(f'refresh_token:{email}/{user_agent}')
        if refresh_token is not None:
            refresh_token_str: str = refresh_token.decode('utf-8')
            if refresh_token_str == refresh_token_client:
                return True
        raise TokenRefreshExpireError()

    async def delete_tokens_user(self, email: str) -> None:
        pattern = f'access_token:{email}/*'
        async for key in self.redis_client.scan_iter(pattern):
            await self.redis_client.delete(key)

        pattern = f'refresh_token:{email}/*'
        async for key in self.redis_client.scan_iter(pattern):
            await self.redis_client.delete(key)
