from typing import Iterator

from fastapi import APIRouter, HTTPException
from fastapi_utils.cbv import cbv

from src.controllers.dtos import EventDTO
from src.domain.entities import Event
from src.domain.exceptions import EventNotFoundException, CategoryNotFoundException, ParticipantNotFoundException, \
    ParticipantsMismatchException, CategoriesMismatchException
from src.domain.interactors import EventInteractor
from src.services import PgDataBase

router = APIRouter()

@cbv(router)
class EventController:
    @router.get('/events/')
    async def read_events(self, limit: int = 0, offset: int = 0):
        interactor = EventInteractor(PgDataBase())
        try:
            events: Iterator[Event] = interactor.get_events(limit, offset)
        except EventNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')

        return [EventDTO.from_entity(event) for event in events]

    @router.get('/events/{event_id}')
    async def read_event(self, event_id: int):
        interactor = EventInteractor(PgDataBase())
        try:
            event = interactor.get_event(event_id)
        except EventNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return EventDTO.from_entity(event)

    @router.delete('/events/{event_id}')
    async def delete_event(self, event_id: int):
        interactor = EventInteractor(PgDataBase())
        try:
            event = interactor.remove_event(event_id)
        except EventNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return EventDTO.from_entity(event)

    @router.post('/events/')
    async def create_event(self, dto: EventDTO):
        interactor = EventInteractor(PgDataBase())
        event = dto.to_entity(True)
        try:
            event_saved = interactor.create_event(event)
        except (EventNotFoundException, CategoryNotFoundException, ParticipantNotFoundException) as err:
            raise HTTPException(status_code=404, detail=str(err))
        except (CategoriesMismatchException, ParticipantsMismatchException) as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return EventDTO.from_entity(event_saved)

    @router.put('/events/')
    async def update_event(self, dto: EventDTO):
        interactor = EventInteractor(PgDataBase())
        event = dto.to_entity(False)
        try:
            event_saved = interactor.update_event(event)
        except (EventNotFoundException, CategoryNotFoundException, ParticipantNotFoundException) as err:
            raise HTTPException(status_code=404, detail=str(err))
        except (CategoriesMismatchException, ParticipantsMismatchException) as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return EventDTO.from_entity(event_saved)
