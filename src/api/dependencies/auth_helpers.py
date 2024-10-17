from fastapi import Request

from src.apps.user.dtos import UserResponseDTO
from src.apps.user.services import GetUserService


async def authenticate_and_create_tokens(
    request: Request,
    get_user_service: GetUserService,
) -> UserResponseDTO:
    user_agent = request.headers.get('User-Agent')
    access_token = request.cookies.get('sup_access_token')
    refresh_token = request.cookies.get('sup_refresh_token')
    user, new_access_token, max_age_access, new_refresh_token, max_age_refresh = (
        await get_user_service.get_user_info(
            access_token=access_token, refresh_token=refresh_token, user_agent=user_agent
        )
    )

    if new_access_token and new_refresh_token:
        request.state.new_access_token = new_access_token
        request.state.new_refresh_token = new_refresh_token
        request.state.max_age_access = max_age_access
        request.state.max_age_refresh = max_age_refresh
    return user
