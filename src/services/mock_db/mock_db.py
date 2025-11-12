from typing import Dict, AsyncGenerator
from uuid import UUID

from src.domain.entities import Participant, Category, Event
from src.domain.exceptions import RecordNotFoundException
from src.domain.interfaces import ParticipantDataProvider, CategoryDataProvider, EventDataProvider
from src.library import singleton


@singleton
class DataBaseMock(ParticipantDataProvider, CategoryDataProvider, EventDataProvider):
    participants: Dict[str, Participant] = {}
    categories: Dict[str, Category] = {}
    events: Dict[str, Event] = {}

    async def create_participant(self, p: Participant) -> Participant:
        self.participants[str(p.id)] = p
        return p

    async def get_participant(self, pid: UUID) -> Participant:
        existing = self.participants.get(str(pid))
        if existing is None:
            raise RecordNotFoundException(f'participant {pid} does not exist')
        return existing

    async def get_participants(self, limit: int, offset: int = 0) -> AsyncGenerator[Participant]:
        limit = limit if limit > 0 else len(self.participants)
        for participant in map(lambda e: e[1],
                               filter(lambda e: offset <= e[0] < limit + offset,
                                      enumerate(iter(self.participants.values())))):
            yield participant

    async def update_participant(self, p: Participant) -> Participant:
        existing = self.participants.get(str(p.id))
        if existing is None:
            raise RecordNotFoundException(f'participant {p.id} does not exist')
        self.participants[str(p.id)] = p
        return p

    async def remove_participant(self, pid: UUID) -> Participant:
        existing = self.participants.get(str(pid))
        if existing is None:
            raise RecordNotFoundException(f'participant {pid} does not exist')
        del self.participants[str(pid)]
        return existing

    async def create_category(self, c: Category) -> Category:
        self.categories[str(c.id)] = c
        return c

    async def get_category(self, cid: UUID) -> Category:
        existing = self.categories.get(str(cid))
        if existing is None:
            raise RecordNotFoundException(f'category {cid} does not exist')
        return existing

    async def get_categories(self, limit: int, offset: int = 0) -> AsyncGenerator[Category]:
        limit = limit if limit > 0 else len(self.categories)
        for category in map(lambda e: e[1],
                   filter(lambda e: offset <= e[0] < limit + offset,
                          enumerate(iter(self.categories.values())))):
            yield category

    async def update_category(self, c: Category) -> Category:
        existing = self.categories.get(str(c.id))
        if existing is None:
            raise RecordNotFoundException(f'category {c.id} does not exist')
        self.categories[str(c.id)] = c
        return existing

    async def remove_category(self, cid: UUID) -> Category:
        existing = self.categories.get(str(cid))
        if existing is None:
            raise RecordNotFoundException(f'category {cid} does not exist')
        del self.categories[str(cid)]
        return existing

    async def create_event(self, e: Event) -> Event:
        self.events[str(e.id)] = e
        return e

    async def get_event(self, eid: UUID) -> Event:
        event = self.events.get(str(eid))
        if event is None:
            raise RecordNotFoundException(f'event with id {eid} does not exist')
        return event

    async def get_events(self, limit: int, offset: int = 0) -> AsyncGenerator[Event]:
        limit = limit if limit > 0 else len(self.events)
        for event in map(lambda e: e[1],
                   filter(lambda e: offset <= e[0] < limit + offset,
                          enumerate(iter(self.events.values())))):
            yield event

    async def update_event(self, e: Event) -> Event:
        existing = self.events.get(str(e.id))
        if existing is None:
            raise RecordNotFoundException(f'event with id {e.id} does not exist')
        self.events[str(e.id)] = e
        return e

    async def remove_event(self, eid: UUID) -> Event:
        existing = self.events.get(str(eid))
        if existing is None:
            raise RecordNotFoundException(f'event with id {eid} does not exist')
        del self.events[str(eid)]
        return existing
