
from sqlalchemy import Integer, String, Column

from src.domain.entities import Category
from .base import Base


class CategoryModel(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)

    def to_entity(self) -> Category:
        c = Category()
        c.id = self.id
        c.title = self.title
        return c

    @staticmethod
    def from_entity(entity: Category) -> 'CategoryModel':
        model = CategoryModel()
        model.id = entity.id
        model.title = entity.title
        return model
