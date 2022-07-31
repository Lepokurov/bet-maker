from fastapi import APIRouter

ping_router = APIRouter(prefix="/ping", tags=["ping"])


@ping_router.get("", summary="Check connection")
async def ping():
    return {"message": "Pong!"}
