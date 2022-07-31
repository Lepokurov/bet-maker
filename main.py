from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from api import ping_router, bet_router, login_router, event_router
from controllers.errors import controller_exceptions_handler

app = FastAPI(
    title="bet-maker",
    version="1.0.0",
    description="Сервис bet-maker",
)

app.include_router(ping_router)
app.include_router(bet_router)
app.include_router(login_router)
app.include_router(event_router)

app.add_exception_handler(SQLAlchemyError, controller_exceptions_handler)
