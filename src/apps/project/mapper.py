from dataclasses import asdict

from src.apps.project.domain.entity.project import Project
from src.apps.project.domain.types_ids import (
    AssignedId,
    OwnerId,
    ParticipantId,
    ProjectId,
    WorkspaceId,
)
from src.apps.project.dtos import (
    CreateProjectAppDTO,
    ProjectWithParticipantCountAppDTO,
    UpdateProjectAppDTO,
)


class ProjectMapper:
    @staticmethod
    def entity_to_dto(project: Project) -> ProjectWithParticipantCountAppDTO:
        return ProjectWithParticipantCountAppDTO(**asdict(project))

    @staticmethod
    def dto_to_entity(dto: CreateProjectAppDTO) -> Project:
        return Project(
            _id=ProjectId(dto.id) if isinstance(dto, ProjectWithParticipantCountAppDTO) else None,
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
    def update_data(existing_project: Project, dto: UpdateProjectAppDTO) -> Project:
        for field, value in asdict(dto).items():
            if value is not None:
                setattr(existing_project, field, value)

        return existing_project

    @staticmethod
    def list_tuple_to_dto(
        projects: list[tuple[Project, int]]
    ) -> list[ProjectWithParticipantCountAppDTO]:
        projects_with_user_count = []
        for project in projects:
            projects_with_user_count.append(
                ProjectWithParticipantCountAppDTO(
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
