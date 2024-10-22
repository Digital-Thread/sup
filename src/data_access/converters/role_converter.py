from src.apps.workspace.domain.entities.role import Role
from src.data_access.models.workspace_models.role import RoleModel


class RoleConverter[T]:
    @staticmethod
    def model_to_entity(role_model: T) -> Role:
        clean_data = {
            column.name: getattr(role_model, column.name) for column in role_model.__table__.columns
        }
        role = Role(
            _id=clean_data['id'],
            _name=clean_data['name'],
            _color=clean_data['color'],
            _workspace_id=clean_data['workspace_id'],
        )
        return role

    @staticmethod
    def entity_to_model(entity: Role) -> RoleModel:
        model = RoleModel(**entity.__dict__)
        return model
