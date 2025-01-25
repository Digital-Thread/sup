from dishka import Provider, Scope, provide

from src.apps.comment import (
    CreateCommentInteractor,
    DeleteCommentInteractor,
    GetCommentsByFeatureIdInteractor,
    GetCommentsByTaskIdInteractor,
    UpdateCommentInteractor,
)
from src.apps.feature import (
    CreateFeatureInteractor,
    DeleteFeatureInteractor,
    GetFeatureByIdInteractor,
    GetFeaturesByWorkspaceInteractor,
    UpdateFeatureInteractor,
)
from src.apps.meet import (
    CreateMeetInteractor,
    CreateParticipantInteractor,
    DeleteMeetInteractor,
    DeleteParticipantInteractor,
    GetListMeetsInteractor,
    GetListParticipantsInteractor,
    GetMeetInteractor,
    GetParticipantInteractor,
    UpdateMeetInteractor,
    UpdateParticipantInteractor,
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
    GetTaskByIdInteractor,
    GetTasksByFeatureIdInteractor,
    UpdateTaskInteractor,
)
from src.apps.workspace.interactors.category_interactors import (
    CreateCategoryInteractor,
    DeleteCategoryInteractor,
    GetCategoryByWorkspaceInteractor,
    UpdateCategoryInteractor,
)
from src.apps.workspace.interactors.category_interactors.get_category_by_id import (
    GetCategoryByIdInteractor,
)
from src.apps.workspace.interactors.role_interactors import (
    AssignRoleToWorkspaceMemberInteractor,
    CreateRoleInteractor,
    DeleteRoleInteractor,
    GetRoleByIdInteractor,
    GetRolesByWorkspaceInteractor,
    RemoveRoleFromWorkspaceMemberInteractor,
    UpdateRoleInteractor,
)
from src.apps.workspace.interactors.tag_interactors import (
    CreateTagInteractor,
    DeleteTagInteractor,
    GetTagByIdInteractor,
    GetTagByWorkspaceInteractor,
    UpdateTagInteractor,
)
from src.apps.workspace.interactors.workspace_interactors import (
    AddMemberInWorkspaceInteractor,
    CreateWorkspaceInteractor,
    DeleteWorkspaceInteractor,
    GetWorkspaceByIdInteractor,
    GetWorkspaceByMemberInteractor,
    UpdateWorkspaceInteractor,
)
from src.apps.workspace.interactors.workspace_interactors.get_workspace_members import (
    GetWorkspaceMembersInteractor,
)
from src.apps.workspace.interactors.workspace_invite_interactors import (
    CreateWorkspaceInviteInteractor,
    DeleteWorkspaceInviteInteractor,
    GetWorkspaceIdByInviteCodeInteractor,
    GetWorkspaceInvitesByWorkspaceInteractor,
    UpdateWorkspaceInviteInteractor,
)


class CommentInteractorProvider(Provider):
    scope = Scope.REQUEST

    create_comment = provide(CreateCommentInteractor)
    get_comments_by_task_id = provide(GetCommentsByTaskIdInteractor)
    get_comments_by_feature_id = provide(GetCommentsByFeatureIdInteractor)
    update_comment = provide(UpdateCommentInteractor)
    delete_comment = provide(DeleteCommentInteractor)


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
    get_role_by_workspace = provide(GetRolesByWorkspaceInteractor)
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
    get_workspace_invite_by_workspace = provide(GetWorkspaceInvitesByWorkspaceInteractor)
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
    get_feature_by_id = provide(GetFeatureByIdInteractor)
    get_features = provide(GetFeaturesByWorkspaceInteractor)
    update_feature = provide(UpdateFeatureInteractor)
    delete_feature = provide(DeleteFeatureInteractor)


class TaskInteractorProvider(Provider):
    scope = Scope.REQUEST

    create_task = provide(CreateTaskInteractor)
    get_task_by_id = provide(GetTaskByIdInteractor)
    get_tasks = provide(GetTasksByFeatureIdInteractor)
    update_task = provide(UpdateTaskInteractor)
    delete_task = provide(DeleteTaskInteractor)


class MeetInteractorProvider(Provider):
    scope = Scope.REQUEST

    create_meet = provide(CreateMeetInteractor)
    get_meet_by_id = provide(GetMeetInteractor)
    get_meets = provide(GetListMeetsInteractor)
    update_meet = provide(UpdateMeetInteractor)
    delete_meet = provide(DeleteMeetInteractor)


class MeetParticipantInteractorProvider(Provider):
    scope = Scope.REQUEST

    create_participant = provide(CreateParticipantInteractor)
    get_participant_by_id = provide(GetParticipantInteractor)
    get_participants = provide(GetListParticipantsInteractor)
    update_participant = provide(UpdateParticipantInteractor)
    delete_participant = provide(DeleteParticipantInteractor)
