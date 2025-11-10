import uuid

from src.controllers.dtos.base import BaseDTO
from src.domain.entities import Category


class CategoryCreateDTO(BaseDTO):
    title: str

    def to_entity(self) -> Category:
        c = Category()
        c.id = uuid.uuid7()
        c.title = self.title
        return c
