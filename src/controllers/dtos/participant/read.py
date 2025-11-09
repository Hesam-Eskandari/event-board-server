from pydantic import BaseModel

from src.domain.entities import Participant


class ParticipantReadDTO(BaseModel):
    firstname: str
    lastname: str
    imageUrl: str
    id: str

    @staticmethod
    def from_entity(entity: Participant) -> ParticipantReadDTO:
        return ParticipantReadDTO(
            id=str(entity.id),
            firstname=entity.firstname,
            lastname=entity.lastname,
            imageUrl=entity.image_url,
        )
