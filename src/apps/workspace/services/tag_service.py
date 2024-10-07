from typing import Callable, Any
from uuid import UUID

from src.apps.workspace.domain.entities.tag import Tag
from src.apps.workspace.repositories.i_tag_repository import ITagRepository
from src.apps.workspace.services.base_service import BaseService


class TagService(BaseService[Tag, int, ITagRepository]):
    async def retrieve_by_workspace_id(
        self, workspace_id: UUID, use_case: Callable[[ITagRepository], Any]
    ) -> list[Tag]:
        return await self.retrieve_by_workspace_id(workspace_id, use_case)