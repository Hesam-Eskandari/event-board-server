from typing import Any

from sqlalchemy import String, Column, UUID, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from src.domain.entities import Category
from src.services.postgres.models import Base


class CategoryModel(Base):
    __tablename__ = 'category'
    id = Column(UUID, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    events = relationship("EventModel", back_populates="category")

    @staticmethod
    def from_entity(entity: Category) -> 'CategoryModel':
        model = CategoryModel()
        model.id = entity.id
        model.title = entity.title
        model.created_at = entity.created_at
        return model

    def to_entity(self) -> Category:
        c = Category()
        c.id = self.id
        c.title = self.title
        c.created_at = self.created_at
        return c

    def to_dict(self, exclude_id: bool=False, exclude_fields: list[str] = None) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if (not exclude_id or c.name != "id") and c.name not in exclude_fields}
