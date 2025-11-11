from typing import Any

from sqlalchemy import Column, String, DateTime, UUID, Boolean, func
from sqlalchemy.orm import relationship

from src.domain.entities import Participant
from src.services.postgres.models import Base


class ParticipantModel(Base):
    __tablename__ = 'participant'
    id = Column(UUID, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    events = relationship("EventModel", back_populates="participant")

    @staticmethod
    def from_entity(entity: Participant) -> 'ParticipantModel':
        model = ParticipantModel()
        model.firstname = entity.firstname
        model.lastname = entity.lastname
        model.image_url = entity.image_url
        model.id = entity.id
        model.created_at = entity.created_at
        return model

    def to_entity(self) -> Participant:
        p = Participant()
        p.firstname = self.firstname
        p.lastname = self.lastname
        p.image_url = self.image_url
        p.id = self.id
        p.created_at = self.created_at
        return p

    def to_dict(self, exclude_id: bool=False, exclude_fields: list[str] = None) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if not exclude_id or c.name != "id" and c.name not in exclude_fields}
