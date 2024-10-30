from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.apps.workspace.domain.entities.workspace_invite import StatusInvite


@dataclass
class WorkspaceInviteAppDTO:
    id: int
    workspace_id: UUID
    code: UUID
    status: str
    created_at: datetime
    expired_at: datetime


@dataclass
class UpdateWorkspaceInviteAppDTO:
    status: StatusInvite | None = None
