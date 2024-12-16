from src.apps.workspace.domain.types_ids import TagId
from src.apps.workspace.exceptions.tag_exceptions import (
    TagException,
    TagNotFound,
    WorkspaceTagNotFound,
)
from src.apps.workspace.repositories.tag_repository import ITagRepository


class DeleteTagInteractor:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, tag_id: int) -> None:
        try:
            await self._tag_repository.delete(TagId(tag_id))
        except (TagNotFound, WorkspaceTagNotFound) as error:
            raise TagException(f'{str(error)}')
