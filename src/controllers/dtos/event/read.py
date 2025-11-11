from datetime import datetime

from src.controllers.dtos.base import BaseDTO
from src.domain.entities import  Event

from src.controllers.dtos import CategoryReadDTO, ParticipantReadDTO


class EventReadDTO(BaseDTO):
    id: str
    title: str
    start: str
    end: str
    category: CategoryReadDTO
    participant: ParticipantReadDTO
    createdAt: datetime

    @staticmethod
    def from_entity(event: Event) -> EventReadDTO:
        dto = EventReadDTO(
            id=str(event.id),
            title=event.title,
            start=event.start.isoformat(timespec='seconds').replace("+00:00", "Z"),
            end=event.end.isoformat(timespec='seconds').replace("+00:00", "Z"),
            category=CategoryReadDTO.from_entity(event.category),
            participant = ParticipantReadDTO.from_entity(event.participant),
            createdAt=event.created_at
        )
        return dto
