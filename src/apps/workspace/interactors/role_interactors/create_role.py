from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.role_dtos import CreateRoleAppDTO
from src.apps.workspace.exceptions.role_exceptions import (
    RoleException,
    WorkspaceRoleNotFound,
)
from src.apps.workspace.repositories.role_repository import IRoleRepository


class CreateRoleInteractor:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, create_role_data: CreateRoleAppDTO) -> None:
        try:
            await self._role_repository.save(
                RoleEntity(
                    _name=create_role_data.name,
                    _color=create_role_data.color,
                    _workspace_id=WorkspaceId(create_role_data.workspace_id),
                )
            )
        except (ValueError, WorkspaceRoleNotFound) as error:
            raise RoleException(f'{str(error)}')
