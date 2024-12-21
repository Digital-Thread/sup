from dataclasses import asdict
from uuid import UUID

from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import (
    AssignedId,
    OwnerId,
    ParticipantId,
    ProjectId,
    WorkspaceId,
)
from src.apps.project.dtos import (
    ProjectCreateDTO,
    ProjectUpdateDTO,
    ProjectWithParticipantCountDTO,
    ProjectWithParticipantsDTO,
)


class ProjectMapper:
    @staticmethod
    def entity_to_dto(
        project: ProjectEntity, participants: list[dict[str, UUID | str | bool]]
    ) -> ProjectWithParticipantsDTO:
        return ProjectWithParticipantsDTO(
            id=project.id,
            owner_id=project.owner_id,
            workspace_id=project.workspace_id,
            name=project.name,
            description=project.description,
            logo=project.logo,
            status=project.status,
            created_at=project.created_at,
            assigned_to=project.assigned_to,
            participants=participants,
        )

    @staticmethod
    def entity_to_dto_with_participant_count(
        project: ProjectEntity,
    ) -> ProjectWithParticipantCountDTO:
        return ProjectWithParticipantCountDTO(**asdict(project))

    @staticmethod
    def dto_to_entity(dto: ProjectCreateDTO) -> ProjectEntity:
        return ProjectEntity(
            _owner_id=OwnerId(dto.owner_id),
            _name=dto.name,
            _description=dto.description,
            logo=dto.logo,
            _status=dto.status,
            assigned_to=AssignedId(dto.assigned_to),
            participant_ids=(
                [ParticipantId(participant) for participant in dto.participant_ids]
                if dto.participant_ids
                else None
            ),
        )

    @staticmethod
    def update_data(existing_project: ProjectEntity, dto: ProjectUpdateDTO) -> ProjectEntity:
        for field, value in asdict(dto).items():
            if value is not None:
                setattr(existing_project, field, value)

        return existing_project

    @staticmethod
    def list_tuple_to_dto(
        projects: list[tuple[ProjectEntity, int]]
    ) -> list[ProjectWithParticipantCountDTO]:
        projects_with_user_count = []
        for project in projects:
            projects_with_user_count.append(
                ProjectWithParticipantCountDTO(
                    id=ProjectId(project[0].id),
                    workspace_id=WorkspaceId(project[0].workspace_id),
                    owner_id=OwnerId(project[0].owner_id),
                    name=project[0].name,
                    description=project[0].description,
                    logo=project[0].logo,
                    status=project[0].status,
                    created_at=project[0].created_at,
                    assigned_to=AssignedId(project[0].assigned_to),
                    participants_count=project[1],
                )
            )

        return projects_with_user_count

    @staticmethod
    def map_to_set_users(
        assigned_to: UUID | None = None, participants: list[UUID] | None = None
    ) -> set[UUID]:
        user_ids = set(participants or [])
        if assigned_to:
            user_ids.add(assigned_to)

        return user_ids
