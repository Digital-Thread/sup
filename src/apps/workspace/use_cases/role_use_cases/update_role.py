from src.apps.workspace.repositories.i_role_repository import IRoleRepository


class UpdateRoleUseCase:
    def __init__(self, role_repository: IRoleRepository):
        self.role_repository = role_repository

    async def execute(self, role_id: int, update_data: dict[str, str]) -> None:
        """
        Используем метод с полной загрузкой объекта из БД, т.к. есть поля с валидацией
        """
        role = await self.role_repository.find_by_id(role_id)

        if update_data.get('name'):
            role.name = update_data['name']

        if update_data.get('color'):
            role.color = update_data['color']

        await self.role_repository.update(role, update_data)
