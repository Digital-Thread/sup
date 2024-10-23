from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.role_dtos import RoleAppDTO
from src.apps.workspace.exceptions.role_exceptions import WorkspaceRoleNotFound
from src.apps.workspace.mappers.role_mapper import RoleMapper
from src.apps.workspace.repositories.i_role_repository import IRoleRepository


class GetRoleByWorkspaceUseCase:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, workspace_id: WorkspaceId) -> list[RoleAppDTO]:
        try:
            roles = await self._role_repository.find_by_workspace_id(workspace_id)
        except WorkspaceRoleNotFound:
            raise ValueError(f'Рабочее пространство роли с id={workspace_id} не найдено')
        else:
            return [RoleMapper.entity_to_dto(role, RoleAppDTO) for role in roles]
