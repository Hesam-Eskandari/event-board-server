from typing import List

from src.domain.entities import Participant
from src.domain.interfaces import ParticipantDataProvider


class ParticipantInteractor:

    def __init__(self, data_provider: ParticipantDataProvider):
        self.dataProvider: ParticipantDataProvider = data_provider

    def create_participant(self, p: Participant) -> Participant:
        return self.dataProvider.create_participant(p)

    def read_participant(self, pid: int) -> Participant:
        return self.dataProvider.get_participant(pid)

    def read_participants(self, limit: int, offset: int) -> List[Participant]:
        return list(self.dataProvider.get_participants(limit, offset))

    def update_participant(self, p: Participant) -> Participant:
        return self.dataProvider.update_participant(p)

    def remove_participant(self, pid: int) -> Participant:
        return self.dataProvider.remove_participant(pid)
