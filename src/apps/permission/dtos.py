from dataclasses import dataclass

from src.apps.permission.domain import (
    PermissionId,
    WorkspaceId,
    PermissionGroupId,
    UserId,
    OptionalPermissionGroupUpdateFields,
)


@dataclass
class PermissionOutputDTO:
    id: PermissionId
    description: str


@dataclass
class PermissionGroupInputDTO:
    workspace_id: WorkspaceId
    name: str
    description: str | None
    permissions: set[PermissionId]
    authorized_users: set[UserId] | None


@dataclass
class PermissionGroupUpdateDTO:
    id: PermissionGroupId
    updated_fields: OptionalPermissionGroupUpdateFields


@dataclass
class PermissionGroupOutputDTO:
    id: PermissionGroupId
    name: str
    description: str | None
    permissions: set[PermissionId]
    authorized_users: set[UserId]
