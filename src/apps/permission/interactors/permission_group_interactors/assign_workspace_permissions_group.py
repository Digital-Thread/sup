from src.apps.permission.exceptions import PermissionGroupDoesNotExistError
from src.apps.permission.domain import WorkspaceId, UserId
from src.apps.permission.repositories.permission_group_repository import IPermissionGroupRepository


class AssignWorkspacePermissionsGroupInteractor:
    def __init__(self, permission_repository: IPermissionGroupRepository):
        self._repository = permission_repository
        self.permission_group_name = 'Workspace_owner'

    async def execute(self, workspace_id: WorkspaceId, owner_id: UserId) -> None:
        try:
            await self._repository.assign_permission_group(
                user_id=owner_id,
                group_name=self.permission_group_name,
                workspace_id=workspace_id,
            )
        except PermissionGroupDoesNotExistError as e:
            raise
