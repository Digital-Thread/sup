from fastapi import FastAPI

from .comment import comment_router
from .health_check import router


def init_routes(app: FastAPI) -> None:
    prefix: str = '/api/v1'
    app.include_router(
        router=router,
        prefix=f'{prefix}/health-check',
        tags=['Test'],
    )
    app.include_router(router=comment_router, prefix=f'{prefix}/comments', tags=['Comment'])


__all__ = ('init_routes',)
