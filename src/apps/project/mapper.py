from dataclasses import asdict
from uuid import UUID

from src.apps.project.domain.project import ProjectEntity
from src.apps.project.domain.types_ids import (
    AssignedId,
    OwnerId,
    ParticipantId,
    WorkspaceId,
)
from src.apps.project.dtos import (
    ParticipantOutDTO,
    ProjectCreateDTO,
    ProjectUpdateDTO,
    ProjectWithParticipantsDTO,
    WorkspaceMemberOutDTO,
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
            participants=[
                WorkspaceMemberOutDTO(
                    id=participant.get('id'),  # type: ignore
                    full_name=str(participant.get('full_name')),
                    is_project_participant=bool(participant.get('is_project_participant')),
                )
                for participant in participants
            ],
        )

    @staticmethod
    def entity_to_dto_with_participant_count(
        project: ProjectEntity,
    ) -> ProjectWithParticipantsDTO:
        return ProjectWithParticipantsDTO(**asdict(project))

    @staticmethod
    def dto_to_entity(dto: ProjectCreateDTO) -> ProjectEntity:
        return ProjectEntity(
            _workspace_id=WorkspaceId(dto.workspace_id),
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
            if value is not None and field != 'workspace_id':
                setattr(existing_project, field, value)

        return existing_project

    @staticmethod
    def list_tuple_to_dto(
        projects_with_participants: list[tuple[ProjectEntity, list[dict[str, str]] | None]]
    ) -> list[ProjectWithParticipantsDTO]:
        return [
            ProjectWithParticipantsDTO(
                id=project.id,
                workspace_id=project.workspace_id,
                owner_id=project.owner_id,
                name=project.name,
                description=project.description,
                logo=project.logo,
                status=project.status,
                created_at=project.created_at,
                assigned_to=project.assigned_to,
                participants=(
                    [
                        ParticipantOutDTO(
                            participant_id=participant['participant_id'],  # type: ignore
                            first_name=str(participant['first_name']),
                            last_name=str(participant['last_name']),
                            avatar=str(participant.get('avatar', None)),
                        )
                        for participant in participants
                    ]
                    if participants
                    else []
                ),
            )
            for project, participants in projects_with_participants
        ]

    @staticmethod
    def map_to_set_users(
        assigned_to: UUID | None = None, participants: list[UUID] | None = None
    ) -> set[UUID]:
        user_ids = set(participants or [])
        if assigned_to:
            user_ids.add(assigned_to)

        return user_ids
