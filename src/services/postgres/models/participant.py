from sqlalchemy import Column, Integer, String

from src.domain.entities import Participant
from .base import Base


class ParticipantModel(Base):
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    image_url = Column(String, nullable=False)

    def to_entity(self) -> Participant:
        p = Participant()
        p.firstname = self.firstname
        p.lastname = self.lastname
        p.image_url = self.image_url
        p.id = self.id
        return p

    @staticmethod
    def from_entity(entity: Participant) -> 'ParticipantModel':
        model = ParticipantModel()
        model.firstname = entity.firstname
        model.lastname = entity.lastname
        model.image_url = entity.image_url
        model.id = entity.id
        return model
