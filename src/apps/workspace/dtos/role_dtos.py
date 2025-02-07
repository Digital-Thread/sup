from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateRoleAppDTO:
    name: str
    color: str


@dataclass
class RoleWithUserCountAppDTO:
    id: int
    name: str
    color: str
    user_count: int


@dataclass
class RoleOutDTO:
    id: int
    workspace_id: UUID
    name: str
    color: str


@dataclass
class UpdateRoleAppDTO:
    id: int
    name: str | None = None
    color: str | None = None


@dataclass
class AssignRoleToWorkspaceMemberDTO:
    id: int
    member_id: UUID
