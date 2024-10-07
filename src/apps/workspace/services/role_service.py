from typing import Callable, Any
from uuid import UUID

from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.repositories.i_role_repository import IRoleRepository
from src.apps.workspace.services.base_service import BaseService


class RoleService(BaseService[Role, int, IRoleRepository]):
    async def retrieve_by_workspace_id(
        self, workspace_id: UUID, use_case: Callable[[IRoleRepository], Any]
    ) -> list[Role]:
        return await self.retrieve_by_workspace_id(workspace_id, use_case)