from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union

import jwt
import redis
from pydantic import EmailStr

from src.apps.auth.dto import AccessTokenDTO, RefreshTokenDTO
from src.config import JWTConfig, RedisConfig


class JWTService:

    def __init__(self, jwt_config: JWTConfig, redis_config: RedisConfig):
        self.secret_key = jwt_config.SECRET_KEY
        self.algorithm = jwt_config.ALGORITHM
        self.token_expire_minutes = jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES

        self.ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
        self.REFRESH_TOKEN_LIFETIME = timedelta(days=7)

        dsn = redis_config.construct_redis_dsn
        self.redis_client = redis.StrictRedis.from_url(dsn)

    def create_access_token(self, email: EmailStr) -> AccessTokenDTO:
        expiration = datetime.now(timezone.utc) + self.ACCESS_TOKEN_LIFETIME
        token = jwt.encode(
            {'email': email, 'exp': expiration}, self.secret_key, algorithm=self.algorithm
        )
        return token

    def create_refresh_token(self, email: EmailStr) -> RefreshTokenDTO:
        expiration = datetime.now(timezone.utc) + self.REFRESH_TOKEN_LIFETIME
        token = jwt.encode(
            {'email': email, 'exp': expiration}, self.secret_key, algorithm=self.algorithm
        )
        return token

    def decode_token(self, token: AccessTokenDTO) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=self.algorithm)
            print(payload)
            return payload
        except jwt.ExpiredSignatureError:
            print('Токе истек!')
            return None
        except jwt.InvalidTokenError:
            print('Невалидный токен!')
            return None

    def creating_tokens(self, email: EmailStr) -> tuple[AccessTokenDTO, RefreshTokenDTO]:
        access_token = self.create_access_token(email)
        refresh_token = self.create_refresh_token(email)

        self.redis_client.set(f'access_token:{email}', access_token, ex=self.ACCESS_TOKEN_LIFETIME)
        self.redis_client.set(
            f'refresh_token:{email}', refresh_token, ex=self.REFRESH_TOKEN_LIFETIME
        )

        print(f'Успешный вход! Токен доступа: {access_token}')
        print(f'Токен обновления: {refresh_token}')
        return access_token, refresh_token

    def removing_tokens(self, email: EmailStr) -> None:
        self.redis_client.delete(f'access_token:{email}')
        self.redis_client.delete(f'refresh_token:{email}')
        return

    def access_protected_resource(self, email: EmailStr) -> Union[bool, RefreshTokenDTO]:
        access_token = self.redis_client.get(f'access_token:{email}')
        if access_token:
            decoded = self.decode_token(access_token)
            if decoded:
                print(f"Предоставлен доступ для электронной почты: {decoded['email']}")
                return True
        else:
            print(
                'Срок действия токена доступа истек или он отсутствует, при попытке обновления...'
            )
            return self.refresh_access_token(email)
        return False

    # Функция для обновления access token с использованием refresh token
    def refresh_access_token(self, email: EmailStr) -> bool:
        refresh_token = self.redis_client.get(f'refresh_token:{email}')
        if refresh_token:
            decoded = self.decode_token(refresh_token)
            if decoded and decoded['email'] == email:
                new_access_token = self.create_access_token(email)
                new_refresh_token = self.create_refresh_token(email)
                self.redis_client.set(
                    f'access_token:{email}', new_access_token, ex=self.ACCESS_TOKEN_LIFETIME
                )
                self.redis_client.set(
                    f'refresh_token:{email}', new_refresh_token, ex=self.REFRESH_TOKEN_LIFETIME
                )
                print(f'Обновлен токен доступа! Новый токен доступа: {new_access_token}')
                return True
        print(
            'Токен обновления недействителен или срок его действия истек. Пожалуйста, войдите в систему еще раз.'
        )
        return False
