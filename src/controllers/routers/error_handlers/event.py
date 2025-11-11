from typing import Coroutine, Any, AsyncGenerator

from fastapi import HTTPException, status

from src.domain.entities import Event
from src.domain.exceptions import EventNotFoundException, CategoryNotFoundException, ParticipantNotFoundException


class EventErrorHandler:

    @staticmethod
    async def handle_create_async(event_async: Coroutine[Any, Any, Event]) -> Event:
        try:
            event = await event_async
        except (EventNotFoundException, CategoryNotFoundException, ParticipantNotFoundException) as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return event

    @staticmethod
    async def handle_read_async(event_async: Coroutine[Any, Any, Event]) -> Event:
        try:
            event = await event_async
        except EventNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return event

    @staticmethod
    async def handle_read_all_async(events_async: AsyncGenerator[Event, None]) -> AsyncGenerator[Event, None]:
        try:
            async for event in events_async:
                yield event
        except EventNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')

    @staticmethod
    async def handle_update_async(event_async: Coroutine[Any, Any, Event]) -> Event:
        try:
            event = await event_async
        except (EventNotFoundException, CategoryNotFoundException, ParticipantNotFoundException) as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return event

    @staticmethod
    async def handle_delete_async(event_async: Coroutine[Any, Any, Event]) -> Event:
        try:
            event = await event_async
        except EventNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return event
