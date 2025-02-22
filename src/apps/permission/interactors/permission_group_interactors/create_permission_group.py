from src.apps.permission.exceptions import PermissionGroupCreateError, PermissionGroupRepositoryError
from src.apps.permission.permission_group_mapper import PermissionGroupMapper
from src.apps.permission.dtos import PermissionGroupInputDTO
from src.apps.permission.repositories.permission_group_repository import IPermissionGroupRepository


class CreatePermissionGroupInteractor:
    def __init__(self, permission_repository: IPermissionGroupRepository):
        self._repository = permission_repository

    async def execute(self, dto: PermissionGroupInputDTO) -> None:
        try:
            perm_group = PermissionGroupMapper.dto_to_entity(dto=dto)
        except (ValueError, AttributeError) as e:
            raise PermissionGroupCreateError(context=e) from None

        # TODO: Добавить проверку, что пользователи из authorized_users - входят в member-ы рабочей области

        try:
            await self._repository.save(perm_group=perm_group)
        except PermissionGroupRepositoryError as e:
            raise PermissionGroupCreateError(context=e) from None
