from typing import Any

from sqlalchemy import Column, Boolean, DateTime, UUID, String, ForeignKey, func
from sqlalchemy.orm import relationship

from src.domain.entities import Event
from src.services.postgres.models import EventBoardBase


class EventModel(EventBoardBase):
    __tablename__ = 'event'
    id = Column(UUID, primary_key=True)
    title = Column(String, nullable=False)
    start = Column(DateTime(timezone=True), nullable=False)
    end = Column(DateTime(timezone=True), nullable=False)
    category_id = Column(UUID, ForeignKey("category.id"), nullable=False)
    category = relationship("CategoryModel", back_populates="events")
    participant_id = Column(UUID, ForeignKey("participant.id"), nullable=False)
    participant = relationship("ParticipantModel", back_populates="events")
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    @staticmethod
    def from_entity(entity: Event) -> EventModel:
        model = EventModel()
        model.id = entity.id
        model.title = entity.title
        model.start = entity.start
        model.end = entity.end
        model.category_id = entity.category.id
        model.participant_id = entity.participant.id
        model.created_at = entity.created_at
        return model

    def to_entity(self) -> Event:
        entity = Event()
        entity.id = self.id
        entity.title = self.title
        entity.start = self.start
        entity.end = self.end
        category = self.category.to_entity()
        participant = self.participant.to_entity()
        entity.category = category
        entity.participant = participant
        entity.created_at = self.created_at
        return entity

    def to_dict(self, exclude_id: bool=False, exclude_fields: list[str] = None) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if not exclude_id or c.name != "id" and c.name not in exclude_fields}
