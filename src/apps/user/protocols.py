from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol, Union

from pydantic import EmailStr


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


@dataclass
class SendMailServiceProtocol(Protocol):

    async def send_activation_email(self, email: str, token: str) -> None:
        pass

    async def send_invite_email(self, email: str, token: str) -> None:
        pass

    async def send_login_and_activate_email(self, email: str, password: str, token: str) -> None:
        pass

    async def send_login_email(self, email: str, password: str) -> None:
        pass
