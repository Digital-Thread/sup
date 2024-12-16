from uuid import UUID

from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.apps.workspace.dtos.tag_dtos import TagOutDTO
from src.apps.workspace.exceptions.tag_exceptions import TagNotFound, TagException
from src.apps.workspace.mappers.tag_mapper import TagMapper
from src.apps.workspace.repositories.tag_repository import ITagRepository


class GetTagByIdInteractor:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, tag_id: int, workspace_id: UUID) -> TagOutDTO:
        try:
            tag = await self._tag_repository.get_by_id(TagId(tag_id), WorkspaceId(workspace_id))
        except TagNotFound:
            raise TagException(f'Тег с id={tag_id} не найден')
        else:
            return TagMapper.entity_to_dto(tag, TagOutDTO)
