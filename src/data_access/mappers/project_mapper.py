from collections import defaultdict
from typing import Sequence
from uuid import UUID

from sqlalchemy import Row

from src.apps.project.domain.project import ProjectEntity, StatusProject
from src.apps.project.domain.types_ids import (
    AssignedId,
    OwnerId,
    ParticipantId,
    ProjectId,
    WorkspaceId,
)
from src.data_access.models.project import ProjectModel
from src.data_access.models.project_participants import ProjectParticipantsModel


class ProjectMapper:
    @staticmethod
    def model_to_entity(project_model: ProjectModel) -> ProjectEntity:
        project = ProjectEntity(
            _id=ProjectId(project_model.id),
            _workspace_id=WorkspaceId(project_model.workspace_id),
            _owner_id=OwnerId(project_model.owner_id),
            _name=project_model.name,
            _description=project_model.description,
            logo=project_model.logo,
            _status=StatusProject(project_model.status),
            created_at=project_model.created_at,
            assigned_to=AssignedId(project_model.assigned_to),
            participant_ids=[
                ParticipantId(participant.participant_id)
                for participant in project_model.participants
            ],
        )
        return project

    @staticmethod
    def entity_to_model(project: ProjectEntity) -> ProjectModel:
        project_model = ProjectModel(
            id=project.id,
            workspace_id=project.workspace_id,
            owner_id=project.owner_id,
            name=project.name,
            description=project.description,
            logo=project.logo,
            status=project.status.value,
            created_at=project.created_at,
            assigned_to=project.assigned_to,
        )
        if project.participant_ids:
            project_model.participants = [
                ProjectParticipantsModel(
                    workspace_id=project.workspace_id,
                    participant_id=participant,
                )
                for participant in project.participant_ids
            ]

        return project_model

    @staticmethod
    def entity_to_dict(project: ProjectEntity) -> dict[str, str | AssignedId]:
        return {
            'name': project.name,
            'description': project.description,
            'logo': project.logo,
            'status': project.status.value,
            'assigned_to': project.assigned_to,
        }

    @staticmethod
    def list_to_entity(
        projects: Sequence[ProjectModel],
        participants: Sequence[Row[tuple[int, UUID, str, str, str]]],
    ) -> list[tuple[ProjectEntity, list[dict[str, str]] | None]]:
        project_participants_map = defaultdict(list)

        for project_id, participant_id, first_name, last_name, avatar in participants:
            project_participants_map[project_id].append(
                {
                    'participant_id': participant_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'avatar': avatar,
                }
            )

        projects_with_participants = [
            (
                ProjectEntity(
                    _id=ProjectId(project.id),
                    _name=project.name,
                    _owner_id=OwnerId(project.owner_id),
                    _workspace_id=WorkspaceId(project.workspace_id),
                    _description=project.description,
                    logo=project.logo,
                    _status=StatusProject(project.status),
                    created_at=project.created_at,
                    assigned_to=AssignedId(project.assigned_to),
                ),
                project_participants_map.get(project.id, None),
            )
            for project in projects
        ]

        return projects_with_participants
