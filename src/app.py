from fastapi import FastAPI, HTTPException

from src.domain.exceptions import ParticipantNotFoundException
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
    try:
        participants = interactor.read_participants(limit, offset)
    except ParticipantNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return [ParticipantDTO.from_entity(p) for p in participants]

@app.post('/participants/')
async def create_participant(p: ParticipantDTO):
    participant = p.to_entity(True)
    interactor = ParticipantInteractor(PgDataBase())
    try:
        participant_saved = interactor.create_participant(participant)
    except ParticipantNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return ParticipantDTO.from_entity(participant_saved)

@app.get('/participants/{participant_id}')
async def read_participant(participant_id: int):
    interactor = ParticipantInteractor(PgDataBase())
    try:
        participant = interactor.read_participant(participant_id)
    except ParticipantNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return ParticipantDTO.from_entity(participant)

@app.put('/participants/')
async def update_participant(p: ParticipantDTO):
    participant = p.to_entity(False)
    interactor = ParticipantInteractor(PgDataBase())
    try:
        participant_saved = interactor.update_participant(participant)
    except ParticipantNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return ParticipantDTO.from_entity(participant_saved)

@app.delete('/participants/{participant_id}')
async def delete_participant(participant_id: int):
    interactor = ParticipantInteractor(PgDataBase())
    try:
        participant = interactor.remove_participant(participant_id)
    except ParticipantNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return ParticipantDTO.from_entity(participant)

