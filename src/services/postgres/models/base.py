from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class EventBoardBase(DeclarativeBase):
    metadata = MetaData(schema="event_board")


class TenantBase(DeclarativeBase):
    metadata = MetaData(schema="tenant")

