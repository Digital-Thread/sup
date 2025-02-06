from logging import warning

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.entities.role import RoleEntity
from src.apps.workspace.domain.types_ids import RoleId, WorkspaceId
from src.apps.workspace.exceptions.role_exceptions import (
    RoleNotFound,
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
        role_model = result.scalar_one_or_none()
        return RoleMapper.model_to_entity(role_model) if role_model else None

    async def get_by_workspace_id(
        self, workspace_id: WorkspaceId, page:int, page_size:int
    ) -> list[tuple[RoleEntity, list[dict[str, str]] | None]]:
        roles_query = (
            select(RoleModel)
            .filter(RoleModel.workspace_id == workspace_id)
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        roles_result = await self._session.execute(roles_query)
        roles = roles_result.scalars().all()

        if not roles:
            return []

        role_ids = [role.id for role in roles]

        members_query = (
            select(UserWorkspaceRoleModel.role_id, UserModel.first_name, UserModel.last_name, UserModel.avatar)
            .join(UserModel, UserWorkspaceRoleModel.user_id == UserModel.id)
            .filter(UserWorkspaceRoleModel.role_id.in_(role_ids))
        )
        members_result = await self._session.execute(members_query)
        members = members_result.all()

        roles_with_members = RoleMapper.list_to_entity(members=members, roles=roles)

        return roles_with_members

    async def update(self, role: RoleEntity) -> None:
        update_data = RoleMapper.entity_to_dict(role)
        stmt = update(RoleModel).filter_by(id=role.id).values(**update_data)
        await self._session.execute(stmt)

    async def delete(self, role_id: RoleId, workspace_id: WorkspaceId) -> None:
        stmt = delete(RoleModel).filter_by(id=role_id, workspace_id=workspace_id)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise RoleNotFound(
                f'Роль с id={role_id} не найдена в рабочем пространстве с id={workspace_id}'
            )
