from abc import abstractmethod
from uuid import UUID

from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.repositories.base_repository import IBaseRepository


class IWorkspaceRepository(IBaseRepository[Workspace, UUID]):
    @abstractmethod
    async def find_by_owner_id(self, owner_id: UUID) -> list[Workspace]:
        raise NotImplementedError
