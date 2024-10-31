from src.apps.project.domain.entity.project import Project, StatusProject
from src.apps.project.domain.types_ids import (
    AssignedId,
    OwnerId,
    ProjectId,
    WorkspaceId,
)
from src.data_access.models.project import ProjectModel


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
        model = ProjectModel(
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
        return model

    @staticmethod
    def entity_to_dict(project: Project) -> dict[str, str | AssignedId]:
        return {
            'name': project.name,
            'description': project.description,
            'logo': project.logo,
            'status': project.status.value,
            'assigned_to': project.assigned_to,
        }
