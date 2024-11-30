from typing import Awaitable, Callable
from uuid import UUID

from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute, Match
from starlette.middleware.base import BaseHTTPMiddleware


class WorkspaceMiddleware(BaseHTTPMiddleware):
    """
    Этот middleware необходим для работы с несколькими рабочими пространствами в рамках одного пользователя.
    Его задача — удостовериться, что данные каждого запроса связаны с правильным рабочим пространством.
    """
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        if  self._is_excluded_route(request):
            return await call_next(request)

        workspace_id = self._get_workspace_id_from_headers(request)
        if workspace_id is None:
            raise HTTPException(status_code=400, detail="Workspace ID is missing in request headers")

        request.state.workspace_id = workspace_id

        return await call_next(request)

    @staticmethod
    def _is_excluded_route(request: Request) -> bool:
        if request.url.path in ['/', '/openapi.json']:
            return True

        for route in request.app.routes:
            if isinstance(route, APIRoute):
                match, _ = route.matches(request.scope)
                if match == Match.FULL:
                    return 'Users' in route.tags

        return False

    @staticmethod
    def _get_workspace_id_from_headers(request: Request) -> UUID | None:
        workspace_id_str = request.headers.get("X-Workspace-Id")
        if workspace_id_str:
            try:
                return UUID(workspace_id_str)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid Workspace ID format")

        return None
