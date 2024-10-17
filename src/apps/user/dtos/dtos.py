import datetime
import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


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

    @field_validator('first_name', 'last_name')
    def capitalize_first_letter(cls, v: str) -> str:
        return v.capitalize() if isinstance(v, str) else v

    @field_validator('email')
    def lowercase_email(cls, v: str) -> str:
        return v.lower() if isinstance(v, str) else v


class UserCreateDTO(BaseUserDto):
    password: str = ''

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if value == '':
            return value
        if not re.search(r'[A-Z]', value):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву.')
        if not re.search(r'\d', value):
            raise ValueError('Пароль должен содержать хотя бы одну цифру.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError('Пароль должен содержать хотя бы один специальный символ.')
        return value


class AdminCreateUserDTO(UserCreateDTO):
    is_active: Optional[bool] = False
    send_mail: Optional[bool] = False


class UserResponseDTO(BaseUserDto):
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = False
    _created_at: datetime.datetime
    _updated_at: datetime.datetime


class UserUpdateDTO(BaseUserDto):
    pass


class AuthDTO(BaseModel):
    email: str
    password: str
