from datetime import datetime

from src.controllers.dtos.base import BaseDTO
from src.domain.entities import Category


class CategoryReadDTO(BaseDTO):
    title: str
    id: str
    createdAt: datetime

    @staticmethod
    def from_entity(entity: Category) -> CategoryReadDTO:
        return CategoryReadDTO(
            id=str(entity.id),
            title=entity.title,
            createdAt=entity.created_at
        )

    def __eq__(self, other: 'CategoryReadDTO') -> bool:
        return isinstance(other, CategoryReadDTO) and self.id == other.id and self.title == other.title
