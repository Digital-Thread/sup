from uuid import UUID

from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.tag_dtos import TagOutDTO
from src.apps.workspace.mappers.tag_mapper import TagMapper
from src.apps.workspace.repositories.tag_repository import ITagRepository


class GetTagByWorkspaceInteractor:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, workspace_id: UUID) -> list[TagOutDTO]:
        tags = await self._tag_repository.get_by_workspace_id(
            workspace_id=WorkspaceId(workspace_id)
        )
        return [TagMapper.entity_to_dto(tag) for tag in tags]
