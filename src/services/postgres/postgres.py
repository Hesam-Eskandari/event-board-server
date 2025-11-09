from typing import Dict, Iterator
from uuid import UUID

from src.domain.entities import Participant, Category, Event
from src.domain.exceptions import (
    ParticipantNotFoundException, CategoryNotFoundException, EventNotFoundException)
from src.domain.interfaces import ParticipantDataProvider, CategoryDataProvider, EventDataProvider
from src.library import singleton
from src.services.postgres.models import EventModel


@singleton
class PgDataBase(ParticipantDataProvider, CategoryDataProvider, EventDataProvider):
    eid_max: int = 0
    participants: Dict[str, Participant] = {}
    categories: Dict[str, Category] = {}
    events: Dict[int, EventModel] = {}

    def create_participant(self, p: Participant) -> Participant:
        self.participants[str(p.id)] = p
        return p

    def get_participant(self, pid: UUID) -> Participant:
        existing = self.participants.get(str(pid))
        if existing is None:
            raise ParticipantNotFoundException(f'participant {pid} does not exist')
        return existing

    def get_participants(self, limit: int, offset: int = 0) -> Iterator[Participant]:
        limit = limit if limit > 0 else len(self.participants)
        return map(lambda e: e[1], filter(lambda e: offset <= e[0] < limit + offset, enumerate(iter(self.participants.values()))))

    def update_participant(self, p: Participant) -> Participant:
        existing = self.participants.get(str(p.id))
        if existing is None:
            raise ParticipantNotFoundException(f'participant {p.id} does not exist')
        self.participants[str(p.id)] = p
        return p

    def remove_participant(self, pid: UUID) -> Participant:
        existing = self.participants.get(str(pid))
        if existing is None:
            raise ParticipantNotFoundException(f'participant {pid} does not exist')
        del self.participants[str(pid)]
        return existing

    def create_category(self, c: Category) -> Category:
        self.categories[str(c.id)] = c
        return c

    def get_category(self, cid: UUID) -> Category:
        existing = self.categories.get(str(cid))
        if existing is None:
            raise CategoryNotFoundException(f'category {cid} does not exist')
        return existing

    def get_categories(self, limit: int, offset: int = 0) -> Iterator[Category]:
        limit = limit if limit > 0 else len(self.categories)
        return map(lambda e: e[1],
                   filter(lambda e: offset <= e[0] < limit + offset, enumerate(iter(self.categories.values()))))

    def update_category(self, c: Category) -> Category:
        existing = self.categories.get(str(c.id))
        if existing is None:
            raise CategoryNotFoundException(f'category {c.id} does not exist')
        self.categories[str(c.id)] = c
        return existing

    def remove_category(self, cid: UUID) -> Category:
        existing = self.categories.get(str(cid))
        if existing is None:
            raise CategoryNotFoundException(f'category {cid} does not exist')
        del self.categories[str(cid)]
        return existing

    def create_event(self, e: Event) -> Event:
        e.id = self.eid_max
        model = EventModel.from_entity(e, self.categories, self.participants)
        self.eid_max += 1
        self.events[model.id] = model
        return e

    def get_event(self, eid: int) -> Event:
        model = self.events.get(eid)
        if model is None:
            raise EventNotFoundException(f'event with id {eid} does not exist')
        event = model.to_entity(categories=self.categories, participants=self.participants)
        return event

    def get_events(self, limit: int, offset: int = 0) -> Iterator[Event]:
        limit = limit if limit > 0 else len(self.events)
        models: Iterator[EventModel] = map(lambda e: e[1], filter(lambda e: offset <= e[0] < limit + offset, enumerate(iter(self.events.values()))))
        return map(lambda m: m.to_entity(categories=self.categories, participants=self.participants), models)

    def update_event(self, e: Event) -> Event:
        existing = self.events.get(e.id)
        if existing is None:
            raise EventNotFoundException(f'event with id {e.id} does not exist')
        model = EventModel.from_entity(e, self.categories, self.participants)
        self.events[e.id] = model
        return e

    def remove_event(self, eid: int) -> Event:
        existing = self.events.get(eid)
        if existing is None:
            raise EventNotFoundException(f'event with id {eid} does not exist')
        del self.events[eid]
        event = existing.to_entity(categories=self.categories, participants=self.participants)
        return event
