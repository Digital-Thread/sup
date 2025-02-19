from dataclasses import asdict

from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.dtos.role_dtos import (
    MemberOutDTO,
    RoleOutDTO,
    RoleWithMemberOutDTO,
    UpdateRoleAppDTO,
)


class RoleMapper:

    @staticmethod
    def entity_to_dto(role: RoleEntity) -> RoleOutDTO:
        return RoleOutDTO(
            id=role.id,
            name=role.name,
            color=role.color,
        )

    @staticmethod
    def update_data(existing_role: RoleEntity, dto: UpdateRoleAppDTO) -> RoleEntity:
        for field, value in asdict(dto).items():
            if value is not None and field in ['name', 'color']:
                setattr(existing_role, field, value)

        return existing_role

    @staticmethod
    def list_tuple_to_dto(
        roles_with_members: list[tuple[RoleEntity, list[dict[str, str]] | None]]
    ) -> list[RoleWithMemberOutDTO]:
        role_with_members_dtos = []

        for role, members in roles_with_members:
            role_with_members_dtos.append(
                RoleWithMemberOutDTO(
                    id=role.id,
                    name=role.name,
                    color=role.color,
                    members=(
                        [
                            MemberOutDTO(
                                first_name=member.get('first_name'),
                                last_name=member.get('last_name'),
                                avatar=member.get('avatar'),
                            )
                            for member in members
                        ]
                        if members
                        else None
                    ),
                )
            )

        return role_with_members_dtos
