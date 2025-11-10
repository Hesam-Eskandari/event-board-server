from pydantic import BaseModel

from src.domain.entities import  Event
from src.controllers.dtos import CategoryReadDTO, ParticipantReadDTO


class EventReadDTO(BaseModel):
    id: str
    title: str
    start: str
    end: str
    category: CategoryReadDTO
    participant: ParticipantReadDTO

    @staticmethod
    def from_entity(event: Event) -> EventReadDTO:
        dto = EventReadDTO(
            id=str(event.id),
            title=event.title,
            start=event.start.isoformat(timespec='seconds').replace("+00:00", "Z"),
            end=event.end.isoformat(timespec='seconds').replace("+00:00", "Z"),
            category=CategoryReadDTO.from_entity(event.category),
            participant = ParticipantReadDTO.from_entity(event.participant)
        )
        return dto
