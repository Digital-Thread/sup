from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.domain.types_ids import (
    InviteId,
    MeetId,
    MemberId,
    ProjectId,
    RoleId,
    TagId, OwnerId, WorkspaceId,
)
from src.data_access.models.workspace_models.workspace import WorkspaceModel


class WorkspaceConverter:

    @staticmethod
    def model_to_entity(workspace_model: WorkspaceModel) -> Workspace:

        return Workspace(
            owner_id=OwnerId(workspace_model.owner_id),
            _name=workspace_model.name,
            _id=WorkspaceId(workspace_model.id),
            _description=workspace_model.description,
            logo=workspace_model.logo,
            created_at=workspace_model.created_at,
            invite_ids=[InviteId(invite.id) for invite in workspace_model.invites],
            project_ids=[
                ProjectId(project.id) for project in workspace_model.projects
            ],
            meet_ids=[MeetId(meet.id) for meet in workspace_model.meets],
            tag_ids=[TagId(tag.id) for tag in workspace_model.tags],
            role_ids=[RoleId(role.id) for role in workspace_model.roles],
            member_ids=[MemberId(member.id) for member in workspace_model.members],
        )


    @staticmethod
    def entity_to_model(entity: Workspace) -> WorkspaceModel:
        model = WorkspaceModel(
            id=entity.id,
            owner_id=entity.owner_id,
            name=entity.name,
            description=entity.description,
            logo=entity.logo,
            created_at=entity.created_at,
        )
        return model

    @staticmethod
    def entity_to_dict(workspace: Workspace) -> dict:
        return {
            'name': workspace.name,
            'description': workspace.description,
            'logo': workspace.logo,
        }