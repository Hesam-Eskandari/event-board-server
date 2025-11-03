from datetime import datetime
from typing import Dict

from src.domain.entities import Event, Category, Participant
from src.domain.exceptions import CategoryNotFoundException, CategoriesMismatchException, ParticipantNotFoundException, \
    ParticipantsMismatchException


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
