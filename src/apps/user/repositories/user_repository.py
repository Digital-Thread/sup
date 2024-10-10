from abc import ABC, abstractmethod
from typing import List, Optional

from src.apps.user.domain.entities import User
from src.apps.user.dtos import UserResponseDTO


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[UserResponseDTO]:
        pass

    @abstractmethod
    async def find_all_users(self) -> List[UserResponseDTO]:
        pass

    @abstractmethod
    async def delete(self, email: str) -> None:
        pass

    @abstractmethod
    async def update(self, user: User) -> None:
        pass
