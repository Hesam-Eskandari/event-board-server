from src.controllers.dtos.base import BaseDTO
from src.domain.entities import Participant


class ParticipantReadDTO(BaseDTO):
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
