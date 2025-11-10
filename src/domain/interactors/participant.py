from typing import List, Iterator
from uuid import UUID

from src.domain.entities import Participant
from src.domain.interfaces import ParticipantDataProvider


class ParticipantInteractor:

    def __init__(self, data_provider: ParticipantDataProvider):
        self.dataProvider: ParticipantDataProvider = data_provider

    async def create_participant(self, p: Participant) -> Participant:
        return self.dataProvider.create_participant(p)

    async def get_participant(self, pid: UUID) -> Participant:
        return self.dataProvider.get_participant(pid)

    async def get_participants(self, limit: int, offset: int) -> Iterator[Participant]:
        return self.dataProvider.get_participants(limit, offset)

    async def update_participant(self, p: Participant) -> Participant:
        return self.dataProvider.update_participant(p)

    async def remove_participant(self, pid: UUID) -> Participant:
        return self.dataProvider.remove_participant(pid)
