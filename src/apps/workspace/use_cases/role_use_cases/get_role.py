from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.dtos.role_dtos import RoleAppDTO
from src.apps.workspace.exceptions.role_exceptions import RoleNotFound
from src.apps.workspace.repositories.i_role_repository import IRoleRepository


class GetRoleByIdUseCase:
    def __init__(self, role_repository: IRoleRepository):
        self._role_repository = role_repository

    async def execute(self, role_id: int) -> RoleAppDTO:
        try:
            role = await self._role_repository.find_by_id(role_id)
        except RoleNotFound:
            raise ValueError(f'Роль с id={role_id} не найдена')
        else:
            return RoleAppDTO.from_entity(role)
