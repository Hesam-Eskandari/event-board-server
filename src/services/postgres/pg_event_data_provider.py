import sys
from typing import AsyncGenerator
from uuid import UUID

from sqlalchemy import select, ScalarResult, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.entities import Event
from src.domain.exceptions import RecordNotFoundException
from src.domain.interfaces import EventDataProvider
from src.services.postgres.models import EventModel
from src.services.postgres.pg_base import PgBase


class PgEventDataProvider(PgBase, EventDataProvider):
    async def create_event(self, e: Event) -> Event:
        session: AsyncSession
        async with self._setup_connection() as session:
            event_model: EventModel = EventModel.from_entity(e)
            session.add(event_model)
            await session.commit()
            stmt = select(EventModel) \
                .where(EventModel.is_deleted.is_(False)) \
                .where(EventModel.id == e.id) \
                .options(
                selectinload(EventModel.category),
                selectinload(EventModel.participant)
            )
            persisted_model: EventModel | None = await session.scalar(stmt)
            return persisted_model.to_entity()

    async def get_event(self, eid: UUID) -> Event:
        session: AsyncSession
        async with (self._setup_connection() as session):
            stmt = select(EventModel)\
                .where(EventModel.is_deleted.is_(False))\
                .where(EventModel.id == eid)\
                .options(
                    selectinload(EventModel.category),
                    selectinload(EventModel.participant)
                )
            model: EventModel | None = await session.scalar(stmt)
            if model is None:
                raise RecordNotFoundException(f"event {eid} not found")
            return model.to_entity()

    async def get_events(self, limit: int, offset: int = 0) -> AsyncGenerator[Event]:
        limit = limit if limit > 0 else sys.maxsize
        session: AsyncSession
        async with self._setup_connection() as session:
            stmt = select(EventModel)\
                .where(EventModel.is_deleted.is_(False))\
                .limit(limit).offset(offset)\
                .options(
                    selectinload(EventModel.category),
                    selectinload(EventModel.participant)
                )
            models: ScalarResult[EventModel] = await session.scalars(stmt)
            for model in models.all():
                yield model.to_entity()

    async def update_event(self, e: Event) -> Event:
        session: AsyncSession
        async with self._setup_connection() as session:
            model = EventModel.from_entity(e)
            stmt = (
                update(EventModel)
                .where(EventModel.is_deleted.is_(False))
                .where(EventModel.id == e.id)
                .options(
                    selectinload(EventModel.category),
                    selectinload(EventModel.participant),
                )
                .values(**model.to_dict(exclude_id=True, exclude_fields=['is_deleted', 'created_at']))
            .returning(EventModel)
            )
            result = await session.execute(stmt)
            updated_model: EventModel | None = result.scalar_one_or_none()
            if updated_model is None:
                raise RecordNotFoundException(f"event {e.id} not found")
            await session.commit()
            return updated_model.to_entity()

    async def remove_event(self, eid: UUID) -> Event:
        session: AsyncSession
        async with self._setup_connection() as session:
            stmt = (
                update(EventModel)
                .where(EventModel.is_deleted.is_(False))
                .where(EventModel.id == eid)
                .options(
                    selectinload(EventModel.category),
                    selectinload(EventModel.participant),
                )
                .values(is_deleted=True)
                .returning(EventModel)
            )

            result = await session.execute(stmt)
            deleted_model: EventModel | None = result.scalar_one_or_none()
            if deleted_model is None:
                raise RecordNotFoundException(f"event {eid} not found")

            await session.commit()
            return deleted_model.to_entity()
