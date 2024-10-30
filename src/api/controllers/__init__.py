from fastapi import FastAPI

from .category import category_router
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
    app.include_router(router=category_router, prefix=f'{prefix}/category', tags=['Category'])


__all__ = ('init_routes',)
