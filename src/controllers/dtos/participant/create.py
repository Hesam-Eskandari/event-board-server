from datetime import datetime, timezone
import uuid

from src.controllers.dtos.base import BaseDTO
from src.domain.entities import Participant


class ParticipantCreateDTO(BaseDTO):
    firstname: str
    lastname: str
    imageUrl: str

    def to_entity(self) -> Participant:
        p = Participant()
        p.firstname = self.firstname
        p.lastname = self.lastname
        p.image_url = self.imageUrl
        p.id = uuid.uuid7()
        p.created_at = datetime.now(timezone.utc)
        return p
