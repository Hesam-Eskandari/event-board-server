from typing import Iterator

import uvicorn
from fastapi import FastAPI, HTTPException

from src.domain.entities import Event
from src.domain.exceptions import ParticipantNotFoundException, CategoryNotFoundException, EventNotFoundException, \
    CategoriesMismatchException, ParticipantsMismatchException
from src.domain.interactors import ParticipantInteractor, CategoryInteractor, EventInteractor
from src.dtos import ParticipantDTO, CategoryDTO, EventDTO
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

@app.get('/categories/')
async def read_categories(limit: int = 0, offset: int = 0):
    interactor = CategoryInteractor(PgDataBase())
    try:
        categories = interactor.get_categories(limit, offset)
    except CategoryNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return [CategoryDTO.from_entity(category) for category in categories]

@app.get('/categories/{category_id}')
async def read_category(category_id: int):
    interactor = CategoryInteractor(PgDataBase())
    try:
        category = interactor.get_category(category_id)
    except CategoryNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return CategoryDTO.from_entity(category)

@app.post('/categories/')
async def create_category(c: CategoryDTO):
    category = c.to_entity(True)
    interactor = CategoryInteractor(PgDataBase())
    try:
        category_saved = interactor.create_category(category)
    except CategoryNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return CategoryDTO.from_entity(category_saved)

@app.delete('/categories/{category_id}')
async def delete_category(category_id: int):
    interactor = CategoryInteractor(PgDataBase())
    try:
        category_saved = interactor.remove_category(category_id)
    except CategoryNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return CategoryDTO.from_entity(category_saved)

@app.put('/categories/')
async def update_category(c: CategoryDTO):
    category = c.to_entity(False)
    interactor = CategoryInteractor(PgDataBase())
    try:
        category_saved = interactor.update_category(category)
    except CategoryNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return CategoryDTO.from_entity(category_saved)


@app.get('/events/')
async def read_events(limit: int = 0, offset: int = 0):
    interactor = EventInteractor(PgDataBase())
    try:
        events: Iterator[Event] = interactor.get_events(limit, offset)
    except EventNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))

    return [EventDTO.from_entity(event) for event in events]

@app.get('/events/{event_id}')
async def read_event(event_id: int):
    interactor = EventInteractor(PgDataBase())
    try:
        event = interactor.get_event(event_id)
    except EventNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return EventDTO.from_entity(event)

@app.delete('/events/{event_id}')
async def delete_event(event_id: int):
    interactor = EventInteractor(PgDataBase())
    try:
        event = interactor.remove_event(event_id)
    except EventNotFoundException as err:
        raise HTTPException(status_code=404, detail=str(err))
    return EventDTO.from_entity(event)

@app.post('/events/')
async def create_event(dto: EventDTO):
    interactor = EventInteractor(PgDataBase())
    event = dto.to_entity(True)
    try:
        event_saved = interactor.create_event(event)
    except (EventNotFoundException, CategoriesMismatchException, ParticipantsMismatchException, CategoryNotFoundException, ParticipantNotFoundException) as err:
        raise HTTPException(status_code=404, detail=str(err))
    return EventDTO.from_entity(event_saved)

@app.put('/events/')
async def update_event(dto: EventDTO):
    interactor = EventInteractor(PgDataBase())
    event = dto.to_entity(False)
    print('$$$$$$$$$$$$$$$$ here')
    try:
        event_saved = interactor.update_event(event)
    except (EventNotFoundException, CategoriesMismatchException, ParticipantsMismatchException, CategoryNotFoundException, ParticipantNotFoundException) as err:
        raise HTTPException(status_code=404, detail=str(err))
    return EventDTO.from_entity(event_saved)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
