from datetime import datetime

from src.apps.workspace.domain.types_ids import OwnerId, WorkspaceId
from src.apps.workspace.dtos.workspace_dtos import (
    UpdateWorkspaceAppDTO,
    WorkspaceAppDTO,
)
from src.apps.workspace.exceptions.workspace_exceptions import (
    WorkspaceNotFound,
    WorkspaceNotUpdated,
)
from src.apps.workspace.mappers.workspace_mapper import WorkspaceMapper
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository

# class UpdateWorkspaceUseCase:
#     def __init__(self, workspace_repository: IWorkspaceRepository):
#         self.workspace_repository = workspace_repository
#
#     async def execute(
#         self,
#         owner_id: OwnerId,
#         workspace_id: WorkspaceId,
#         created_at: datetime,
#         update_data: UpdateWorkspaceAppDTO,
#     ) -> None:
#         workspace = WorkspaceMapper.dto_to_entity(
#             update_data,
#             {'owner_id': owner_id, 'workspace_id': workspace_id, 'created_at': created_at},
#         )
#         try:
#             await self.workspace_repository.update(workspace)
#         except WorkspaceNotUpdated:
#             pass
#             # TODO пробросить дальше


class UpdateWorkspaceUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self.workspace_repository = workspace_repository

    async def execute(self, workspace_id: WorkspaceId, updated_data: UpdateWorkspaceAppDTO) -> None:
        try:
            existing_workspace = await self.workspace_repository.find_by_id(workspace_id)
        except WorkspaceNotFound:
            pass
            # TODO пробросить дальше
        else:
            updated_workspace = WorkspaceMapper.update_data(updated_data, existing_workspace)

            try:
                await self.workspace_repository.update(updated_workspace)
            except WorkspaceNotUpdated:
                pass
                # TODO пробросить дальше
