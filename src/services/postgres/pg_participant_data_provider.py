import sys
from typing import AsyncGenerator
from uuid import UUID

from sqlalchemy import select, ScalarResult, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Participant
from src.domain.exceptions import RecordNotFoundException
from src.domain.interfaces import ParticipantDataProvider
from src.services.postgres.models import ParticipantModel
from src.services.postgres.pg_base import PgBase


class PgParticipantDataProvider(PgBase, ParticipantDataProvider):
    async def create_participant(self, p: Participant) -> Participant:
        session: AsyncSession
        async with self._setup_connection() as session:
            participant_model: ParticipantModel = ParticipantModel.from_entity(p)
            session.add(participant_model)
            await session.commit()
            await session.refresh(participant_model)
            return participant_model.to_entity()

    async def get_participant(self, pid: UUID) -> Participant:
        session: AsyncSession
        async with self._setup_connection() as session:
            stmt = select(ParticipantModel).where(ParticipantModel.is_deleted.is_(False)).where(ParticipantModel.id == pid)
            model: ParticipantModel | None = await session.scalar(stmt)
            if model is None:
                raise RecordNotFoundException(f"participant {pid} not found")
            entity = model.to_entity()
            return entity


    async def get_participants(self, limit: int, offset: int = 0) -> AsyncGenerator[Participant]:
        limit = limit if limit > 0 else sys.maxsize
        session: AsyncSession
        async with self._setup_connection() as session:
            stmt = select(ParticipantModel).where(ParticipantModel.is_deleted.is_(False)).limit(limit).offset(offset)
            models: ScalarResult[ParticipantModel] = await session.scalars(stmt)
            for model in models.all():
                yield model.to_entity()

    async def update_participant(self, p: Participant) -> Participant:
        session: AsyncSession
        async with self._setup_connection() as session:
            model = ParticipantModel.from_entity(p)
            stmt = (
                update(ParticipantModel)
                .where(ParticipantModel.is_deleted.is_(False))
                .where(ParticipantModel.id == p.id)
                .values(**model.to_dict(exclude_id=True, exclude_fields=['is_deleted', 'created_at']))
            .returning(ParticipantModel)
            )
            result = await session.execute(stmt)
            updated_model: ParticipantModel | None = result.scalar_one_or_none()
            if updated_model is None:
                raise RecordNotFoundException(f"participant {p.id} not found")
            await session.commit()
            return updated_model.to_entity()

    async def remove_participant(self, pid: UUID) -> Participant:
        session: AsyncSession
        async with self._setup_connection() as session:
            stmt = (
                update(ParticipantModel)
                .where(ParticipantModel.is_deleted.is_(False))
                .where(ParticipantModel.id == pid)
                .values(is_deleted=True)
                .returning(ParticipantModel)
            )

            result = await session.execute(stmt)
            deleted_model: ParticipantModel | None = result.scalar_one_or_none()
            if deleted_model is None:
                raise RecordNotFoundException(f"participant {pid} not found")

            await session.commit()
            return deleted_model.to_entity()
