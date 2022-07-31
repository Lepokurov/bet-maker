from fastapi import APIRouter, Depends, Response
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db_session

ping_router = APIRouter(prefix="/ping", tags=["ping"])


@ping_router.get("", summary="Проверка доступности")
async def ping(db_session: AsyncSession = Depends(get_db_session)):
    try:
        await db_session.execute(text("SELECT 1"))
    except Exception as err:
        return Response(status_code=503)
    return {"message": "Pong!"}
