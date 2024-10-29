from fastapi import FastAPI

from .health_check import router
from .role import role_router
from .tag import tag_router
from .workspace import workspace_router


def init_routes(app: FastAPI) -> None:
    prefix: str = '/api/v1'
    app.include_router(
        router=router,
        prefix=f'{prefix}/health-check',
        tags=['Test'],
    )
    app.include_router(router=workspace_router, prefix=f'{prefix}/workspace', tags=['Workspace'])
    app.include_router(router=role_router, prefix=f'{prefix}/role', tags=['Role'])
    app.include_router(router=tag_router, prefix=f'{prefix}/tag', tags=['Tag'])


__all__ = ('init_routes',)
