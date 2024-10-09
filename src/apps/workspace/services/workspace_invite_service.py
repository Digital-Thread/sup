from typing import Any, Callable
from uuid import UUID

from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInvite
from src.apps.workspace.dtos.workspace_invite_dtos import WorkspaceInviteAppDTO
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)
from src.apps.workspace.services.base_service import BaseService


class WorkspaceInviteService(
    BaseService[WorkspaceInvite, WorkspaceInviteAppDTO, int, IWorkspaceInviteRepository]
):
    pass
