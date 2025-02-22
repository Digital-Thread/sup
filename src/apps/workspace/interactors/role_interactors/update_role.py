from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.dtos.role_dtos import UpdateRoleAppDTO
from src.apps.workspace.exceptions.role_exceptions import RoleException, RoleNotFound
from src.apps.workspace.mappers.role_mapper import RoleMapper
from src.apps.workspace.repositories.role_repository import IRoleRepository
from tests.fixtures.workspace_fixtures import workspace_id


class UpdateRoleInteractor:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, updated_role_data: UpdateRoleAppDTO) -> None:
        existing_role = await self._get_existing_role_in_workspace(
            role_id=RoleId(updated_role_data.id),
            workspace_id=WorkspaceId(updated_role_data.workspace_id),
        )
        updated_role = self._map_to_update_data(existing_role, updated_role_data)

        await self._role_repository.update(updated_role)

    async def _get_existing_role_in_workspace(
        self, role_id: RoleId, workspace_id: WorkspaceId
    ) -> RoleEntity:
        existing_role = await self._role_repository.get_by_id(role_id, workspace_id)

        if not existing_role:
            raise RoleNotFound(
                f'Роль с id={role_id} в рабочем пространстве с id={workspace_id} не найдена.'
            )

        return existing_role

    @staticmethod
    def _map_to_update_data(role: RoleEntity, update_data: UpdateRoleAppDTO) -> RoleEntity:
        try:
            updated_role = RoleMapper.update_data(role, update_data)
        except ValueError as error:
            raise RoleException(f'{str(error)}')
        else:
            return updated_role
