from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class BaseWorkspaceDto:
    id: UUID

@dataclass
class CreateWorkspaceAppDTO:
    name: str
    owner_id: UUID


@dataclass
class WorkspaceAppDTO(BaseWorkspaceDto):
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
class GetWorkspaceAppDTO(BaseWorkspaceDto):
    pass


@dataclass
class GetWorkspacesByMemberIdDTO:
    member_id: UUID


@dataclass
class UpdateWorkspaceAppDTO(BaseWorkspaceDto):
    name: str | None = None
    description: str | None = None
    logo: str | None = None


@dataclass
class DeleteWorkspaceAppDTO(BaseWorkspaceDto):
    owner_id: UUID
