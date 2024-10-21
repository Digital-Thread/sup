from dataclasses import MISSING, dataclass, fields
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, EmailStr, create_model, field_validator

from src.apps.user.dtos import (
    AdminCreateUserDTO,
    AdminPasswordUpdateDTO,
    AuthDTO,
    BaseUserDTO,
    UserCreateDTO,
    UserPasswordUpdateDTO,
    UserResponseDTO,
    UserUpdateDTO,
)

StdlibDataclass = type(dataclass)


class CustomBaseModel(BaseModel):
    @field_validator('first_name', mode='before', check_fields=False)
    def validate_first_name(cls, value: str) -> str:
        return value.capitalize() if isinstance(value, str) else value

    @field_validator('last_name', mode='before', check_fields=False)
    def validate_last_name(cls, value: str) -> str:
        return value.capitalize() if isinstance(value, str) else value

    @field_validator('email', mode='before', check_fields=False)
    def validate_email(cls, value: str) -> str:
        return value.lower() if isinstance(value, str) else value


def model_from_dataclass(kls: 'StdlibDataclass') -> Type[BaseModel]:
    field_definitions: Dict[str, Any] = {}
    for field in fields(kls):
        field_type = field.type
        if field.name == 'email':
            field_type = Optional[EmailStr]
        default_value = field.default if field.default is not MISSING else ...
        field_definitions[field.name] = (field_type, default_value)

    model = create_model(kls.__name__, __base__=CustomBaseModel, **field_definitions)

    return model


BaseUserDto = model_from_dataclass(BaseUserDTO)
UserCreateDTO = model_from_dataclass(UserCreateDTO)
AdminCreateUserDTO = model_from_dataclass(AdminCreateUserDTO)
UserResponseDTO = model_from_dataclass(UserResponseDTO)
UserUpdateDTO = model_from_dataclass(UserUpdateDTO)
AuthDTO = model_from_dataclass(AuthDTO)
UserPasswordUpdateDTO = model_from_dataclass(UserPasswordUpdateDTO)
AdminPasswordUpdateDTO = model_from_dataclass(AdminPasswordUpdateDTO)
