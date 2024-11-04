from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class CreateWorkspaceAppDTO:
    name: str
    owner_id: UUID


@dataclass
class WorkspaceAppDTO:
    id: UUID
    owner_id: UUID
    name: str
    created_at: datetime
    description: str | None = field(default=None)
    logo: str | None = field(default=None)
    invite_ids: list[int] = field(default_factory=list)
    project_ids: list[int] = field(default_factory=list)
    meet_ids: list[int] = field(default_factory=list)
    tag_ids: list[int] = field(default_factory=list)
    role_ids: list[int] = field(default_factory=list)
    member_ids: list[UUID] = field(default_factory=list)


@dataclass
class UpdateWorkspaceAppDTO:
    name: str | None = None
    description: str | None = None
    logo: str | None = None
