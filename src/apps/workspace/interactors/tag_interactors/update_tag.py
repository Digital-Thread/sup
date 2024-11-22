from uuid import UUID

from src.apps.workspace.domain.entities.tag import TagEntity
from src.apps.workspace.domain.types_ids import TagId, WorkspaceId
from src.apps.workspace.dtos.tag_dtos import UpdateTagAppDTO
from src.apps.workspace.exceptions.tag_exceptions import (
    TagException,
    TagNotFound,
    TagNotUpdated,
)
from src.apps.workspace.mappers.tag_mapper import TagMapper
from src.apps.workspace.repositories.i_tag_repository import ITagRepository


class UpdateTagInteractor:
    def __init__(self, tag_repository: ITagRepository):
        self._tag_repository = tag_repository

    async def execute(self, tag_id: int, workspace_id: UUID, update_data: UpdateTagAppDTO) -> None:
        existing_tag = await self._get_existing_tag_in_workspace(
            TagId(tag_id), WorkspaceId(workspace_id)
        )
        updated_tag = self._map_to_update_data(existing_tag, update_data)
        try:
            await self._tag_repository.update(updated_tag)
        except TagNotUpdated as error:
            raise TagException(f'{str(error)}')

    async def _get_existing_tag_in_workspace(self, tag_id: TagId, workspace_id: WorkspaceId) -> TagEntity:
        try:
            existing_tag = await self._tag_repository.find_by_id(tag_id, workspace_id)
        except TagNotFound as error:
            raise TagException(f'{str(error)}')
        else:
            return existing_tag

    @staticmethod
    def _map_to_update_data(tag: TagEntity, update_data: UpdateTagAppDTO) -> TagEntity:
        try:
            updated_tag = TagMapper.update_data(tag, update_data)
        except ValueError as error:
            raise TagException(f'{str(error)}')
        else:
            return updated_tag
