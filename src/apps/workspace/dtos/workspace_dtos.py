from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class CreateWorkspaceDTO:
    name: str
    owner_id: UUID


@dataclass
class WorkspaceOutDTO:
    workspace_id: UUID
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
class GetWorkspacesByMemberIdDTO:
    member_id: UUID


@dataclass
class UpdateWorkspaceDTO:
    workspace_id: UUID
    name: str | None = None
    description: str | None = None
    logo: str | None = None


@dataclass
class DeleteWorkspaceDTO:
    workspace_id: UUID
    owner_id: UUID


@dataclass
class MemberOutDTO:
    id: UUID
    name: str
