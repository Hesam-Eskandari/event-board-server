import uuid

from pydantic import BaseModel

from src.domain.entities import Participant


class ParticipantCreateDTO(BaseModel):
    firstname: str
    lastname: str
    imageUrl: str

    def to_entity(self) -> Participant:
        p = Participant()
        p.firstname = self.firstname
        p.lastname = self.lastname
        p.image_url = self.imageUrl
        p.id = uuid.uuid7()
        return p
