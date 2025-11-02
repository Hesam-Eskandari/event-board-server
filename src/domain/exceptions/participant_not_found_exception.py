

class ParticipantNotFoundException(Exception):
    def __init__(self, message: str) -> None:
        self._message: str = message

    def __str__(self) -> str:
        return self._message
