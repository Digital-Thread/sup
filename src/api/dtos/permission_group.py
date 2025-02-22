from pydantic import BaseModel, ConfigDict

from src.apps.permission.domain import (
    PermissionId,
    UserId,
    PermissionGroupId,
)


class CreateGroupRequestDTO(BaseModel):
    name: str
    description: str | None = None
    permissions: set[PermissionId]
    authorized_users: set[UserId] | None = None


class UpdateGroupRequestDTO(BaseModel):
    name: str | None = None
    description: str | None = None
    permissions: set[PermissionId] | None = None
    authorized_users: set[UserId] | None = None


class GroupResponseDTO(BaseModel):
    id: PermissionGroupId
    name: str
    description: str | None
    permissions: set[PermissionId]
    authorized_users: set[UserId]
    model_config = ConfigDict(
        from_attributes=True,
    )
