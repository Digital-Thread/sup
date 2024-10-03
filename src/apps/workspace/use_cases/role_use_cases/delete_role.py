from src.apps.workspace.exceptions.role_exceptions import RoleNotFound
from src.apps.workspace.repositories.i_role_repository import IRoleRepository


class DeleteRoleUseCase:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, role_id: int) -> None:
        try:
            await self._role_repository.delete(role_id)
        except RoleNotFound:
            ValueError(f'Роли с id={role_id} не существует')
