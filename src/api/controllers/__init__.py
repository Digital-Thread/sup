from fastapi import FastAPI

from .health_check import router
from .user import router as user_router


def init_routes(app: FastAPI) -> None:
    prefix: str = '/api/v1'
    app.include_router(
        router=router,
        prefix=f'{prefix}/health-check',
        tags=['Test'],
    )
    app.include_router(
        router=user_router,
        prefix=f'{prefix}/user',
        tags=['Users'],
    )


__all__ = ('init_routes',)
