from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status

from src.api.dtos.project_dtos import (
    CreateProjectDTO,
    ResponseProjectDTO,
    UpdateProjectDTO,
)
from src.apps.project.dtos import CreateProjectAppDTO, UpdateProjectAppDTO
from src.apps.project.exceptions import ProjectException
from src.apps.project.interactors import (
    CreateProjectInteractor,
    DeleteProjectInteractor,
    GetProjectByWorkspaceInteractor,
    UpdateProjectInteractor,
)

project_router = APIRouter(route_class=DishkaRoute)


@project_router.post('', status_code=status.HTTP_201_CREATED)
async def create_project(
    body: CreateProjectDTO, interactor: FromDishka[CreateProjectInteractor]
) -> dict[str, str]:
    project = CreateProjectAppDTO(**body.model_dump(exclude_none=True))
    try:
        await interactor.execute(project)
    except ProjectException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return {'redirect_url': '/'}


@project_router.get('/', status_code=status.HTTP_200_OK, response_model=list[ResponseProjectDTO])
async def get_projects_by_workspace_id(
    workspace_id: UUID, interactor: FromDishka[GetProjectByWorkspaceInteractor]
) -> list[ResponseProjectDTO]:
    try:
        response = await interactor.execute(workspace_id)
    except ProjectException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    else:
        return [ResponseProjectDTO(**project.__dict__) for project in response]


@project_router.patch('/{project_id}', status_code=status.HTTP_200_OK)
async def update_project(
    body: UpdateProjectDTO,
    project_id: int,
    workspace_id: UUID,
    interactor: FromDishka[UpdateProjectInteractor],
) -> dict[str, str]:
    update_data = UpdateProjectAppDTO(**body.model_dump(exclude_none=True))
    try:
        await interactor.execute(project_id, workspace_id, update_data)
    except ProjectException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    else:
        return {'redirect_url': '/'}


@project_router.delete('/{project_id}', status_code=status.HTTP_200_OK)
async def delete_project(
    project_id: int, workspace_id: UUID, interactor: FromDishka[DeleteProjectInteractor]
) -> dict[str, str]:
    try:
        await interactor.execute(project_id, workspace_id)
    except ProjectException as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    else:
        return {'redirect_url': '/'}
