from dishka import Provider, Scope, provide

from src.apps.workspace.use_cases.category_use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryByIdUseCase,
    GetCategoryByWorkspaceUseCase,
    UpdateCategoryUseCase,
)
from src.apps.workspace.use_cases.role_use_cases import (
    CreateRoleUseCase,
    DeleteRoleUseCase,
    GetRoleByIdUseCase,
    GetRoleByWorkspaceUseCase,
    UpdateRoleUseCase,
)
from src.apps.workspace.use_cases.tag_use_cases import (
    CreateTagUseCase,
    DeleteTagUseCase,
    GetTagByIdUseCase,
    GetTagByWorkspaceUseCase,
    UpdateTagUseCase,
)
from src.apps.workspace.use_cases.workspace_invite_use_cases import (
    CreateWorkspaceInviteUseCase,
    DeleteWorkspaceInviteUseCase,
    GetWorkspaceInviteByIdUseCase,
    GetWorkspaceInviteByWorkspaceUseCase,
    UpdateWorkspaceInviteUseCase,
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


class TagUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_tag = provide(CreateTagUseCase)
    get_tag_by_id = provide(GetTagByIdUseCase)
    get_tag_by_workspace = provide(GetTagByWorkspaceUseCase)
    update_tag = provide(UpdateTagUseCase)
    delete_tag = provide(DeleteTagUseCase)


class CategoryUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_category = provide(CreateCategoryUseCase)
    get_category_by_id = provide(GetCategoryByIdUseCase)
    get_category_by_workspace = provide(GetCategoryByWorkspaceUseCase)
    update_category = provide(UpdateCategoryUseCase)
    delete_category = provide(DeleteCategoryUseCase)


class WorkspaceInviteUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_workspace_invite = provide(CreateWorkspaceInviteUseCase)
    get_workspace_invite_by_id = provide(GetWorkspaceInviteByIdUseCase)
    get_workspace_invite_by_workspace = provide(GetWorkspaceInviteByWorkspaceUseCase)
    update_workspace_invite = provide(UpdateWorkspaceInviteUseCase)
    delete_workspace_invite = provide(DeleteWorkspaceInviteUseCase)
