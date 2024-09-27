from fastapi import FastAPI

from .health_check import router as health_check_router
from .meet import router as meet_router


def init_routes(app: FastAPI) -> None:
    prefix: str = '/api/v1'
    app.include_router(
        router=health_check_router,
        prefix=f'{prefix}/health-check',
        tags=['Test'],
    )
    app.include_router(
        router=meet_router,
        prefix=f'{prefix}/meet',
        tags=['Meets'],
    )


__all__ = ('init_routes',)
