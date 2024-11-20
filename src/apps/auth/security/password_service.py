from src.apps.auth.repositories.password_repository import IPasswordRepository


class PasswordService:
    def __init__(self, repository: IPasswordRepository):
        self.repository = repository

    def hash_password(self, password: str) -> str:
        return self.repository.hash_password(password)

    def verify_password(self, hashed_password: str, password: str) -> bool:
        return self.repository.verify_password(hashed_password, password)
