from src.apps.permission.exceptions import (
    PermissionGroupDoesNotExistError,
    PermissionGroupUpdateError,
    PermissionGroupRepositoryError,
)
from src.apps.permission.dtos import PermissionGroupUpdateDTO
from src.apps.permission.repositories.permission_group_repository import IPermissionGroupRepository


class UpdatePermissionGroupInteractor:
    def __init__(self, permission_repository: IPermissionGroupRepository):
        self._repository = permission_repository

    async def execute(self, dto: PermissionGroupUpdateDTO) -> None:
        perm_group = await self._repository.get_perm_group_entity(perm_group_id=dto.id)
        if not perm_group:
            raise PermissionGroupDoesNotExistError(dto.id)

        try:
            perm_group.update_fields(dto.updated_fields)
        except ValueError as e:
            raise PermissionGroupUpdateError(context=e) from None

        # TODO: Добавить проверку для authorized_users

        try:
            await self._repository.update(perm_group=perm_group)
        except PermissionGroupRepositoryError as e:
            raise PermissionGroupUpdateError(context=e) from None
