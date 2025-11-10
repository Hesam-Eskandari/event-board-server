import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status, Response
from fastapi_utils.cbv import cbv

from src.controllers.dtos import ParticipantReadDTO, ParticipantCreateDTO, ParticipantPatchDTO
from src.domain.exceptions import ParticipantNotFoundException
from src.domain.interactors import ParticipantInteractor
from src.services import PgDataBase

router = APIRouter()

@cbv(router)
class ParticipantController:

    @router.post('/participants/', status_code=status.HTTP_201_CREATED, response_model=ParticipantReadDTO)
    async def create_participant(self, p: ParticipantCreateDTO):
        participant = p.to_entity()
        interactor = ParticipantInteractor(PgDataBase())
        try:
            participant_saved = interactor.create_participant(participant)
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return ParticipantReadDTO.from_entity(participant_saved)

    @router.get('/participants/', status_code=status.HTTP_200_OK, response_model=List[ParticipantReadDTO])
    async def read_participants(self, limit: int = 0, offset: int = 0):
        interactor = ParticipantInteractor(PgDataBase())
        try:
            participants = interactor.read_participants(limit, offset)
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return [ParticipantReadDTO.from_entity(p) for p in participants]

    @router.get('/participants/{participant_id}', status_code=status.HTTP_200_OK, response_model=ParticipantReadDTO)
    async def read_participant(self, participant_id: str):
        try:
            pid = uuid.UUID(participant_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'invalid participant id {participant_id}')
        interactor = ParticipantInteractor(PgDataBase())
        try:
            participant = interactor.read_participant(pid)
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return ParticipantReadDTO.from_entity(participant)

    @router.patch('/participants/{participant_id}', status_code=status.HTTP_200_OK, response_model=ParticipantReadDTO)
    async def patch_participant(self, participant_id: str,  p: ParticipantPatchDTO):
        try:
            pid = uuid.UUID(participant_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'invalid participant id {participant_id}')
        interactor = ParticipantInteractor(PgDataBase())
        try:
            old_entity = interactor.read_participant(pid)
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        entity = p.to_entity(old_entity)
        if entity == old_entity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='participant update failed. no field is changed')
        try:
            _ = interactor.update_participant(entity)
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return ParticipantReadDTO.from_entity(entity)

    @router.delete('/participants/{participant_id}')
    async def delete_participant(self, participant_id: str):
        try:
            pid = uuid.UUID(participant_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'invalid participant id {participant_id}')
        interactor = ParticipantInteractor(PgDataBase())
        try:
            participant = interactor.remove_participant(pid)
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='unexpected error happened')
        return ParticipantReadDTO.from_entity(participant)
