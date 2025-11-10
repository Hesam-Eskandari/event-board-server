import uuid
from typing import Iterator, List

from fastapi import APIRouter, HTTPException, status, Response
from fastapi_utils.cbv import cbv

from src.controllers.dtos import EventReadDTO, EventCreateDTO, EventPatchDTO
from src.domain.entities import Event
from src.domain.exceptions import EventNotFoundException, CategoryNotFoundException, ParticipantNotFoundException, \
    ParticipantsMismatchException, CategoriesMismatchException
from src.domain.interactors import EventInteractor, CategoryInteractor, ParticipantInteractor
from src.services import PgDataBase

router = APIRouter()

@cbv(router)
class EventController:

    @router.post('/events/', status_code=status.HTTP_201_CREATED, response_model=EventReadDTO)
    async def create_event(self, dto: EventCreateDTO):
        try:
            cid = uuid.UUID(dto.categoryId)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid category id")

        try:
            pid = uuid.UUID(dto.participantId)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid participant id")

        category_interactor = CategoryInteractor(PgDataBase())
        try:
            category = category_interactor.get_category(cid)
        except CategoryNotFoundException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')

        participant_interactor = ParticipantInteractor(PgDataBase())
        try:
            participant = participant_interactor.read_participant(pid)
        except ParticipantNotFoundException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="participant not found")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')


        event = dto.to_entity(category, participant)
        interactor = EventInteractor(PgDataBase())
        try:
            _ = interactor.create_event(event)
        except (EventNotFoundException, CategoryNotFoundException, ParticipantNotFoundException) as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except (CategoriesMismatchException, ParticipantsMismatchException) as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return EventReadDTO.from_entity(event)

    @router.get('/events/', status_code=status.HTTP_200_OK, response_model=List[EventReadDTO])
    async def read_events(self, limit: int = 0, offset: int = 0):
        interactor = EventInteractor(PgDataBase())
        try:
            events: Iterator[Event] = interactor.get_events(limit, offset)
        except EventNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        es = list(events)
        print('[')
        for e in es:
            print(e)
            print(',')
        print(']')
        return [EventReadDTO.from_entity(event) for event in es]

    @router.get('/events/{event_id}')
    async def read_event(self, event_id: str):
        try:
            eid = uuid.UUID(event_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'invalid event id: {event_id}')
        interactor = EventInteractor(PgDataBase())
        try:
            event = interactor.get_event(eid)
        except EventNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return EventReadDTO.from_entity(event)

    @router.patch('/events/{event_id}', status_code=status.HTTP_200_OK, response_model=EventReadDTO)
    async def patch_event(self, event_id: str, dto: EventPatchDTO):
        try:
            cid = uuid.UUID(dto.categoryId)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid category id")

        try:
            pid = uuid.UUID(dto.participantId)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid participant id")

        try:
            eid = uuid.UUID(event_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid event id")

        category_interactor = CategoryInteractor(PgDataBase())
        try:
            category = category_interactor.get_category(cid)
        except CategoryNotFoundException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category not found")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')

        participant_interactor = ParticipantInteractor(PgDataBase())
        try:
            participant = participant_interactor.read_participant(pid)
        except ParticipantNotFoundException:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="participant not found")
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')

        interactor = EventInteractor(PgDataBase())
        try:
            old_entity = interactor.get_event(eid)
        except EventNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')

        event = dto.to_entity(old_entity, category, participant)
        try:
            _ = interactor.update_event(event)
        except (EventNotFoundException, CategoryNotFoundException, ParticipantNotFoundException) as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except (CategoriesMismatchException, ParticipantsMismatchException) as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return EventReadDTO.from_entity(event)

    @router.delete('/events/{event_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def delete_event(self, event_id: str):
        try:
            eid = uuid.UUID(event_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid event id")
        interactor = EventInteractor(PgDataBase())
        try:
            _ = interactor.remove_event(eid)
        except EventNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return Response(status_code=status.HTTP_204_NO_CONTENT)
