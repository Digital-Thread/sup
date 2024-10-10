import datetime
from typing import Optional

from src.apps.user.dtos import BaseUserDto


class UserResponseDTO(BaseUserDto):
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = False
    _created_at: datetime.datetime
    _updated_at: datetime.datetime
