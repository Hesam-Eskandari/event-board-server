from datetime import datetime

from pydantic import BaseModel

from src.domain.entities import Category, Event, Participant
from src.dtos import CategoryDTO, ParticipantDTO


class EventDTO(BaseModel):
    title: str
    start: str
    end: str
    category: CategoryDTO
    participant: ParticipantDTO
    id: int | None = None

    def to_entity(self, omit_id: bool = False) -> Event:
        category: Category = self.category.to_entity(False)
        participant: Participant = self.participant.to_entity(False)
        event: Event = Event()
        event.title = self.title
        event.id = self.id if not omit_id else None
        event.category = category
        event.participant = participant
        event.start = datetime.fromisoformat(self.start.replace('Z', '+00:00'))
        event.end = datetime.fromisoformat(self.end.replace('Z', '+00:00'))
        return event

    @staticmethod
    def from_entity(event: Event) -> EventDTO:
        dto = EventDTO(
            id=event.id,
            title=event.title,
            start=event.start.isoformat(timespec='seconds').replace("+00:00", "Z"),
            end=event.end.isoformat(timespec='seconds').replace("+00:00", "Z"),
            category=CategoryDTO.from_entity(event.category),
            participant = ParticipantDTO.from_entity(event.participant)

        )
        return dto
