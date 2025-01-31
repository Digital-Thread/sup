from dataclasses import asdict
from uuid import UUID

from src.apps.workspace.domain.entities.workspace import WorkspaceEntity
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
    MemberOutDTO,
    UpdateWorkspaceDTO,
    WorkspaceOutDTO,
)


class WorkspaceMapper:

    @staticmethod
    def entity_to_dto(entity: WorkspaceEntity) -> WorkspaceOutDTO:
        return WorkspaceOutDTO(
            workspace_id=entity.id,
            owner_id=entity.owner_id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            logo=entity.logo,
            invite_ids=[int(invite) for invite in entity.invite_ids],
            project_ids=[int(project) for project in entity.project_ids],
            meet_ids=[int(meet) for meet in entity.meet_ids],
            tag_ids=[int(tag) for tag in entity.tag_ids],
            role_ids=[int(role) for role in entity.role_ids],
            member_ids=[UUID(str(member)) for member in entity.member_ids],
        )

    @staticmethod
    def dto_to_entity(dto: WorkspaceOutDTO) -> WorkspaceEntity:

        return WorkspaceEntity(
            _id=WorkspaceId(dto.workspace_id) if dto.workspace_id else None,
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
    def update_data(
        dto: UpdateWorkspaceDTO, existing_workspace: WorkspaceEntity
    ) -> WorkspaceEntity:
        for field, value in asdict(dto).items():
            if value is not None and field != 'id':
                setattr(existing_workspace, field, value)

        return existing_workspace

    @staticmethod
    def dict_to_dto(members: dict[MemberId, str]) -> list[MemberOutDTO]:
        return [
            MemberOutDTO(
                id=member_id,
                name=name,
            )
            for member_id, name in members.items()
        ]
