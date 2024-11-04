from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.apps.workspace.domain.entities.workspace_invite import StatusInvite


class ResponseWorkspaceInviteDTO(BaseModel):
    id: int
    url: str
    status: str
    created_at: datetime
    expired_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateWorkspaceInviteDTO(BaseModel):
    status: StatusInvite
