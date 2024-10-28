from dishka import Provider, Scope, provide

from src.apps.workspace.use_cases.role_use_cases import (
    CreateRoleUseCase,
    DeleteRoleUseCase,
    GetRoleByIdUseCase,
    GetRoleByWorkspaceUseCase,
    UpdateRoleUseCase,
)
from src.apps.workspace.use_cases.workspace_use_cases import (
    CreateWorkspaceUseCase,
    DeleteWorkspaceUseCase,
    GetWorkspaceByIdUseCase,
    GetWorkspaceByMemberUseCase,
    UpdateWorkspaceUseCase,
)


class WorkspaceUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_workspace = provide(CreateWorkspaceUseCase)
    get_workspace_by_id = provide(GetWorkspaceByIdUseCase)
    get_workspace_by_owner_id = provide(GetWorkspaceByMemberUseCase)
    update_workspace = provide(UpdateWorkspaceUseCase)
    delete_workspace = provide(DeleteWorkspaceUseCase)


class RoleUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_role = provide(CreateRoleUseCase)
    get_role_by_id = provide(GetRoleByIdUseCase)
    get_role_by_workspace = provide(GetRoleByWorkspaceUseCase)
    update_role = provide(UpdateRoleUseCase)
    delete_role = provide(DeleteRoleUseCase)
