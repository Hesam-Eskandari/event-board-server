from typing import List, Union

from fastapi import APIRouter, HTTPException, status, Response
from fastapi_utils.cbv import cbv

from src.controllers.dtos import EventReadDTO, EventCreateDTO, EventPatchDTO
from src.controllers.routers import ErrorHandler
from src.domain.entities import Event, Category, Participant
from src.domain.interactors import EventInteractor, CategoryInteractor, ParticipantInteractor
from src.domain.interfaces import EventDataProvider, CategoryDataProvider, ParticipantDataProvider
from src.services import PgDataBase

router = APIRouter()

@cbv(router)
class EventController:

    def __init__(self):
        self._data_provider: Union[EventDataProvider, CategoryDataProvider, ParticipantDataProvider] = PgDataBase()

    @router.post('/events/', status_code=status.HTTP_201_CREATED, response_model=EventReadDTO)
    async def create_event(self, dto: EventCreateDTO):
        cid = ErrorHandler.handle_str_to_uuid(dto.categoryId, "invalid category id")
        pid = ErrorHandler.handle_str_to_uuid(dto.participantId, "invalid participant id")

        category_interactor = CategoryInteractor(self._data_provider)
        participant_interactor = ParticipantInteractor(self._data_provider)

        category_async = category_interactor.get_category(cid)
        participant_async = participant_interactor.get_participant(pid)

        category: Category = await ErrorHandler.handle_await_async(category_async)
        participant: Participant = await ErrorHandler.handle_await_async(participant_async)
        event: Event = dto.to_entity(category, participant)
        event_interactor = EventInteractor(self._data_provider)
        _ = await ErrorHandler.handle_await_async(event_interactor.create_event(event))
        return EventReadDTO.from_entity(event)

    @router.get('/events/', status_code=status.HTTP_200_OK, response_model=List[EventReadDTO])
    async def read_events(self, limit: int = 0, offset: int = 0):
        interactor = EventInteractor(self._data_provider)
        return [EventReadDTO.from_entity(event) async for event in \
                ErrorHandler.handle_await_all_async(interactor.get_events(limit, offset))]

    @router.get('/events/{event_id}')
    async def read_event(self, event_id: str):
        eid = ErrorHandler.handle_str_to_uuid(event_id, f'invalid event id: {event_id}')
        interactor = EventInteractor(self._data_provider)
        event: Event  = await ErrorHandler.handle_await_async(interactor.get_event(eid))
        return EventReadDTO.from_entity(event)

    @router.patch('/events/{event_id}', status_code=status.HTTP_200_OK, response_model=EventReadDTO)
    async def patch_event(self, event_id: str, dto: EventPatchDTO):
        cid = ErrorHandler.handle_str_to_uuid(dto.categoryId, "invalid category id")
        pid = ErrorHandler.handle_str_to_uuid(dto.participantId, "invalid participant id")
        eid = ErrorHandler.handle_str_to_uuid(event_id, "invalid event id")

        category_interactor = CategoryInteractor(self._data_provider)
        participant_interactor = ParticipantInteractor(self._data_provider)
        event_interactor = EventInteractor(self._data_provider)

        category_async = category_interactor.get_category(cid)
        participant_async = participant_interactor.get_participant(pid)
        old_entity_async = event_interactor.get_event(eid)

        category = await ErrorHandler.handle_await_async(category_async)
        participant = await ErrorHandler.handle_await_async(participant_async)
        old_entity = await ErrorHandler.handle_await_async(old_entity_async)

        entity: Event  = dto.to_entity(old_entity, category, participant)
        if entity == old_entity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='event update failed. no field is changed')

        _ = await ErrorHandler.handle_await_async(event_interactor.update_event(entity))
        return EventReadDTO.from_entity(entity)

    @router.delete('/events/{event_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def delete_event(self, event_id: str):
        eid = ErrorHandler.handle_str_to_uuid(event_id, f'invalid event id: {event_id}')
        interactor = EventInteractor(self._data_provider)
        _ = await ErrorHandler.handle_await_async(interactor.remove_event(eid))
        return Response(status_code=status.HTTP_204_NO_CONTENT)
