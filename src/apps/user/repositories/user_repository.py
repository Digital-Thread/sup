from abc import ABC, abstractmethod
from typing import List, Optional

from src.apps.user.domain.entities import User
from src.apps.user.dtos import UserResponseDTO


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[UserResponseDTO]:
        pass

    @abstractmethod
    def find_all_users(self) -> List[UserResponseDTO]:
        pass

