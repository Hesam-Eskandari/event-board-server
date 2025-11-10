from typing import Coroutine, Any, Iterator

from fastapi import HTTPException, status

from src.domain.entities import Participant
from src.domain.exceptions import ParticipantNotFoundException


class ParticipantErrorHandler:

    @staticmethod
    async def handle_create_async(participant_async: Coroutine[Any, Any, Participant]) -> Participant:
        try:
            participant = await participant_async
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return participant

    @staticmethod
    async def handle_read_async(participant_async: Coroutine[Any, Any, Participant]) -> Participant:
        try:
            participant = await participant_async
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return participant

    @staticmethod
    async def handle_read_all_async(participants_async: Coroutine[Any, Any, Iterator[Participant]]) -> Iterator[Participant]:
        try:
            participants = await participants_async
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return participants

    @staticmethod
    async def handle_update_async(participant_async: Coroutine[Any, Any, Participant]) -> Participant:
        try:
            participant = await participant_async
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return participant

    @staticmethod
    async def handle_delete_async(participant_async: Coroutine[Any, Any, Participant]) -> Participant:
        try:
            participant = await participant_async
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return participant
