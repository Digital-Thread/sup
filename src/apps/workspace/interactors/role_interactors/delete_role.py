from uuid import UUID

from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.exceptions.role_exceptions import (
    RoleException,
    RoleNotFound,
    WorkspaceRoleNotFound,
)
from src.apps.workspace.repositories.role_repository import IRoleRepository


class DeleteRoleInteractor:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, role_id: int, workspace_id: UUID) -> None:
        try:
            await self._role_repository.delete(
                RoleId(role_id), workspace_id=WorkspaceId(workspace_id)
            )
        except (RoleNotFound, WorkspaceRoleNotFound) as error:
            raise RoleException(f'{str(error)}')
