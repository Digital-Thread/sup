from uuid import UUID

from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.dtos.role_dtos import UpdateRoleAppDTO
from src.apps.workspace.exceptions.role_exceptions import (
    RoleException,
    RoleNotFound,
    RoleNotUpdated,
)
from src.apps.workspace.mappers.role_mapper import RoleMapper
from src.apps.workspace.repositories.i_role_repository import IRoleRepository


class UpdateRoleInteractor:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(
        self, role_id: int, workspace_id: UUID, update_data: UpdateRoleAppDTO
    ) -> None:
        existing_role = await self._get_existing_role_in_workspace(
            RoleId(role_id), WorkspaceId(workspace_id)
        )
        updated_role = self._map_to_update_data(existing_role, update_data)
        try:
            await self._role_repository.update(updated_role)
        except RoleNotUpdated as error:
            raise RoleException(f'{str(error)}')

    async def _get_existing_role_in_workspace(
        self, role_id: RoleId, workspace_id: WorkspaceId
    ) -> RoleEntity:
        try:
            existing_role = await self._role_repository.find_by_id(role_id, workspace_id)
        except RoleNotFound as error:
            raise RoleException(f'{str(error)}')
        else:
            return existing_role

    @staticmethod
    def _map_to_update_data(role: RoleEntity, update_data: UpdateRoleAppDTO) -> RoleEntity:
        try:
            updated_role = RoleMapper.update_data(role, update_data)
        except ValueError as error:
            raise RoleException(f'{str(error)}')
        else:
            return updated_role
