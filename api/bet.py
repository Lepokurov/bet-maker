import time

from fastapi import APIRouter, Body, Depends, HTTPException

from controllers.bet import BetController
from db.models import User
from dependencies import get_bet_controller, get_user
from line_provider_client import LineProviderClient, get_line_provider_client
from schemas import BetModel

bet_router = APIRouter(prefix="/bets", tags=["bet"])


@bet_router.post("", summary="create bet")
async def create_bet(
    bet_data: BetModel = Body(...),
    controller: BetController = Depends(get_bet_controller),
    line_provider_client: LineProviderClient = Depends(get_line_provider_client),
    user: User = Depends(get_user)
):
    event = await line_provider_client.get_event(bet_data.event_id)
    if event.get("deadline", 0) < int(time.time()):
        raise HTTPException(status_code=400, detail="Event deadline is over")
    bet = await controller.create(data={"user_id": user.id, **bet_data.dict()})
    return bet


@bet_router.get("", summary="get bets")
async def get_bets(
    controller: BetController = Depends(get_bet_controller),
):
    bets = await controller.get_many()
    return bets


@bet_router.get("/my", summary="get bets")
async def get_my_bets(
    controller: BetController = Depends(get_bet_controller),
    user: User = Depends(get_user)
):
    bets = await controller.get_many(filters={"user_id": user.id})
    return bets
