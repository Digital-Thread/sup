from uuid import UUID

from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.dtos.role_dtos import RoleOutDTO
from src.apps.workspace.exceptions.role_exceptions import RoleNotFound
from src.apps.workspace.mappers.role_mapper import RoleMapper
from src.apps.workspace.repositories.role_repository import IRoleRepository


class GetRoleByIdInteractor:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, role_id: int, workspace_id: UUID) -> RoleOutDTO:
        role_entity = await self._role_repository.get_by_id(RoleId(role_id), WorkspaceId(workspace_id))

        try:
            role_out_dto = RoleMapper.entity_to_dto(role_entity)
        except AttributeError as error:
            raise RoleNotFound(f'Роль с id={role_id} не найдена') from error

        return role_out_dto