from dataclasses import asdict

from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.domain.types_ids import RoleId
from src.apps.workspace.dtos.role_dtos import RoleWithUserCountAppDTO, UpdateRoleAppDTO
from src.apps.workspace.mappers.base_mapper import BaseMapper


class RoleMapper(BaseMapper[RoleEntity, RoleWithUserCountAppDTO]):

    @staticmethod
    def update_data(existing_role: RoleEntity, dto: UpdateRoleAppDTO) -> RoleEntity:
        for field, value in asdict(dto).items():
            if value is not None:
                setattr(existing_role, field, value)

        return existing_role

    @staticmethod
    def list_tuple_to_dto(roles: list[tuple[RoleEntity, int]]) -> list[RoleWithUserCountAppDTO]:
        roles_with_user_count = []
        for role in roles:
            roles_with_user_count.append(
                RoleWithUserCountAppDTO(
                    id=RoleId(role[0].id),
                    name=role[0].name,
                    color=role[0].color,
                    user_count=role[1],
                )
            )
        return roles_with_user_count
