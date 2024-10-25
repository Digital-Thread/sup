from dishka import Provider, Scope, provide

from src.apps.workspace.use_cases.workspace_use_cases import (
    CreateWorkspaceUseCase,
    DeleteWorkspaceUseCase,
    GetWorkspaceByIdUseCase,
    GetWorkspaceByOwnerUseCase,
    UpdateWorkspaceUseCase,
)


class WorkspaceUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_workspace = provide(CreateWorkspaceUseCase)
    get_workspace_by_id = provide(GetWorkspaceByIdUseCase)
    get_workspace_by_owner_id = provide(GetWorkspaceByOwnerUseCase)
    update_workspace = provide(UpdateWorkspaceUseCase)
    delete_workspace = provide(DeleteWorkspaceUseCase)
