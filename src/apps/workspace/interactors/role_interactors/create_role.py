from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.domain.types_ids import WorkspaceId
from src.apps.workspace.dtos.role_dtos import CreateRoleAppDTO
from src.apps.workspace.exceptions.role_exceptions import (
    RoleException,
    WorkspaceRoleNotFound,
)
from src.apps.workspace.repositories.i_role_repository import IRoleRepository


class CreateRoleInteractor:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, role_data: CreateRoleAppDTO) -> None:

        try:
            await self._role_repository.save(
                RoleEntity(
                    _workspace_id=WorkspaceId(role_data.workspace_id),
                    _name=role_data.name,
                    _color=role_data.color,
                )
            )
        except (ValueError, WorkspaceRoleNotFound) as error:
            raise RoleException(f'{str(error)}')
