from dataclasses import asdict
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from src.api.dtos.task import (
    CreateTaskRequestDTO,
    QueryParams,
    SuccessResponse,
    TaskResponseDTO,
    UpdateTaskRequestDTO,
)
from src.apps.task import (
    CreateTaskInteractor,
    DeleteTaskInteractor,
    GetAllTasksInteractor,
    GetTaskInteractor,
    TaskInputDTO,
    TaskUpdateDTO,
    UpdateTaskInteractor,
)
from src.apps.task.domain import OptionalTaskUpdateFields, TaskId
from src.apps.task.repositories import TaskListQuery
from apps.task.task_repository import OrderBy, PaginateParams

task_router = APIRouter(route_class=DishkaRoute)


@task_router.post('/', status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
async def create_task(
        dto: CreateTaskRequestDTO,
        interactor: FromDishka[CreateTaskInteractor],
) -> SuccessResponse:
    task = TaskInputDTO(**dto.model_dump())
    await interactor.execute(dto=task)

    return SuccessResponse(message='Task created')


@task_router.get('/', status_code=status.HTTP_200_OK, response_model=list[TaskResponseDTO])
async def get_tasks(
        query: Annotated[QueryParams, Query()],
        interactor: FromDishka[GetAllTasksInteractor],
) -> list[TaskResponseDTO]:
    feature_id = query.feature_id
    query_params = TaskListQuery(
        order_by=OrderBy(field=query.order_by_field, order=query.sort_order),
        paginate_by=PaginateParams(offset=query.offset, limit_by=query.per_page.limit_by),
    )
    tasks = await interactor.execute(feature_id=feature_id, query=query_params)
    return [TaskResponseDTO(**asdict(task)) for task in tasks] if tasks else []


@task_router.get(
    '/{task_id}', status_code=status.HTTP_200_OK, response_model=TaskResponseDTO
)
async def get_task_by_id(
        task_id: TaskId,
        interactor: FromDishka[GetTaskInteractor],
) -> TaskResponseDTO:
    task = await interactor.execute(task_id=task_id)
    return TaskResponseDTO(**asdict(task))


@task_router.patch(
    '/{task_id}', status_code=status.HTTP_200_OK, response_model=SuccessResponse
)
async def update_task(
        task_id: TaskId,
        dto: UpdateTaskRequestDTO,
        interactor: FromDishka[UpdateTaskInteractor],
) -> SuccessResponse:
    update_data = TaskUpdateDTO(
        id=task_id,
        updated_fields=OptionalTaskUpdateFields(**dto.model_dump(exclude_unset=True)),
    )
    await interactor.execute(update_data)
    return SuccessResponse(message='Task updated')


@task_router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: TaskId,
        interactor: FromDishka[DeleteTaskInteractor],
) -> None:
    await interactor.execute(task_id=task_id)
