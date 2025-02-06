from collections import defaultdict
from typing import Sequence

from sqlalchemy.engine.row import Row

from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.data_access.models.workspace_models.role import RoleModel


class RoleMapper:
    @staticmethod
    def model_to_entity(role_model: RoleModel) -> RoleEntity:

        return RoleEntity(
            _id=RoleId(role_model.id),
            _name=role_model.name,
            _color=role_model.color,
            _workspace_id=WorkspaceId(role_model.workspace_id),
        )

    @staticmethod
    def entity_to_model(entity: RoleEntity) -> RoleModel:
        model = RoleModel(
            id=entity.id,
            name=entity.name,
            color=entity.color,
            workspace_id=entity.workspace_id,
        )
        return model

    @staticmethod
    def entity_to_dict(role: RoleEntity) -> dict[str, str | RoleId | WorkspaceId]:
        return {
            'id': role.id,
            'name': role.name,
            'color': role.color,
            'workspace_id': role.workspace_id,
        }

    @staticmethod
    def list_to_entity(
        roles: Sequence[RoleModel], members: Sequence[Row[tuple[int, str, str, str]]]
    ) -> list[tuple[RoleEntity, list[dict[str, str]] | None]]:
        role_member_map = defaultdict(list)

        for role_id, first_name, last_name, avatar in members:
            role_member_map[role_id].append(
                {'first_name': first_name, 'last_name': last_name, 'avatar': avatar}
            )

        roles_with_members = [
            (
                RoleEntity(
                    _id=RoleId(role.id),
                    _name=role.name,
                    _color=role.color,
                    _workspace_id=WorkspaceId(role.workspace_id),
                ),
                role_member_map.get(role.id, None),
            )
            for role in roles
        ]

        return roles_with_members
