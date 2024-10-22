from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.domain.types_ids import (
    InviteId,
    MeetId,
    MemberId,
    ProjectId,
    RoleId,
    TagId,
)
from src.data_access.models.workspace_models.workspace import WorkspaceModel


class WorkspaceConverter[T]:

    @staticmethod
    def model_to_entity(workspace_model: T) -> Workspace:
        clean_data = {
            column.name: getattr(workspace_model, column.name)
            for column in workspace_model.__table__.columns
        }
        workspace = Workspace(
            owner_id=clean_data['owner_id'],
            _name=clean_data['name'],
            _id=clean_data['id'],
            _description=clean_data['description'],
            logo=clean_data['logo'],
            created_at=clean_data['created_at'],
            invite_ids=[InviteId(invite.id) for invite in getattr(workspace_model, 'invites', [])],
            project_ids=[
                ProjectId(project.id) for project in getattr(workspace_model, 'projects', [])
            ],
            meet_ids=[MeetId(meet.id) for meet in getattr(workspace_model, 'meets', [])],
            tag_ids=[TagId(tag.id) for tag in getattr(workspace_model, 'tags', [])],
            role_ids=[RoleId(role.id) for role in getattr(workspace_model, 'roles', [])],
            member_ids=[MemberId(member.id) for member in getattr(workspace_model, 'members', [])],
        )
        return workspace

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
