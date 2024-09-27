from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username_tg: str
    nick_tg: str
    nick_gmeet: str
    nick_gitlab: Optional[str] = None
    nick_github: Optional[str] = None
    avatar: Optional[str] = None


class UserResponseDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username_tg: str
    nick_tg: str
    nick_gmeet: str
    nick_gitlab: Optional[str] = None
    nick_github: Optional[str] = None
    avatar: Optional[str] = None
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = False
    date_joined: datetime
