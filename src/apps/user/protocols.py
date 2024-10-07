from dataclasses import dataclass
from typing import Protocol

from pydantic import EmailStr


@dataclass
class JWTServiceProtocol(Protocol):

    async def creating_tokens(self, email: EmailStr) -> None:
        pass


@dataclass
class SendMailServiceProtocol(Protocol):

    async def send_activation_email(self, email: str, token: str) -> None:
        pass
