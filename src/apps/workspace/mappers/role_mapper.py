from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.dtos.role_dtos import RoleAppDTO, UpdateRoleAppDTO
from src.apps.workspace.mappers.base_mapper import BaseMapper


class RoleMapper(BaseMapper[Role, RoleAppDTO]):

    @staticmethod
    def dto_to_entity(dto: RoleAppDTO) -> Role:

        return Role(
            _workspace_id=WorkspaceId(dto.workspace_id),
            _name=dto.name,
            _color=dto.color,
            _id=RoleId(dto.id),
        )

    @staticmethod
    def update_data(existing_role: Role, dto: UpdateRoleAppDTO) -> Role:
        existing_role.name = dto.get('name')
        existing_role.color = dto.get('color')

        return existing_role
