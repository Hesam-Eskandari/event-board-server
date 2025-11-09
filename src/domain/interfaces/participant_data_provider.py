from abc import ABC
from typing import Iterator
from uuid import UUID

from src.domain.entities import Participant


class ParticipantDataProvider(ABC):
    def create_participant(self, p: Participant) -> Participant:
        raise NotImplementedError('create_participant is not implemented')

    def get_participant(self, pid: UUID) -> Participant:
        raise NotImplementedError('get_participant is not implemented')

    def get_participants(self, limit: int, offset: int = 0) -> Iterator[Participant]:
        raise NotImplementedError('get_participants is not implemented')

    def update_participant(self, p: Participant) -> Participant:
        raise NotImplementedError('update_participant is not implemented')

    def remove_participant(self, pid: UUID) -> Participant:
        raise NotImplementedError('remove_participant is not implemented')
