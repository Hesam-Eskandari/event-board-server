from fastapi import FastAPI, HTTPException

from src.dtos import ParticipantDTO
from src.domain.interactors import ParticipantInteractor
from src.services import PgDataBase

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/participants/')
async def read_participants(limit: int = 0, offset: int = 0):
    interactor = ParticipantInteractor(PgDataBase())
    participants, err_message = interactor.read_participants(limit, offset)
    if err_message is not None:
        raise HTTPException(status_code=404, detail=err_message)
    return [ParticipantDTO.from_entity(p) for p in participants]

@app.post('/participants/')
async def create_participant(p: ParticipantDTO):
    participant = p.to_entity(True)
    interactor = ParticipantInteractor(PgDataBase())
    participant_saved, err_message = interactor.create_participant(participant)
    if err_message is not None:
        raise HTTPException(status_code=404, detail=err_message)
    return ParticipantDTO.from_entity(participant_saved)

@app.get('/participants/{participant_id}')
async def read_participant(participant_id: int):
    interactor = ParticipantInteractor(PgDataBase())
    participant, err_message = interactor.read_participant(participant_id)
    if err_message is not None:
        raise HTTPException(status_code=404, detail=err_message)
    return ParticipantDTO.from_entity(participant)

@app.put('/participants/')
async def update_participant(p: ParticipantDTO):
    participant = p.to_entity(False)
    interactor = ParticipantInteractor(PgDataBase())
    participant_saved, err_message = interactor.update_participant(participant)
    if err_message is not None:
        raise HTTPException(status_code=404, detail=err_message)
    return ParticipantDTO.from_entity(participant_saved)

@app.delete('/participants/{participant_id}')
async def delete_participant(participant_id: int):
    interactor = ParticipantInteractor(PgDataBase())
    participant, err_message = interactor.remove_participant(participant_id)
    if err_message is not None:
        raise HTTPException(status_code=404, detail=err_message)
    return ParticipantDTO.from_entity(participant)

