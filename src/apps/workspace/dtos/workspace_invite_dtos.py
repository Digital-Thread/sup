from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.apps.workspace.domain.entities.workspace_invite import StatusInvite


@dataclass
class BaseWorkspaceInviteDto:
    workspace_id: UUID


@dataclass
class CreateWorkspaceInviteDTO(BaseWorkspaceInviteDto):
    pass


@dataclass
class WorkspaceInviteAppDTO(BaseWorkspaceInviteDto):
    id: int
    code: UUID
    status: str
    created_at: datetime
    expired_at: datetime


@dataclass
class GetWorkspaceInvitesAppDTO(BaseWorkspaceInviteDto):
    pass


@dataclass
class UpdateWorkspaceInviteAppDTO(BaseWorkspaceInviteDto):
    id_: int
    status: StatusInvite | None = None


@dataclass
class DeleteWorkspaceInviteAppDTO(BaseWorkspaceInviteDto):
    id_: int
