from typing import List
from fastapi import APIRouter, HTTPException, status, Response
from fastapi_utils.cbv import cbv

from src.controllers.dtos import ParticipantReadDTO, ParticipantCreateDTO, ParticipantPatchDTO
from src.controllers.routers import ErrorHandler
from src.domain.interactors import ParticipantInteractor
from src.domain.interfaces import ParticipantDataProvider
from src.services import PgParticipantDataProvider

router = APIRouter()

@cbv(router)
class ParticipantController:

    def __init__(self):
        self._data_provider: ParticipantDataProvider = PgParticipantDataProvider()

    @router.post('/participants/', status_code=status.HTTP_201_CREATED, response_model=ParticipantReadDTO)
    async def create_participant(self, p: ParticipantCreateDTO):
        entity = p.to_entity()
        interactor = ParticipantInteractor(self._data_provider)
        _ = await ErrorHandler.handle_await_async(interactor.create_participant(entity))
        return ParticipantReadDTO.from_entity(entity)

    @router.get('/participants/', status_code=status.HTTP_200_OK, response_model=List[ParticipantReadDTO])
    async def read_participants(self, limit: int = 0, offset: int = 0):
        interactor = ParticipantInteractor(self._data_provider)
        return [ParticipantReadDTO.from_entity(participant) async for participant in \
                ErrorHandler.handle_await_all_async(interactor.get_participants(limit, offset))]

    @router.get('/participants/{participant_id}', status_code=status.HTTP_200_OK, response_model=ParticipantReadDTO)
    async def read_participant(self, participant_id: str):
        pid = ErrorHandler.handle_str_to_uuid(participant_id, f'invalid participant id {participant_id}')
        interactor = ParticipantInteractor(self._data_provider)
        participant = await ErrorHandler.handle_await_async(interactor.get_participant(pid))
        return ParticipantReadDTO.from_entity(participant)

    @router.patch('/participants/{participant_id}', status_code=status.HTTP_200_OK, response_model=ParticipantReadDTO)
    async def patch_participant(self, participant_id: str,  p: ParticipantPatchDTO):
        pid = ErrorHandler.handle_str_to_uuid(participant_id, f'invalid participant id {participant_id}')
        interactor = ParticipantInteractor(self._data_provider)
        old_entity = await ErrorHandler.handle_await_async(interactor.get_participant(pid))
        entity = p.to_entity(old_entity)
        if entity == old_entity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='participant update failed. no field is changed')
        _ = await ErrorHandler.handle_await_async(interactor.update_participant(entity))
        return ParticipantReadDTO.from_entity(entity)

    @router.delete('/participants/{participant_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def delete_participant(self, participant_id: str):
        pid = ErrorHandler.handle_str_to_uuid(participant_id, f'invalid participant id {participant_id}')
        interactor = ParticipantInteractor(self._data_provider)
        _ = await ErrorHandler.handle_await_async(interactor.remove_participant(pid))
        return Response(status_code=status.HTTP_204_NO_CONTENT)
