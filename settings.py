import os

DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DB_POOL_SIZE = 20
DB_MAX_OVERFLOW = 5

LINE_PROVIDER_API_HOST_URL = "localhost"
LINE_PROVIDER_API_TOKEN = "123"
SERVICE_NAME = "bet-maker"

try:
    from settings_local import *  # NOQA
except ImportError:
    pass

if DATABASE_USER and DATABASE_PASSWORD:
    SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
else:
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql+asyncpg://{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )
