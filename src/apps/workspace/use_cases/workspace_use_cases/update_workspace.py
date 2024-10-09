from uuid import UUID

from src.apps.workspace.dtos.workspace_dtos import UpdateWorkspaceAppDTO
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository


class UpdateWorkspaceUseCase:
    def __init__(self, workspace_repository: IWorkspaceRepository):
        self.workspace_repository = workspace_repository

    async def execute(self, workspace_id: UUID, update_data: UpdateWorkspaceAppDTO) -> None:
        if any(field in update_data for field in ['name', 'description']):
            await self._update_with_validation(workspace_id, update_data)

        else:
            await self._update_without_validation(workspace_id, update_data)

    async def _update_with_validation(
        self, workspace_id: UUID, update_data: UpdateWorkspaceAppDTO
    ) -> None:
        """
        Используем метод с полной загрузкой объекта из БД, т.к. есть поля с валидацией
        """
        workspace = await self.workspace_repository.find_by_id(workspace_id)

        if update_data.get('name'):
            workspace.name = update_data['name']

        if update_data.get('description'):
            workspace.description = update_data['description']

        # Остальные поля обновляем напрямую, так как они не нуждаются в валидации
        for key, value in update_data.items():
            if key not in ['name', 'description']:
                setattr(workspace, key, value)

        await self.workspace_repository.update(workspace)

    async def _update_without_validation(
        self, workspace_id: UUID, update_data: UpdateWorkspaceAppDTO
    ) -> None:
        """Метод для частичного обновления, без загрузки объекта из БД"""
        await self.workspace_repository.update_partial(workspace_id, update_data)
