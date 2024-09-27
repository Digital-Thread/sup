from src.apps.user.repositories import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
