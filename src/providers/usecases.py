from dishka import Provider, Scope, provide

from src.apps.comment import (
    AddCommentDto,
    AddCommentInteractor,
    CommentOutDto,
    CommentPaginationDto,
    DeleteCommentDto,
    DeleteCommentInteractor,
    FetchAllCommentsInteractor,
    FetchAllFeatureCommentsInteractor,
    FetchAllTaskCommentsInteractor,
    FetchCommentDto,
    FetchCommentInteractor,
    FetchFeatureCommentDto,
    FetchTaskCommentDto,
    UpdateCommentDto,
    UpdateCommentInteractor,
)
from src.apps.comment.domain import Interactor
from src.apps.feature import (
    CreateFeatureInteractor,
    DeleteFeatureInteractor,
    GetAllFeaturesInteractor,
    GetFeatureInteractor,
    UpdateFeatureInteractor,
)
from src.apps.project.use_cases import (
    CreateProjectUseCase,
    DeleteProjectUseCase,
    GetProjectByWorkspaceUseCase,
    UpdateProjectUseCase,
)
from src.apps.task import (
    CreateTaskInteractor,
    DeleteTaskInteractor,
    GetAllTasksInteractor,
    GetTaskInteractor,
    UpdateTaskInteractor,
)
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
    AssignRoleToWorkspaceMemberUseCase,
    RemoveRoleFromWorkspaceMemberUseCase
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
    GetWorkspaceIdByInviteCodeUseCase,
    GetWorkspaceInviteByWorkspaceUseCase,
    UpdateWorkspaceInviteUseCase,
)
from src.apps.workspace.use_cases.workspace_use_cases import (
    AddMemberInWorkspaceUseCase,
    CreateWorkspaceUseCase,
    DeleteWorkspaceUseCase,
    GetWorkspaceByIdUseCase,
    GetWorkspaceByMemberUseCase,
    UpdateWorkspaceUseCase,
)


class InteractorProvider(Provider):
    scope = Scope.REQUEST
    comment = provide(AddCommentInteractor, provides=Interactor[AddCommentDto, CommentOutDto])
    fetch_comment = provide(
        FetchCommentInteractor, provides=Interactor[FetchCommentDto, CommentOutDto]
    )
    fetch_comments = provide(
        FetchAllCommentsInteractor, provides=Interactor[CommentPaginationDto, list[CommentOutDto]]
    )
    update_comment = provide(
        UpdateCommentInteractor, provides=Interactor[UpdateCommentDto, CommentOutDto]
    )
    delete_comment = provide(DeleteCommentInteractor, provides=Interactor[DeleteCommentDto, None])
    fetch_task_comments = provide(
        FetchAllTaskCommentsInteractor,
        provides=Interactor[FetchTaskCommentDto, list[CommentOutDto]],
    )

    fetch_feature_comments = provide(
        FetchAllFeatureCommentsInteractor,
        provides=Interactor[FetchFeatureCommentDto, list[CommentOutDto]],
    )


class WorkspaceUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_workspace = provide(CreateWorkspaceUseCase)
    get_workspace_by_id = provide(GetWorkspaceByIdUseCase)
    get_workspace_by_owner_id = provide(GetWorkspaceByMemberUseCase)
    update_workspace = provide(UpdateWorkspaceUseCase)
    delete_workspace = provide(DeleteWorkspaceUseCase)
    add_member = provide(AddMemberInWorkspaceUseCase)


class RoleUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_role = provide(CreateRoleUseCase)
    get_role_by_id = provide(GetRoleByIdUseCase)
    get_role_by_workspace = provide(GetRoleByWorkspaceUseCase)
    update_role = provide(UpdateRoleUseCase)
    delete_role = provide(DeleteRoleUseCase)
    assign_role_to_user = provide(AssignRoleToWorkspaceMemberUseCase)
    remove_role_from_member = provide(RemoveRoleFromWorkspaceMemberUseCase)


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
    get_workspace_invite_by_id = provide(GetWorkspaceIdByInviteCodeUseCase)
    get_workspace_invite_by_workspace = provide(GetWorkspaceInviteByWorkspaceUseCase)
    update_workspace_invite = provide(UpdateWorkspaceInviteUseCase)
    delete_workspace_invite = provide(DeleteWorkspaceInviteUseCase)


class ProjectUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_project = provide(CreateProjectUseCase)
    get_project_by_workspace = provide(GetProjectByWorkspaceUseCase)
    update_project = provide(UpdateProjectUseCase)
    delete_project = provide(DeleteProjectUseCase)


class FeatureInteractorProvider(Provider):
    scope = Scope.REQUEST

    create_feature = provide(CreateFeatureInteractor)
    get_feature_by_id = provide(GetFeatureInteractor)
    get_features = provide(GetAllFeaturesInteractor)
    update_feature = provide(UpdateFeatureInteractor)
    delete_feature = provide(DeleteFeatureInteractor)


class TaskInteractorProvider(Provider):
    scope = Scope.REQUEST

    create_task = provide(CreateTaskInteractor)
    get_task_by_id = provide(GetTaskInteractor)
    get_tasks = provide(GetAllTasksInteractor)
    update_task = provide(UpdateTaskInteractor)
    delete_task = provide(DeleteTaskInteractor)
