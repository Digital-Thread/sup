from logging import warning
from typing import Optional
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.exceptions.role_exceptions import (
    RoleCreatedException,
    RoleNotDeleted,
    RoleNotUpdated,
)
from src.apps.workspace.repositories.i_role_repository import IRoleRepository
from src.data_access.converters.role_converter import RoleConverter
from src.data_access.models.workspace_models.role import RoleModel


class RoleRepository(IRoleRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, role: Role) -> None:
        stmt = RoleConverter.entity_to_model(role)
        self._session.add(stmt)

        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            raise RoleCreatedException

    async def find_by_id(self, role_id: RoleId) -> Optional[Role]:
        query: Optional[RoleModel] = await self._session.get(RoleModel, role_id)
        role = RoleConverter.model_to_entity(query) if query else None
        return role

    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[Role]:
        query = select(RoleModel).filter_by(workspace_id=workspace_id)
        result = await self._session.execute(query)
        roles = [RoleConverter.model_to_entity(role) for role in result.scalars().all()]
        return roles

    async def update(self, role: Role) -> None:
        update_data = RoleConverter.entity_to_dict(role)
        stmt = update(RoleModel).filter_by(id=role.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise RoleNotUpdated(f'Роль с id={role.id} не обновлена')

    async def delete(self, role_id: RoleId) -> None:
        stmt = delete(RoleModel).filter_by(id=role_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise RoleNotDeleted(f'Роль с id={role_id} не удалена')
