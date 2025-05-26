from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserUpdateDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username_tg: str
    nick_tg: str
    nick_gmeet: str
    nick_gitlab: str | None = None
    nick_github: str | None = None
    avatar: str | None = None


class UserCreateDTO(UserUpdateDTO):
    password: str = None


class UserResponseDTO(UserUpdateDTO):
    is_superuser: bool | None = False
    is_active: bool | None = False

    model_config = ConfigDict(from_attributes=True)


class RegistrationResponseDTO(BaseModel):
    new_user: UserResponseDTO
    inviter_user_id: UUID
