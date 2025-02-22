from src.apps.permission.dtos import PermissionGroupInputDTO
from src.apps.permission.domain import PermissionGroupEntity


class PermissionGroupMapper:
    @staticmethod
    def dto_to_entity(dto: PermissionGroupInputDTO) -> PermissionGroupEntity:
        return PermissionGroupEntity(
            workspace_id=dto.workspace_id,
            name=dto.name,
            description=dto.description,
            permissions=dto.permissions,
            authorized_users=dto.authorized_users,
        )
