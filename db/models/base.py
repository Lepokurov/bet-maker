from sqlalchemy import func, Column, DateTime, String

from db import BaseSQL


class BaseSQLModel(BaseSQL):
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

