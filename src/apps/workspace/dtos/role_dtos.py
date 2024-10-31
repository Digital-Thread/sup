from dataclasses import dataclass
from uuid import UUID


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
class UpdateRoleAppDTO:
    name: str | None = None
    color: str | None = None
