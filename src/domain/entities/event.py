from datetime import datetime

from src.domain.entities import Category, Participant


class Event:
    id: int | None
    title: str
    start: datetime
    end: datetime
    category: Category
    participant: Participant
