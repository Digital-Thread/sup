from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.permission.domain import UserId, WorkspaceId, PermissionCode
from src.data_access.models.permission_group import (
    permission_group_permissions,
    PermissionGroupModel,
    permission_group_users,
)
from src.data_access.mappers import PermissionMapper
from src.data_access.models import PermissionModel
from src.apps.permission import IPermissionRepository, PermissionOutputDTO


class PermissionRepository(IPermissionRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = PermissionModel
        self.mapper = PermissionMapper()

    async def get_permissions(self, exclude_hidden: bool) -> list[PermissionOutputDTO]:
        stmt = select(self.model).where(self.model.is_hidden == False)
        result = await self._session.execute(stmt)
        permissions = result.scalars().all()
        return (
            [self.mapper.map_model_to_output_dto(model=model) for model in permissions]
            if permissions
            else None
        )

    async def get_user_permissions(self, user_id: UserId, workspace_id: WorkspaceId) -> set[PermissionCode]:
        stmt = select(PermissionModel.code).join(
            permission_group_permissions,
            permission_group_permissions.c.permission_id == PermissionModel.id
        ).join(
            PermissionGroupModel,
            PermissionGroupModel.id == permission_group_permissions.c.permission_group_id
        ).join(
            permission_group_users,
            permission_group_users.c.permission_group_id == PermissionGroupModel.id
        ).where(
            permission_group_users.c.user_id == user_id,
            (
                (permission_group_users.c.workspace_id == workspace_id) |
                (PermissionGroupModel.workspace_id == workspace_id)
            )
        )

        result = await self._session.execute(stmt)
        permissions = {row[0] for row in result.fetchall()}

        return permissions
