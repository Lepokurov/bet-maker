from fastapi import APIRouter, Depends, Query, Body, Response

from controllers.bet import BetController
from dependencies import get_bet_controller, check_inner_token
from line_provider_client import LineProviderClient, get_line_provider_client
from schemas import EventStatusModel

event_router = APIRouter(prefix="", tags=["event"])


@event_router.get("api/events")
async def get_events(
    line_provider_client: LineProviderClient = Depends(get_line_provider_client),
):
    data = await line_provider_client.get_events()
    return data


@event_router.put("in/events/status", dependencies=[Depends(check_inner_token)])
async def change_event_status(
    controller: BetController = Depends(get_bet_controller),
    event_status_data: EventStatusModel = Body(...),
):
    await controller.update_bet_state(event_status_data.dict())
    return Response()
