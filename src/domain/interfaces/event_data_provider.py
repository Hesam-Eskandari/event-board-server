from abc import ABC
from typing import Iterator
from uuid import UUID

from src.domain.entities import Event


class EventDataProvider(ABC):
    def create_event(self, e: Event) -> Event:
        raise NotImplementedError('create_event is not implemented')

    def get_event(self, eid: UUID) -> Event:
        raise NotImplementedError('get_event is not implemented')

    def get_events(self, limit: int, offset: int = 0) -> Iterator[Event]:
        raise NotImplementedError('get_events is not implemented')

    def update_event(self, e: Event) -> Event:
        raise NotImplementedError('update_event is not implemented')

    def remove_event(self, eid: UUID) -> Event:
        raise NotImplementedError('remove_event is not implemented')
