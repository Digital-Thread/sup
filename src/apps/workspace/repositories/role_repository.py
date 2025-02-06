from abc import abstractmethod

from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.repositories.base_repository import IBaseRepository


class IRoleRepository(IBaseRepository[RoleEntity, RoleId]):
    @abstractmethod
    async def get_by_workspace_id(
        self, workspace_id: WorkspaceId, page: int, page_size:int
    ) -> list[tuple[RoleEntity, list[dict[str, str]] | None]]:
        raise NotImplementedError
