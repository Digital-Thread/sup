from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.dtos.role_dtos import RoleAppDTO, UpdateRoleAppDTO
from src.apps.workspace.exceptions.role_exceptions import RoleNotUpdated
from src.apps.workspace.mappers.role_mapper import RoleMapper
from src.apps.workspace.repositories.i_role_repository import IRoleRepository


class UpdateRoleUseCase:
    def __init__(self, role_repository: IRoleRepository):
        self.role_repository = role_repository

    async def execute(
        self, workspace_id: WorkspaceId, role_id: RoleId, update_data: UpdateRoleAppDTO
    ) -> None:
        role = RoleMapper.dto_to_entity(
            update_data, {'workspace_id': workspace_id, 'role_id': role_id}
        )
        try:
            await self.role_repository.update(role)
        except RoleNotUpdated:
            pass
            # TODO пробросить дальше
