from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.role_dtos import RoleWithUserCountAppDTO, GetRolesAppDTO
from src.apps.workspace.exceptions.role_exceptions import RoleException, RoleNotFound
from src.apps.workspace.mappers.role_mapper import RoleMapper
from src.apps.workspace.repositories.role_repository import IRoleRepository


class GetRoleByWorkspaceInteractor:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, request_data: GetRolesAppDTO) -> list[RoleWithUserCountAppDTO]:
        try:
            roles = await self._role_repository.find_by_workspace_id(WorkspaceId(request_data.workspace_id))
        except RoleNotFound as error:
            raise RoleException(f'{str(error)}')
        else:
            return RoleMapper.list_tuple_to_dto(roles)
