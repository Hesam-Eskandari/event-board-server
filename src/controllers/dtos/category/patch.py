from pydantic import BaseModel

from src.domain.entities import Category


class CategoryPatchDTO(BaseModel):
    title: str | None

    def to_entity(self, old_entity: Category) -> Category:
        c = Category()
        c.id = old_entity.id
        c.title = self.title if self.title is not None else old_entity.title
        return c
