from src.apps.permission import PermissionGroupOutputDTO
from src.apps.permission.domain import (
    PermissionGroupEntity,
    PermissionId,
    WorkspaceId,
    UserId,
    PermissionGroupId,
)
from src.data_access.models import PermissionGroupModel


class PermissionGroupMapper:
    @staticmethod
    def model_to_entity(model: PermissionGroupModel) -> PermissionGroupEntity:
        entity = PermissionGroupEntity(
            name=model.name,
            permissions={PermissionId(perm.id) for perm in model.permissions},
            is_global=model.is_global,
            workspace_id=WorkspaceId(model.workspace_id) if model.workspace_id else None,
            description=model.description,
            authorized_users={UserId(user.id) for user in model.authorized_users}
        )
        entity.id = PermissionGroupId(model.id)
        return entity

    @staticmethod
    def entity_to_model(entity: PermissionGroupEntity) -> PermissionGroupModel:
        return PermissionGroupModel(
            id=entity.id if entity.id is not None else None,
            name=entity.name,
            is_global=entity.is_global,
            workspace_id=entity.workspace_id if entity.workspace_id else None,
            description=entity.description,
        )

    @staticmethod
    def model_to_dto(model: PermissionGroupModel) -> PermissionGroupOutputDTO:
        return PermissionGroupOutputDTO(
            id=PermissionGroupId(model.id),
            name=model.name,
            description=model.description,
            permissions={PermissionId(perm.id) for perm in model.permissions},
            authorized_users={UserId(user.id) for user in model.authorized_users},
        )
