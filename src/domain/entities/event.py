from datetime import datetime
from uuid import UUID

from src.domain.entities import Category, Participant


class Event:
    id: UUID
    title: str
    start: datetime
    end: datetime
    category: Category
    participant: Participant

    def __repr__(self) -> str:
        print('__repr__ is called')
        return self.__str__()

    def __str__(self) -> str:
        return f'{{\n'\
                f'  id: {self.id}\n'\
                f'  title: {self.title}\n'\
                f'  start: {self.start}\n'\
                f'  end: {self.end}\n'\
                f'  category: {self.category}\n'\
                f'  participant: {self.participant}\n'\
                f'}}\n'
