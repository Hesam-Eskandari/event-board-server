from uuid import UUID


class Category:
    id: UUID
    title: str

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: 'Category') -> bool:
        return self.id == other.id and self.title == other.title

    def __str__(self) -> str:
        return f'{{ id: {self.id}, title: {self.title} }}'
