from logging import warning

from sqlalchemy import delete, exists, func, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.exceptions.role_exceptions import (
    RoleNotFound,
    RoleNotUpdated,
    WorkspaceRoleNotFound,
)
from src.apps.workspace.repositories.i_role_repository import IRoleRepository
from src.data_access.converters.role_converter import RoleConverter
from src.data_access.models import UserWorkspaceRoleModel
from src.data_access.models.workspace_models.role import RoleModel


class RoleRepository(IRoleRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, role: RoleEntity) -> None:
        stmt = RoleConverter.entity_to_model(role)
        self._session.add(stmt)

        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            raise WorkspaceRoleNotFound(
                f'Рабочего пространства с id={role.workspace_id} не существует'
            )

    async def find_by_id(self, role_id: RoleId, workspace_id: WorkspaceId) -> RoleEntity | None:
        query = select(RoleModel).filter_by(id=role_id, workspace_id=workspace_id)
        result = await self._session.execute(query)
        try:
            role_model = result.scalar_one()
        except NoResultFound as error:
            warning(error)
            raise RoleNotFound(f'Роль с id={role_id} не найдена')
        else:
            return RoleConverter.model_to_entity(role_model)

    async def find_by_workspace_id(self, workspace_id: WorkspaceId) -> list[tuple[RoleEntity, int]]:
        query = (
            select(RoleModel, func.count(UserWorkspaceRoleModel.user_id).label('user_count'))
            .outerjoin(UserWorkspaceRoleModel, RoleModel.id == UserWorkspaceRoleModel.role_id)
            .filter(RoleModel.workspace_id == workspace_id)
            .group_by(RoleModel.id)
        )

        result = await self._session.execute(query)
        roles_with_user_count = result.all()
        roles = RoleConverter.list_to_entity(roles_with_user_count)
        return roles

    async def update(self, role: RoleEntity) -> None:
        update_data = RoleConverter.entity_to_dict(role)
        stmt = update(RoleModel).filter_by(id=role.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise RoleNotUpdated(f'Роль с id={role.id} не обновлена')

    async def delete(self, role_id: RoleId, workspace_id: WorkspaceId) -> None:
        exists_role = await self._session.execute(
            select(exists().where(RoleModel.id == role_id, RoleModel.workspace_id == workspace_id))
        )

        if not exists_role.scalar():
            raise RoleNotFound(f'Роль с id={role_id} не найдена в рабочем пространстве')

        stmt = delete(RoleModel).filter_by(id=role_id, workspace_id=workspace_id)
        await self._session.execute(stmt)
