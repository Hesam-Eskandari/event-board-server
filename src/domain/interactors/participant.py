from typing import AsyncGenerator
from uuid import UUID

from src.domain.entities import Participant
from src.domain.interfaces import ParticipantDataProvider


class ParticipantInteractor:

    def __init__(self, data_provider: ParticipantDataProvider):
        self.dataProvider: ParticipantDataProvider = data_provider

    async def create_participant(self, p: Participant) -> Participant:
        return await self.dataProvider.create_participant(p)

    async def get_participant(self, pid: UUID) -> Participant:
        return await self.dataProvider.get_participant(pid)

    async def get_participants(self, limit: int, offset: int) -> AsyncGenerator[Participant]:
        async for participant in self.dataProvider.get_participants(limit, offset):
            yield participant

    async def update_participant(self, p: Participant) -> Participant:
        return await self.dataProvider.update_participant(p)

    async def remove_participant(self, pid: UUID) -> Participant:
        return await self.dataProvider.remove_participant(pid)
