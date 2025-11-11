from src.controllers.dtos.base import BaseDTO
from src.domain.entities import Participant


class ParticipantPatchDTO(BaseDTO):
    firstname: str | None = None
    lastname: str | None = None
    imageUrl: str | None = None

    def to_entity(self, old_entity: Participant) -> Participant:
        p = Participant()
        p.firstname = self.firstname if self.firstname is not None else old_entity.firstname
        p.lastname = self.lastname if self.lastname is not None else old_entity.lastname
        p.image_url = self.imageUrl if self.imageUrl is not None else old_entity.image_url
        p.id = old_entity.id
        p.created_at = old_entity.created_at
        return p
