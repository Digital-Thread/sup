from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.data_access.models.workspace_models.role import RoleModel


class RoleConverter:
    @staticmethod
    def model_to_entity(role_model: RoleModel) -> Role:

        return Role(
            _id=role_model.id,
            _name=role_model.name,
            _color=role_model.color,
            _workspace_id=WorkspaceId(role_model.workspace_id),
        )

    @staticmethod
    def entity_to_model(entity: Role) -> RoleModel:
        model = RoleModel(**entity.__dict__)
        return model

    @staticmethod
    def entity_to_dict(role: Role) -> dict:
        return {
            'id': role.id,
            'name': role.name,
            'color': role.color,
            'workspace_id': role.workspace_id,
        }