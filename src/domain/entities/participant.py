class Participant:
    id: int | None
    firstname: str
    lastname: str
    image_url: str

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname} {self.id} {self.image_url}'
