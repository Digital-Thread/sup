from abc import ABC, abstractmethod


class IPasswordRepository(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, hashed_password: str, password: str) -> bool:
        pass
