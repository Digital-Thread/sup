from passlib.context import CryptContext

from src.apps.auth.repositories import IPasswordRepository


class PasswordRepository(IPasswordRepository):
    def __init__(self, pwd_context: CryptContext = None):
        self.pwd_context = pwd_context or CryptContext(schemes=['bcrypt'], deprecated='auto')

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, hashed_password: str, password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
