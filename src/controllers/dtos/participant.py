from pydantic import BaseModel

from src.domain.entities import Participant


class ParticipantDTO(BaseModel):
    firstname: str
    lastname: str
    imageUrl: str
    id: int | None = None

    def to_entity(self, omit_id: bool = False) -> Participant:
        p = Participant()
        p.id = self.id if not omit_id else None
        p.firstname = self.firstname
        p.lastname = self.lastname
        p.image_url = self.imageUrl
        return p

    @staticmethod
    def from_entity(entity: Participant) -> ParticipantDTO:
        return ParticipantDTO(
            id=entity.id,
            firstname=entity.firstname,
            lastname=entity.lastname,
            imageUrl=entity.image_url,
        )
