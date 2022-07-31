from fastapi import Depends, HTTPException

from controllers.bet import BetController
from controllers.user import UserController
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from settings import INNER_TOKEN

auth = HTTPBearer(description="токен авторизации")


async def get_bet_controller() -> BetController:
    async with BetController() as controller_session:
        yield controller_session


async def get_user_controller() -> UserController:
    async with UserController() as controller_session:
        yield controller_session


async def get_user(
    authorization: HTTPAuthorizationCredentials = Depends(auth),
    controller: UserController = Depends(get_user_controller),
):
    user = await controller.get_one(filters={"token": authorization.credentials})
    if user:
        return user
    raise HTTPException(status_code=403, detail="Invalid user auth token")


def check_inner_token(authorization: HTTPAuthorizationCredentials = Depends(auth)):
    """Проверка статичного токена."""
    if authorization.credentials == INNER_TOKEN:
        return
    raise HTTPException(status_code=403, detail="Invalid inner auth token")
