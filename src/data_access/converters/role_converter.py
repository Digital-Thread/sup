from typing import Any, Sequence

from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.dtos.role_dtos import RoleWithUserCountAppDTO
from src.data_access.models.workspace_models.role import RoleModel


class RoleConverter:
    @staticmethod
    def model_to_entity(role_model: RoleModel) -> Role:

        return Role(
            _id=RoleId(role_model.id),
            _name=role_model.name,
            _color=role_model.color,
            _workspace_id=WorkspaceId(role_model.workspace_id),
        )

    @staticmethod
    def entity_to_model(entity: Role) -> RoleModel:
        model = RoleModel(
            id=entity.id,
            name=entity.name,
            color=entity.color,
            workspace_id=entity.workspace_id,
        )
        return model

    @staticmethod
    def entity_to_dict(role: Role) -> dict[str, str | RoleId | WorkspaceId]:
        return {
            'id': role.id,
            'name': role.name,
            'color': role.color,
            'workspace_id': role.workspace_id,
        }

    @staticmethod
    def list_to_entity(roles_list: Sequence[Any]) -> list[tuple[Role, int]]:
        roles_with_user_count = []
        for role in roles_list:
            roles_with_user_count.append(
                (
                    Role(
                        _id=RoleId(role[0].id),
                        _name=role[0].name,
                        _color=role[0].color,
                        _workspace_id=WorkspaceId(role[0].workspace_id),
                    ),
                    role[1],
                )
            )

        return roles_with_user_count
