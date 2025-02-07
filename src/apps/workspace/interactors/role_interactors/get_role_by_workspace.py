from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.role_dtos import GetRolesDTO, RoleWithMemberOutDTO
from src.apps.workspace.mappers.role_mapper import RoleMapper
from src.apps.workspace.repositories.role_repository import IRoleRepository


class GetRolesByWorkspaceInteractor:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, request_data: GetRolesDTO) -> list[RoleWithMemberOutDTO]:
        roles_with_members = await self._role_repository.get_by_workspace_id(
            workspace_id=WorkspaceId(request_data.workspace_id),
            page=request_data.page,
            page_size=request_data.page_size,
        )
        return RoleMapper.list_tuple_to_dto(roles_with_members)
