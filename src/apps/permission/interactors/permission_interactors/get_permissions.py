from src.apps.permission.repositories.permission_repository import IPermissionRepository
from src.apps.permission.dtos import PermissionOutputDTO


class GetPermissionsInteractor:
    def __init__(self, permission_repository: IPermissionRepository):
        self._repository = permission_repository

    async def execute(self) -> list[PermissionOutputDTO]:
        permissions = await self._repository.get_permissions(exclude_hidden=True)
        return permissions
