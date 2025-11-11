from typing import Dict, Iterator
from uuid import UUID

from src.domain.entities import Participant, Category, Event
from src.domain.exceptions import (
    ParticipantNotFoundException, CategoryNotFoundException, EventNotFoundException)
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
            raise ParticipantNotFoundException(f'participant {pid} does not exist')
        return existing

    async def get_participants(self, limit: int, offset: int = 0) -> Iterator[Participant]:
        limit = limit if limit > 0 else len(self.participants)
        return map(lambda e: e[1], filter(lambda e: offset <= e[0] < limit + offset, enumerate(iter(self.participants.values()))))

    async def update_participant(self, p: Participant) -> Participant:
        existing = self.participants.get(str(p.id))
        if existing is None:
            raise ParticipantNotFoundException(f'participant {p.id} does not exist')
        self.participants[str(p.id)] = p
        return p

    async def remove_participant(self, pid: UUID) -> Participant:
        existing = self.participants.get(str(pid))
        if existing is None:
            raise ParticipantNotFoundException(f'participant {pid} does not exist')
        del self.participants[str(pid)]
        return existing

    async def create_category(self, c: Category) -> Category:
        self.categories[str(c.id)] = c
        return c

    async def get_category(self, cid: UUID) -> Category:
        existing = self.categories.get(str(cid))
        if existing is None:
            raise CategoryNotFoundException(f'category {cid} does not exist')
        return existing

    async def get_categories(self, limit: int, offset: int = 0) -> Iterator[Category]:
        limit = limit if limit > 0 else len(self.categories)
        return map(lambda e: e[1],
                   filter(lambda e: offset <= e[0] < limit + offset, enumerate(iter(self.categories.values()))))

    async def update_category(self, c: Category) -> Category:
        existing = self.categories.get(str(c.id))
        if existing is None:
            raise CategoryNotFoundException(f'category {c.id} does not exist')
        self.categories[str(c.id)] = c
        return existing

    async def remove_category(self, cid: UUID) -> Category:
        existing = self.categories.get(str(cid))
        if existing is None:
            raise CategoryNotFoundException(f'category {cid} does not exist')
        del self.categories[str(cid)]
        return existing

    def create_event(self, e: Event) -> Event:
        self.events[str(e.id)] = e
        return e

    def get_event(self, eid: UUID) -> Event:
        event = self.events.get(str(eid))
        if event is None:
            raise EventNotFoundException(f'event with id {eid} does not exist')
        return event

    def get_events(self, limit: int, offset: int = 0) -> Iterator[Event]:
        limit = limit if limit > 0 else len(self.events)
        return map(lambda e: e[1],
                   filter(lambda e: offset <= e[0] < limit + offset, enumerate(iter(self.events.values()))))

    def update_event(self, e: Event) -> Event:
        existing = self.events.get(str(e.id))
        if existing is None:
            raise EventNotFoundException(f'event with id {e.id} does not exist')
        self.events[str(e.id)] = e
        return e

    def remove_event(self, eid: UUID) -> Event:
        existing = self.events.get(str(eid))
        if existing is None:
            raise EventNotFoundException(f'event with id {eid} does not exist')
        del self.events[str(eid)]
        return existing
