from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.dtos.tag_dtos import TagAppDTO, UpdateTagAppDTO
from src.apps.workspace.exceptions.tag_exceptions import TagNotUpdated
from src.apps.workspace.mappers.tag_mapper import TagMapper
from src.apps.workspace.repositories.i_tag_repository import ITagRepository


class UpdateTagUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self.tag_repository = tag_repository

    async def execute(
        self, workspace_id: WorkspaceId, role_id: RoleId, update_data: UpdateTagAppDTO
    ) -> None:
        tag = TagMapper.dto_to_entity(
            update_data, {'workspace_id': workspace_id, 'role_id': role_id}
        )
        try:
            await self.tag_repository.update(tag)
        except TagNotUpdated:
            pass
            # TODO пробросить дальше
