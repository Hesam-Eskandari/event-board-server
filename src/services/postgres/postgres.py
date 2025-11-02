from typing import Dict, Iterator

from src.domain.entities import Participant
from src.domain.exceptions import ParticipantNotFoundException
from src.domain.interfaces import ParticipantDataProvider
from src.library import singleton

@singleton
class PgDataBase(ParticipantDataProvider):
    pid_max: int = 0
    participants: Dict[int, Participant] = {}

    def create_participant(self, p: Participant) -> Participant:
        self.pid_max += 1
        p.id = self.pid_max
        self.participants[p.id] = p
        return p

    def get_participant(self, pid: int) -> Participant:
        existing = self.participants.get(pid)
        if existing is None:
            raise ParticipantNotFoundException(f"Participant {pid} does not exist")
        return existing

    def get_participants(self, limit: int, offset: int = 0) -> Iterator[Participant]:
        limit = limit if limit > 0 else len(self.participants)
        return map(lambda e: e[1], filter(lambda e: offset <= e[0] < limit + offset, enumerate(iter(self.participants.values()))))

    def update_participant(self, p: Participant) -> Participant:
        existing = self.participants.get(p.id)
        print('updating')
        print(p)
        print(self.participants)
        if existing is None:
            raise ParticipantNotFoundException(f"Participant {p.id} does not exist")
        self.participants[p.id] = p
        return p

    def remove_participant(self, pid: int) -> Participant:
        existing = self.participants.get(pid)
        if existing is None:
            raise ParticipantNotFoundException(f"Participant {pid} does not exist")
        del self.participants[pid]
        return existing
