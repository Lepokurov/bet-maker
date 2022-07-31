from fastapi import FastAPI
from api import ping_router

app = FastAPI(
    title="line-provider",
    version="1.0.0",
    description="Сервис line-provide",
)

app.include_router(ping_router)