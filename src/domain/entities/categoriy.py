from datetime import datetime
from uuid import UUID


class Category:
    id: UUID
    title: str
    created_at: datetime

    def __eq__(self, other: 'Category') -> bool:
        return self.id == other.id and self.title == other.title

