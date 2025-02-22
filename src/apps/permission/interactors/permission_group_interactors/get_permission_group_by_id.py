from src.apps.permission.dtos import PermissionGroupOutputDTO
from src.apps.permission.domain import PermissionGroupId
from src.apps.permission.exceptions import PermissionGroupDoesNotExistError
from src.apps.permission.repositories.permission_group_repository import IPermissionGroupRepository


class GetPermissionGroupByIdInteractor:
    def __init__(self, permission_repository: IPermissionGroupRepository):
        self._repository = permission_repository

    async def execute(self, perm_group_id: PermissionGroupId) -> PermissionGroupOutputDTO:
        perm_group = await self._repository.get_perm_group_by_id(perm_group_id=perm_group_id)
        if not perm_group:
            raise PermissionGroupDoesNotExistError(perm_group_id)

        return perm_group
