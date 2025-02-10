from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from src.api.dtos.project import (
    CreateProjectRequestDTO,
    ProjectResponseDTO,
    UpdateProjectRequestDTO,
)
from src.apps.project.dtos import PaginationDTO, ProjectCreateDTO, ProjectUpdateDTO
from src.apps.project.interactors import (
    CreateProjectInteractor,
    DeleteProjectInteractor,
    GetProjectByWorkspaceInteractor,
    UpdateProjectInteractor,
)
from src.apps.project.use_cases.get_project_by_id import GetProjectByIdUseCase
from src.providers.context import WorkspaceContext

project_router = APIRouter(route_class=DishkaRoute)


@project_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_project(
    body: CreateProjectRequestDTO,
    interactor: FromDishka[CreateProjectInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    project = ProjectCreateDTO(
        **body.model_dump(exclude_none=True), workspace_id=context.workspace_id
    )
    await interactor.execute(project)


@project_router.get(
    '/{project_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProjectResponseDTO,
)
async def get_project_by_id(
    project_id: int,
    use_case: FromDishka[GetProjectByIdUseCase],
    context: FromDishka[WorkspaceContext],
) -> ProjectResponseDTO:
    project = await use_case.execute(project_id=project_id, workspace_id=context.workspace_id)
    return ProjectResponseDTO.model_validate(project)


@project_router.get('/', status_code=status.HTTP_200_OK, response_model=list[ProjectResponseDTO])
async def get_projects_in_workspace(
    interactor: FromDishka[GetProjectByWorkspaceInteractor],
    context: FromDishka[WorkspaceContext],
    page: int = Query(1, description='Page number', ge=1),
    page_size: int = Query(10, description='Number of roles per page', ge=5, le=100),
) -> list[ProjectResponseDTO]:
    projects_with_participants = await interactor.execute(
        workspace_id=context.workspace_id,
        pagination_data=PaginationDTO(page=page, page_size=page_size),
    )
    return [ProjectResponseDTO.model_validate(project) for project in projects_with_participants]


@project_router.patch('/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_project(
    body: UpdateProjectRequestDTO,
    project_id: int,
    interactor: FromDishka[UpdateProjectInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    updated_data = ProjectUpdateDTO(
        **body.model_dump(exclude_none=True),
        project_id=project_id,
        workspace_id=context.workspace_id,
    )
    await interactor.execute(updated_data)


@project_router.delete('/{project_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    interactor: FromDishka[DeleteProjectInteractor],
    context: FromDishka[WorkspaceContext],
) -> None:
    await interactor.execute(project_id=project_id, workspace_id=context.workspace_id)
