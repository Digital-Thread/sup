from dataclasses import asdict

from src.apps.workspace.domain.entities.workspace import Workspace
from src.apps.workspace.domain.types_ids import (
    InviteId,
    MeetId,
    MemberId,
    OwnerId,
    ProjectId,
    RoleId,
    TagId,
    WorkspaceId,
)
from src.apps.workspace.dtos.workspace_dtos import (
    UpdateWorkspaceAppDTO,
    WorkspaceAppDTO,
)
from src.apps.workspace.mappers.base_mapper import BaseMapper


class WorkspaceMapper(BaseMapper[Workspace, WorkspaceAppDTO]):

    @staticmethod
    def dto_to_entity(dto: WorkspaceAppDTO) -> Workspace:

        return Workspace(
            _id=WorkspaceId(dto.id) if dto.id else None,
            owner_id=OwnerId(dto.owner_id),
            _name=dto.name,
            _description=dto.description,
            logo=dto.logo,
            created_at=dto.created_at,
            invite_ids=[InviteId(invite) for invite in dto.invite_ids],
            project_ids=[ProjectId(project) for project in dto.project_ids],
            meet_ids=[MeetId(meet) for meet in dto.meet_ids],
            tag_ids=[TagId(tag) for tag in dto.tag_ids],
            role_ids=[RoleId(role) for role in dto.role_ids],
            member_ids=[MemberId(member) for member in dto.member_ids],
        )

    @staticmethod
    def update_data(dto: UpdateWorkspaceAppDTO, existing_workspace: Workspace) -> Workspace:
        for field, value in asdict(dto).items():
            if value is not None:
                setattr(existing_workspace, field, value)

        return existing_workspace
