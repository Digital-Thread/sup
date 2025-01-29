from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateRoleAppDTO:
    name: str
    color: str
    workspace_id: UUID


@dataclass
class MemberOutDTO:
    first_name: str
    last_name: str
    avatar: str


@dataclass
class RoleWithMemberOutDTO:
    id: int
    name: str
    color: str
    members: list[MemberOutDTO] | None


@dataclass
class RoleOutDTO:
    id: int
    name: str
    color: str


@dataclass
class UpdateRoleAppDTO:
    id: int
    workspace_id: UUID
    name: str | None = None
    color: str | None = None


@dataclass
class AssignRoleToWorkspaceMemberDTO:
    id: int
    workspace_id: UUID
    member_id: UUID
