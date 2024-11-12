from sqlalchemy import exists, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.workspace.domain.types_ids import MemberId, RoleId, WorkspaceId
from src.apps.workspace.exceptions.role_exceptions import RoleNotFound
from src.apps.workspace.exceptions.workspace_exceptions import WorkspaceMemberNotFound, WorkspaceNotFound
from src.apps.workspace.repositories.i_user_workspace_role_repository import IUserWorkspaceRoleRepository
from src.data_access.models.workspace_models import WorkspaceModel, RoleModel, WorkspaceMemberModel, UserWorkspaceRoleModel


class UserWorkspaceRoleRepository(IUserWorkspaceRoleRepository):
    def __init__(self, session_factory: AsyncSession):
        self._session = session_factory

    async def assign_role_to_workspace_member(
            self, workspace_id: WorkspaceId, member_id: MemberId, role_id: RoleId
    ) -> None:
        await self._check_exists_workspace(workspace_id)
        await self._check_member_in_workspace(workspace_id, member_id)
        await self._check_exists_role_in_workspace(role_id, workspace_id)

        is_exists_member_role = await self._is_exists_role_for_member_in_workspace(member_id, workspace_id)

        if is_exists_member_role:
            await self._session.execute(
                update(UserWorkspaceRoleModel)
                .filter_by(user_id=member_id, workspace_id=workspace_id)
                .values(role_id=role_id)
            )

        else:
            stmt = UserWorkspaceRoleModel(
                user_id=member_id, workspace_id=workspace_id, role_id=role_id
            )
            self._session.add(stmt)

    async def _check_member_in_workspace(self, workspace_id: WorkspaceId, member_id: MemberId) -> None:
        user_exists = await self._session.execute(
            select(exists().where(
                WorkspaceMemberModel.user_id == member_id,
                WorkspaceMemberModel.workspace_id == workspace_id
            )
            )
        )

        if not user_exists.scalar():
            raise WorkspaceMemberNotFound(
                f'Участник с id={member_id} отсутствует в рабочем пространстве с id={workspace_id}')

    async def _check_exists_workspace(self, workspace_id: WorkspaceId) -> None:
        workspace_exists = await self._session.execute(select(exists().where(WorkspaceModel.id == workspace_id)))
        if not workspace_exists.scalar():
            raise WorkspaceNotFound(f'Рабочее пространство с id={workspace_id} не найдено')

    async def _check_exists_role_in_workspace(self, role_id: RoleId, workspace_id: WorkspaceId) -> None:
        role_exists = await self._session.execute(
            select(exists().where(RoleModel.id == role_id, RoleModel.workspace_id == workspace_id)))
        if not role_exists.scalar():
            raise RoleNotFound('Роль не найдена')

    async def _is_exists_role_for_member_in_workspace(self, member_id: MemberId, workspace_id: WorkspaceId) -> bool:
        member_role_exists = await self._session.execute(
            select(
                exists().where(
                    UserWorkspaceRoleModel.user_id == member_id,
                    UserWorkspaceRoleModel.workspace_id == workspace_id,
                )
            )
        )

        return member_role_exists.scalar()

    async def remove_role_from_workspace_member(self, workspace_id: WorkspaceId, member_id: MemberId) -> None:
        is_exists_member_role = await self._is_exists_role_for_member_in_workspace(member_id, workspace_id)
        if is_exists_member_role:
            await self._session.execute(
                delete(UserWorkspaceRoleModel).filter_by(user_id=member_id, workspace_id=workspace_id)
            )
        else:
            await self._check_exists_workspace(workspace_id)
            await self._check_member_in_workspace(workspace_id, member_id)

