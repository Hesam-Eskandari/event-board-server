from datetime import datetime
from uuid import UUID

from src.domain.entities import Category, Participant


class Event:
    id: UUID
    title: str
    start: datetime
    end: datetime
    category: Category
    participant: Participant

    def __eq__(self, other: 'Event') -> bool:
        return self.id == other.id \
            and self.title == other.title \
            and self.start == other.start \
            and self.end == other.end \
            and self.category == other.category \
            and self.participant == other.participant
