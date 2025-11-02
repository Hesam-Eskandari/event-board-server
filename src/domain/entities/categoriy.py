class Category:
    id: int | None
    title: str

    def __eq__(self, other: 'Category') -> bool:
        return self.id == other.id and self.title == other.title
