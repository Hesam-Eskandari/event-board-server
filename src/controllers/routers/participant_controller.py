from typing import List
from fastapi import APIRouter, HTTPException, status, Response
from fastapi_utils.cbv import cbv

from src.controllers.dtos import ParticipantReadDTO, ParticipantCreateDTO, ParticipantPatchDTO
from src.controllers.routers import ParticipantErrorHandler, UUIDErrorHandler
from src.domain.interactors import ParticipantInteractor
from src.services import DataBaseMock

router = APIRouter()

@cbv(router)
class ParticipantController:

    @router.post('/participants/', status_code=status.HTTP_201_CREATED, response_model=ParticipantReadDTO)
    async def create_participant(self, p: ParticipantCreateDTO):
        entity = p.to_entity()
        interactor = ParticipantInteractor(DataBaseMock())
        _ = await ParticipantErrorHandler.handle_create_async(interactor.create_participant(entity))
        return ParticipantReadDTO.from_entity(entity)

    @router.get('/participants/', status_code=status.HTTP_200_OK, response_model=List[ParticipantReadDTO])
    async def read_participants(self, limit: int = 0, offset: int = 0):
        interactor = ParticipantInteractor(DataBaseMock())
        return [ParticipantReadDTO.from_entity(participant) async for participant in \
                ParticipantErrorHandler.handle_read_all_async(interactor.get_participants(limit, offset))]

    @router.get('/participants/{participant_id}', status_code=status.HTTP_200_OK, response_model=ParticipantReadDTO)
    async def read_participant(self, participant_id: str):
        pid = UUIDErrorHandler.handle_str_to_uuid(participant_id, f'invalid participant id {participant_id}')
        interactor = ParticipantInteractor(DataBaseMock())
        participant = await ParticipantErrorHandler.handle_read_async(interactor.get_participant(pid))
        return ParticipantReadDTO.from_entity(participant)

    @router.patch('/participants/{participant_id}', status_code=status.HTTP_200_OK, response_model=ParticipantReadDTO)
    async def patch_participant(self, participant_id: str,  p: ParticipantPatchDTO):
        pid = UUIDErrorHandler.handle_str_to_uuid(participant_id, f'invalid participant id {participant_id}')
        interactor = ParticipantInteractor(DataBaseMock())
        old_entity = await ParticipantErrorHandler.handle_read_async(interactor.get_participant(pid))
        entity = p.to_entity(old_entity)
        if entity == old_entity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='participant update failed. no field is changed')
        _ = await ParticipantErrorHandler.handle_update_async(interactor.update_participant(entity))
        return ParticipantReadDTO.from_entity(entity)

    @router.delete('/participants/{participant_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def delete_participant(self, participant_id: str):
        pid = UUIDErrorHandler.handle_str_to_uuid(participant_id, f'invalid participant id {participant_id}')
        interactor = ParticipantInteractor(DataBaseMock())
        _ = await ParticipantErrorHandler.handle_delete_async(interactor.remove_participant(pid))
        return Response(status_code=status.HTTP_204_NO_CONTENT)
