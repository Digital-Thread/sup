from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserUpdateDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username_tg: str
    nick_tg: str
    nick_gmeet: str
    nick_gitlab: Optional[str] = None
    nick_github: Optional[str] = None
    avatar: Optional[str] = None


class UserCreateDTO(UserUpdateDTO):
    password: str = None


class AdminCreateUserDTO(UserCreateDTO):
    is_active: Optional[bool] = False
    send_mail: Optional[bool] = False


class UserResponseDTO(UserUpdateDTO):
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)


class UserPasswordUpdateDTO(BaseModel):
    plain_password: Optional[str] = None
    new_password: Optional[str] = None


class AdminPasswordUpdateDTO(BaseModel):
    new_password: Optional[str] = None


class AuthDTO(BaseModel):
    email: EmailStr
    password: str
