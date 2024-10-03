from collections.abc import Callable
from typing import Any
from uuid import UUID

from src.apps.workspace.domain.entities.category import Category
from src.apps.workspace.domain.entities.role import Role
from src.apps.workspace.domain.entities.tag import Tag
from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.domain.entities.workspace_invite import WorkspaceInvite
from src.apps.workspace.repositories.i_category_repository import ICategoryRepository
from src.apps.workspace.repositories.i_role_repository import IRoleRepository
from src.apps.workspace.repositories.i_tag_repository import ITagRepository
from src.apps.workspace.repositories.i_workspace_invite_repository import (
    IWorkspaceInviteRepository,
)
from src.apps.workspace.repositories.i_workspace_repository import IWorkspaceRepository
from src.apps.workspace.services.base_service import BaseService


class WorkspaceService(BaseService[Workspace, UUID, IWorkspaceRepository]):
    async def retrieve_by_owner_id(
        self, owner_id: UUID, use_case: Callable[[IWorkspaceRepository], Any]
    ) -> list[Workspace]:
        return await self._execute_use_case(use_case, owner_id)


class WorkspaceInviteService(BaseService[WorkspaceInvite, int, IWorkspaceInviteRepository]):
    async def retrieve_by_workspace_id(
        self, workspace_id: UUID, use_case: Callable[[IWorkspaceInviteRepository], Any]
    ) -> list[WorkspaceInvite]:
        return await self.retrieve_by_workspace_id(workspace_id, use_case)


class RoleService(BaseService[Role, int, IRoleRepository]):
    async def retrieve_by_workspace_id(
        self, workspace_id: UUID, use_case: Callable[[IRoleRepository], Any]
    ) -> list[Role]:
        return await self.retrieve_by_workspace_id(workspace_id, use_case)


class TagService(BaseService[Tag, int, ITagRepository]):
    async def retrieve_by_workspace_id(
        self, workspace_id: UUID, use_case: Callable[[ITagRepository], Any]
    ) -> list[Tag]:
        return await self.retrieve_by_workspace_id(workspace_id, use_case)


class CategoryService(BaseService[Category, int, ICategoryRepository]):
    async def retrieve_by_workspace_id(
        self, workspace_id: UUID, use_case: Callable[[ICategoryRepository], Any]
    ) -> list[Category]:
        return await self.retrieve_by_workspace_id(workspace_id, use_case)
