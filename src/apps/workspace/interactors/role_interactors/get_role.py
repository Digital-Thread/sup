from uuid import UUID

from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.dtos.role_dtos import RoleOutDTO
from src.apps.workspace.exceptions.role_exceptions import RoleException, RoleNotFound
from src.apps.workspace.mappers.role_mapper import RoleMapper
from src.apps.workspace.repositories.role_repository import IRoleRepository


class GetRoleByIdInteractor:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, role_id: int, workspace_id: UUID) -> RoleOutDTO:
        try:
            role = await self._role_repository.get_by_id(RoleId(role_id), WorkspaceId(workspace_id))
        except RoleNotFound as error:
            raise RoleException(f'{str(error)}')
        else:
            return RoleMapper.entity_to_dto(role, RoleOutDTO)
