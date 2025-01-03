from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.apps.workspace.dtos.tag_dtos import TagAppDTO
from src.apps.workspace.exceptions.tag_exceptions import TagNotFound
from src.apps.workspace.mappers.tag_mapper import TagMapper
from src.apps.workspace.repositories.i_tag_repository import ITagRepository


class GetTagByIdUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, tag_id: TagId, workspace_id: WorkspaceId) -> TagAppDTO:
        try:
            tag = await self._tag_repository.find_by_id(tag_id, workspace_id)
        except TagNotFound:
            raise ValueError(f'Тег с id={tag_id} не найден')
        else:
            return TagMapper.entity_to_dto(tag, TagAppDTO)
