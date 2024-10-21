from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BaseUserDTO:
    first_name: str
    last_name: str
    email: str
    username_tg: str
    nick_tg: str
    nick_gmeet: str
    nick_gitlab: Optional[str] = None
    nick_github: Optional[str] = None
    avatar: Optional[str] = None


@dataclass
class UserCreateDTO(BaseUserDTO):
    password: str = None


@dataclass
class AdminCreateUserDTO(UserCreateDTO):
    is_active: Optional[bool] = False
    send_mail: Optional[bool] = False


@dataclass
class UserResponseDTO(BaseUserDTO):
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = False


@dataclass
class UserUpdateDTO:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    username_tg: Optional[str] = None
    nick_tg: Optional[str] = None
    nick_gmeet: Optional[str] = None
    nick_gitlab: Optional[str] = None
    nick_github: Optional[str] = None
    avatar: Optional[str] = None


@dataclass
class UserPasswordUpdateDTO:
    plain_password: Optional[str] = None
    new_password: Optional[str] = None


@dataclass
class AdminPasswordUpdateDTO:
    new_password: Optional[str] = None


@dataclass
class AuthDTO:
    email: str
    password: str
