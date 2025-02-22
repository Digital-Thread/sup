from src.apps.permission.domain import PermissionGroupId
from src.apps.permission.exceptions import PermissionGroupDoesNotExistError, PermissionGroupDeleteError
from src.apps.permission.repositories.permission_group_repository import IPermissionGroupRepository


class DeletePermissionGroupInteractor:
    def __init__(self, permission_repository: IPermissionGroupRepository):
        self._repository = permission_repository

    async def execute(self, perm_group_id: PermissionGroupId) -> None:
        try:
            await self._repository.delete(perm_group_id=perm_group_id)
        except PermissionGroupDoesNotExistError as e:
            raise PermissionGroupDeleteError(context=e) from None
