from src.apps.workspace.domain.types_ids import RoleId
from src.apps.workspace.dtos.role_dtos import UpdateRoleAppDTO
from src.apps.workspace.exceptions.role_exceptions import RoleNotFound, RoleNotUpdated
from src.apps.workspace.mappers.role_mapper import RoleMapper
from src.apps.workspace.repositories.i_role_repository import IRoleRepository


class UpdateRoleUseCase:
    def __init__(self, role_repository: IRoleRepository):
        self.role_repository = role_repository

    async def execute(self, role_id: RoleId, update_data: UpdateRoleAppDTO) -> None:
        try:
            existing_role = await self.role_repository.find_by_id(role_id)
        except RoleNotFound:
            pass
            # TODO пробросить дальше
        else:
            updated_role = RoleMapper.update_data(existing_role, update_data)

            try:
                await self.role_repository.update(updated_role)
            except RoleNotUpdated:
                pass
                # TODO пробросить дальше
