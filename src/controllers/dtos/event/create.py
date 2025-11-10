import uuid
from datetime import datetime

from pydantic import BaseModel

from src.domain.entities import Category, Event, Participant

class EventCreateDTO(BaseModel):
    title: str
    start: str
    end: str
    categoryId: str
    participantId: str

    def to_entity(self, c: Category, p: Participant) -> Event:
        event: Event = Event()
        event.title = self.title
        event.id = uuid.uuid7()
        event.category = c
        event.participant = p
        event.start = datetime.fromisoformat(self.start.replace('Z', '+00:00'))
        event.end = datetime.fromisoformat(self.end.replace('Z', '+00:00'))
        return event
