import uuid
from pydantic import BaseModel

from src.domain.entities import Category


class CategoryCreateDTO(BaseModel):
    title: str

    def to_entity(self) -> Category:
        c = Category()
        c.id = uuid.uuid7()
        c.title = self.title
        return c
