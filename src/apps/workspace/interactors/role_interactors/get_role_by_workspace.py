from uuid import UUID

from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.role_dtos import RoleWithMemberOutDTO
from src.apps.workspace.exceptions.role_exceptions import RoleException, RoleNotFound
from src.apps.workspace.mappers.role_mapper import RoleMapper
from src.apps.workspace.repositories.role_repository import IRoleRepository


class GetRolesByWorkspaceInteractor:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, workspace_id: UUID) -> list[RoleWithMemberOutDTO]:
        try:
            roles_with_members = await self._role_repository.get_by_workspace_id(
                workspace_id=WorkspaceId(workspace_id)
            )
        except RoleNotFound as error:
            raise RoleException(f'{str(error)}')
        else:
            return RoleMapper.list_tuple_to_dto(roles_with_members)
