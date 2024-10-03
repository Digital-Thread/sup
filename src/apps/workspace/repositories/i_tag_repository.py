from abc import abstractmethod
from uuid import UUID

from src.apps.workspace.domain.entities.tag import Tag
from src.apps.workspace.repositories.base_repository import IBaseRepository


class ITagRepository(IBaseRepository[Tag, int]):
    @abstractmethod
    async def find_by_workspace_id(self, workspace_id: UUID) -> list[Tag]:
        raise NotImplementedError
