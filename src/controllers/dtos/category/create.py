import uuid
from datetime import datetime, timezone

from src.controllers.dtos.base import BaseDTO
from src.domain.entities import Category


class CategoryCreateDTO(BaseDTO):
    title: str

    def to_entity(self) -> Category:
        c = Category()
        c.id = uuid.uuid7()
        c.title = self.title
        c.created_at = datetime.now(timezone.utc)
        return c
