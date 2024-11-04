from uuid import UUID

from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.apps.workspace.exceptions.tag_exceptions import (
    TagException,
    TagNotFound,
    WorkspaceTagNotFound,
)
from src.apps.workspace.repositories.i_tag_repository import ITagRepository


class DeleteTagUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, tag_id: int, workspace_id: UUID) -> None:
        try:
            await self._tag_repository.delete(TagId(tag_id), WorkspaceId(workspace_id))
        except (TagNotFound, WorkspaceTagNotFound) as error:
            raise TagException(f'{str(error)}')
