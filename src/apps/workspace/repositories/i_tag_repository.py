from abc import abstractmethod

from src.apps.workspace.domain.entities.tag import TagEntity
from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.apps.workspace.repositories.base_repository import IBaseRepository


class ITagRepository(IBaseRepository[TagEntity, TagId]):
    @abstractmethod
    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[TagEntity]:
        raise NotImplementedError
