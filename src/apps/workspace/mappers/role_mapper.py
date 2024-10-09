from typing import Any

from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.dtos.role_dtos import RoleAppDTO, UpdateRoleAppDTO
from src.apps.workspace.mappers.base_mapper import BaseMapper


class RoleMapper(BaseMapper[Role, RoleAppDTO]):
    @staticmethod
    def dto_to_entity(dto: RoleAppDTO | UpdateRoleAppDTO, immutable_data: dict[str, Any]) -> Role:

        if isinstance(dto, RoleAppDTO):
            role = Role(
                _workspace_id=WorkspaceId(dto.workspace_id),
                _name=dto.name,
                _color=dto.color,
                _id=RoleId(dto.id),
            )
        else:
            role = Role(
                _workspace_id=WorkspaceId(immutable_data.get('workspace_id')),
                _id=RoleId(immutable_data.get('id')),
                _name=dto.get('name'),
                _color=dto.get('color'),
            )
        return role
