from typing import Tuple, List

from src.entities import Participant
from src.services.postgres.postgres import PgDataBase


class ParticipantInteractor:

    def __init__(self):
        self.dataProvider = PgDataBase()

    def create_participant(self, p: Participant) -> Tuple[Participant | None, str | None]:
        try:
            participant = self.dataProvider.create_participant(p)
        except Exception as e:
            return None, 'failed to create participant'
        return participant, None

    def read_participant(self, pid: int) -> Tuple[Participant | None, str | None]:
        try:
            participant = self.dataProvider.get_participant(pid)
        except Exception as e:
            return None, 'failed to get participant'
        return participant, None

    def read_participants(self, limit: int, offset: int) -> Tuple[List[Participant] | None, str | None]:
        try:
            participants = self.dataProvider.get_participants(limit, offset)
        except Exception as e:
            return None, 'failed to get participants'
        return list(participants), None

    def update_participant(self, p: Participant) -> Tuple[Participant | None, str | None]:
        try:
            participant = self.dataProvider.update_participant(p)
        except Exception as e:
            return None, 'failed to update participant'
        return participant, None

    def remove_participant(self, pid: int) -> Tuple[Participant | None, str | None]:
        try:
            participant = self.dataProvider.remove_participant(pid)
        except Exception as e:
            return None, 'failed to remove participant'
        return participant, None
