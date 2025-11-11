from typing import Coroutine, Any, Iterator, AsyncGenerator

from fastapi import HTTPException, status

from src.controllers.dtos import ParticipantReadDTO
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
    async def handle_read_all_async(participants_async: AsyncGenerator[Participant, None]) -> AsyncGenerator[Participant, None]:
        try:
            async for participant in participants_async:
                yield participant
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')

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
