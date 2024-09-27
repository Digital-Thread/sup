from dataclasses import dataclass
from typing import Protocol

from pydantic import EmailStr


@dataclass
class JWTServiceProtocol(Protocol):

    def creating_tokens(self, email: EmailStr) -> None:
        pass
