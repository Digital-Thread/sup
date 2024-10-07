from typing import Callable, Any
from uuid import UUID

from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInvite
from src.apps.workspace.repositories.i_workspace_invite_repository import IWorkspaceInviteRepository
from src.apps.workspace.services.base_service import BaseService


class WorkspaceInviteService(BaseService[WorkspaceInvite, int, IWorkspaceInviteRepository]):
    async def retrieve_by_workspace_id(
        self, workspace_id: UUID, use_case: Callable[[IWorkspaceInviteRepository], Any]
    ) -> list[WorkspaceInvite]:
        return await self.retrieve_by_workspace_id(workspace_id, use_case)