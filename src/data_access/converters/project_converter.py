from typing import Any, Sequence

from src.apps.project.domain.entity.project import Project, StatusProject
from src.apps.project.domain.types_ids import (
    AssignedId,
    OwnerId,
    ProjectId,
    WorkspaceId,
)
from src.data_access.models.project import ProjectModel
from src.data_access.models.project_participants import ProjectParticipantsModel


class ProjectConverter:
    @staticmethod
    def model_to_entity(project_model: ProjectModel) -> Project:
        project = Project(
            _id=ProjectId(project_model.id),
            _workspace_id=WorkspaceId(project_model.workspace_id),
            _owner_id=OwnerId(project_model.owner_id),
            _name=project_model.name,
            _description=project_model.description,
            logo=project_model.logo,
            _status=StatusProject(project_model.status),
            created_at=project_model.created_at,
            assigned_to=AssignedId(project_model.assigned_to),
        )
        return project

    @staticmethod
    def entity_to_model(project: Project) -> ProjectModel:
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
    def entity_to_dict(project: Project) -> dict[str, str | AssignedId]:
        return {
            'name': project.name,
            'description': project.description,
            'logo': project.logo,
            'status': project.status.value,
            'assigned_to': project.assigned_to,
        }

    @staticmethod
    def list_to_entity(projects_list: Sequence[Any]) -> list[tuple[Project, int]]:
        projects_with_user_count = []
        for project in projects_list:
            projects_with_user_count.append(
                (
                    Project(
                        _id=ProjectId(project[0].id),
                        _workspace_id=WorkspaceId(project[0].workspace_id),
                        _owner_id=OwnerId(project[0].owner_id),
                        _name=project[0].name,
                        _description=project[0].description,
                        logo=project[0].logo,
                        _status=project[0].status,
                        created_at=project[0].created_at,
                        assigned_to=project[0].assigned_to,
                    ),
                    project[1],
                )
            )

        return projects_with_user_count
