from passlib.context import CryptContext

from src.apps.user.protocols import JWTServiceProtocol
from src.apps.user.repositories import IUserRepository


class LogoutUserService:

    def __init__(
        self,
        jwt_service: JWTServiceProtocol,
        repository: IUserRepository,
        pwd_context: CryptContext,
    ):
        self.repository = repository
        self.jwt_service = jwt_service
        self.pwd_context = pwd_context or CryptContext(schemes=['bcrypt'], deprecated='auto')
