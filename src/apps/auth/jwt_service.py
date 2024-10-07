from datetime import datetime, timezone
from typing import Any, Dict, Optional, Union

import jwt
import redis.asyncio as redis
from pydantic import EmailStr

from src.apps.auth.dto import AccessTokenDTO, RefreshTokenDTO
from src.apps.auth.exceptions import InvalidTokenError, TokenExpireError, TokenRefreshExpireError
from src.config import JWTConfig, RedisConfig


class JWTService:

    def __init__(self, jwt_config: JWTConfig, redis_config: RedisConfig):
        self.secret_key = jwt_config.secret_key
        self.algorithm = jwt_config.algorithm
        self.token_expire_minutes = jwt_config.access_token_expire_minutes
        self.access_token_lifetime = jwt_config.access_token_lifetime
        self.refresh_token_lifetime = jwt_config.refresh_token_lifetime

        dsn = redis_config.construct_redis_dsn
        self.redis_client = redis.StrictRedis.from_url(dsn)

    async def create_access_token(self, email: EmailStr) -> AccessTokenDTO:
        expiration = datetime.now(timezone.utc) + self.access_token_lifetime
        token = jwt.encode(
            {'email': email, 'exp': expiration}, self.secret_key, algorithm=self.algorithm
        )
        return token

    async def create_refresh_token(self, email: EmailStr) -> RefreshTokenDTO:
        expiration = datetime.now(timezone.utc) + self.refresh_token_lifetime
        token = jwt.encode(
            {'email': email, 'exp': expiration}, self.secret_key, algorithm=self.algorithm
        )
        return token

    async def decode_token(self, token: AccessTokenDTO) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=self.algorithm)
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpireError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    async def creating_tokens(self, email: EmailStr) -> tuple[AccessTokenDTO, RefreshTokenDTO]:
        access_token = await self.create_access_token(email)
        refresh_token = await self.create_refresh_token(email)

        await self.redis_client.set(f'access_token:{email}', access_token, ex=self.access_token_lifetime)
        await self.redis_client.set(
            f'refresh_token:{email}', refresh_token, ex=self.refresh_token_lifetime
        )
        return access_token, refresh_token

    async def removing_tokens(self, email: EmailStr) -> None:
        await self.redis_client.delete(f'access_token:{email}')
        await self.redis_client.delete(f'refresh_token:{email}')
        return

    async def access_protected_resource(self, email: EmailStr) -> Union[bool, RefreshTokenDTO]:
        access_token = await self.redis_client.get(f'access_token:{email}')
        if access_token:
            decoded = await self.decode_token(access_token)
            if decoded:
                return True
        else:
            return await self.refresh_access_token(email)
        return False

    async def refresh_access_token(self, email: EmailStr) -> bool:
        refresh_token = await self.redis_client.get(f'refresh_token:{email}')
        if refresh_token:
            decoded = await self.decode_token(refresh_token)
            if decoded and decoded['email'] == email:
                new_access_token = await self.create_access_token(email)
                new_refresh_token = await self.create_refresh_token(email)
                await self.redis_client.set(
                    f'access_token:{email}', new_access_token, ex=self.access_token_lifetime
                )
                await self.redis_client.set(
                    f'refresh_token:{email}', new_refresh_token, ex=self.refresh_token_lifetime
                )
                return True
        raise TokenRefreshExpireError()
