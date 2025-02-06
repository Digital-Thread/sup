from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.tag_dtos import TagOutDTO, GetTagsDTO
from src.apps.workspace.mappers.tag_mapper import TagMapper
from src.apps.workspace.repositories.tag_repository import ITagRepository


class GetTagByWorkspaceInteractor:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, request_data: GetTagsDTO) -> list[TagOutDTO]:
        tags = await self._tag_repository.get_by_workspace_id(
            workspace_id=WorkspaceId(request_data.workspace_id),
            page=request_data.page,
            page_size=request_data.page_size
        )
        return [TagMapper.entity_to_dto(tag) for tag in tags]
