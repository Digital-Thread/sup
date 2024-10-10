from fastapi import FastAPI

from .health_check import router as health_check_router
from .meet import router as meet_router
from .meet_participant import router as meet_participant_router


def init_routes(app: FastAPI) -> None:
    prefix: str = '/api/v1'
    app.include_router(
        router=health_check_router,
        prefix=f'{prefix}/health-check',
        tags=['Test'],
    )

    meet_router.include_router(
        router=meet_participant_router,
        prefix='/{meet_id}/participants',
    )
    app.include_router(
        router=meet_router,
        prefix=f'{prefix}/meets',
        tags=['Meets'],
    )


__all__ = ('init_routes',)
