from datetime import datetime

from src.controllers.dtos.base import BaseDTO
from src.domain.entities import Category, Event, Participant


class EventPatchDTO(BaseDTO):
    title: str | None = None
    start: str | None = None
    end: str | None = None
    categoryId: str | None = None
    participantId: str | None = None

    def to_entity(self, old_entity: Event, c: Category, p: Participant) -> Event:
        entity: Event = Event()
        entity.title = self.title if self.title is not None else old_entity.title
        entity.id = old_entity.id
        entity.category = c if self.categoryId is not None else old_entity.category
        entity.participant = p if self.participantId is not None else old_entity.participant
        entity.start = datetime.fromisoformat(self.start.replace('Z', '+00:00')) if self.start is not None else old_entity.start
        entity.end = datetime.fromisoformat(self.end.replace('Z', '+00:00')) if self.end is not None else old_entity.end
        return entity
