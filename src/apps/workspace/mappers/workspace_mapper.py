from typing import Any

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
    def dto_to_entity(
        dto: WorkspaceAppDTO | UpdateWorkspaceAppDTO, immutable_data: dict[str, Any]
    ) -> Workspace:

        if isinstance(dto, WorkspaceAppDTO):
            workspace = Workspace(
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
        else:
            workspace = Workspace(
                _id=immutable_data.get('workspace_id'),
                owner_id=immutable_data.get('owner_id'),
                created_at=immutable_data.get('created_at'),
                _name=dto.get('name'),
                _description=dto.get('description'),
                logo=dto.get('logo'),
                invite_ids=immutable_data.get('invite_ids'),
                project_ids=immutable_data.get('project_ids'),
                meet_ids=immutable_data.get('meet_ids'),
                tag_ids=immutable_data.get('tag_ids'),
                role_ids=immutable_data.get('role_ids'),
                member_ids=immutable_data.get('member_ids'),
            )

        return workspace
