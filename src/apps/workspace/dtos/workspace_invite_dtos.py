from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.apps.workspace.domain.entities.workspace_invite import StatusInvite
from src.apps.workspace.dtos.pagination_dto import PaginationDTO


@dataclass
class WorkspaceInviteOutDTO:
    id: int
    workspace_id: UUID
    code: UUID
    status: str
    created_at: datetime
    expired_at: datetime


@dataclass
class GetWorkspaceInvitesDTO(PaginationDTO):
    workspace_id: UUID


@dataclass
class UpdateWorkspaceInviteAppDTO:
    id_: int
    workspace_id: UUID
    status: StatusInvite | None = None
