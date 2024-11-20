from dataclasses import dataclass
from typing import Optional, Protocol, Union

from pydantic import EmailStr

from src.config import SMTPConfig


@dataclass
class JWTServiceProtocol(Protocol):

    async def creating_tokens(self, email: EmailStr, user_agent: str) -> tuple[str, int, str, int]:
        pass

    async def refresh_token_protected_resource(
        self, email: EmailStr, refresh_token_client: str, user_agent: str
    ) -> bool:
        pass

    async def decode_access_token(self, token: str) -> Optional[str]:
        pass

    async def decode_refresh_token(self, token: str) -> str | None:
        pass

    async def create_refresh_token(self, email: EmailStr) -> str:
        pass

    async def access_token_protected_resource(
        self, email: EmailStr, access_token_client: str, user_agent: str
    ) -> Union[bool, str]:
        pass

    async def removing_tokens(self, email: EmailStr, user_agent: str) -> None:
        pass

    async def delete_tokens_user(self, email: EmailStr) -> None:
        pass


@dataclass
class PasswordServiceProtocol(Protocol):

    def hash_password(self, password: str) -> str:
        pass

    def verify_password(self, hashed_password: str, password: str) -> bool:
        pass
