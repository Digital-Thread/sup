from uuid import UUID

from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.exceptions.role_exceptions import RoleNotDeleted, RoleNotFound
from src.apps.workspace.repositories.role_repository import IRoleRepository


class DeleteRoleInteractor:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, role_id: int, workspace_id: UUID) -> None:
        try:
            await self._role_repository.delete(
                RoleId(role_id), workspace_id=WorkspaceId(workspace_id)
            )
        except RoleNotFound as error:
            if isinstance(error, RoleNotFound):
                raise

            raise RoleNotDeleted(f'Роль с id={role_id} не удалена')
