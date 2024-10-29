from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.tag_dtos import TagAppDTO
from src.apps.workspace.exceptions.tag_exceptions import (
    TagException,
    WorkspaceTagNotFound,
)
from src.apps.workspace.mappers.tag_mapper import TagMapper
from src.apps.workspace.repositories.i_tag_repository import ITagRepository


class GetTagByWorkspaceUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, workspace_id: WorkspaceId) -> list[TagAppDTO]:
        try:
            tags = await self._tag_repository.find_by_workspace_id(workspace_id)
        except WorkspaceTagNotFound as error:
            raise TagException(f'{str(error)}')
        else:
            return [TagMapper.entity_to_dto(tag, TagAppDTO) for tag in tags]
