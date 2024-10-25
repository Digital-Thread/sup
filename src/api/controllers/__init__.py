from fastapi import FastAPI

from .health_check import router
from .workspace import workspace_router


def init_routes(app: FastAPI) -> None:
    prefix: str = '/api/v1'
    app.include_router(
        router=router,
        prefix=f'{prefix}/health-check',
        tags=['Test'],
    )
    app.include_router(router=workspace_router, prefix=f'{prefix}/workspace', tags=['Workspace'])


__all__ = ('init_routes',)
