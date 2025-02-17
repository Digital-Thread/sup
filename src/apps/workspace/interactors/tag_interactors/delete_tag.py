from uuid import UUID

from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.apps.workspace.exceptions.tag_exceptions import TagNotDeleted, TagNotFound
from src.apps.workspace.repositories.tag_repository import ITagRepository


class DeleteTagInteractor:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, tag_id: int, workspace_id: UUID) -> None:
        try:
            await self._tag_repository.delete(TagId(tag_id), workspace_id=WorkspaceId(workspace_id))
        except TagNotFound as error:
            if isinstance(error, TagNotFound):
                raise

            raise TagNotDeleted(f'Тег с id={tag_id} не удален')
