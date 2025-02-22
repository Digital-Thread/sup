from src.apps.permission.domain import WorkspaceId
from src.apps.permission.dtos import PermissionGroupOutputDTO
from src.apps.permission.repositories.permission_group_repository import IPermissionGroupRepository


class GetPermissionGroupsByWorkspaceIdInteractor:
    def __init__(self, permission_repository: IPermissionGroupRepository):
        self._repository = permission_repository

    async def execute(self, workspace_id: WorkspaceId) -> list[PermissionGroupOutputDTO]:
        perm_groups = await self._repository.get_perm_groups_by_workspace_id(workspace_id=workspace_id)
        return perm_groups
