from typing import Any, Callable
from uuid import UUID

from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.dtos.workspace_dtos import WorkspaceAppDTO
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository
from src.apps.workspace.services.base_service import BaseService


class WorkspaceService(BaseService[Workspace, WorkspaceAppDTO, UUID, IWorkspaceRepository]):
    async def retrieve_by_owner_id(
        self, owner_id: UUID, use_case: Callable[[IWorkspaceRepository], Any]
    ) -> list[WorkspaceAppDTO]:
        return await self._execute_use_case(use_case, owner_id)
