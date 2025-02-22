from asyncpg import ForeignKeyViolationError
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert

from src.data_access.models.permission_group import permission_group_users
from src.apps.permission import (
    IPermissionGroupRepository,
    PermissionGroupRepositoryError,
    PermissionGroupOutputDTO,
    PermissionGroupDoesNotExistError,
)
from src.apps.permission.domain import PermissionGroupId, PermissionGroupEntity, WorkspaceId, UserId
from src.data_access.mappers import PermissionGroupMapper
from src.data_access.models import PermissionGroupModel, PermissionModel, UserModel


class PermissionGroupRepository(IPermissionGroupRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = PermissionGroupModel
        self.mapper = PermissionGroupMapper()

    async def _get_m2m_objects[M, ID](self, _ids: set[ID] | None, model: type[M]) -> set[ID]:
        if _ids:
            query = select(model).where(model.id.in_(_ids))
            result = await self._session.execute(query)
            m2m_objects = result.scalars().all()
            return set(m2m_objects)
        return set()

    async def get_perm_group_model(self, perm_group_id: PermissionGroupId) -> PermissionGroupModel | None:
        stmt = (
            select(self.model)
            .where(self.model.id == perm_group_id)
            .options(
                selectinload(self.model.permissions),
                selectinload(self.model.authorized_users),
            )
        )
        result = await self._session.execute(stmt)
        perm_group_model = result.scalar_one_or_none()
        return perm_group_model

    async def save(self, perm_group: PermissionGroupEntity) -> None:
        perm_group_model = self.mapper.entity_to_model(perm_group)
        perm_group_model.permissions = await self._get_m2m_objects(perm_group.permissions, PermissionModel)
        perm_group_model.authorized_users = await self._get_m2m_objects(perm_group.authorized_users, UserModel)

        try:
            self._session.add(perm_group_model)
            await self._session.flush()
        except IntegrityError as e:
            orig_exception = e.orig.__cause__
            if isinstance(orig_exception, ForeignKeyViolationError):
                detail_message = orig_exception.detail
                raise PermissionGroupRepositoryError(detail_message)
            raise

    async def get_perm_group_entity(self, perm_group_id: PermissionGroupId) -> PermissionGroupEntity | None:
        perm_group_model = await self.get_perm_group_model(perm_group_id=perm_group_id)
        if perm_group_model:
            return self.mapper.model_to_entity(perm_group_model)
        return None

    async def get_perm_group_by_id(self, perm_group_id: PermissionGroupId) -> PermissionGroupOutputDTO | None:
        perm_group_model = await self.get_perm_group_model(perm_group_id=perm_group_id)
        if perm_group_model:
            return self.mapper.model_to_dto(perm_group_model)
        return None

    async def get_perm_groups_by_workspace_id(self, workspace_id: WorkspaceId) -> list[PermissionGroupOutputDTO] | None:
        stmt = (
            select(self.model)
            .where(self.model.workspace_id == workspace_id)
            .options(
                selectinload(self.model.permissions),
                selectinload(self.model.authorized_users),
            )
        )
        result = await self._session.execute(stmt)
        perm_groups = result.scalars().all()
        return (
            [self.mapper.model_to_dto(model=pg) for pg in perm_groups]
            if perm_groups
            else None
        )

    async def update(self, perm_group: PermissionGroupEntity) -> None:
        perm_group_model = await self.get_perm_group_model(perm_group_id=perm_group.id)
        if perm_group_model:
            perm_group_model.name = perm_group.name
            perm_group_model.description = perm_group.description
            perm_group_model.is_global = perm_group.is_global
            perm_group_model.workspace_id = perm_group.workspace_id
            perm_group_model.permissions = await self._get_m2m_objects(perm_group.permissions, PermissionModel)
            perm_group_model.authorized_users = await self._get_m2m_objects(perm_group.authorized_users, UserModel)
            try:
                await self._session.flush()
            except IntegrityError as e:
                orig_exception = e.orig.__cause__
                if isinstance(orig_exception, ForeignKeyViolationError):
                    detail_message = orig_exception.detail
                    raise PermissionGroupRepositoryError(detail_message)
                raise
        else:
            raise PermissionGroupRepositoryError()

    async def delete(self, perm_group_id: PermissionGroupId) -> None:
        stmt = delete(self.model).where(self.model.id == perm_group_id)
        result = await self._session.execute(stmt)
        if result.rowcount == 0:
            raise PermissionGroupDoesNotExistError(perm_group_id=perm_group_id)

    async def assign_permission_group(
            self,
            group_name: str,
            user_id: UserId,
            workspace_id: WorkspaceId | None = None,
    ) -> None:
        group_stmt = select(self.model.id).where(self.model.name == group_name)
        result = await self._session.execute(group_stmt)
        group_id = result.scalar_one_or_none()

        if not group_id:
            raise PermissionGroupDoesNotExistError(message=f"Permission group '{group_name}' not found")

        assign_stmt = insert(permission_group_users).values(
            permission_group_id=group_id,
            user_id=user_id,
            workspace_id=workspace_id
        ).on_conflict_do_nothing()
        await self._session.execute(assign_stmt)
