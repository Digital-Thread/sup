from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.exceptions.role_exceptions import RoleAlreadyExists
from src.apps.workspace.repositories.i_role_repository import IRoleRepository


class CreateRoleUseCase:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, role: Role) -> None:
        try:
            await self._role_repository.save(role)
        except RoleAlreadyExists:
            raise ValueError(f'Роль {role.name} уже существует')
