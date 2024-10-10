import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseUserDto(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username_tg: str
    nick_tg: str
    nick_gmeet: str
    nick_gitlab: Optional[str] = None
    nick_github: Optional[str] = None
    avatar: Optional[str] = None


class UserCreateDTO(BaseUserDto):
    password: str


class UserResponseDTO(BaseUserDto):
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = False
    _created_at: datetime.datetime
    _updated_at: datetime.datetime


class UserUpdateDTO(BaseUserDto):
    is_active: Optional[bool] = False
