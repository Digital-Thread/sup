from abc import ABC, abstractmethod
from typing import List, Optional

from src.apps.user.domain.entity import User


class IUserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def find_all_users(
        self, limit: int, offset: int, sort_by: Optional[str] = None, sort_order: str = 'asc'
    ) -> List[User]:
        pass

    @abstractmethod
    async def delete(self, email: str) -> None:
        pass

    @abstractmethod
    async def update(self, user: User) -> None:
        pass
