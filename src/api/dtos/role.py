from pydantic import BaseModel, ConfigDict, Field


class CreateRoleDTO(BaseModel):
    name: str
    color: str


class MemberResponseDTO(BaseModel):
    first_name: str
    last_name: str
    avatar: str

    model_config = ConfigDict(from_attributes=True)


class RoleWithMembersResponseDTO(BaseModel):
    id: int
    name: str
    color: str
    members: list[MemberResponseDTO] | None

    model_config = ConfigDict(from_attributes=True)


class RoleResponseDTO(BaseModel):
    id: int
    name: str
    color: str

    model_config = ConfigDict(from_attributes=True)


class UpdateRoleDTO(BaseModel):
    name: str | None = Field(default=None)
    color: str | None = Field(default=None)
