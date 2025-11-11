from typing import AsyncGenerator
from uuid import UUID

from src.domain.entities import Event
from src.domain.interfaces import EventDataProvider


class EventInteractor:
    def __init__(self, data_provider: EventDataProvider):
        self._data_provider: EventDataProvider = data_provider

    async def create_event(self, e: Event) -> Event:
        return await self._data_provider.create_event(e)

    async def get_event(self, eid: UUID) -> Event:
        return await self._data_provider.get_event(eid)

    async def get_events(self, limit: int, offset: int = 0) -> AsyncGenerator[Event, None]:
        async for event in self._data_provider.get_events(limit, offset):
            yield event

    async def update_event(self, e: Event) -> Event:
        return await self._data_provider.update_event(e)

    async def remove_event(self, eid: UUID) -> Event:
        return await self._data_provider.remove_event(eid)
