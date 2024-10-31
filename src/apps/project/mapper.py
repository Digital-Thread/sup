from dataclasses import asdict

from src.apps.project.domain.entity.project import Project
from src.apps.project.domain.types_ids import (
    AssignedId,
    FeatureId,
    OwnerId,
    ParticipantId,
    ProjectId,
    WorkspaceId,
)
from src.apps.project.dtos import (
    CreateProjectAppDTO,
    ProjectAppDTO,
    UpdateProjectAppDTO,
)


class ProjectMapper:
    @staticmethod
    def entity_to_dto(project: Project) -> ProjectAppDTO:
        return ProjectAppDTO(**asdict(project))

    @staticmethod
    def dto_to_entity(dto: ProjectAppDTO | CreateProjectAppDTO) -> Project:
        return Project(
            _id=ProjectId(dto.id) if isinstance(dto, ProjectAppDTO) else None,
            _workspace_id=WorkspaceId(dto.workspace_id),
            _owner_id=OwnerId(dto.owner_id),
            _name=dto.name,
            _description=dto.description,
            logo=dto.logo,
            _status=dto.status,
            created_at=dto.created_at if isinstance(dto, ProjectAppDTO) else None,
            assigned_to=AssignedId(dto.assigned_to),
            feature_ids=(
                [FeatureId(feature) for feature in dto.feature_ids] if dto.feature_ids else None
            ),
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
