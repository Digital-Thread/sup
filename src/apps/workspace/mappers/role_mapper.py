from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.dtos.role_dtos import RoleAppDTO, UpdateRoleAppDTO
from src.apps.workspace.mappers.base_mapper import BaseMapper


class RoleMapper(BaseMapper[Role, RoleAppDTO]):
    ATTRIBUTE_MAP = {'name': '_name', 'color': '_color'}

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

        for key, value in dto.items():
            attr_name = RoleMapper.ATTRIBUTE_MAP.get(key, key)
            setattr(existing_role, attr_name, value)

        return existing_role
