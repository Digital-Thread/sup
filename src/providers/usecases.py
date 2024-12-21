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
from src.apps.project.interactors import (
    CreateProjectInteractor,
    DeleteProjectInteractor,
    GetProjectByWorkspaceInteractor,
    UpdateProjectInteractor,
)
from src.apps.project.interactors.update_participants import UpdateParticipantsInteractor
from src.apps.project.use_cases.get_project_by_id import GetProjectByIdUseCase
from src.apps.task import (
    CreateTaskInteractor,
    DeleteTaskInteractor,
    GetAllTasksInteractor,
    GetTaskInteractor,
    UpdateTaskInteractor,
)
from src.apps.workspace.interactors.category_interactors import (
    CreateCategoryInteractor,
    DeleteCategoryInteractor,
    GetCategoryByWorkspaceInteractor,
    UpdateCategoryInteractor,
)
from src.apps.workspace.interactors.category_interactors.get_category_by_id import GetCategoryByIdInteractor
from src.apps.workspace.interactors.role_interactors import (
    CreateRoleInteractor,
    DeleteRoleInteractor,
    GetRoleByIdInteractor,
    GetRoleByWorkspaceInteractor,
    UpdateRoleInteractor,
    AssignRoleToWorkspaceMemberInteractor,
    RemoveRoleFromWorkspaceMemberInteractor
)
from src.apps.workspace.interactors.tag_interactors import (
    CreateTagInteractor,
    DeleteTagInteractor,
    GetTagByIdInteractor,
    GetTagByWorkspaceInteractor,
    UpdateTagInteractor,
)
from src.apps.workspace.interactors.workspace_interactors.get_workspace_members import GetWorkspaceMembersInteractor
from src.apps.workspace.interactors.workspace_invite_interactors import (
    CreateWorkspaceInviteInteractor,
    DeleteWorkspaceInviteInteractor,
    GetWorkspaceIdByInviteCodeInteractor,
    GetWorkspaceInviteByWorkspaceInteractor,
    UpdateWorkspaceInviteInteractor,
)
from src.apps.workspace.interactors.workspace_interactors import (
    AddMemberInWorkspaceInteractor,
    CreateWorkspaceInteractor,
    DeleteWorkspaceInteractor,
    GetWorkspaceByIdInteractor,
    GetWorkspaceByMemberInteractor,
    UpdateWorkspaceInteractor,
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

    create_workspace = provide(CreateWorkspaceInteractor)
    get_workspace_by_id = provide(GetWorkspaceByIdInteractor)
    get_workspace_by_owner_id = provide(GetWorkspaceByMemberInteractor)
    update_workspace = provide(UpdateWorkspaceInteractor)
    delete_workspace = provide(DeleteWorkspaceInteractor)
    add_member = provide(AddMemberInWorkspaceInteractor)
    get_workspace_member = provide(GetWorkspaceMembersInteractor)


class RoleUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_role = provide(CreateRoleInteractor)
    get_role_by_id = provide(GetRoleByIdInteractor)
    get_role_by_workspace = provide(GetRoleByWorkspaceInteractor)
    update_role = provide(UpdateRoleInteractor)
    delete_role = provide(DeleteRoleInteractor)
    assign_role_to_user = provide(AssignRoleToWorkspaceMemberInteractor)
    remove_role_from_member = provide(RemoveRoleFromWorkspaceMemberInteractor)


class TagUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_tag = provide(CreateTagInteractor)
    get_tag_by_id = provide(GetTagByIdInteractor)
    get_tag_by_workspace = provide(GetTagByWorkspaceInteractor)
    update_tag = provide(UpdateTagInteractor)
    delete_tag = provide(DeleteTagInteractor)


class CategoryUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_category = provide(CreateCategoryInteractor)
    get_category_by_workspace = provide(GetCategoryByWorkspaceInteractor)
    get_category_by_id = provide(GetCategoryByIdInteractor)
    update_category = provide(UpdateCategoryInteractor)
    delete_category = provide(DeleteCategoryInteractor)


class WorkspaceInviteUseCaseProvider(Provider):
    scope = Scope.REQUEST

    create_workspace_invite = provide(CreateWorkspaceInviteInteractor)
    get_workspace_invite_by_id = provide(GetWorkspaceIdByInviteCodeInteractor)
    get_workspace_invite_by_workspace = provide(GetWorkspaceInviteByWorkspaceInteractor)
    update_workspace_invite = provide(UpdateWorkspaceInviteInteractor)
    delete_workspace_invite = provide(DeleteWorkspaceInviteInteractor)


class ProjectInteractorProvider(Provider):
    scope = Scope.REQUEST

    create_project = provide(CreateProjectInteractor)
    get_project_by_workspace = provide(GetProjectByWorkspaceInteractor)
    get_project_by_id = provide(GetProjectByIdUseCase)
    update_project = provide(UpdateProjectInteractor)
    update_participants = provide(UpdateParticipantsInteractor)
    delete_project = provide(DeleteProjectInteractor)


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
