from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status

from src.api.dtos.project import (
    CreateProjectRequestDTO,
    ProjectResponseDTO,
    ProjectWithParticipantsResponseDTO,
    UpdateProjectRequestDTO,
)
from src.apps.project.dtos import ProjectCreateDTO, ProjectUpdateDTO
from src.apps.project.exceptions import ProjectException
from src.apps.project.interactors import (
    CreateProjectInteractor,
    DeleteProjectInteractor,
    GetProjectByWorkspaceInteractor,
    UpdateProjectInteractor,
)
from src.apps.project.use_cases.get_project_by_id import GetProjectByIdUseCase

project_router = APIRouter(route_class=DishkaRoute)


@project_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_project(
    body: CreateProjectRequestDTO, interactor: FromDishka[CreateProjectInteractor]
) -> dict[str, str]:
    project = ProjectCreateDTO(**body.model_dump(exclude_none=True))
    try:
        await interactor.execute(project)
    except ProjectException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return {'redirect_url': '/'}


@project_router.get(
    '/{project_id}',
    status_code=status.HTTP_200_OK,
    response_model=ProjectWithParticipantsResponseDTO,
)
async def get_project_by_id(
    project_id: int, use_case: FromDishka[GetProjectByIdUseCase]
) -> ProjectWithParticipantsResponseDTO:
    try:
        response = await use_case.execute(project_id)
    except ProjectException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    else:
        return ProjectWithParticipantsResponseDTO(**response.__dict__)


@project_router.get('/', status_code=status.HTTP_200_OK, response_model=list[ProjectResponseDTO])
async def get_projects_in_workspace(
    interactor: FromDishka[GetProjectByWorkspaceInteractor],
) -> list[ProjectResponseDTO]:
    try:
        response = await interactor.execute()
    except ProjectException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    else:
        return [ProjectResponseDTO(**project.__dict__) for project in response]


@project_router.patch('/{project_id}', status_code=status.HTTP_200_OK)
async def update_project(
    body: UpdateProjectRequestDTO,
    project_id: int,
    interactor: FromDishka[UpdateProjectInteractor],
) -> dict[str, str]:
    updated_data = ProjectUpdateDTO(**body.model_dump(exclude_none=True))
    try:
        await interactor.execute(project_id, updated_data)
    except ProjectException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    else:
        return {'redirect_url': '/'}


@project_router.delete('/{project_id}', status_code=status.HTTP_200_OK)
async def delete_project(
    project_id: int, interactor: FromDishka[DeleteProjectInteractor]
) -> dict[str, str]:
    try:
        await interactor.execute(project_id)
    except ProjectException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    else:
        return {'redirect_url': '/'}
