from fastapi import APIRouter, Body, Depends

from controllers.user import UserController
from dependencies import get_user_controller
from schemas import UserLoginModel, UserModel

login_router = APIRouter(prefix="/login", tags=["login"])


@login_router.post("", summary="login user", response_model=UserModel)
async def login(
    user_data: UserLoginModel = Body(...),
    controller: UserController = Depends(get_user_controller),
):
    user = await controller.login(data=user_data.dict())
    return user

