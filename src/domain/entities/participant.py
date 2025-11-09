from uuid import UUID


class Participant:
    id: UUID
    firstname: str
    lastname: str
    image_url: str

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname} {self.id} {self.image_url}'

    def __eq__(self, other: 'Participant') -> bool:
        return self.id == other.id and self.firstname == other.firstname and self.lastname == other.lastname and self.image_url == other.image_url
