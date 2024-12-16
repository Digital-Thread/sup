from src.apps.workspace.dtos.tag_dtos import TagOutDTO
from src.apps.workspace.exceptions.tag_exceptions import (
    TagException,
    WorkspaceTagNotFound,
)
from src.apps.workspace.mappers.tag_mapper import TagMapper
from src.apps.workspace.repositories.tag_repository import ITagRepository


class GetTagByWorkspaceInteractor:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self) -> list[TagOutDTO]:
        try:
            tags = await self._tag_repository.get_by_workspace_id()
        except WorkspaceTagNotFound as error:
            raise TagException(f'{str(error)}')
        else:
            return [TagMapper.entity_to_dto(tag, TagOutDTO) for tag in tags]
