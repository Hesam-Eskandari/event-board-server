from datetime import datetime
from typing import Dict, Iterator

from src.domain.entities import Participant, Category, Event
from src.domain.exceptions import (
    ParticipantNotFoundException, CategoryNotFoundException, EventNotFoundException,
    CategoriesMismatchException, ParticipantsMismatchException )
from src.domain.interfaces import ParticipantDataProvider, CategoryDataProvider, EventDataProvider
from src.library import singleton

class EventModel:
    id: int
    title: str
    start: datetime
    end: datetime
    category_id: int
    participant_id: int

    @staticmethod
    def from_entity(entity: Event, categories: Dict[int, Category], participants: Dict[int, Participant]) -> EventModel:
        existing_category = categories.get(entity.category.id)
        if existing_category is None:
            raise CategoryNotFoundException(f'category {entity.category.id} does not exist')
        if existing_category != entity.category:
            raise CategoriesMismatchException(f'found category with id {existing_category.id}, but other properties of the given category do not match')
        existing_participant = participants.get(entity.participant.id)
        if existing_participant is None:
            raise ParticipantNotFoundException(f'participant {entity.participant.id} does not exist')
        if existing_participant != entity.participant:
            raise ParticipantsMismatchException(f'found participant with id {entity.participant.id} but other properties of the given participant do not match')
        model = EventModel()
        model.id = entity.id
        model.title = entity.title
        model.start = entity.start
        model.end = entity.end
        model.category_id = entity.category.id
        model.participant_id = entity.participant.id
        return model

    def to_entity(self, categories: Dict[int, Category], participants: Dict[int, Participant]) -> Event:
        entity = Event()
        entity.id = self.id
        entity.title = self.title
        entity.start = self.start
        entity.end = self.end
        category = categories.get(self.category_id)
        if category is None:
            raise CategoryNotFoundException(f'category with id {self.category_id} not found')
        participant = participants.get(self.participant_id)
        if participant is None:
            raise ParticipantNotFoundException(f'participant with id {self.participant_id} not found')
        entity.category = category
        entity.participant = participant
        return entity


@singleton
class PgDataBase(ParticipantDataProvider, CategoryDataProvider, EventDataProvider):
    pid_max: int = 0
    cid_max: int = 0
    eid_max: int = 0
    participants: Dict[int, Participant] = {}
    categories: Dict[int, Category] = {}
    events: Dict[int, EventModel] = {}

    def create_participant(self, p: Participant) -> Participant:
        p.id = self.pid_max
        self.pid_max += 1
        self.participants[p.id] = p
        return p

    def get_participant(self, pid: int) -> Participant:
        existing = self.participants.get(pid)
        if existing is None:
            raise ParticipantNotFoundException(f'participant {pid} does not exist')
        return existing

    def get_participants(self, limit: int, offset: int = 0) -> Iterator[Participant]:
        limit = limit if limit > 0 else len(self.participants)
        return map(lambda e: e[1], filter(lambda e: offset <= e[0] < limit + offset, enumerate(iter(self.participants.values()))))

    def update_participant(self, p: Participant) -> Participant:
        existing = self.participants.get(p.id)
        if existing is None:
            raise ParticipantNotFoundException(f'participant {p.id} does not exist')
        self.participants[p.id] = p
        return p

    def remove_participant(self, pid: int) -> Participant:
        existing = self.participants.get(pid)
        if existing is None:
            raise ParticipantNotFoundException(f'participant {pid} does not exist')
        del self.participants[pid]
        return existing

    def create_category(self, c: Category) -> Category:
        c.id = self.cid_max
        self.cid_max += 1
        self.categories[c.id] = c
        return c

    def get_category(self, cid: int) -> Category:
        existing = self.categories.get(cid)
        if existing is None:
            raise CategoryNotFoundException(f'category {cid} does not exist')
        return existing

    def get_categories(self, limit: int, offset: int = 0) -> Iterator[Category]:
        limit = limit if limit > 0 else len(self.categories)
        return map(lambda e: e[1],
                   filter(lambda e: offset <= e[0] < limit + offset, enumerate(iter(self.categories.values()))))

    def update_category(self, c: Category) -> Category:
        existing = self.categories.get(c.id)
        if existing is None:
            raise CategoryNotFoundException(f'category {c.id} does not exist')
        self.categories[c.id] = c
        return c

    def remove_category(self, cid: int) -> Category:
        existing = self.categories.get(cid)
        if existing is None:
            raise CategoryNotFoundException(f'category {cid} does not exist')
        del self.categories[cid]
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
