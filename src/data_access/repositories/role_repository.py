from logging import warning

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.exceptions.role_exceptions import (
    RoleNotFound,
    RoleNotUpdated,
    WorkspaceRoleNotFound,
)
from src.apps.workspace.repositories.role_repository import IRoleRepository
from src.data_access.mappers.role_mapper import RoleMapper
from src.data_access.models import UserModel, UserWorkspaceRoleModel
from src.data_access.models.workspace_models.role import RoleModel


class RoleRepository(IRoleRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def save(self, role: RoleEntity) -> None:
        stmt = RoleMapper.entity_to_model(role)
        self._session.add(stmt)

        try:
            await self._session.flush()
        except IntegrityError as error:
            warning(error)
            raise WorkspaceRoleNotFound(
                f'Рабочего пространства с id={role.workspace_id} не существует'
            )

    async def get_by_id(self, role_id: RoleId, workspace_id: WorkspaceId) -> RoleEntity | None:
        query = select(RoleModel).filter_by(id=role_id, workspace_id=workspace_id)
        result = await self._session.execute(query)
        try:
            role_model = result.scalar_one()
        except NoResultFound as error:
            warning(error)
            raise RoleNotFound(f'Роль с id={role_id} не найдена')
        else:
            return RoleMapper.model_to_entity(role_model)

    async def get_by_workspace_id(
        self, workspace_id: WorkspaceId
    ) -> list[tuple[RoleEntity, list[dict[str, str]] | None]]:
        query = (
            select(RoleModel, UserModel.first_name, UserModel.last_name, UserModel.avatar)
            .outerjoin(UserWorkspaceRoleModel, RoleModel.id == UserWorkspaceRoleModel.role_id)
            .outerjoin(UserModel, UserWorkspaceRoleModel.user_id == UserModel.id)
            .filter(RoleModel.workspace_id == workspace_id)
        )
        result = await self._session.execute(query)
        roles_with_members = RoleMapper.list_to_entity(result.all())
        return roles_with_members

    async def update(self, role: RoleEntity) -> None:
        update_data = RoleMapper.entity_to_dict(role)
        stmt = update(RoleModel).filter_by(id=role.id).values(**update_data)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise RoleNotUpdated(f'Роль с id={role.id} не обновлена')

    async def delete(self, role_id: RoleId, workspace_id: WorkspaceId) -> None:
        stmt = delete(RoleModel).filter_by(id=role_id, workspace_id=workspace_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise RoleNotFound(f'Роль с id={role_id} не найдена в рабочем пространстве')
