from typing import Iterator

from src.domain.entities import Event
from src.domain.interfaces import EventDataProvider


class EventInteractor:
    def __init__(self, data_provider: EventDataProvider):
        self._data_provider: EventDataProvider = data_provider

    def create_event(self, e: Event) -> Event:
        return self._data_provider.create_event(e)

    def get_event(self, eid: int) -> Event:
        return self._data_provider.get_event(eid)

    def get_events(self, limit: int, offset: int = 0) -> Iterator[Event]:
        return self._data_provider.get_events(limit, offset)

    def update_event(self, e: Event) -> Event:
        return self._data_provider.update_event(e)

    def remove_event(self, eid: int) -> Event:
        return self._data_provider.remove_event(eid)
