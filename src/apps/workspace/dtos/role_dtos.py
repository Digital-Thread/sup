from dataclasses import dataclass
from uuid import UUID


@dataclass
class BaseRoleDTO:
    id: int
    workspace_id: UUID


@dataclass
class CreateRoleAppDTO:
    name: str
    color: str
    workspace_id: UUID


@dataclass
class RoleWithUserCountAppDTO:
    id: int
    name: str
    color: str
    user_count: int


@dataclass
class GetRolesAppDTO:
    workspace_id: UUID


@dataclass
class UpdateRoleAppDTO(BaseRoleDTO):
    name: str | None = None
    color: str | None = None


class DeleteRoleAppDTO(BaseRoleDTO):
    pass


@dataclass
class AssignRoleToWorkspaceMemberDTO(BaseRoleDTO):
    member_id: UUID


@dataclass
class RemoveRoleFromWorkspaceMemberDTO:
    workspace_id: UUID
    member_id: UUID