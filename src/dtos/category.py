from pydantic import BaseModel

from src.domain.entities import Category


class CategoryDTO(BaseModel):
    title: str
    id: int | None = None

    def to_entity(self, omit_id: bool = False) -> Category:
        c = Category()
        c.id = self.id if not omit_id else None
        c.title = self.title
        return c

    @staticmethod
    def from_entity(entity: Category) -> CategoryDTO:
        return CategoryDTO(
            id=entity.id,
            title=entity.title,
        )