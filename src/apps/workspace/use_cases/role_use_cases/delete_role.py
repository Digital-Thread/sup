from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.exceptions.role_exceptions import (
    RoleException,
    RoleNotFound,
    WorkspaceRoleNotFound,
)
from src.apps.workspace.repositories.i_role_repository import IRoleRepository


class DeleteRoleUseCase:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, role_id: RoleId, workspace_id: WorkspaceId) -> None:
        try:
            await self._role_repository.delete(role_id, workspace_id)
        except (RoleNotFound, WorkspaceRoleNotFound) as error:
            raise RoleException(f'{str(error)}')
