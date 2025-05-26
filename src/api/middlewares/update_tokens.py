from typing import Awaitable, Callable

from fastapi import Request, Response


async def update_tokens_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response: Response = await call_next(request)
    access_token = getattr(request.state, 'new_access_token', None)
    refresh_token = getattr(request.state, 'new_refresh_token', None)
    max_age_access = getattr(request.state, 'max_age_access', None)
    max_age_refresh = getattr(request.state, 'max_age_refresh', None)
    if access_token and refresh_token:
        response.set_cookie('sup_access_token', access_token, httponly=True, max_age=max_age_access)
        response.set_cookie(
            'sup_refresh_token', refresh_token, httponly=True, max_age=max_age_refresh
        )
    return response
