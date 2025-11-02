from fastapi import APIRouter, HTTPException
from fastapi_utils.cbv import cbv

from src.controllers.dtos import ParticipantDTO
from src.domain.exceptions import ParticipantNotFoundException
from src.domain.interactors import ParticipantInteractor
from src.services import PgDataBase

router = APIRouter()

@cbv(router)
class ParticipantController:
    @router.get('/participants/')
    async def read_participants(self, limit: int = 0, offset: int = 0):
        interactor = ParticipantInteractor(PgDataBase())
        try:
            participants = interactor.read_participants(limit, offset)
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return [ParticipantDTO.from_entity(p) for p in participants]

    @router.post('/participants/')
    async def create_participant(self, p: ParticipantDTO):
        participant = p.to_entity(True)
        interactor = ParticipantInteractor(PgDataBase())
        try:
            participant_saved = interactor.create_participant(participant)
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return ParticipantDTO.from_entity(participant_saved)

    @router.get('/participants/{participant_id}')
    async def read_participant(self, participant_id: int):
        interactor = ParticipantInteractor(PgDataBase())
        try:
            participant = interactor.read_participant(participant_id)
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return ParticipantDTO.from_entity(participant)

    @router.put('/participants/')
    async def update_participant(self, p: ParticipantDTO):
        participant = p.to_entity(False)
        interactor = ParticipantInteractor(PgDataBase())
        try:
            participant_saved = interactor.update_participant(participant)
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return ParticipantDTO.from_entity(participant_saved)

    @router.delete('/participants/{participant_id}')
    async def delete_participant(self, participant_id: int):
        interactor = ParticipantInteractor(PgDataBase())
        try:
            participant = interactor.remove_participant(participant_id)
        except ParticipantNotFoundException as err:
            raise HTTPException(status_code=404, detail=str(err))
        except Exception:
            raise HTTPException(status_code=500, detail='unexpected error happened')
        return ParticipantDTO.from_entity(participant)
