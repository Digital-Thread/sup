from logging import warning
from typing import Optional

from sqlalchemy import delete, exists, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.domain.types_ids import OwnerId, RoleId, WorkspaceId
from src.apps.workspace.exceptions.role_exceptions import RoleNotFound
from src.apps.workspace.exceptions.workspace_exceptions import (
    WorkspaceCreatedException,
    WorkspaceNotFound,
    WorkspaceNotUpdated,
)
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository
from src.data_access.converters.role_converter import RoleConverter
from src.data_access.converters.workspace_converter import WorkspaceConverter
from src.data_access.models.stubs import UserModel
from src.data_access.models.workspace_models.role import RoleModel
from src.data_access.models.workspace_models.user_workspace_role import (
    UserWorkspaceRoleModel,
)
from src.data_access.models.workspace_models.workspace import WorkspaceModel


class WorkspaceRepository(IWorkspaceRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, workspace: Workspace) -> None:
        stmt = WorkspaceConverter.entity_to_model(workspace)
        self._session.add(stmt)
        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            raise WorkspaceCreatedException('Ошибка создания рабочего пространства')

    async def find_by_id(self, workspace_id: WorkspaceId) -> Optional[Workspace]:
        query: Optional[WorkspaceModel] = await self._session.get(WorkspaceModel, workspace_id)
        workspace = WorkspaceConverter.model_to_entity(query) if query else None
        return workspace

    async def find_by_owner_id(self, owner_id: OwnerId) -> list[Workspace]:
        query = select(WorkspaceModel).filter_by(owner_id=owner_id)
        result = await self._session.execute(query)
        workspaces = [
            WorkspaceConverter.model_to_entity(workspace) for workspace in result.scalars().all()
        ]
        return workspaces

    async def update(self, workspace: Workspace) -> None:
        update_data = WorkspaceConverter.entity_to_dict(workspace)

        stmt = (
            update(WorkspaceModel)
            .filter_by(workspace_id=workspace.id)
            .values(**update_data)
        )
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise WorkspaceNotUpdated('Рабочее пространство не обновлено')

    async def delete(self, workspace_id: WorkspaceId) -> None:
        stmt = delete(WorkspaceModel).filter_by(workspace_id=workspace_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise ValueError(f'Рабочее пространство с id = {workspace_id} не было удалено')

    async def assign_role_to_user(
        self, workspace_id: WorkspaceId, user_id: OwnerId, role_id: RoleId
    ) -> None:
        user_exists = await self._session.execute(select(exists().where(UserModel.id == user_id)))

        if not user_exists.scalar():
            pass
            # TODO выбросить not found user

        workspace_exists = await self._session.execute(
            select(exists().where(WorkspaceModel.id == workspace_id))
        )

        if not workspace_exists.scalar():
            raise WorkspaceNotFound('Рабочее пространство не найдено')

        role_exists = await self._session.execute(select(exists().where(RoleModel.id == role_id)))

        if not role_exists.scalar():
            raise RoleNotFound('Роль не найдена')

        user_role_exists = await self._session.execute(
            select(
                exists().where(
                    UserWorkspaceRoleModel.user_id == user_id,
                    UserWorkspaceRoleModel.workspace_id == workspace_id,
                )
            )
        )

        if user_role_exists.scalar():
            update_role = await self._session.execute(
                update(UserWorkspaceRoleModel)
                .filter_by(user_id=user_id, workspace_id=user_id)
                .values(role_id=role_id)
            )
        else:
            new_user_role = UserWorkspaceRoleModel(
                user_id=user_id, workspace_id=workspace_id, role_id=role_id
            )
            self._session.add(new_user_role)

        await self._session.commit()

    async def find_user_role_in_workspace(
        self, user_id: OwnerId, workspace_id: WorkspaceId
    ) -> Optional[Role]:
        query = (
            select(UserWorkspaceRoleModel)
            .options(joinedload(UserWorkspaceRoleModel.role))
            .filter_by(user_id=user_id, workspace_id=workspace_id)
        )
        result = await self._session.execute(query)
        user_workspace_role = result.scalars().first()
        role = (
            RoleConverter.model_to_entity(user_workspace_role.role) if user_workspace_role else None
        )
        return role
