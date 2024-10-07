import datetime

from src.apps.user.dtos import UserUpdateDTO, UserResponseDTO
from src.apps.user.exceptions import UserNotFoundException, PermissionDeniedException
from src.apps.user.repositories import IUserRepository


class UpdateUserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def update_user(self, email: str, current_user: UserUpdateDTO, new_data: dict) -> UserResponseDTO:
        user = await self.user_repository.find_by_email(email)
        if not user:
            raise UserNotFoundException(user.email)
        if not current_user.is_superuser and user.email != current_user.email:
            raise PermissionDeniedException()
        restricted_fields = ['is_superuser', '_created_at', '_id']
        admin_only_fields = ['is_active']
        for key, value in new_data.items():
            if key in restricted_fields:
                continue
            if key in admin_only_fields and not current_user.is_superuser:
                continue
            if hasattr(user, key):
                setattr(user, key, value)
        user._updated_at = datetime.datetime.now
        await self.user_repository.update(user)
        return user
