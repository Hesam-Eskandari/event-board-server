import enum
from typing import Optional


class Application(enum.Enum):
    EventBoard = 'event-board'

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def from_value(val: str) -> Optional['Application']:
        return Application._value2member_map_.get(val)
