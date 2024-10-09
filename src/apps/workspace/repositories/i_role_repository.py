from abc import abstractmethod
from uuid import UUID

from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.repositories.base_repository import IBaseRepository


class IRoleRepository(IBaseRepository[Role, RoleId]):
    @abstractmethod
    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[Role]:
        raise NotImplementedError
